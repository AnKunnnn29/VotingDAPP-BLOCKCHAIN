# 🏗️ Kiến trúc và Lý thuyết DApp Voting System

## 1. Tổng quan kiến trúc

Ứng dụng này mô phỏng một hệ thống bỏ phiếu phi tập trung (DApp) với đầy đủ các thành phần:

```
┌─────────────────────────────────────────────────┐
│              UI Layer (PySide6)                 │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │  Voter View  │         │   Admin View    │  │
│  └──────────────┘         └─────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│            Service Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Voting   │  │ Election │  │     Auth     │  │
│  │ Service  │  │ Service  │  │   Service    │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘
         ↓                    ↓
┌──────────────────┐   ┌─────────────────────────┐
│ Crypto Service   │   │   Blockchain Layer      │
│  (RSA, Sign)     │   │  ┌────────────────────┐ │
└──────────────────┘   │  │  Block → Block →   │ │
                       │  │  Block → Block     │ │
                       │  └────────────────────┘ │
                       └─────────────────────────┘
                                  ↓
                       ┌─────────────────────────┐
                       │   Database (SQLite)     │
                       └─────────────────────────┘
```

## 2. Smart Contract State Machine

### 2.1. Các trạng thái

```
┌───────┐     ┌──────────────┐     ┌──────┐
│ Start │ ──→ │ValidateVoter │ ──→ │ Vote │
└───────┘     └──────────────┘     └──────┘
                                       ↓
┌──────┐     ┌──────────────┐     ┌───────┐
│ Done │ ←── │DeclareWinner │ ←── │ Count │
└──────┘     └──────────────┘     └───────┘
```

### 2.2. Quy tắc chuyển trạng thái

| Trạng thái hiện tại | Trạng thái tiếp theo hợp lệ |
|---------------------|------------------------------|
| Start               | ValidateVoter                |
| ValidateVoter       | Vote                         |
| Vote                | Count                        |
| Count               | DeclareWinner                |
| DeclareWinner       | Done                         |
| Done                | (Kết thúc)                   |

### 2.3. Hành động theo trạng thái

- **Start**: Khởi tạo cuộc bầu cử
- **ValidateVoter**: Admin xác thực danh tính cử tri
- **Vote**: Cử tri bỏ phiếu
- **Count**: Hệ thống kiểm phiếu
- **DeclareWinner**: Công bố người thắng
- **Done**: Kết thúc và lưu trữ kết quả

## 3. Cryptography Implementation

### 3.1. Key Generation
```python
# Mỗi cử tri có cặp khóa RSA 2048-bit
private_key, public_key = generate_key_pair()
```

### 3.2. Digital Signature Flow
```
Vote Data: "voter_id:proposal_id:election_id"
         ↓
    Private Key (Voter)
         ↓
   Sign with RSA-PSS
         ↓
    Digital Signature
         ↓
    Public Key (System)
         ↓
      Verify
         ↓
   Valid / Invalid
```

### 3.3. Security Properties
- **Authenticity**: Chỉ người có private key mới tạo được chữ ký hợp lệ
- **Integrity**: Thay đổi vote data làm chữ ký không hợp lệ
- **Non-repudiation**: Không thể phủ nhận đã bỏ phiếu

## 4. Blockchain Implementation

### 4.1. Block Structure
```python
Block {
    index: int              # Vị trí trong chain
    timestamp: str          # Thời gian tạo
    voter_id: int          # ID cử tri
    proposal_id: int       # ID ứng viên được chọn
    signature: str         # Chữ ký số của cử tri
    previous_hash: str     # Hash của block trước
    hash: str             # Hash của block này
}
```

### 4.2. Hash Calculation
```python
hash = SHA256(
    index + timestamp + voter_id + 
    proposal_id + signature + previous_hash
)
```

### 4.3. Chain Validation
```python
for each block in chain:
    # Kiểm tra hash của block
    if block.hash != calculate_hash(block):
        return False
    
    # Kiểm tra liên kết với block trước
    if block.previous_hash != previous_block.hash:
        return False

return True
```

