"""
Demo script for Privacy-Enhanced Voting System

Features demonstrated:
1. Advanced Face Recognition with Liveness Detection
2. Anonymous Token-based Voting
3. Zero-Knowledge Proof Voting
4. Identity Revocation for Privacy
"""

from services.face_recognition_service_advanced import FaceRecognitionServiceAdvanced
from services.anonymous_token_service import AnonymousTokenService
from services.zkp_service import ZKPVotingSystem
from services.voting_service_enhanced import VotingServiceEnhanced
from database.db_manager import DatabaseManager
from blockchain.blockchain import Blockchain
from models.voter import Voter
from models.election import Election
from models.proposal import Proposal
from services.crypto_service import CryptoService

def demo_face_recognition_advanced():
    """Demo: Advanced Face Recognition with Liveness Detection"""
    print("\n" + "="*70)
    print("DEMO 1: ADVANCED FACE RECOGNITION + LIVENESS DETECTION")
    print("="*70)
    
    face_service = FaceRecognitionServiceAdvanced()
    
    print("\n📋 Tính năng:")
    print("  ✅ Deep Learning (128-D face encoding)")
    print("  ✅ Liveness Detection (blink + head movement)")
    print("  ✅ Threshold nghiêm ngặt (0.4 thay vì 0.6)")
    print("  ✅ Chống ảnh in, video, deepfake cơ bản")
    
    print("\n⚠️ Để test, cần webcam và thực hiện:")
    print("  1. Nhấp nháy mắt 2-3 lần")
    print("  2. Quay đầu sang trái, sau đó sang phải")
    print("  3. Nhấn SPACE để chụp ảnh")
    
    choice = input("\n🎯 Bạn có muốn test face recognition? (y/n): ")
    if choice.lower() == 'y':
        # Register
        print("\n--- ĐĂNG KÝ KHUÔN MẶT ---")
        success = face_service.register_face("123456789012", "Nguyễn Văn A")
        if success:
            print("✅ Đăng ký thành công!")
            
            # Verify
            print("\n--- XÁC THỰC KHUÔN MẶT ---")
            is_match, confidence = face_service.verify_face("123456789012")
            if is_match:
                print(f"✅ Xác thực thành công! Confidence: {confidence:.2%}")
            else:
                print(f"❌ Xác thực thất bại! Confidence: {confidence:.2%}")
    else:
        print("⏭️ Bỏ qua demo face recognition")

def demo_anonymous_token():
    """Demo: Anonymous Token System"""
    print("\n" + "="*70)
    print("DEMO 2: ANONYMOUS TOKEN SYSTEM")
    print("="*70)
    
    token_service = AnonymousTokenService()
    
    print("\n📋 Kiến trúc:")
    print("  1. Identity DB: CCCD ↔ Token (riêng biệt)")
    print("  2. Voting DB: Token ↔ Vote (không có CCCD)")
    print("  3. Blockchain: Token ↔ Proposal (không có CCCD)")
    
    # Simulate voters
    voters = [
        ("123456789012", "Nguyễn Văn A"),
        ("123456789013", "Trần Thị B"),
        ("123456789014", "Lê Văn C")
    ]
    
    election_id = 1
    
    print(f"\n--- TẠO ANONYMOUS TOKENS ---")
    tokens = {}
    for cccd, name in voters:
        token = token_service.generate_anonymous_token(cccd, election_id)
        tokens[name] = token
        print(f"  {name} (CCCD: {cccd})")
        print(f"    → Token: {token[:32]}...")
    
    print(f"\n--- KIỂM TRA TOKEN ---")
    for name, token in tokens.items():
        is_valid = token_service.verify_token(token, election_id)
        is_used = token_service.is_token_used(token)
        print(f"  {name}: Valid={is_valid}, Used={is_used}")
    
    print(f"\n--- ĐÁNH DẤU TOKEN ĐÃ SỬ DỤNG ---")
    token_service.mark_token_used(tokens["Nguyễn Văn A"])
    print(f"  Token của Nguyễn Văn A đã được đánh dấu")
    
    print(f"\n--- THỐNG KÊ TRƯỚC KHI REVOKE ---")
    stats = token_service.get_statistics(election_id)
    print(f"  Total tokens: {stats['total_tokens']}")
    print(f"  Used tokens: {stats['used_tokens']}")
    print(f"  Identity mappings exist: {stats['identity_mappings_exist']}")
    print(f"  Privacy protected: {stats['privacy_protected']}")
    
    print(f"\n--- REVOKE IDENTITY MAPPING (SAU BẦU CỬ) ---")
    token_service.revoke_identity_mapping(election_id)
    
    print(f"\n--- THỐNG KÊ SAU KHI REVOKE ---")
    stats_after = token_service.get_statistics(election_id)
    print(f"  Total tokens: {stats_after['total_tokens']}")
    print(f"  Used tokens: {stats_after['used_tokens']}")
    print(f"  Identity mappings exist: {stats_after['identity_mappings_exist']}")
    print(f"  Privacy protected: {stats_after['privacy_protected']}")
    
    if stats_after['privacy_protected']:
        print(f"\n🎉 SUCCESS: Không thể trace votes về voters nữa!")
    
    # Try to get CCCD by token (should fail after revocation)
    print(f"\n--- THỬ TRACE TOKEN VỀ CCCD (SAU REVOKE) ---")
    for name, token in tokens.items():
        cccd = token_service.get_cccd_by_token(token, election_id)
        if cccd:
            print(f"  ❌ {name}: CCCD = {cccd} (KHÔNG NÊN XẢY RA!)")
        else:
            print(f"  ✅ {name}: CCCD = None (Privacy protected!)")

