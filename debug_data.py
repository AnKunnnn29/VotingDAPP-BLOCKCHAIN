"""Debug script to check database data"""
import sqlite3

conn = sqlite3.connect('voting_dapp.db')
cursor = conn.cursor()

print("=" * 50)
print("PROPOSALS:")
print("=" * 50)
cursor.execute('SELECT id, candidate_name, election_id FROM proposals')
for row in cursor.fetchall():
    print(f"  ID={row[0]}, Name={row[1]}, ElectionID={row[2]}")

print("\n" + "=" * 50)
print("ELECTIONS:")
print("=" * 50)
cursor.execute('SELECT id, title, state FROM elections')
for row in cursor.fetchall():
    print(f"  ID={row[0]}, Title={row[1]}, State={row[2]}")

print("\n" + "=" * 50)
print("VOTERS (voted status):")
print("=" * 50)
cursor.execute('SELECT id, full_name, voted, selected_proposal_id FROM voters LIMIT 10')
for row in cursor.fetchall():
    print(f"  ID={row[0]}, Name={row[1]}, Voted={row[2]}, ProposalID={row[3]}")

conn.close()
