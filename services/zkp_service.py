"""Zero-Knowledge Proof Service for Anonymous Voting"""
import hashlib
import secrets
from typing import Tuple, Optional
import json

class ZKPService:
    """
    Simplified Zero-Knowledge Proof for voting
    
    Concept: Prove you are a valid voter WITHOUT revealing your identity
    
    This is a simplified educational implementation.
    Production systems should use libraries like libsnark, circom, or zk-SNARKs
    """
    
    def __init__(self):
        # In production, this would be a trusted setup parameter
        self.system_params = {
            'modulus': 2**256 - 2**32 - 977,  # Large prime
            'generator': 3
        }
    
    def generate_commitment(self, voter_id: int, secret: str) -> Tuple[str, str]:
        """
        Generate a commitment to voter identity
        
        Commitment = Hash(voter_id || secret)
        
        Args:
            voter_id: Voter ID (secret)
            secret: Random secret (nonce)
            
        Returns:
            (commitment, secret) - commitment is public, secret is private
        """
        data = f"{voter_id}:{secret}".encode()
        commitment = hashlib.sha256(data).hexdigest()
        return commitment, secret
    
    def generate_nullifier(self, voter_id: int, election_id: int) -> str:
        """
        Generate a nullifier to prevent double voting
        
        Nullifier = Hash(voter_id || election_id)
        
        The nullifier is unique per voter per election but doesn't reveal voter_id
        
        Args:
            voter_id: Voter ID
            election_id: Election ID
            
        Returns:
            Nullifier hash
        """
        data = f"{voter_id}:{election_id}:nullifier".encode()
        nullifier = hashlib.sha256(data).hexdigest()
        return nullifier
    
    def generate_proof(self, voter_id: int, election_id: int, 
                      registered_voters: list) -> dict:
        """
        Generate a zero-knowledge proof that voter is registered
        
        Proof contains:
        1. Commitment to voter identity
        2. Nullifier (to prevent double voting)
        3. Proof that voter is in registered set (simplified)
        
        Args:
            voter_id: Voter ID (will be hidden)
            election_id: Election ID
            registered_voters: List of registered voter IDs
            
        Returns:
            Proof dictionary
        """
        # Check if voter is registered
        if voter_id not in registered_voters:
            raise ValueError("Voter not registered")
        
        # Generate random secret
        secret = secrets.token_hex(32)
        
        # Generate commitment
        commitment, _ = self.generate_commitment(voter_id, secret)
        
        # Generate nullifier
        nullifier = self.generate_nullifier(voter_id, election_id)
        
        # Generate Merkle root of registered voters (simplified)
        merkle_root = self._compute_merkle_root(registered_voters)
        
        # Generate proof of membership (simplified)
        # In real ZKP, this would be a zk-SNARK proof
        membership_proof = self._generate_membership_proof(
            voter_id, registered_voters, secret
        )
        
        proof = {
            'commitment': commitment,
            'nullifier': nullifier,
            'merkle_root': merkle_root,
            'membership_proof': membership_proof,
            'election_id': election_id,
            'timestamp': str(secrets.randbits(64))  # Random timestamp for privacy
        }
        
        return proof
    
    def verify_proof(self, proof: dict, registered_voters: list, 
                    used_nullifiers: set) -> Tuple[bool, str]:
        """
        Verify a zero-knowledge proof
        
        Checks:
        1. Proof is well-formed
        2. Voter is in registered set (via Merkle root)
        3. Nullifier hasn't been used (no double voting)
        
        Args:
            proof: Proof dictionary
            registered_voters: List of registered voter IDs
            used_nullifiers: Set of already used nullifiers
            
        Returns:
            (is_valid, message)
        """
        # Check proof structure
        required_fields = ['commitment', 'nullifier', 'merkle_root', 
                          'membership_proof', 'election_id']
        if not all(field in proof for field in required_fields):
            return False, "Proof thiếu trường bắt buộc"
        
        # Check nullifier hasn't been used (prevent double voting)
        if proof['nullifier'] in used_nullifiers:
            return False, "Nullifier đã được sử dụng (double voting detected)"
        
        # Verify Merkle root matches registered voters
        expected_merkle_root = self._compute_merkle_root(registered_voters)
        if proof['merkle_root'] != expected_merkle_root:
            return False, "Merkle root không khớp (voter set changed)"
        
        # Verify membership proof (simplified)
        # In real ZKP, this would verify the zk-SNARK proof
        if not self._verify_membership_proof(proof['membership_proof']):
            return False, "Membership proof không hợp lệ"
        
        return True, "Proof hợp lệ"
    
    def _compute_merkle_root(self, voter_ids: list) -> str:
        """
        Compute Merkle root of voter set
        
        This allows proving membership without revealing which voter
        """
        if not voter_ids:
            return hashlib.sha256(b"empty").hexdigest()
        
        # Sort for deterministic root
        sorted_ids = sorted(voter_ids)
        
        # Hash all voter IDs
        hashes = [hashlib.sha256(str(vid).encode()).hexdigest() 
                 for vid in sorted_ids]
        
        # Build Merkle tree (simplified - just hash all together)
        combined = "".join(hashes).encode()
        merkle_root = hashlib.sha256(combined).hexdigest()
        
        return merkle_root
    
    def _generate_membership_proof(self, voter_id: int, 
                                   registered_voters: list, 
                                   secret: str) -> str:
        """
        Generate proof that voter_id is in registered_voters
        
        This is simplified. Real implementation would use:
        - Merkle path
        - zk-SNARK circuit
        - Groth16 or PLONK proof system
        """
        # Simplified: Hash voter_id with secret
        data = f"{voter_id}:{secret}:membership".encode()
        proof = hashlib.sha256(data).hexdigest()
        return proof
    
    def _verify_membership_proof(self, proof: str) -> bool:
        """
        Verify membership proof
        
        Simplified: Just check it's a valid hash
        """
        # In real ZKP, this would verify the cryptographic proof
        return len(proof) == 64 and all(c in '0123456789abcdef' for c in proof)
    
    def create_anonymous_vote(self, voter_id: int, proposal_id: int, 
                             election_id: int, registered_voters: list) -> dict:
        """
        Create an anonymous vote with ZKP
        
        Returns:
            Anonymous vote data (no voter_id exposed)
        """
        # Generate proof
        proof = self.generate_proof(voter_id, election_id, registered_voters)
        
        # Create vote data (no voter_id!)
        vote_data = {
            'proof': proof,
            'proposal_id': proposal_id,
            'election_id': election_id,
            'vote_hash': self._hash_vote(proof['nullifier'], proposal_id)
        }
        
        return vote_data
    
    def _hash_vote(self, nullifier: str, proposal_id: int) -> str:
        """Hash vote for integrity"""
        data = f"{nullifier}:{proposal_id}".encode()
        return hashlib.sha256(data).hexdigest()