### 4.4. Immutability
- Thay đổi bất kỳ dữ liệu nào trong block → hash thay đổi
- Hash thay đổi → previous_hash của block sau không khớp
- Toàn bộ chain từ điểm thay đổi trở đi bị invalid

## 5. Permissionless vs Permissioned

### 5.1. Permissionless Mode (Ethereum-like)
**Đặc điểm:**
- Mọi cử tri đều có thể bỏ phiếu
- Không cần xác thực trước
- Phi tập trung cao
- Chậm hơn do cần consensus

**Use case:**
- Bỏ phiếu công cộng
- Khảo sát cộng đồng
- DAO voting

### 5.2. Permissioned Mode (Hyperledger-like)
**Đặc điểm:**
- Chỉ cử tri đã xác thực mới bỏ phiếu được
- Admin kiểm soát quyền truy cập
- Nhanh hơn
- Kém phi tập trung hơn

**Use case:**
- Bầu cử chính thức
- Bỏ phiếu doanh nghiệp
- Hội đồng quản trị

### 5.3. So sánh

| Tiêu chí           | Permissionless | Permissioned |
|--------------------|----------------|--------------|
| Decentralization   | ⭐⭐⭐⭐⭐      | ⭐⭐⭐        |
| Performance        | ⭐⭐⭐          | ⭐⭐⭐⭐⭐    |
| Security           | ⭐⭐⭐⭐        | ⭐⭐⭐⭐⭐    |
| Transparency       | ⭐⭐⭐⭐⭐      | ⭐⭐⭐⭐      |
| Access Control     | ⭐⭐            | ⭐⭐⭐⭐⭐    |

## 6. Data Models

### 6.1. Voter Model
```python
Voter {
    id: int                      # Unique identifier
    full_name: str              # Tên đầy đủ
    public_key: str             # RSA public key (PEM)
    private_key: str            # RSA private key (PEM)
    weight: int                 # Quyền biểu quyết (1-10)
    voted: bool                 # Đã bỏ phiếu chưa
    selected_proposal_id: int   # ID ứng viên đã chọn
    digital_signature: str      # Chữ ký số
    verified: bool              # Đã xác thực chưa
}
```

### 6.2. Proposal Model
```python
Proposal {
    id: int                # Unique identifier
    candidate_name: str    # Tên ứng viên
    description: str       # Mô tả
    vote_count: int       # Số phiếu nhận được
}
```

### 6.3. Election Model
```python
Election {
    id: int                    # Unique identifier
    title: str                 # Tiêu đề cuộc bầu cử
    description: str           # Mô tả
    state: str                 # Trạng thái hiện tại
    blockchain_mode: str       # Permissionless/Permissioned
    start_time: datetime       # Thời gian bắt đầu
    end_time: datetime         # Thời gian kết thúc
    winner_id: int            # ID người thắng
}
```

## 7. Voting Flow

### 7.1. Voter Perspective
```
1. Login với voter ID
2. Hệ thống load voter từ database
3. Kiểm tra voter.verified (nếu Permissioned mode)
4. Hiển thị danh sách proposals
5. Voter chọn 1 proposal
6. Click "Bỏ phiếu"
7. Tạo vote_data = "voter_id:proposal_id:election_id"
8. Sign vote_data với private_key → signature
9. Verify signature với public_key
10. Cập nhật voter.voted = True
11. Thêm block vào blockchain
12. Lưu blockchain vào database
13. Hiển thị thông báo thành công
```

### 7.2. Admin Perspective
```
1. Login với "admin"
2. Tạo election mới
3. Thêm proposals (ứng viên)
4. Thêm/xác thực voters
5. Chuyển state: Start → ValidateVoter
6. Chuyển state: ValidateVoter → Vote
7. (Voters bỏ phiếu)
8. Chuyển state: Vote → Count
9. Hệ thống đếm phiếu từ blockchain
10. Chuyển state: Count → DeclareWinner
11. Hệ thống xác định winner
12. Chuyển state: DeclareWinner → Done
13. Xem kết quả và biểu đồ
```

