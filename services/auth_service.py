"""Authentication service for voter verification"""
from typing import Optional
from models.voter import Voter
from database.db_manager import DatabaseManager

class AuthService:
    """Service for authentication and authorization"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def authenticate_voter(self, voter_id: int) -> Optional[Voter]:
        """Authenticate a voter by ID"""
        voter = self.db_manager.get_voter_by_id(voter_id)
        if voter and voter.verified:
            return voter
        return None
    
    def verify_voter(self, voter_id: int) -> bool:
        """Verify a voter (admin action)"""
        voter = self.db_manager.get_voter_by_id(voter_id)
        if voter:
            voter.verified = True
            self.db_manager.update_voter(voter)
            return True
        return False
    
    def is_voter_eligible(self, voter_id: int, blockchain_mode: str) -> tuple[bool, str]:
        """Check if voter is eligible to vote"""
        voter = self.db_manager.get_voter_by_id(voter_id)
        
        if not voter:
            return False, "Cử tri không tồn tại"
        
        if not voter.verified:
            if blockchain_mode == "Permissioned":
                return False, "Cử tri chưa được xác thực (Permissioned mode)"
            # In Permissionless mode, unverified voters can still vote
        
        if voter.voted:
            return False, "Cử tri đã bỏ phiếu rồi"
        
        return True, "Hợp lệ"
