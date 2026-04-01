"""Script to setup demo data for quick testing"""
from database.db_manager import DatabaseManager
from services.crypto_service import CryptoService
from services.election_service import ElectionService
from models.voter import Voter
from models.proposal import Proposal
from models.election import Election
from utils.constants import BlockchainMode

def setup_demo():
    """Setup complete demo environment"""
    db = DatabaseManager()
    crypto = CryptoService()
    election_service = ElectionService(db)
    
    print("🚀 Setting up demo data...")
    
    # Clear existing data
    db.clear_all_data()
    print("✅ Cleared existing data")
    
    # Create voters
    print("👥 Creating 20 voters...")
    for i in range(1, 21):
        private_key, public_key = crypto.generate_key_pair()
        voter = Voter(
            id=0,
            full_name=f"Cử tri {i}",
            public_key=public_key,
            private_key=private_key,
            weight=1,
            verified=(i <= 10)
        )
        db.add_voter(voter)
    print("✅ Created 20 voters (1-10 verified, 11-20 unverified)")
    
    # Create election
    print("📋 Creating election...")
    election = election_service.create_election(
        title="Bầu cử Tổng thống 2026",
        description="Bầu chọn tổng thống nhiệm kỳ 2026-2030",
        blockchain_mode=BlockchainMode.PERMISSIONLESS
    )
    print(f"✅ Created election: {election.title}")
    
    # Create proposals
    print("🎯 Creating proposals...")
    proposals_data = [
        ("Nguyễn Văn A", "Ứng viên có kinh nghiệm 20 năm trong lĩnh vực quản lý"),
        ("Trần Thị B", "Ứng viên trẻ năng động với tầm nhìn đổi mới"),
        ("Lê Văn C", "Ứng viên cải cách với chương trình phát triển bền vững"),
    ]
    
    for name, desc in proposals_data:
        proposal = Proposal(id=0, candidate_name=name, description=desc)
        db.add_proposal(proposal)
    print("✅ Created 3 proposals")
    
    print("\n🎉 Demo setup complete!")
    print("\n📝 Quick start:")
    print("1. Run: python main.py")
    print("2. Login as admin (role: Quản trị viên, code: admin)")
    print("3. Go to tab '📋 Cuộc bầu cử'")
    print("4. Click: 1️⃣ Xác thực cử tri → 2️⃣ Mở bỏ phiếu")
    print("5. Logout and login as voter (role: Cử tri, code: 1-20)")
    print("6. Vote for a candidate")
    print("7. Login as admin again and complete the process")

if __name__ == "__main__":
    setup_demo()
