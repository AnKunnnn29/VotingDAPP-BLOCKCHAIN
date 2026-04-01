"""Database manager for SQLite operations"""
import sqlite3
import json
from typing import List, Optional
from models.voter import Voter
from models.proposal import Proposal
from models.election import Election
from blockchain.blockchain import Blockchain
from utils.constants import ElectionState, BlockchainMode

class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self, db_path: str = "voting_dapp.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Voters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                public_key TEXT NOT NULL,
                private_key TEXT NOT NULL,
                weight INTEGER DEFAULT 1,
                voted INTEGER DEFAULT 0,
                selected_proposal_id INTEGER,
                digital_signature TEXT,
                verified INTEGER DEFAULT 0
            )
        ''')
        
        # Proposals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_name TEXT NOT NULL,
                description TEXT,
                vote_count INTEGER DEFAULT 0,
                election_id INTEGER DEFAULT 0
            )
        ''')
        
        # Elections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                state TEXT DEFAULT 'Start',
                blockchain_mode TEXT DEFAULT 'Permissionless',
                start_time TEXT,
                end_time TEXT,
                winner_id INTEGER
            )
        ''')
        
        # Blockchain table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chain_data TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Voter operations
    def add_voter(self, voter: Voter) -> int:
        """Add a new voter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO voters (full_name, public_key, private_key, weight, verified)
            VALUES (?, ?, ?, ?, ?)
        ''', (voter.full_name, voter.public_key, voter.private_key, voter.weight, voter.verified))
        voter_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return voter_id
    
    def get_voter_by_id(self, voter_id: int) -> Optional[Voter]:
        """Get voter by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM voters WHERE id = ?', (voter_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Voter(
                id=row[0], full_name=row[1], public_key=row[2], private_key=row[3],
                weight=row[4], voted=bool(row[5]), selected_proposal_id=row[6],
                digital_signature=row[7], verified=bool(row[8])
            )
        return None
    
    def get_all_voters(self) -> List[Voter]:
        """Get all voters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM voters')
        rows = cursor.fetchall()
        conn.close()
        
        return [Voter(
            id=row[0], full_name=row[1], public_key=row[2], private_key=row[3],
            weight=row[4], voted=bool(row[5]), selected_proposal_id=row[6],
            digital_signature=row[7], verified=bool(row[8])
        ) for row in rows]
    
    def update_voter(self, voter: Voter):
        """Update voter information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE voters SET full_name=?, public_key=?, private_key=?, weight=?,
            voted=?, selected_proposal_id=?, digital_signature=?, verified=?
            WHERE id=?
        ''', (voter.full_name, voter.public_key, voter.private_key, voter.weight,
              voter.voted, voter.selected_proposal_id, voter.digital_signature,
              voter.verified, voter.id))
        conn.commit()
        conn.close()
    
    # Proposal operations
    def add_proposal(self, proposal: Proposal) -> int:
        """Add a new proposal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proposals (candidate_name, description, vote_count, election_id)
            VALUES (?, ?, ?, ?)
        ''', (proposal.candidate_name, proposal.description, proposal.vote_count, proposal.election_id))
        proposal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return proposal_id
    
    def get_all_proposals(self, election_id: Optional[int] = None) -> List[Proposal]:
        """Get all proposals, optionally filtered by election_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if election_id is not None:
            cursor.execute('SELECT * FROM proposals WHERE election_id=?', (election_id,))
        else:
            cursor.execute('SELECT * FROM proposals')
        rows = cursor.fetchall()
        conn.close()
        
        return [Proposal(id=row[0], candidate_name=row[1], description=row[2], 
                        vote_count=row[3], election_id=row[4] if len(row) > 4 else 0) 
                for row in rows]
    
    def update_proposal(self, proposal: Proposal):
        """Update proposal information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE proposals SET candidate_name=?, description=?, vote_count=?, election_id=?
            WHERE id=?
        ''', (proposal.candidate_name, proposal.description, proposal.vote_count, 
              proposal.election_id, proposal.id))
        conn.commit()
        conn.close()
    
    def delete_proposal(self, proposal_id: int):
        """Delete a proposal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM proposals WHERE id=?', (proposal_id,))
        conn.commit()
        conn.close()
    
    # Election operations
    def add_election(self, election: Election) -> int:
        """Add a new election"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO elections (title, description, state, blockchain_mode, start_time, end_time, winner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (election.title, election.description, election.state, election.blockchain_mode,
              election.start_time.isoformat() if election.start_time else None,
              election.end_time.isoformat() if election.end_time else None,
              election.winner_id))
        election_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return election_id
    
    def get_current_election(self) -> Optional[Election]:
        """Get the current active election"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM elections ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Election.from_dict({
                'id': row[0], 'title': row[1], 'description': row[2],
                'state': row[3], 'blockchain_mode': row[4],
                'start_time': row[5], 'end_time': row[6], 'winner_id': row[7]
            })
        return None
    
    def update_election(self, election: Election):
        """Update election information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE elections SET title=?, description=?, state=?, blockchain_mode=?,
            start_time=?, end_time=?, winner_id=?
            WHERE id=?
        ''', (election.title, election.description, election.state, election.blockchain_mode,
              election.start_time.isoformat() if election.start_time else None,
              election.end_time.isoformat() if election.end_time else None,
              election.winner_id, election.id))
        conn.commit()
        conn.close()
    
    # Blockchain operations
    def save_blockchain(self, blockchain: Blockchain):
        """Save blockchain to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        chain_data = json.dumps(blockchain.to_dict_list())
        
        # Clear existing blockchain data
        cursor.execute('DELETE FROM blockchain')
        cursor.execute('INSERT INTO blockchain (chain_data) VALUES (?)', (chain_data,))
        
        conn.commit()
        conn.close()
    
    def load_blockchain(self) -> Blockchain:
        """Load blockchain from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT chain_data FROM blockchain ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        
        blockchain = Blockchain()
        if row:
            chain_data = json.loads(row[0])
            blockchain.from_dict_list(chain_data)
        
        return blockchain
    
    def clear_all_data(self):
        """Clear all data from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM voters')
        cursor.execute('DELETE FROM proposals')
        cursor.execute('DELETE FROM elections')
        cursor.execute('DELETE FROM blockchain')
        conn.commit()
        conn.close()
