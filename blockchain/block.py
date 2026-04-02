"""Block implementation for blockchain ledger"""
import hashlib
import json
from datetime import datetime
from typing import Optional

class Block:
    """Represents a block in the blockchain"""
    
    def __init__(self, index: int, timestamp: str, voter_id: int, 
                 proposal_id: int, signature: str, previous_hash: str, election_id: int = 0,
                 nonce: int = 0, difficulty: int = 4, miner: str = "system"):
        self.index = index
        self.timestamp = timestamp
        self.voter_id = voter_id
        self.proposal_id = proposal_id
        self.signature = signature
        self.previous_hash = previous_hash
        self.election_id = election_id
        self.nonce = nonce
        self.difficulty = difficulty
        self.miner = miner
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'voter_id': self.voter_id,
            'proposal_id': self.proposal_id,
            'signature': self.signature,
            'previous_hash': self.previous_hash,
            'election_id': self.election_id,
            'nonce': self.nonce,
            'miner': self.miner
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> tuple[str, int, float]:
        """
        Mine the block using Proof of Work
        Returns: (hash, nonce, mining_time)
        """
        import time
        start_time = time.time()
        target = "0" * difficulty
        
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        mining_time = time.time() - start_time
        return self.hash, self.nonce, mining_time
    
    def is_valid_proof(self) -> bool:
        """Verify that the block's hash meets the difficulty requirement"""
        target = "0" * self.difficulty
        return self.hash.startswith(target)
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'voter_id': self.voter_id,
            'proposal_id': self.proposal_id,
            'signature': self.signature,
            'previous_hash': self.previous_hash,
            'election_id': self.election_id,
            'nonce': self.nonce,
            'difficulty': self.difficulty,
            'miner': self.miner,
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
            previous_hash=data['previous_hash'],
            election_id=data.get('election_id', 0),
            nonce=data.get('nonce', 0),
            difficulty=data.get('difficulty', 4),
            miner=data.get('miner', 'system')
        )
        block.hash = data['hash']
        return block