def demo_zkp_voting():
    """Demo: Zero-Knowledge Proof Voting"""
    print("\n" + "="*70)
    print("DEMO 3: ZERO-KNOWLEDGE PROOF VOTING")
    print("="*70)
    
    zkp_system = ZKPVotingSystem()
    
    print("\n📋 Concept:")
    print("  Chứng minh bạn là cử tri hợp lệ KHÔNG tiết lộ danh tính")
    print("  - Không có voter_id trên blockchain")
    print("  - Sử dụng nullifier để ngăn double voting")
    print("  - Không thể trace votes về voters")
    
    # Setup
    registered_voters = [1, 2, 3, 4, 5]
    election_id = 1
    
    print(f"\n--- REGISTERED VOTERS ---")
    print(f"  Voter IDs: {registered_voters}")
    
    print(f"\n--- VOTER 1 BỎ PHIẾU CHO PROPOSAL 5 ---")
    success, message = zkp_system.cast_anonymous_vote(
        voter_id=1,
        proposal_id=5,
        election_id=election_id,
        registered_voters=registered_voters
    )
    print(f"  Result: {message}")
    
    if success:
        print(f"  ✅ Vote recorded anonymously!")
        print(f"  ⚠️ Blockchain KHÔNG chứa voter_id=1")
        print(f"  ⚠️ Chỉ có nullifier (không thể trace về voter)")
    
    print(f"\n--- VOTER 1 THỬ BỎ PHIẾU LẦN 2 (DOUBLE VOTING) ---")
    success2, message2 = zkp_system.cast_anonymous_vote(
        voter_id=1,
        proposal_id=3,
        election_id=election_id,
        registered_voters=registered_voters
    )
    print(f"  Result: {message2}")
    
    if not success2:
        print(f"  ✅ Double voting prevented by nullifier!")
    
    print(f"\n--- VOTER 2 BỎ PHIẾU CHO PROPOSAL 5 ---")
    success3, message3 = zkp_system.cast_anonymous_vote(
        voter_id=2,
        proposal_id=5,
        election_id=election_id,
        registered_voters=registered_voters
    )
    print(f"  Result: {message3}")
    
    print(f"\n--- VOTER 3 BỎ PHIẾU CHO PROPOSAL 3 ---")
    success4, message4 = zkp_system.cast_anonymous_vote(
        voter_id=3,
        proposal_id=3,
        election_id=election_id,
        registered_voters=registered_voters
    )
    print(f"  Result: {message4}")
    
    print(f"\n--- KẾT QUẢ BẦU CỬ ---")
    results = zkp_system.get_results(election_id)
    print(f"  Total votes: {results['total_votes']}")
    print(f"  Results: {results['results']}")
    print(f"  Privacy preserved: {results['privacy_preserved']}")
    
    print(f"\n🎉 ZKP Voting: HOÀN TOÀN ẨN DANH!")

