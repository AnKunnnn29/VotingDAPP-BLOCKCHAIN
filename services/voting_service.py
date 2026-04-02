"""Voting service for managing vote operations"""
from typing import Optional
from models.voter import Voter
from models.proposal import Proposal
from models.election import Election
from blockchain.blockchain import Blockchain
from services.crypto_service import CryptoService
from database.db_manager import DatabaseManager
from utils.constants import ElectionState

class VotingService:
    """Service for voting operations"""
    
    def __init__(self, db_manager: DatabaseManager, blockchain: Blockchain):
        self.db_manager = db_manager
        self.blockchain = blockchain
        self.crypto_service = CryptoService()
    
    def cast_vote(self, voter: Voter, proposal_id: int, election: Election) -> tuple[bool, str]:
        """Cast a vote for a proposal"""
        # Check election state
        if election.state != ElectionState.VOTE:
            return False, f"Không thể bỏ phiếu ở trạng thái {election.state}"
        
        # Check voter verification for Permissioned mode
        if election.blockchain_mode == "Permissioned" and not voter.verified:
            return False, "Cử tri chưa được xác thực (Permissioned mode)"
        
        # CRITICAL: Check if voter already voted for THIS election by checking blockchain
        # This is the source of truth, not the database voter.voted flag
        existing_vote = self.blockchain.get_vote_by_voter_and_election(voter.id, election.id)
        if existing_vote:
            return False, "Bạn đã bỏ phiếu cho cuộc bầu cử này rồi"
        
        # Get proposals for current election
        current_election_proposals = self.db_manager.get_all_proposals(election.id)
        if not current_election_proposals:
            return False, "Cuộc bầu cử này chưa có ứng viên nào"
        
        # Check if proposal exists and belongs to current election
        proposal = next((p for p in current_election_proposals if p.id == proposal_id), None)
        if not proposal:
            return False, "Ứng viên không tồn tại trong cuộc bầu cử này"
        
        # Validate voter weight
        if voter.weight < 0:
            return False, "Quyền biểu quyết không hợp lệ"
        
        # Create vote data with election_id
        vote_data = f"{voter.id}:{proposal_id}:{election.id}"
        
        # Sign the vote
        try:
            signature = self.crypto_service.sign_vote(voter.private_key, vote_data)
        except Exception as e:
            return False, f"Lỗi ký số: {str(e)}"
        
        # Verify signature
        if not self.crypto_service.verify_signature(voter.public_key, vote_data, signature):
            return False, "Chữ ký không hợp lệ"
        
        # Transaction: Update voter and blockchain atomically
        try:
            # Update voter - mark as voted for tracking (but blockchain is source of truth)
            voter.voted = True
            voter.selected_proposal_id = proposal_id
            voter.digital_signature = signature
            self.db_manager.update_voter(voter)
            
            # Add to blockchain with election_id - THIS IS THE SOURCE OF TRUTH
            block = self.blockchain.add_vote_block(voter.id, proposal_id, signature, election.id)
            self.db_manager.save_blockchain(self.blockchain)
            
            return True, f"Bỏ phiếu thành công! Block #{block.index}"
        except Exception as e:
            # Rollback voter state if blockchain fails
            voter.voted = False
            voter.selected_proposal_id = None
            voter.digital_signature = None
            self.db_manager.update_voter(voter)
            return False, f"Lỗi khi ghi vào blockchain: {str(e)}"
    
    def get_voter_vote_status(self, voter: Voter) -> Optional[dict]:
        """Get the vote status of a voter from blockchain"""
        block = self.blockchain.get_vote_by_voter(voter.id)
        if block:
            proposal = None
            proposals = self.db_manager.get_all_proposals()
            for p in proposals:
                if p.id == block.proposal_id:
                    proposal = p
                    break
            
            return {
                'block_index': block.index,
                'timestamp': block.timestamp,
                'proposal': proposal,
                'signature': block.signature,
                'hash': block.hash
            }
        return None
