"""Anonymous Token Service for Privacy-Preserving Voting"""
import secrets
import hashlib
import time
from typing import Optional, Dict
from pathlib import Path
import json

class AnonymousTokenService:
    """
    Service for managing anonymous tokens to separate identity from votes
    
    Architecture:
    1. Identity DB: CCCD ↔ Token (stored separately)
    2. Voting DB: Token ↔ Vote (no CCCD)
    3. Blockchain: Token ↔ Proposal (no CCCD)
    """
    
    def __init__(self, token_db_path: str = "face_data/anonymous_tokens.json"):
        self.token_db_path = Path(token_db_path)
        self.token_db_path.parent.mkdir(exist_ok=True)
        
        # Identity mapping: CCCD -> Token (SENSITIVE - should be encrypted)
        self.identity_map: Dict[str, str] = {}
        
        # Token metadata: Token -> {created_at, used, election_id}
        self.token_metadata: Dict[str, dict] = {}
        
        self.load_token_data()
    
    def load_token_data(self):
        """Load token data from file"""
        if self.token_db_path.exists():
            with open(self.token_db_path, 'r') as f:
                data = json.load(f)
                self.identity_map = data.get('identity_map', {})
                self.token_metadata = data.get('token_metadata', {})
    
    def save_token_data(self):
        """Save token data to file"""
        data = {
            'identity_map': self.identity_map,
            'token_metadata': self.token_metadata
        }
        with open(self.token_db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_anonymous_token(self, cccd: str, election_id: int) -> str:
        """
        Generate a cryptographically secure anonymous token
        
        Args:
            cccd: Citizen ID (for identity mapping only)
            election_id: Election ID
            
        Returns:
            Anonymous token (hex string)
        """
        # Check if token already exists for this CCCD and election
        existing_token = self.get_token_by_cccd(cccd, election_id)
        if existing_token:
            print(f"ℹ️ Token đã tồn tại cho CCCD {cccd} trong cuộc bầu cử {election_id}")
            return existing_token
        
        # Generate cryptographically secure random token
        random_bytes = secrets.token_bytes(32)
        
        # Add timestamp and election_id for uniqueness
        timestamp = str(time.time()).encode()
        election_bytes = str(election_id).encode()
        
        # Hash everything together
        token_hash = hashlib.sha256(random_bytes + timestamp + election_bytes).hexdigest()
        
        # Store mapping (SENSITIVE DATA)
        token_key = f"{cccd}:{election_id}"
        self.identity_map[token_key] = token_hash
        
        # Store metadata (non-sensitive)
        self.token_metadata[token_hash] = {
            'created_at': time.time(),
            'election_id': election_id,
            'used': False
        }
        
        self.save_token_data()
        
        print(f"✅ Tạo anonymous token: {token_hash[:16]}...")
        return token_hash
    
    def get_token_by_cccd(self, cccd: str, election_id: int) -> Optional[str]:
        """
        Get token for a CCCD in a specific election
        
        Args:
            cccd: Citizen ID
            election_id: Election ID
            
        Returns:
            Token or None
        """
        token_key = f"{cccd}:{election_id}"
        return self.identity_map.get(token_key)
    
    def verify_token(self, token: str, election_id: int) -> bool:
        """
        Verify if token is valid for an election
        
        Args:
            token: Anonymous token
            election_id: Election ID
            
        Returns:
            True if valid
        """
        if token not in self.token_metadata:
            return False
        
        metadata = self.token_metadata[token]
        return metadata['election_id'] == election_id
    
    def mark_token_used(self, token: str) -> bool:
        """
        Mark token as used (voted)
        
        Args:
            token: Anonymous token
            
        Returns:
            True if successful
        """
        if token not in self.token_metadata:
            return False
        
        self.token_metadata[token]['used'] = True
        self.token_metadata[token]['used_at'] = time.time()
        self.save_token_data()
        return True
    
    def is_token_used(self, token: str) -> bool:
        """Check if token has been used"""
        if token not in self.token_metadata:
            return False
        return self.token_metadata[token].get('used', False)
    
    def revoke_identity_mapping(self, election_id: int):
        """
        CRITICAL: Revoke identity mapping after election ends
        This ensures no one can trace votes back to voters
        
        Args:
            election_id: Election ID to revoke mappings for
        """
        print(f"🔒 Revoking identity mappings for election {election_id}...")
        
        # Remove all CCCD -> Token mappings for this election
        keys_to_remove = [k for k in self.identity_map.keys() if k.endswith(f":{election_id}")]
        
        for key in keys_to_remove:
            del self.identity_map[key]
        
        self.save_token_data()
        
        print(f"✅ Đã xóa {len(keys_to_remove)} identity mappings")
        print("⚠️ Từ giờ KHÔNG THỂ trace votes về voters!")
    
    def get_cccd_by_token(self, token: str, election_id: int) -> Optional[str]:
        """
        Get CCCD by token (ONLY for admin audit before revocation)
        
        WARNING: This should only be used for debugging/audit
        After revoke_identity_mapping(), this will return None
        """
        for key, stored_token in self.identity_map.items():
            if stored_token == token and key.endswith(f":{election_id}"):
                cccd = key.split(':')[0]
                return cccd
        return None
    
    def get_statistics(self, election_id: int) -> dict:
        """Get statistics for an election"""
        tokens = [t for t, m in self.token_metadata.items() 
                 if m['election_id'] == election_id]
        
        used_tokens = [t for t in tokens if self.token_metadata[t].get('used', False)]
        
        # Check if identity mapping still exists
        identity_mappings = [k for k in self.identity_map.keys() 
                            if k.endswith(f":{election_id}")]
        
        return {
            'total_tokens': len(tokens),
            'used_tokens': len(used_tokens),
            'unused_tokens': len(tokens) - len(used_tokens),
            'identity_mappings_exist': len(identity_mappings) > 0,
            'privacy_protected': len(identity_mappings) == 0
        }