def demo_full_workflow():
    """Demo: Full workflow with enhanced voting service"""
    print("\n" + "="*70)
    print("DEMO 4: FULL WORKFLOW - ENHANCED VOTING")
    print("="*70)
    
    # Setup
    db_manager = DatabaseManager(":memory:")  # In-memory database for demo
    blockchain = Blockchain(difficulty=2)  # Lower difficulty for demo
    voting_service = VotingServiceEnhanced(db_manager, blockchain)
    crypto_service = CryptoService()
    
    print("\n📋 Setup:")
    print("  - Database: In-memory")
    print("  - Blockchain: Difficulty 2")
    print("  - Privacy mode: TOKEN (default)")
    
    # Create election
    election = Election(
        id=1,
        title="Bầu cử Chủ tịch 2026",
        description="Bầu chọn chủ tịch nhiệm kỳ 2026-2031",
        state="Vote",
        blockchain_mode="Permissionless"
    )
    db_manager.add_election(election)
    
    # Create proposals
    proposals = [
        Proposal(id=1, candidate_name="Nguyễn Văn X", description="Ứng viên 1", election_id=1),
        Proposal(id=2, candidate_name="Trần Thị Y", description="Ứng viên 2", election_id=1),
        Proposal(id=3, candidate_name="Lê Văn Z", description="Ứng viên 3", election_id=1)
    ]
    for p in proposals:
        db_manager.add_proposal(p)
    
    print(f"\n--- ELECTION CREATED ---")
    print(f"  Title: {election.title}")
    print(f"  Proposals: {len(proposals)}")
    
    # Create voters
    voters = []
    for i in range(1, 4):
        pub_key, priv_key = crypto_service.generate_keypair()
        voter = Voter(
            id=i,
            full_name=f"Voter {i}",
            public_key=pub_key,
            private_key=priv_key,
            cccd=f"12345678901{i}",
            verified=True,
            face_registered=True
        )
        db_manager.add_voter(voter)
        voters.append(voter)
    
    print(f"\n--- VOTERS REGISTERED ---")
    for v in voters:
        print(f"  {v.full_name} (CCCD: {v.cccd})")
    
    # Vote with TOKEN mode
    print(f"\n--- VOTING (TOKEN MODE) ---")
    for i, voter in enumerate(voters):
        proposal_id = (i % 3) + 1  # Distribute votes
        success, message = voting_service.cast_vote(voter, proposal_id, election)
        print(f"  {voter.full_name} → Proposal {proposal_id}: {message[:50]}...")
    
    # Check blockchain
    print(f"\n--- BLOCKCHAIN ANALYSIS ---")
    print(f"  Total blocks: {len(blockchain.chain)}")
    print(f"  Vote blocks: {len(blockchain.chain) - 1}")  # Exclude genesis
    
    # Finalize election (revoke identity mapping)
    print(f"\n--- FINALIZE ELECTION ---")
    voting_service.finalize_election(election)
    
    # Try ZKP mode
    print(f"\n--- SWITCH TO ZKP MODE ---")
    voting_service.set_privacy_mode('zkp')
    
    # Create new election for ZKP
    election2 = Election(
        id=2,
        title="Bầu cử Phó Chủ tịch 2026",
        description="Bầu chọn phó chủ tịch",
        state="Vote",
        blockchain_mode="Permissionless"
    )
    db_manager.add_election(election2)
    
    # Add proposals for election 2
    for i in range(1, 3):
        p = Proposal(id=i+10, candidate_name=f"Candidate {i}", description=f"Ứng viên {i}", election_id=2)
        db_manager.add_proposal(p)
    
    print(f"\n--- VOTING (ZKP MODE) ---")
    for voter in voters[:2]:  # Only 2 voters for demo
        success, message = voting_service.cast_vote(voter, 11, election2)
        print(f"  {voter.full_name}: {message[:50]}...")
    
    # Get ZKP results
    print(f"\n--- ZKP RESULTS ---")
    zkp_results = voting_service.get_election_results_zkp(election2.id)
    print(f"  Total votes: {zkp_results['total_votes']}")
    print(f"  Results: {zkp_results['results']}")
    print(f"  Privacy preserved: {zkp_results['privacy_preserved']}")

def main():
    """Main demo menu"""
    print("\n" + "="*70)
    print("🔒 PRIVACY-ENHANCED VOTING SYSTEM - DEMO")
    print("="*70)
    
    print("\nChọn demo:")
    print("  1. Advanced Face Recognition + Liveness Detection")
    print("  2. Anonymous Token System")
    print("  3. Zero-Knowledge Proof Voting")
    print("  4. Full Workflow (Token + ZKP)")
    print("  5. Chạy tất cả demos")
    print("  0. Thoát")
    
    choice = input("\nNhập lựa chọn (0-5): ")
    
    if choice == '1':
        demo_face_recognition_advanced()
    elif choice == '2':
        demo_anonymous_token()
    elif choice == '3':
        demo_zkp_voting()
    elif choice == '4':
        demo_full_workflow()
    elif choice == '5':
        demo_face_recognition_advanced()
        demo_anonymous_token()
        demo_zkp_voting()
        demo_full_workflow()
    elif choice == '0':
        print("👋 Tạm biệt!")
        return
    else:
        print("❌ Lựa chọn không hợp lệ")
        return
    
    print("\n" + "="*70)
    print("✅ DEMO HOÀN TẤT")
    print("="*70)

if __name__ == "__main__":
    main()
