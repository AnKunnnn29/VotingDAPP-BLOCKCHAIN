"""Proposal model representing a candidate or voting option"""
from dataclasses import dataclass

@dataclass
class Proposal:
    """Represents a candidate or proposal in the election"""
    id: int
    candidate_name: str
    description: str
    vote_count: int = 0
    election_id: int = 0
    
    def to_dict(self):
        """Convert proposal to dictionary"""
        return {
            'id': self.id,
            'candidate_name': self.candidate_name,
            'description': self.description,
            'vote_count': self.vote_count,
            'election_id': self.election_id
        }
    
    @staticmethod
    def from_dict(data):
        """Create proposal from dictionary"""
        return Proposal(
            id=data['id'],
            candidate_name=data['candidate_name'],
            description=data['description'],
            vote_count=data.get('vote_count', 0),
            election_id=data.get('election_id', 0)
        )
