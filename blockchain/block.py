"""Block implementation for blockchain ledger"""
import hashlib
import json
from datetime import datetime
from typing import Optional

class Block:
    """Represents a block in the blockchain"""
    
    def __init__(self, index: int, timestamp: str, voter_id: int, 
                 proposal_id: int, signature: str, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.voter_id = voter_id
        self.proposal_id = proposal_id
        self.signature = signature
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'voter_id': self.voter_id,
            'proposal_id': self.proposal_id,
            'signature': self.signature,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'voter_id': self.voter_id,
            'proposal_id': self.proposal_id,
            'signature': self.signature,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }
    
    @staticmethod
    def from_dict(data):
        """Create block from dictionary"""
        block = Block(
            index=data['index'],
            timestamp=data['timestamp'],
            voter_id=data['voter_id'],
            proposal_id=data['proposal_id'],
            signature=data['signature'],
            previous_hash=data['previous_hash']
        )
        block.hash = data['hash']
        return block
