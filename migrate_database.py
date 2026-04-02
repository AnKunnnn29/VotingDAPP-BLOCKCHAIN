"""Database migration script to add CCCD and face_registered columns"""
import sqlite3

def migrate_database():
    """Add new columns to voters table"""
    conn = sqlite3.connect('voting_dapp.db')
    cursor = conn.cursor()
    
    # Check if columns exist
    cursor.execute("PRAGMA table_info(voters)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add cccd column if not exists
    if 'cccd' not in columns:
        print("Adding 'cccd' column...")
        cursor.execute("ALTER TABLE voters ADD COLUMN cccd TEXT DEFAULT ''")
        print("✅ Added 'cccd' column")
    else:
        print("'cccd' column already exists")
    
    # Add face_registered column if not exists
    if 'face_registered' not in columns:
        print("Adding 'face_registered' column...")
        cursor.execute("ALTER TABLE voters ADD COLUMN face_registered INTEGER DEFAULT 0")
        print("✅ Added 'face_registered' column")
    else:
        print("'face_registered' column already exists")
    
    conn.commit()
    conn.close()
    print("\n✅ Database migration completed!")

if __name__ == "__main__":
    migrate_database()
