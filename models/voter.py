"""Voter model representing a voter in the system"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Voter:
    """Represents a voter with cryptographic identity"""
    id: int
    full_name: str
    public_key: str
    private_key: str  # In production, this would be stored securely
    weight: int = 1
    voted: bool = False
    selected_proposal_id: Optional[int] = None
    digital_signature: Optional[str] = None
    verified: bool = False
    
    def to_dict(self):
        """Convert voter to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'public_key': self.public_key,
            'private_key': self.private_key,
            'weight': self.weight,
            'voted': self.voted,
            'selected_proposal_id': self.selected_proposal_id,
            'digital_signature': self.digital_signature,
            'verified': self.verified
        }
    
    @staticmethod
    def from_dict(data):
        """Create voter from dictionary"""
        return Voter(
            id=data['id'],
            full_name=data['full_name'],
            public_key=data['public_key'],
            private_key=data['private_key'],
            weight=data.get('weight', 1),
            voted=data.get('voted', False),
            selected_proposal_id=data.get('selected_proposal_id'),
            digital_signature=data.get('digital_signature'),
            verified=data.get('verified', False)
        )
