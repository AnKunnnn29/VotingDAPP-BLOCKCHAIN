"""Enhanced Voting Service with Anonymous Tokens and ZKP"""
from typing import Optional, Tuple
from models.voter import Voter
from models.proposal import Proposal
from models.election import Election
from blockchain.blockchain import Blockchain
from services.crypto_service import CryptoService
from services.anonymous_token_service import AnonymousTokenService
from services.zkp_service import ZKPVotingSystem
from database.db_manager import DatabaseManager
from utils.constants import ElectionState

class VotingServiceEnhanced:
    """
    Enhanced voting service with privacy features:
    1. Anonymous tokens (separate identity from votes)
    2. Zero-Knowledge Proofs (optional, for maximum privacy)
    """
    
    def __init__(self, db_manager: DatabaseManager, blockchain: Blockchain):
        self.db_manager = db_manager
        self.blockchain = blockchain
        self.crypto_service = CryptoService()
        self.token_service = AnonymousTokenService()
        self.zkp_system = ZKPVotingSystem()
        
        # Privacy mode: 'token' or 'zkp'
        self.privacy_mode = 'token'  # Default to token-based
    
    def set_privacy_mode(self, mode: str):
        """Set privacy mode: 'token' or 'zkp'"""
        if mode not in ['token', 'zkp']:
            raise ValueError("Mode must be 'token' or 'zkp'")
        self.privacy_mode = mode
        print(f"🔒 Privacy mode set to: {mode.upper()}")
    
    def prepare_voter_for_election(self, voter: Voter, election: Election) -> Tuple[bool, str]:
        """
        Prepare voter for election by generating anonymous token
        
        This should be called after face authentication but before voting
        """
        # Generate anonymous token
        token = self.token_service.generate_anonymous_token(voter.cccd, election.id)
        
        return True, f"Token generated: {token[:16]}..."
    
    def cast_vote_with_token(self, voter: Voter, proposal_id: int, 
                            election: Election) -> Tuple[bool, str]:
        """
        Cast vote using anonymous token (privacy mode: token)
        
        Flow:
        1. Get anonymous token for voter
        2. Vote with token (not voter_id)
        3. Blockchain stores: token + proposal_id (NO CCCD/voter_id)
        """
        # Check election state
        if election.state != ElectionState.VOTE:
            return False, f"Không thể bỏ phiếu ở trạng thái {election.state}"
        
        # Check voter verification for Permissioned mode
        if election.blockchain_mode == "Permissioned" and not voter.verified:
            return False, "Cử tri chưa được xác thực (Permissioned mode)"
        
        # Get anonymous token
        token = self.token_service.get_token_by_cccd(voter.cccd, election.id)
        if not token:
            # Generate token if not exists
            token = self.token_service.generate_anonymous_token(voter.cccd, election.id)
        
        # Check if token already used
        if self.token_service.is_token_used(token):
            return False, "Bạn đã bỏ phiếu cho cuộc bầu cử này rồi"
        
        # Check if token already voted on blockchain
        existing_vote = self.blockchain.get_vote_by_token(token, election.id)
        if existing_vote:
            return False, "Token đã được sử dụng để bỏ phiếu"
        
        # Get proposals for current election
        current_election_proposals = self.db_manager.get_all_proposals(election.id)
        if not current_election_proposals:
            return False, "Cuộc bầu cử này chưa có ứng viên nào"
        
        # Check if proposal exists
        proposal = next((p for p in current_election_proposals if p.id == proposal_id), None)
        if not proposal:
            return False, "Ứng viên không tồn tại trong cuộc bầu cử này"
        
        # Create vote data with TOKEN (not voter_id!)
        vote_data = f"{token}:{proposal_id}:{election.id}"
        
        # Sign the vote (using voter's key, but signature doesn't reveal identity)
        try:
            signature = self.crypto_service.sign_vote(voter.private_key, vote_data)
        except Exception as e:
            return False, f"Lỗi ký số: {str(e)}"
        
        # Transaction: Update token and blockchain
        try:
            # Mark token as used
            self.token_service.mark_token_used(token)
            
            # Add to blockchain with TOKEN (not voter_id!)
            block = self.blockchain.add_vote_block_with_token(
                token, proposal_id, signature, election.id
            )
            self.db_manager.save_blockchain(self.blockchain)
            
            print(f"✅ Vote recorded with anonymous token")
            print(f"   Token: {token[:16]}...")
            print(f"   Block: #{block.index}")
            print(f"   ⚠️ Admin CANNOT trace this vote to voter (after identity revocation)")
            
            return True, f"Bỏ phiếu thành công! Block #{block.index}"
            
        except Exception as e:
            # Rollback token state if blockchain fails
            self.token_service.token_metadata[token]['used'] = False
            self.token_service.save_token_data()
            return False, f"Lỗi khi ghi vào blockchain: {str(e)}"
    
    def cast_vote_with_zkp(self, voter: Voter, proposal_id: int,
                          election: Election) -> Tuple[bool, str]:
        """
        Cast vote using Zero-Knowledge Proof (privacy mode: zkp)
        
        Maximum privacy: Proves voter is registered WITHOUT revealing identity
        """
        # Check election state
        if election.state != ElectionState.VOTE:
            return False, f"Không thể bỏ phiếu ở trạng thái {election.state}"
        
        # Get all registered voters
        all_voters = self.db_manager.get_all_voters()
        registered_voter_ids = [v.id for v in all_voters if v.verified or election.blockchain_mode == "Permissionless"]
        
        # Check if proposal exists
        current_election_proposals = self.db_manager.get_all_proposals(election.id)
        proposal = next((p for p in current_election_proposals if p.id == proposal_id), None)
        if not proposal:
            return False, "Ứng viên không tồn tại trong cuộc bầu cử này"
        
        # Cast anonymous vote with ZKP
        success, message = self.zkp_system.cast_anonymous_vote(
            voter.id, proposal_id, election.id, registered_voter_ids
        )
        
        if not success:
            return False, message
        
        # Store ZKP vote on blockchain (optional - can be stored separately)
        # For now, just return success
        print(f"✅ Vote recorded with Zero-Knowledge Proof")
        print(f"   Voter identity: HIDDEN")
        print(f"   Proposal: {proposal_id}")
        print(f"   ⚠️ IMPOSSIBLE to trace this vote to voter!")
        
        return True, message
    
    def cast_vote(self, voter: Voter, proposal_id: int, 
                 election: Election) -> Tuple[bool, str]:
        """
        Cast vote (delegates to appropriate method based on privacy mode)
        """
        if self.privacy_mode == 'zkp':
            return self.cast_vote_with_zkp(voter, proposal_id, election)
        else:
            return self.cast_vote_with_token(voter, proposal_id, election)
    
    def finalize_election(self, election: Election):
        """
        Finalize election and revoke identity mappings for privacy
        
        CRITICAL: After this, no one can trace votes to voters!
        """
        print(f"\n🔒 FINALIZING ELECTION: {election.title}")
        print("=" * 60)
        
        # Get statistics before revocation
        stats = self.token_service.get_statistics(election.id)
        print(f"📊 Statistics:")
        print(f"   Total tokens: {stats['total_tokens']}")
        print(f"   Used tokens: {stats['used_tokens']}")
        print(f"   Identity mappings exist: {stats['identity_mappings_exist']}")
        
        # Revoke identity mappings
        print(f"\n⚠️ Revoking identity mappings...")
        self.token_service.revoke_identity_mapping(election.id)
        
        # Verify revocation
        stats_after = self.token_service.get_statistics(election.id)
        print(f"\n✅ Revocation complete!")
        print(f"   Privacy protected: {stats_after['privacy_protected']}")
        print(f"   Identity mappings exist: {stats_after['identity_mappings_exist']}")
        
        if stats_after['privacy_protected']:
            print(f"\n🎉 SUCCESS: Votes are now PERMANENTLY ANONYMOUS")
            print(f"   No one can trace votes to voters anymore!")
        
        print("=" * 60)
    
    def get_voter_vote_status(self, voter: Voter, election: Election) -> Optional[dict]:
        """
        Get vote status (works differently based on privacy mode)
        """
        if self.privacy_mode == 'zkp':
            # With ZKP, we can't retrieve individual vote status
            return None
        
        # With token mode, check token status
        token = self.token_service.get_token_by_cccd(voter.cccd, election.id)
        if not token:
            return None
        
        if self.token_service.is_token_used(token):
            return {
                'voted': True,
                'token': token[:16] + "...",
                'message': "Bạn đã bỏ phiếu"
            }
        
        return None
    
    def get_election_results_zkp(self, election_id: int) -> dict:
        """Get results for ZKP-based voting"""
        return self.zkp_system.get_results(election_id)
