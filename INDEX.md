# 📚 Tài liệu DApp Voting System

## 🎯 Bắt đầu nhanh
- **[QUICKSTART.md](QUICKSTART.md)**: Hướng dẫn chạy demo trong 5 phút
- **[INSTALL_WINDOWS.md](INSTALL_WINDOWS.md)**: Hướng dẫn cài đặt chi tiết trên Windows
- **[README.md](README.md)**: Tổng quan về ứng dụng

## 🏗️ Kiến trúc và Lý thuyết
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Kiến trúc hệ thống và luồng dữ liệu
- **[BLOCKCHAIN_CONCEPTS.md](BLOCKCHAIN_CONCEPTS.md)**: Các khái niệm blockchain được mô phỏng
- **[CHALLENGES.md](CHALLENGES.md)**: Thách thức và trade-offs

## 🚀 Hướng dẫn sử dụng

### Cài đặt
```bash
pip install -r requirements.txt
```

### Chạy với demo data
```bash
python demo_setup.py
python main.py
```

### Chạy trực tiếp
```bash
python main.py
```

## 📖 Đọc theo thứ tự

### Người mới bắt đầu
1. **README.md** - Hiểu tổng quan
2. **QUICKSTART.md** - Chạy demo nhanh
3. **BLOCKCHAIN_CONCEPTS.md** - Học các khái niệm

### Người có kinh nghiệm
1. **ARCHITECTURE.md** - Hiểu kiến trúc
2. **CHALLENGES.md** - Hiểu trade-offs
3. Đọc source code

### Giảng viên/Sinh viên
1. **README.md** - Overview
2. **ARCHITECTURE.md** - Technical details
3. **BLOCKCHAIN_CONCEPTS.md** - Theory
4. **CHALLENGES.md** - Real-world issues
5. Source code - Implementation

## 🎓 Mục đích học tập

Ứng dụng này giúp hiểu:
- ✅ Blockchain fundamentals
- ✅ Smart contract state machine
- ✅ Digital signatures
- ✅ Decentralized applications
- ✅ Permissionless vs Permissioned
- ✅ Trade-offs trong thiết kế

## 🔧 Cấu trúc code

```
voting-dapp/
├── main.py                    # Entry point
├── demo_setup.py             # Demo data setup
├── models/                   # Data models
│   ├── voter.py             # Voter với crypto keys
│   ├── proposal.py          # Candidate/proposal
│   └── election.py          # Election với state machine
├── blockchain/              # Blockchain implementation
│   ├── block.py            # Block structure với hash
│   └── blockchain.py       # Chain với validation
├── services/               # Business logic
│   ├── crypto_service.py   # RSA signatures
│   ├── voting_service.py   # Vote operations
│   ├── auth_service.py     # Authentication
│   └── election_service.py # State machine
├── database/               # Persistence
│   └── db_manager.py      # SQLite operations
├── ui/                     # User interface
│   ├── main_window.py     # Main window
│   ├── login_dialog.py    # Login
│   ├── voter_view.py      # Voter interface
│   ├── admin_view.py      # Admin interface
│   └── styles.py          # Modern CSS-like styles
└── utils/                  # Utilities
    └── constants.py       # States, modes, colors
```

## 🎨 Screenshots (Mô tả)

### Login Screen
- Clean, modern design
- Role selection (Voter/Admin)
- ID input
- Blue primary color

### Voter View
- Voter info card
- Proposals table
- Vote button
- Status and results buttons

### Admin View
- 5 tabs: Election, Proposals, Voters, Blockchain, Results
- State machine controls
- CRUD operations
- Blockchain viewer
- Results chart

## 🧪 Testing Scenarios

### Test 1: Complete Election Flow
```
Admin: Create → Add candidates → Open voting
Voters: Vote (multiple voters)
Admin: Count → Declare → Done
Everyone: View results
```

### Test 2: Security Features
```
Test double voting → Blocked ✅
Test unverified voter in Permissioned → Blocked ✅
Test invalid signature → Blocked ✅
```

### Test 3: Blockchain Integrity
```
Vote normally → Chain valid ✅
Modify database → Chain invalid ✅
```

## 📊 Key Metrics

### Performance (Demo)
- Voters: 20 (can scale to 1000+)
- Proposals: 3 (can scale to 100+)
- Vote time: < 1 second
- Blockchain validation: < 1 second

### Security
- RSA 2048-bit keys
- SHA-256 hashing
- Digital signatures on all votes
- Immutable blockchain

## 🌟 Highlights

### Điểm mạnh
- ✅ Giao diện đẹp, hiện đại
- ✅ Code sạch, có cấu trúc
- ✅ Mô phỏng đúng lý thuyết
- ✅ Dễ demo và học tập
- ✅ Có đầy đủ tài liệu

### Giới hạn
- ❌ Single node (không phân tán thật)
- ❌ Không có network layer
- ❌ Không có consensus mechanism
- ❌ Không có privacy
- ❌ Demo only, không production-ready

## 🔗 Resources

### Học thêm về Blockchain Voting
- [Ethereum Voting DApp Tutorial](https://ethereum.org)
- [Hyperledger Fabric Voting](https://hyperledger.org)
- [Blockchain Voting Research Papers](https://scholar.google.com)

### Công nghệ sử dụng
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Cryptography Library](https://cryptography.io/)
- [Python SQLite](https://docs.python.org/3/library/sqlite3.html)

## 💬 Support

Nếu gặp vấn đề:
1. Đọc **INSTALL_WINDOWS.md**
2. Đọc **QUICKSTART.md**
3. Check **Troubleshooting** section trong README.md

## 📝 License

Demo/Academic project - For educational purposes only

---

**Happy Learning! 🎉**
