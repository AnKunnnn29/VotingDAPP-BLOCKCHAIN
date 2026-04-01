"""Blockchain implementation for immutable vote ledger"""
from datetime import datetime
from typing import List, Optional
from blockchain.block import Block

class Blockchain:
    """Immutable ledger for storing votes"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            voter_id=0,
            proposal_id=0,
            signature="genesis",
            previous_hash="0"
        )
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_vote_block(self, voter_id: int, proposal_id: int, signature: str) -> Block:
        """Add a new vote block to the chain"""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            voter_id=voter_id,
            proposal_id=proposal_id,
            signature=signature,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_all_blocks(self) -> List[Block]:
        """Get all blocks in the chain"""
        return self.chain
    
    def get_vote_by_voter(self, voter_id: int) -> Optional[Block]:
        """Find a vote block by voter ID"""
        for block in reversed(self.chain):
            if block.voter_id == voter_id and block.index > 0:
                return block
        return None
    
    def to_dict_list(self):
        """Convert blockchain to list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def from_dict_list(self, data_list):
        """Load blockchain from list of dictionaries"""
        self.chain = [Block.from_dict(data) for data in data_list]
