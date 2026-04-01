"""Migration script to add election_id column to proposals table"""
import sqlite3

def migrate_database():
    """Add election_id column to proposals table"""
    conn = sqlite3.connect('voting_dapp.db')
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(proposals)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'election_id' not in columns:
            print("Adding election_id column to proposals table...")
            cursor.execute('ALTER TABLE proposals ADD COLUMN election_id INTEGER DEFAULT 0')
            conn.commit()
            print("✅ Migration completed successfully!")
        else:
            print("ℹ️ Column election_id already exists, skipping migration")
    
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
