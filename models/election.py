"""Election model representing a voting session"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from utils.constants import ElectionState, BlockchainMode

@dataclass
class Election:
    """Represents an election with state machine"""
    id: int
    title: str
    description: str
    state: str = ElectionState.START
    blockchain_mode: str = BlockchainMode.PERMISSIONLESS
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    winner_id: Optional[int] = None
    
    def to_dict(self):
        """Convert election to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'state': self.state,
            'blockchain_mode': self.blockchain_mode,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'winner_id': self.winner_id
        }
    
    @staticmethod
    def from_dict(data):
        """Create election from dictionary"""
        return Election(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            state=data.get('state', ElectionState.START),
            blockchain_mode=data.get('blockchain_mode', BlockchainMode.PERMISSIONLESS),
            start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
            end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            winner_id=data.get('winner_id')
        )
