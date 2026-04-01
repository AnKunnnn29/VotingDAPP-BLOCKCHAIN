"""Test vote logic"""
import sqlite3

def test_vote_logic(voter_id, proposal_id, election_id):
    conn = sqlite3.connect('voting_dapp.db')
    cursor = conn.cursor()
    
    # Get voter info
    cursor.execute('SELECT id, full_name, voted, selected_proposal_id FROM voters WHERE id=?', (voter_id,))
    voter = cursor.fetchone()
    print(f"\n{'='*60}")
    print(f"VOTER INFO:")
    print(f"  ID: {voter[0]}")
    print(f"  Name: {voter[1]}")
    print(f"  Voted: {voter[2]}")
    print(f"  Selected Proposal ID: {voter[3]}")
    
    # Get current election proposals
    cursor.execute('SELECT id, candidate_name, election_id FROM proposals WHERE election_id=?', (election_id,))
    proposals = cursor.fetchall()
    print(f"\nCURRENT ELECTION PROPOSALS (Election ID={election_id}):")
    proposal_ids = []
    for p in proposals:
        print(f"  Proposal ID={p[0]}, Name={p[1]}, ElectionID={p[2]}")
        proposal_ids.append(p[0])
    
    # Check if voter's selected_proposal_id is in current election
    print(f"\nCHECK:")
    print(f"  Voter's selected_proposal_id ({voter[3]}) in current election proposals {proposal_ids}?")
    if voter[3] in proposal_ids:
        print(f"  → YES - Voter already voted for this election")
        print(f"  → RESULT: CANNOT VOTE")
    else:
        print(f"  → NO - Voter has not voted for this election yet")
        print(f"  → RESULT: CAN VOTE")
    
    # Check if target proposal exists
    print(f"\nTARGET PROPOSAL:")
    print(f"  Proposal ID={proposal_id} in current election proposals {proposal_ids}?")
    if proposal_id in proposal_ids:
        print(f"  → YES - Proposal exists in current election")
    else:
        print(f"  → NO - Proposal does NOT exist in current election")
    
    conn.close()

# Test với cử tri 1 vote cho election 5
print("TEST CASE: Cử tri 1 muốn vote cho Proposal 5 trong Election 5")
test_vote_logic(voter_id=1, proposal_id=5, election_id=5)

print("\n" + "="*60)
print("TEST CASE: Cử tri 2 muốn vote cho Proposal 5 trong Election 5")
test_vote_logic(voter_id=2, proposal_id=5, election_id=5)