class ZKPVotingSystem:
    """
    Complete ZKP-based voting system
    
    Features:
    - Anonymous voting (no voter_id on blockchain)
    - Prevents double voting (via nullifiers)
    - Verifiable (anyone can verify proofs)
    - Privacy-preserving (can't trace votes to voters)
    """
    
    def __init__(self):
        self.zkp_service = ZKPService()
        self.used_nullifiers = set()  # Track used nullifiers per election
        self.anonymous_votes = []  # Store anonymous votes
    
    def cast_anonymous_vote(self, voter_id: int, proposal_id: int,
                           election_id: int, registered_voters: list) -> Tuple[bool, str]:
        """
        Cast an anonymous vote using ZKP
        
        Args:
            voter_id: Voter ID (will be hidden in proof)
            proposal_id: Proposal to vote for
            election_id: Election ID
            registered_voters: List of all registered voter IDs
            
        Returns:
            (success, message)
        """
        try:
            # Generate anonymous vote with proof
            vote_data = self.zkp_service.create_anonymous_vote(
                voter_id, proposal_id, election_id, registered_voters
            )
            
            # Verify proof
            is_valid, message = self.zkp_service.verify_proof(
                vote_data['proof'], registered_voters, self.used_nullifiers
            )
            
            if not is_valid:
                return False, f"Proof không hợp lệ: {message}"
            
            # Check nullifier not used
            nullifier = vote_data['proof']['nullifier']
            if nullifier in self.used_nullifiers:
                return False, "Bạn đã bỏ phiếu rồi (nullifier đã dùng)"
            
            # Record vote
            self.used_nullifiers.add(nullifier)
            self.anonymous_votes.append(vote_data)
            
            return True, f"Bỏ phiếu ẩn danh thành công! Nullifier: {nullifier[:16]}..."
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
    
    def verify_vote(self, vote_data: dict, registered_voters: list) -> bool:
        """Verify an anonymous vote"""
        is_valid, _ = self.zkp_service.verify_proof(
            vote_data['proof'], registered_voters, set()
        )
        return is_valid
    
    def get_results(self, election_id: int) -> dict:
        """
        Get election results (counts only, no voter identities)
        """
        election_votes = [v for v in self.anonymous_votes 
                         if v['election_id'] == election_id]
        
        # Count votes per proposal
        results = {}
        for vote in election_votes:
            proposal_id = vote['proposal_id']
            results[proposal_id] = results.get(proposal_id, 0) + 1
        
        return {
            'total_votes': len(election_votes),
            'results': results,
            'privacy_preserved': True
        }
