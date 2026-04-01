"""Main entry point for the DApp Voting System"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db_manager import DatabaseManager
from services.crypto_service import CryptoService
from models.voter import Voter

def init_sample_data():
    """Initialize sample data for demo"""
    db = DatabaseManager()
    crypto = CryptoService()
    
    # Check if data already exists
    voters = db.get_all_voters()
    if len(voters) > 0:
        return  # Data already initialized
    
    # Create sample voters
    print("Initializing sample data...")
    for i in range(1, 21):
        private_key, public_key = crypto.generate_key_pair()
        voter = Voter(
            id=0,
            full_name=f"Cử tri {i}",
            public_key=public_key,
            private_key=private_key,
            weight=1,
            verified=(i <= 10)  # First 10 voters are verified
        )
        db.add_voter(voter)
    
    print(f"Created 20 sample voters (IDs 1-20)")
    print("First 10 voters are verified, last 10 are unverified")

def main():
    """Main function"""
    # Initialize sample data
    init_sample_data()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("DApp Voting System")
    app.setOrganizationName("Blockchain Voting")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
