"""Election service for managing election state machine"""
from datetime import datetime
from typing import Optional, List
from models.election import Election
from models.proposal import Proposal
from database.db_manager import DatabaseManager
from utils.constants import ElectionState

class ElectionService:
    """Service for managing elections and state transitions"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_election(self, title: str, description: str, blockchain_mode: str) -> Election:
        """Create a new election"""
        election = Election(
            id=0,
            title=title,
            description=description,
            state=ElectionState.START,
            blockchain_mode=blockchain_mode,
            start_time=datetime.now()
        )
        election.id = self.db_manager.add_election(election)
        
        # NOTE: We do NOT reset voters' voted status here
        # The blockchain is the source of truth for who voted in which election
        # voter.voted is just a convenience flag, not authoritative
        # Each election is tracked separately by election_id in blockchain
        
        return election
    
    def get_current_election(self) -> Optional[Election]:
        """Get the current active election"""
        return self.db_manager.get_current_election()
    
    def transition_state(self, election: Election, new_state: str) -> tuple[bool, str]:
        """Transition election to new state following state machine rules"""
        valid_transitions = {
            ElectionState.START: [ElectionState.VALIDATE_VOTER],
            ElectionState.VALIDATE_VOTER: [ElectionState.VOTE],
            ElectionState.VOTE: [ElectionState.COUNT],
            ElectionState.COUNT: [ElectionState.DECLARE_WINNER],
            ElectionState.DECLARE_WINNER: [ElectionState.DONE],
            ElectionState.DONE: []
        }
        
        if new_state not in valid_transitions.get(election.state, []):
            return False, f"Không thể chuyển từ {election.state} sang {new_state}"
        
        election.state = new_state
        self.db_manager.update_election(election)
        return True, f"Đã chuyển sang trạng thái {new_state}"
    
    def count_votes(self, election: Election, blockchain) -> List[Proposal]:
        """Count all votes from blockchain and update proposal vote counts"""
        if election.state != ElectionState.COUNT:
            return []
        
        proposals = self.db_manager.get_all_proposals(election.id)
        voters = self.db_manager.get_all_voters()
        
        # Reset vote counts
        for proposal in proposals:
            proposal.vote_count = 0
        
        # Count votes from blockchain (source of truth)
        vote_blocks = blockchain.get_votes_by_election(election.id)
        
        for block in vote_blocks:
            # Find voter to get weight
            voter = next((v for v in voters if v.id == block.voter_id), None)
            if not voter:
                continue
            
            # Find proposal and add vote
            proposal = next((p for p in proposals if p.id == block.proposal_id), None)
            if proposal:
                proposal.vote_count += voter.weight
        
        # Update database
        for proposal in proposals:
            self.db_manager.update_proposal(proposal)
        
        return proposals
    
    def declare_winner(self, election: Election) -> Optional[Proposal]:
        """Declare the winner of the election"""
        if election.state != ElectionState.DECLARE_WINNER:
            return None
        
        proposals = self.db_manager.get_all_proposals(election.id)
        if not proposals:
            return None
        
        # Find max vote count
        max_votes = max(p.vote_count for p in proposals)
        
        # Get all proposals with max votes (handle ties)
        winners = [p for p in proposals if p.vote_count == max_votes]
        
        # If tie, select first one (deterministic)
        winner = winners[0]
        
        election.winner_id = winner.id
        election.end_time = datetime.now()
        self.db_manager.update_election(election)
        
        return winner
