"""Blockchain implementation for immutable vote ledger with advanced features"""
from datetime import datetime
from typing import List, Optional
from blockchain.block import Block
import time
import hashlib

class Transaction:
    """Represents a pending transaction in the mempool"""
    def __init__(self, voter_id: int, proposal_id: int, signature: str, election_id: int):
        self.voter_id = voter_id
        self.proposal_id = proposal_id
        self.signature = signature
        self.election_id = election_id
        self.timestamp = datetime.now().isoformat()

class Blockchain:
    """Immutable ledger for storing votes with mining and consensus"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty  # Mining difficulty (number of leading zeros)
        self.pending_transactions: List[Transaction] = []  # Mempool
        self.mining_reward = 10  # Reward for mining a block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            voter_id=0,
            proposal_id=0,
            signature="genesis",
            previous_hash="0",
            election_id=0,
            nonce=0,
            difficulty=self.difficulty,
            miner="genesis"
        )
        # Genesis block doesn't need mining
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, voter_id: int, proposal_id: int, signature: str, election_id: int):
        """Add a transaction to the mempool (pending transactions)"""
        transaction = Transaction(voter_id, proposal_id, signature, election_id)
        self.pending_transactions.append(transaction)
        return transaction
    
    def mine_pending_transactions(self, miner_address: str = "system") -> tuple[Block, float]:
        """
        Mine all pending transactions into a new block
        Returns: (block, mining_time)
        """
        if not self.pending_transactions:
            return None, 0
        
        # Take first transaction from mempool
        transaction = self.pending_transactions[0]
        
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            voter_id=transaction.voter_id,
            proposal_id=transaction.proposal_id,
            signature=transaction.signature,
            previous_hash=previous_block.hash,
            election_id=transaction.election_id,
            nonce=0,
            difficulty=self.difficulty,
            miner=miner_address
        )
        
        # Mine the block (Proof of Work)
        print(f"\n⛏️ Mining block #{new_block.index} with difficulty {self.difficulty}...")
        hash_result, nonce, mining_time = new_block.mine_block(self.difficulty)
        print(f"✅ Block mined! Hash: {hash_result[:16]}... Nonce: {nonce} Time: {mining_time:.2f}s")
        
        self.chain.append(new_block)
        self.pending_transactions.pop(0)  # Remove mined transaction
        
        return new_block, mining_time
    
    def add_vote_block(self, voter_id: int, proposal_id: int, signature: str, election_id: int = 0, miner: str = "system") -> Block:
        """
        Add a new vote block to the chain (legacy method for compatibility)
        This adds to mempool and mines immediately
        """
        # Add to mempool
        self.add_transaction(voter_id, proposal_id, signature, election_id)
        
        # Mine immediately
        block, _ = self.mine_pending_transactions(miner)
        return block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain including Proof of Work"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Block {i} hash mismatch")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Block {i} previous hash mismatch")
                return False
            
            # Check Proof of Work (except genesis block)
            if i > 0 and not current_block.is_valid_proof():
                print(f"❌ Block {i} invalid proof of work")
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
    
    def get_vote_by_voter_and_election(self, voter_id: int, election_id: int) -> Optional[Block]:
        """Find a vote block by voter ID and election ID"""
        for block in reversed(self.chain):
            if block.voter_id == voter_id and block.election_id == election_id and block.index > 0:
                return block
        return None
    
    def add_vote_block_with_token(self, token: str, proposal_id: int, signature: str, 
                                   election_id: int = 0, miner: str = "system") -> Block:
        """
        Add a vote block using anonymous token instead of voter_id
        
        PRIVACY: This stores token (not voter_id) on blockchain
        After identity mapping is revoked, votes are permanently anonymous
        
        Args:
            token: Anonymous token (replaces voter_id)
            proposal_id: Proposal ID
            signature: Digital signature
            election_id: Election ID
            miner: Miner address
            
        Returns:
            Block
        """
        # Store token hash instead of raw token for extra privacy
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        # Use voter_id field to store token_hash (for compatibility)
        # In production, Block class should have a separate 'token' field
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            voter_id=int(token_hash[:16], 16) % (2**31),  # Convert hash to int for compatibility
            proposal_id=proposal_id,
            signature=signature,
            previous_hash=previous_block.hash,
            election_id=election_id,
            nonce=0,
            difficulty=self.difficulty,
            miner=miner
        )
        
        # Store original token hash in block for verification
        new_block.token_hash = token_hash
        
        # Mine the block
        print(f"\n⛏️ Mining anonymous vote block #{new_block.index}...")
        hash_result, nonce, mining_time = new_block.mine_block(self.difficulty)
        print(f"✅ Block mined! Hash: {hash_result[:16]}... Time: {mining_time:.2f}s")
        
        self.chain.append(new_block)
        return new_block
    
    def get_vote_by_token(self, token: str, election_id: int) -> Optional[Block]:
        """
        Find a vote block by token and election ID
        
        Args:
            token: Anonymous token
            election_id: Election ID
            
        Returns:
            Block or None
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        for block in reversed(self.chain):
            if hasattr(block, 'token_hash') and block.token_hash == token_hash and \
               block.election_id == election_id and block.index > 0:
                return block
        return None
    
    def get_votes_by_election(self, election_id: int) -> List[Block]:
        """Get all vote blocks for a specific election"""
        return [block for block in self.chain if block.election_id == election_id and block.index > 0]
    
    def has_duplicate_votes(self, election_id: int) -> bool:
        """Check if there are duplicate votes for an election"""
        voter_ids = set()
        for block in self.chain:
            if block.election_id == election_id and block.index > 0:
                if block.voter_id in voter_ids:
                    return True
                voter_ids.add(block.voter_id)
        return False
    
    def to_dict_list(self):
        """Convert blockchain to list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def from_dict_list(self, data_list):
        """Load blockchain from list of dictionaries"""
        self.chain = [Block.from_dict(data) for data in data_list]
