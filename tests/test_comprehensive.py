"""
Comprehensive test suite for Voting DApp
Tests all critical flows and edge cases
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_manager import DatabaseManager
from blockchain.blockchain import Blockchain
from services.crypto_service import CryptoService
from services.voting_service import VotingService
from services.election_service import ElectionService
from services.auth_service import AuthService
from models.voter import Voter
from models.proposal import Proposal
from models.election import Election
from utils.constants import ElectionState, BlockchainMode

class TestVotingDApp:
    """Test suite for Voting DApp"""
    
    def __init__(self):
        self.test_db = "test_voting.db"
        self.setup()
        self.passed = 0
        self.failed = 0
        self.total = 0
    
    def setup(self):
        """Setup test environment"""
        # Remove old test database
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        # Initialize services
        self.db_manager = DatabaseManager(self.test_db)
        self.blockchain = Blockchain()
        self.crypto_service = CryptoService()
        self.voting_service = VotingService(self.db_manager, self.blockchain)
        self.election_service = ElectionService(self.db_manager)
        self.auth_service = AuthService(self.db_manager)
    
    def teardown(self):
        """Cleanup after tests"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def assert_true(self, condition, test_name):
        """Assert condition is true"""
        self.total += 1
        if condition:
            self.passed += 1
            print(f"✅ PASS: {test_name}")
            return True
        else:
            self.failed += 1
            print(f"❌ FAIL: {test_name}")
            return False

    
    def assert_false(self, condition, test_name):
        """Assert condition is false"""
        return self.assert_true(not condition, test_name)
    
    def assert_equal(self, actual, expected, test_name):
        """Assert actual equals expected"""
        self.total += 1
        if actual == expected:
            self.passed += 1
            print(f"✅ PASS: {test_name}")
            return True
        else:
            self.failed += 1
            print(f"❌ FAIL: {test_name} (Expected: {expected}, Got: {actual})")
            return False
    
    # ==================== BLOCKCHAIN TESTS ====================
    
    def test_genesis_block_creation(self):
        """Test 1: Genesis block should be created automatically"""
        blockchain = Blockchain()
        self.assert_equal(len(blockchain.chain), 1, "Genesis block created")
        self.assert_equal(blockchain.chain[0].index, 0, "Genesis block index is 0")
        self.assert_equal(blockchain.chain[0].previous_hash, "0", "Genesis previous_hash is 0")
    
    def test_add_vote_block(self):
        """Test 2: Adding vote block should work correctly"""
        blockchain = Blockchain()
        block = blockchain.add_vote_block(1, 1, "test_sig", 1)
        
        self.assert_equal(len(blockchain.chain), 2, "Block added to chain")
        self.assert_equal(block.index, 1, "Block index is 1")
        self.assert_equal(block.voter_id, 1, "Voter ID correct")
        self.assert_equal(block.proposal_id, 1, "Proposal ID correct")
        self.assert_equal(block.election_id, 1, "Election ID correct")
        self.assert_equal(block.previous_hash, blockchain.chain[0].hash, "Previous hash links correctly")
    
    def test_blockchain_validation(self):
        """Test 3: Blockchain validation should detect tampering"""
        blockchain = Blockchain()
        blockchain.add_vote_block(1, 1, "sig1", 1)
        blockchain.add_vote_block(2, 2, "sig2", 1)
        
        # Valid chain
        self.assert_true(blockchain.is_chain_valid(), "Valid blockchain passes validation")
        
        # Tamper with data
        blockchain.chain[1].voter_id = 999
        
        # Should detect tampering
        self.assert_false(blockchain.is_chain_valid(), "Tampered blockchain fails validation")
    
    def test_hash_deterministic(self):
        """Test 4: Hash calculation should be deterministic"""
        blockchain = Blockchain()
        block = blockchain.add_vote_block(1, 1, "sig", 1)
        
        hash1 = block.calculate_hash()
        hash2 = block.calculate_hash()
        
        self.assert_equal(hash1, hash2, "Hash is deterministic")
    
    def test_hash_changes_with_data(self):
        """Test 5: Hash should change when data changes"""
        blockchain = Blockchain()
        block = blockchain.add_vote_block(1, 1, "sig", 1)
        
        hash1 = block.hash
        block.voter_id = 2
        hash2 = block.calculate_hash()
        
        self.assert_true(hash1 != hash2, "Hash changes when data changes")
    
    def test_get_vote_by_voter_and_election(self):
        """Test 6: Should find vote by voter and election"""
        blockchain = Blockchain()
        blockchain.add_vote_block(1, 1, "sig1", 1)
        blockchain.add_vote_block(2, 2, "sig2", 1)
        blockchain.add_vote_block(1, 3, "sig3", 2)  # Same voter, different election
        
        vote1 = blockchain.get_vote_by_voter_and_election(1, 1)
        vote2 = blockchain.get_vote_by_voter_and_election(1, 2)
        
        self.assert_true(vote1 is not None, "Found vote for election 1")
        self.assert_equal(vote1.proposal_id, 1, "Correct proposal for election 1")
        self.assert_true(vote2 is not None, "Found vote for election 2")
        self.assert_equal(vote2.proposal_id, 3, "Correct proposal for election 2")
    
    def test_get_votes_by_election(self):
        """Test 7: Should get all votes for an election"""
        blockchain = Blockchain()
        blockchain.add_vote_block(1, 1, "sig1", 1)
        blockchain.add_vote_block(2, 2, "sig2", 1)
        blockchain.add_vote_block(3, 1, "sig3", 2)
        
        votes_election1 = blockchain.get_votes_by_election(1)
        votes_election2 = blockchain.get_votes_by_election(2)
        
        self.assert_equal(len(votes_election1), 2, "2 votes for election 1")
        self.assert_equal(len(votes_election2), 1, "1 vote for election 2")
    
    def test_duplicate_vote_detection(self):
        """Test 8: Should detect duplicate votes"""
        blockchain = Blockchain()
        blockchain.add_vote_block(1, 1, "sig1", 1)
        blockchain.add_vote_block(1, 2, "sig2", 1)  # Same voter, same election
        
        self.assert_true(blockchain.has_duplicate_votes(1), "Detects duplicate votes")
    
    # ==================== CRYPTOGRAPHY TESTS ====================
    
    def test_key_generation(self):
        """Test 9: Key generation should create valid key pairs"""
        private_key, public_key = self.crypto_service.generate_key_pair()
        
        self.assert_true(private_key is not None, "Private key generated")
        self.assert_true(public_key is not None, "Public key generated")
        self.assert_true("BEGIN PRIVATE KEY" in private_key, "Private key in PEM format")
        self.assert_true("BEGIN PUBLIC KEY" in public_key, "Public key in PEM format")
    
    def test_sign_and_verify(self):
        """Test 10: Signature should be verifiable"""
        private_key, public_key = self.crypto_service.generate_key_pair()
        vote_data = "1:1:1"
        
        signature = self.crypto_service.sign_vote(private_key, vote_data)
        is_valid = self.crypto_service.verify_signature(public_key, vote_data, signature)
        
        self.assert_true(is_valid, "Valid signature verifies correctly")
    
    def test_invalid_signature(self):
        """Test 11: Invalid signature should fail verification"""
        private_key, public_key = self.crypto_service.generate_key_pair()
        vote_data = "1:1:1"
        
        signature = self.crypto_service.sign_vote(private_key, vote_data)
        
        # Tamper with vote_data
        tampered_data = "1:2:1"
        is_valid = self.crypto_service.verify_signature(public_key, tampered_data, signature)
        
        self.assert_false(is_valid, "Tampered data fails verification")
    
    def test_wrong_public_key(self):
        """Test 12: Wrong public key should fail verification"""
        private_key1, public_key1 = self.crypto_service.generate_key_pair()
        private_key2, public_key2 = self.crypto_service.generate_key_pair()
        
        vote_data = "1:1:1"
        signature = self.crypto_service.sign_vote(private_key1, vote_data)
        
        # Try to verify with wrong public key
        is_valid = self.crypto_service.verify_signature(public_key2, vote_data, signature)
        
        self.assert_false(is_valid, "Wrong public key fails verification")

    
    # ==================== VOTING SERVICE TESTS ====================
    
    def test_vote_success_permissionless(self):
        """Test 13: Vote should succeed in Permissionless mode"""
        # Create voter
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test Voter", public_key=public_key, 
                     private_key=private_key, verified=False)
        voter.id = self.db_manager.add_voter(voter)
        
        # Create election
        election = self.election_service.create_election(
            "Test Election", "Test", BlockchainMode.PERMISSIONLESS
        )
        
        # Create proposal
        proposal = Proposal(id=0, candidate_name="Candidate A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        # Transition to Vote state
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Vote
        success, message = self.voting_service.cast_vote(voter, proposal.id, election)
        
        self.assert_true(success, "Vote succeeds in Permissionless mode (unverified voter)")
    
    def test_vote_blocked_permissioned(self):
        """Test 14: Unverified voter should be blocked in Permissioned mode"""
        # Create unverified voter
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test Voter", public_key=public_key, 
                     private_key=private_key, verified=False)
        voter.id = self.db_manager.add_voter(voter)
        
        # Create election
        election = self.election_service.create_election(
            "Test Election", "Test", BlockchainMode.PERMISSIONED
        )
        
        # Create proposal
        proposal = Proposal(id=0, candidate_name="Candidate A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        # Transition to Vote state
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Vote
        success, message = self.voting_service.cast_vote(voter, proposal.id, election)
        
        self.assert_false(success, "Unverified voter blocked in Permissioned mode")
        self.assert_true("xác thực" in message.lower(), "Error message mentions verification")
    
    def test_double_voting_prevention(self):
        """Test 15: Should prevent double voting"""
        # Create voter
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test Voter", public_key=public_key, 
                     private_key=private_key, verified=True)
        voter.id = self.db_manager.add_voter(voter)
        
        # Create election
        election = self.election_service.create_election(
            "Test Election", "Test", BlockchainMode.PERMISSIONLESS
        )
        
        # Create proposals
        proposal1 = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal1.id = self.db_manager.add_proposal(proposal1)
        proposal2 = Proposal(id=0, candidate_name="B", description="Test", election_id=election.id)
        proposal2.id = self.db_manager.add_proposal(proposal2)
        
        # Transition to Vote state
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # First vote
        success1, _ = self.voting_service.cast_vote(voter, proposal1.id, election)
        
        # Reload voter from DB
        voter = self.db_manager.get_voter_by_id(voter.id)
        
        # Second vote
        success2, message2 = self.voting_service.cast_vote(voter, proposal2.id, election)
        
        self.assert_true(success1, "First vote succeeds")
        self.assert_false(success2, "Second vote blocked")
        self.assert_true("đã bỏ phiếu" in message2.lower(), "Error message mentions already voted")

    
    def test_multi_election_voting(self):
        """Test 16: Voter should be able to vote in multiple elections"""
        # Create voter
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test Voter", public_key=public_key, 
                     private_key=private_key, verified=True)
        voter.id = self.db_manager.add_voter(voter)
        
        # Create election 1
        election1 = self.election_service.create_election(
            "Election 1", "Test", BlockchainMode.PERMISSIONLESS
        )
        proposal1 = Proposal(id=0, candidate_name="A1", description="Test", election_id=election1.id)
        proposal1.id = self.db_manager.add_proposal(proposal1)
        
        # Vote in election 1
        self.election_service.transition_state(election1, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election1, ElectionState.VOTE)
        success1, _ = self.voting_service.cast_vote(voter, proposal1.id, election1)
        
        # Create election 2
        election2 = self.election_service.create_election(
            "Election 2", "Test", BlockchainMode.PERMISSIONLESS
        )
        proposal2 = Proposal(id=0, candidate_name="A2", description="Test", election_id=election2.id)
        proposal2.id = self.db_manager.add_proposal(proposal2)
        
        # Vote in election 2
        self.election_service.transition_state(election2, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election2, ElectionState.VOTE)
        
        # Reload voter
        voter = self.db_manager.get_voter_by_id(voter.id)
        success2, _ = self.voting_service.cast_vote(voter, proposal2.id, election2)
        
        self.assert_true(success1, "Vote in election 1 succeeds")
        self.assert_true(success2, "Vote in election 2 succeeds")
        
        # Check blockchain has both votes
        votes_e1 = self.blockchain.get_votes_by_election(election1.id)
        votes_e2 = self.blockchain.get_votes_by_election(election2.id)
        
        self.assert_equal(len(votes_e1), 1, "1 vote in election 1")
        self.assert_equal(len(votes_e2), 1, "1 vote in election 2")
    
    def test_vote_wrong_state(self):
        """Test 17: Should block voting in wrong state"""
        # Create voter and election
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test", public_key=public_key, 
                     private_key=private_key, verified=True)
        voter.id = self.db_manager.add_voter(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        proposal = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        # Try to vote in START state
        success, message = self.voting_service.cast_vote(voter, proposal.id, election)
        
        self.assert_false(success, "Vote blocked in START state")
        self.assert_true("trạng thái" in message.lower(), "Error mentions state")
    
    def test_vote_nonexistent_proposal(self):
        """Test 18: Should block voting for nonexistent proposal"""
        # Create voter and election
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test", public_key=public_key, 
                     private_key=private_key, verified=True)
        voter.id = self.db_manager.add_voter(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Transition to Vote
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Try to vote for nonexistent proposal
        success, message = self.voting_service.cast_vote(voter, 9999, election)
        
        self.assert_false(success, "Vote blocked for nonexistent proposal")
        self.assert_true("không tồn tại" in message.lower() or "chưa có ứng viên" in message.lower(), "Error mentions nonexistent or no proposals")
    
    def test_negative_weight(self):
        """Test 19: Should block voting with negative weight"""
        # Create voter with negative weight
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test", public_key=public_key, 
                     private_key=private_key, verified=True, weight=-1)
        voter.id = self.db_manager.add_voter(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        proposal = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        # Transition to Vote
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Try to vote
        success, message = self.voting_service.cast_vote(voter, proposal.id, election)
        
        self.assert_false(success, "Vote blocked with negative weight")

    
    # ==================== STATE MACHINE TESTS ====================
    
    def test_state_transitions(self):
        """Test 20: State transitions should follow rules"""
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Valid transitions
        success1, _ = self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        election = self.election_service.get_current_election()
        success2, _ = self.election_service.transition_state(election, ElectionState.VOTE)
        election = self.election_service.get_current_election()
        success3, _ = self.election_service.transition_state(election, ElectionState.COUNT)
        
        self.assert_true(success1, "START → VALIDATE_VOTER succeeds")
        self.assert_true(success2, "VALIDATE_VOTER → VOTE succeeds")
        self.assert_true(success3, "VOTE → COUNT succeeds")
    
    def test_invalid_state_transition(self):
        """Test 21: Invalid state transitions should be blocked"""
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Try to skip states
        success, message = self.election_service.transition_state(election, ElectionState.COUNT)
        
        self.assert_false(success, "Cannot skip states")
        self.assert_true("không thể chuyển" in message.lower(), "Error mentions invalid transition")
    
    def test_state_transition_from_done(self):
        """Test 22: Cannot transition from DONE state"""
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Transition to DONE
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.VOTE)
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.DECLARE_WINNER)
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.DONE)
        election = self.election_service.get_current_election()
        
        # Try to transition from DONE
        success, _ = self.election_service.transition_state(election, ElectionState.START)
        
        self.assert_false(success, "Cannot transition from DONE state")
    
    # ==================== VOTE COUNTING TESTS ====================
    
    def test_vote_counting_accuracy(self):
        """Test 23: Vote counting should be accurate"""
        # Create 3 voters
        voters = []
        for i in range(3):
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(id=0, full_name=f"Voter {i}", public_key=public_key, 
                         private_key=private_key, verified=True, weight=1)
            voter.id = self.db_manager.add_voter(voter)
            voters.append(voter)
        
        # Create election
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Create 2 proposals
        proposal1 = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal1.id = self.db_manager.add_proposal(proposal1)
        proposal2 = Proposal(id=0, candidate_name="B", description="Test", election_id=election.id)
        proposal2.id = self.db_manager.add_proposal(proposal2)
        
        # Transition to Vote
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Vote: 2 for A, 1 for B
        self.voting_service.cast_vote(voters[0], proposal1.id, election)
        voters[0] = self.db_manager.get_voter_by_id(voters[0].id)
        
        self.voting_service.cast_vote(voters[1], proposal1.id, election)
        voters[1] = self.db_manager.get_voter_by_id(voters[1].id)
        
        self.voting_service.cast_vote(voters[2], proposal2.id, election)
        
        # Count votes
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        election = self.election_service.get_current_election()
        
        proposals = self.election_service.count_votes(election, self.blockchain)
        
        # Check counts
        prop1 = next(p for p in proposals if p.id == proposal1.id)
        prop2 = next(p for p in proposals if p.id == proposal2.id)
        
        self.assert_equal(prop1.vote_count, 2, "Proposal A has 2 votes")
        self.assert_equal(prop2.vote_count, 1, "Proposal B has 1 vote")
    
    def test_weighted_voting(self):
        """Test 24: Weighted voting should work correctly"""
        # Create voters with different weights
        voters = []
        weights = [1, 5, 10]
        for i, weight in enumerate(weights):
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(id=0, full_name=f"Voter {i}", public_key=public_key, 
                         private_key=private_key, verified=True, weight=weight)
            voter.id = self.db_manager.add_voter(voter)
            voters.append(voter)
        
        # Create election and proposal
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        proposal = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        # Transition to Vote
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # All vote for same proposal
        for voter in voters:
            self.voting_service.cast_vote(voter, proposal.id, election)
            voter = self.db_manager.get_voter_by_id(voter.id)
        
        # Count votes
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        election = self.election_service.get_current_election()
        
        proposals = self.election_service.count_votes(election, self.blockchain)
        prop = proposals[0]
        
        # Total should be 1 + 5 + 10 = 16
        self.assert_equal(prop.vote_count, 16, "Weighted voting: 1+5+10=16")
    
    def test_winner_declaration(self):
        """Test 25: Winner should be declared correctly"""
        # Setup election with votes
        voters = []
        for i in range(5):
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(id=0, full_name=f"Voter {i}", public_key=public_key, 
                         private_key=private_key, verified=True)
            voter.id = self.db_manager.add_voter(voter)
            voters.append(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        proposals = []
        for name in ["A", "B", "C"]:
            p = Proposal(id=0, candidate_name=name, description="Test", election_id=election.id)
            p.id = self.db_manager.add_proposal(p)
            proposals.append(p)
        
        # Transition and vote
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Votes: A=3, B=1, C=1
        self.voting_service.cast_vote(voters[0], proposals[0].id, election)
        voters[0] = self.db_manager.get_voter_by_id(voters[0].id)
        self.voting_service.cast_vote(voters[1], proposals[0].id, election)
        voters[1] = self.db_manager.get_voter_by_id(voters[1].id)
        self.voting_service.cast_vote(voters[2], proposals[0].id, election)
        voters[2] = self.db_manager.get_voter_by_id(voters[2].id)
        self.voting_service.cast_vote(voters[3], proposals[1].id, election)
        voters[3] = self.db_manager.get_voter_by_id(voters[3].id)
        self.voting_service.cast_vote(voters[4], proposals[2].id, election)
        
        # Count and declare
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        election = self.election_service.get_current_election()
        self.election_service.count_votes(election, self.blockchain)
        
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.DECLARE_WINNER)
        election = self.election_service.get_current_election()
        
        winner = self.election_service.declare_winner(election)
        
        self.assert_equal(winner.candidate_name, "A", "Candidate A wins with 3 votes")
    
    def test_tie_breaking(self):
        """Test 26: Tie should be handled deterministically"""
        # Create 2 voters
        voters = []
        for i in range(2):
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(id=0, full_name=f"Voter {i}", public_key=public_key, 
                         private_key=private_key, verified=True)
            voter.id = self.db_manager.add_voter(voter)
            voters.append(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Create 2 proposals
        proposals = []
        for name in ["A", "B"]:
            p = Proposal(id=0, candidate_name=name, description="Test", election_id=election.id)
            p.id = self.db_manager.add_proposal(p)
            proposals.append(p)
        
        # Vote: A=1, B=1 (tie)
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        self.voting_service.cast_vote(voters[0], proposals[0].id, election)
        voters[0] = self.db_manager.get_voter_by_id(voters[0].id)
        self.voting_service.cast_vote(voters[1], proposals[1].id, election)
        
        # Count and declare
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        election = self.election_service.get_current_election()
        self.election_service.count_votes(election, self.blockchain)
        
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.DECLARE_WINNER)
        election = self.election_service.get_current_election()
        
        winner = self.election_service.declare_winner(election)
        
        # Should select first one deterministically
        self.assert_true(winner is not None, "Winner declared despite tie")
        self.assert_equal(winner.candidate_name, "A", "First proposal wins in tie")

    
    # ==================== DATABASE TESTS ====================
    
    def test_blockchain_persistence(self):
        """Test 27: Blockchain should persist correctly"""
        blockchain = Blockchain()
        blockchain.add_vote_block(1, 1, "sig1", 1)
        blockchain.add_vote_block(2, 2, "sig2", 1)
        
        # Save
        self.db_manager.save_blockchain(blockchain)
        
        # Load
        loaded_blockchain = self.db_manager.load_blockchain()
        
        self.assert_equal(len(loaded_blockchain.chain), 3, "Loaded blockchain has 3 blocks")
        self.assert_equal(loaded_blockchain.chain[1].voter_id, 1, "Block 1 data correct")
        self.assert_equal(loaded_blockchain.chain[2].voter_id, 2, "Block 2 data correct")
    
    def test_voter_crud(self):
        """Test 28: Voter CRUD operations"""
        # Create
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test", public_key=public_key, 
                     private_key=private_key, verified=True)
        voter_id = self.db_manager.add_voter(voter)
        
        # Read
        loaded_voter = self.db_manager.get_voter_by_id(voter_id)
        self.assert_true(loaded_voter is not None, "Voter can be retrieved")
        self.assert_equal(loaded_voter.full_name, "Test", "Voter name correct")
        
        # Update
        loaded_voter.full_name = "Updated"
        self.db_manager.update_voter(loaded_voter)
        updated_voter = self.db_manager.get_voter_by_id(voter_id)
        self.assert_equal(updated_voter.full_name, "Updated", "Voter updated correctly")
    
    def test_proposal_crud(self):
        """Test 29: Proposal CRUD operations"""
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        # Create
        proposal = Proposal(id=0, candidate_name="Test", description="Desc", election_id=election.id)
        proposal_id = self.db_manager.add_proposal(proposal)
        
        # Read
        proposals = self.db_manager.get_all_proposals(election.id)
        self.assert_equal(len(proposals), 1, "Proposal created")
        self.assert_equal(proposals[0].candidate_name, "Test", "Proposal name correct")
        
        # Update
        proposals[0].candidate_name = "Updated"
        self.db_manager.update_proposal(proposals[0])
        updated = self.db_manager.get_all_proposals(election.id)[0]
        self.assert_equal(updated.candidate_name, "Updated", "Proposal updated")
        
        # Delete
        self.db_manager.delete_proposal(proposal_id)
        remaining = self.db_manager.get_all_proposals(election.id)
        self.assert_equal(len(remaining), 0, "Proposal deleted")
    
    # ==================== INTEGRATION TESTS ====================
    
    def test_full_election_flow(self):
        """Test 30: Complete election flow from start to finish"""
        # Create 5 voters
        voters = []
        for i in range(5):
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(id=0, full_name=f"Voter {i}", public_key=public_key, 
                         private_key=private_key, verified=True, weight=1)
            voter.id = self.db_manager.add_voter(voter)
            voters.append(voter)
        
        # Create election
        election = self.election_service.create_election(
            "Presidential Election", "Test", BlockchainMode.PERMISSIONLESS
        )
        
        # Add 3 candidates
        proposals = []
        for name in ["Alice", "Bob", "Charlie"]:
            p = Proposal(id=0, candidate_name=name, description=f"Candidate {name}", election_id=election.id)
            p.id = self.db_manager.add_proposal(p)
            proposals.append(p)
        
        # State: START → VALIDATE_VOTER
        success, _ = self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.assert_true(success, "Transition to VALIDATE_VOTER")
        
        # State: VALIDATE_VOTER → VOTE
        election = self.election_service.get_current_election()
        success, _ = self.election_service.transition_state(election, ElectionState.VOTE)
        self.assert_true(success, "Transition to VOTE")
        
        # Voting: Alice=3, Bob=1, Charlie=1
        election = self.election_service.get_current_election()
        self.voting_service.cast_vote(voters[0], proposals[0].id, election)
        voters[0] = self.db_manager.get_voter_by_id(voters[0].id)
        
        self.voting_service.cast_vote(voters[1], proposals[0].id, election)
        voters[1] = self.db_manager.get_voter_by_id(voters[1].id)
        
        self.voting_service.cast_vote(voters[2], proposals[0].id, election)
        voters[2] = self.db_manager.get_voter_by_id(voters[2].id)
        
        self.voting_service.cast_vote(voters[3], proposals[1].id, election)
        voters[3] = self.db_manager.get_voter_by_id(voters[3].id)
        
        self.voting_service.cast_vote(voters[4], proposals[2].id, election)
        
        # State: VOTE → COUNT
        election = self.election_service.get_current_election()
        success, _ = self.election_service.transition_state(election, ElectionState.COUNT)
        self.assert_true(success, "Transition to COUNT")
        
        # Count votes
        election = self.election_service.get_current_election()
        counted_proposals = self.election_service.count_votes(election, self.blockchain)
        
        alice = next(p for p in counted_proposals if p.candidate_name == "Alice")
        bob = next(p for p in counted_proposals if p.candidate_name == "Bob")
        charlie = next(p for p in counted_proposals if p.candidate_name == "Charlie")
        
        self.assert_equal(alice.vote_count, 3, "Alice has 3 votes")
        self.assert_equal(bob.vote_count, 1, "Bob has 1 vote")
        self.assert_equal(charlie.vote_count, 1, "Charlie has 1 vote")
        
        # State: COUNT → DECLARE_WINNER
        election = self.election_service.get_current_election()
        success, _ = self.election_service.transition_state(election, ElectionState.DECLARE_WINNER)
        self.assert_true(success, "Transition to DECLARE_WINNER")
        
        # Declare winner
        election = self.election_service.get_current_election()
        winner = self.election_service.declare_winner(election)
        
        self.assert_equal(winner.candidate_name, "Alice", "Alice wins")
        
        # State: DECLARE_WINNER → DONE
        election = self.election_service.get_current_election()
        success, _ = self.election_service.transition_state(election, ElectionState.DONE)
        self.assert_true(success, "Transition to DONE")
        
        # Verify blockchain
        self.assert_true(self.blockchain.is_chain_valid(), "Blockchain remains valid")
        self.assert_equal(len(self.blockchain.chain), 6, "6 blocks total (1 genesis + 5 votes)")
    
    def test_blockchain_count_consistency(self):
        """Test 31: Vote count from blockchain should match database"""
        # Create voters and vote
        voters = []
        for i in range(3):
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(id=0, full_name=f"Voter {i}", public_key=public_key, 
                         private_key=private_key, verified=True)
            voter.id = self.db_manager.add_voter(voter)
            voters.append(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        proposal = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # All vote for same proposal
        election = self.election_service.get_current_election()
        for voter in voters:
            self.voting_service.cast_vote(voter, proposal.id, election)
            voter = self.db_manager.get_voter_by_id(voter.id)
        
        # Count from blockchain
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        election = self.election_service.get_current_election()
        
        proposals = self.election_service.count_votes(election, self.blockchain)
        
        # Count from blockchain directly
        blockchain_votes = self.blockchain.get_votes_by_election(election.id)
        
        self.assert_equal(len(blockchain_votes), 3, "3 votes in blockchain")
        self.assert_equal(proposals[0].vote_count, 3, "3 votes counted")

    
    # ==================== EDGE CASE TESTS ====================
    
    def test_empty_election(self):
        """Test 32: Election with no proposals"""
        voter_key = self.crypto_service.generate_key_pair()
        voter = Voter(id=0, full_name="Test", public_key=voter_key[1], 
                     private_key=voter_key[0], verified=True)
        voter.id = self.db_manager.add_voter(voter)
        
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        
        # Try to vote with no proposals
        election = self.election_service.get_current_election()
        success, message = self.voting_service.cast_vote(voter, 1, election)
        
        self.assert_false(success, "Cannot vote in election with no proposals")
        self.assert_true("chưa có ứng viên" in message.lower(), "Error mentions no proposals")
    
    def test_election_with_no_votes(self):
        """Test 33: Election with no votes should handle counting"""
        election = self.election_service.create_election("Test", "Test", BlockchainMode.PERMISSIONLESS)
        proposal = Proposal(id=0, candidate_name="A", description="Test", election_id=election.id)
        proposal.id = self.db_manager.add_proposal(proposal)
        
        # Transition to COUNT without any votes
        self.election_service.transition_state(election, ElectionState.VALIDATE_VOTER)
        self.election_service.transition_state(election, ElectionState.VOTE)
        election = self.election_service.get_current_election()
        self.election_service.transition_state(election, ElectionState.COUNT)
        
        election = self.election_service.get_current_election()
        proposals = self.election_service.count_votes(election, self.blockchain)
        
        self.assert_equal(proposals[0].vote_count, 0, "No votes counted")
    
    def test_blockchain_serialization(self):
        """Test 34: Blockchain serialization and deserialization"""
        blockchain = Blockchain()
        blockchain.add_vote_block(1, 1, "sig1", 1)
        blockchain.add_vote_block(2, 2, "sig2", 1)
        
        # Serialize
        dict_list = blockchain.to_dict_list()
        
        # Deserialize
        new_blockchain = Blockchain()
        new_blockchain.from_dict_list(dict_list)
        
        self.assert_equal(len(new_blockchain.chain), 3, "Deserialized blockchain has 3 blocks")
        self.assert_true(new_blockchain.is_chain_valid(), "Deserialized blockchain is valid")
        self.assert_equal(new_blockchain.chain[1].voter_id, 1, "Block data preserved")
    
    # ==================== RUN ALL TESTS ====================
    
    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "="*70)
        print("🧪 VOTING DAPP - COMPREHENSIVE TEST SUITE")
        print("="*70 + "\n")
        
        print("📦 BLOCKCHAIN TESTS")
        print("-" * 70)
        self.test_genesis_block_creation()
        self.test_add_vote_block()
        self.test_blockchain_validation()
        self.test_hash_deterministic()
        self.test_hash_changes_with_data()
        self.test_get_vote_by_voter_and_election()
        self.test_get_votes_by_election()
        self.test_duplicate_vote_detection()
        
        print("\n🔐 CRYPTOGRAPHY TESTS")
        print("-" * 70)
        self.test_key_generation()
        self.test_sign_and_verify()
        self.test_invalid_signature()
        self.test_wrong_public_key()
        
        print("\n🗳️ VOTING SERVICE TESTS")
        print("-" * 70)
        self.test_vote_success_permissionless()
        self.test_vote_blocked_permissioned()
        self.test_double_voting_prevention()
        self.test_multi_election_voting()
        self.test_vote_wrong_state()
        self.test_vote_nonexistent_proposal()
        self.test_negative_weight()
        
        print("\n🔄 STATE MACHINE TESTS")
        print("-" * 70)
        self.test_state_transitions()
        self.test_invalid_state_transition()
        self.test_state_transition_from_done()
        
        print("\n📊 VOTE COUNTING TESTS")
        print("-" * 70)
        self.test_vote_counting_accuracy()
        self.test_weighted_voting()
        self.test_winner_declaration()
        self.test_tie_breaking()
        
        print("\n💾 DATABASE TESTS")
        print("-" * 70)
        self.test_blockchain_persistence()
        self.test_voter_crud()
        self.test_proposal_crud()
        
        print("\n⚠️ EDGE CASE TESTS")
        print("-" * 70)
        self.test_empty_election()
        self.test_election_with_no_votes()
        self.test_blockchain_serialization()
        
        # Summary
        print("\n" + "="*70)
        print("📈 TEST SUMMARY")
        print("="*70)
        print(f"Total tests: {self.total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success rate: {(self.passed/self.total*100):.1f}%")
        print("="*70 + "\n")
        
        # Cleanup
        self.teardown()
        
        return self.failed == 0


if __name__ == "__main__":
    tester = TestVotingDApp()
    all_passed = tester.run_all_tests()
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("⚠️ SOME TESTS FAILED!")
        sys.exit(1)