## 8. Security Considerations

### 8.1. Implemented
✅ Digital signatures cho mỗi phiếu
✅ Blockchain immutability
✅ One vote per voter enforcement
✅ State machine prevents invalid operations
✅ Public key verification

### 8.2. Production Requirements (Not in Demo)
⚠️ Secure private key storage (HSM, encrypted wallet)
⚠️ Network layer security (TLS, VPN)
⚠️ Consensus mechanism (PoW, PoS, PBFT)
⚠️ Smart contract audit
⚠️ DDoS protection
⚠️ Voter anonymity (zero-knowledge proofs)

## 9. Scalability Challenges

### 9.1. Current Limitations
- SQLite: Single-node, không scale horizontally
- In-memory blockchain: Giới hạn bởi RAM
- No sharding: Tất cả nodes phải lưu toàn bộ chain
- No layer 2: Mọi transaction đều on-chain

### 9.2. Production Solutions
- Distributed database (Cassandra, MongoDB)
- Sharding blockchain
- Layer 2 solutions (rollups)
- Off-chain computation với on-chain verification

## 10. Trade-offs trong thiết kế

### 10.1. Blockchain Trilemma
```
        Decentralization
              /\
             /  \
            /    \
           /      \
          /        \
         /          \
        /            \
       /              \
      /________________\
Security            Scalability
```

Không thể tối ưu cả 3 cùng lúc:
- **Permissionless**: Ưu tiên Decentralization + Security
- **Permissioned**: Ưu tiên Security + Scalability

### 10.2. Privacy vs Transparency
- **Transparency**: Mọi phiếu đều public trên blockchain
- **Privacy**: Cần zero-knowledge proofs (không có trong demo)

### 10.3. Cost vs Speed
- **On-chain**: Chậm, tốn gas, nhưng bảo mật cao
- **Off-chain**: Nhanh, rẻ, nhưng cần trust

## 11. Cách chạy Demo

### Scenario 1: Permissionless Election
```
1. Admin: Tạo election với mode "Permissionless"
2. Admin: Thêm 3 ứng viên
3. Admin: Start → ValidateVoter → Vote
4. Voter 15 (chưa verified): Login và bỏ phiếu → Thành công
5. Voter 5 (đã verified): Login và bỏ phiếu → Thành công
6. Admin: Vote → Count → DeclareWinner → Done
7. Xem kết quả và blockchain
```

### Scenario 2: Permissioned Election
```
1. Admin: Tạo election với mode "Permissioned"
2. Admin: Thêm 3 ứng viên
3. Admin: Xác thực voter 15
4. Admin: Start → ValidateVoter → Vote
5. Voter 15 (đã verified): Login và bỏ phiếu → Thành công
6. Voter 16 (chưa verified): Login và bỏ phiếu → Thất bại
7. Admin: Vote → Count → DeclareWinner → Done
```

### Scenario 3: Blockchain Integrity Check
```
1. Thực hiện bỏ phiếu bình thường
2. Admin: Vào tab Blockchain
3. Click "Kiểm tra tính toàn vẹn" → Valid
4. (Thủ công) Sửa database voting_dapp.db
5. Click "Kiểm tra tính toàn vẹn" → Invalid
```

## 12. Kết luận

Ứng dụng này thành công mô phỏng các khái niệm cốt lõi của DApp voting:

✅ **Smart Contract**: State machine với quy tắc nghiêm ngặt
✅ **Blockchain**: Immutable ledger với hash linking
✅ **Cryptography**: Digital signatures cho authentication
✅ **Decentralization**: Hai chế độ Permissionless/Permissioned
✅ **Transparency**: Mọi phiếu đều có thể audit
✅ **Security**: Chống double voting, verify signatures

Đây là nền tảng tốt để hiểu cách DApp voting hoạt động trước khi triển khai lên blockchain thật như Ethereum hoặc Hyperledger Fabric.
