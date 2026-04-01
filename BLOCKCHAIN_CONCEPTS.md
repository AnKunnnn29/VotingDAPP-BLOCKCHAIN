# 🔗 Các khái niệm Blockchain được phản ánh trong ứng dụng

## 1. Blockchain và Distributed Ledger

### Trong ứng dụng
- File: `blockchain/blockchain.py`, `blockchain/block.py`
- Mỗi phiếu bầu được lưu thành 1 block
- Các block liên kết với nhau qua `previous_hash`
- Genesis block là block đầu tiên (index 0)

### Xem trong UI
- Admin → Tab "⛓️ Blockchain"
- Xem tất cả blocks với hash và previous_hash
- Kiểm tra tính toàn vẹn của chain

### Code minh họa
```python
# Tạo block mới
new_block = Block(
    index=len(chain),
    timestamp=now(),
    voter_id=voter.id,
    proposal_id=proposal.id,
    signature=digital_signature,
    previous_hash=previous_block.hash
)
new_block.hash = calculate_hash(new_block)
```

## 2. Smart Contract State Machine

### Trong ứng dụng
- File: `services/election_service.py`
- Method: `transition_state()`
- Quy tắc chuyển trạng thái được enforce bằng code

### State Flow
```
Start: Khởi tạo
  ↓
ValidateVoter: Admin xác thực cử tri
  ↓
Vote: Cử tri bỏ phiếu
  ↓
Count: Hệ thống đếm phiếu
  ↓
DeclareWinner: Công bố người thắng
  ↓
Done: Kết thúc
```

### Xem trong UI
- Admin → Tab "📋 Cuộc bầu cử"
- Các nút 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ đại diện cho state transitions
- Chỉ có thể click theo đúng thứ tự

### Code minh họa
```python
valid_transitions = {
    'Start': ['ValidateVoter'],
    'ValidateVoter': ['Vote'],
    'Vote': ['Count'],
    'Count': ['DeclareWinner'],
    'DeclareWinner': ['Done']
}

if new_state not in valid_transitions[current_state]:
    raise InvalidStateTransition()
```

## 3. Digital Signatures và Public Key Cryptography

### Trong ứng dụng
- File: `services/crypto_service.py`
- Sử dụng RSA 2048-bit
- Mỗi cử tri có 1 cặp khóa khi được tạo

### Quy trình ký và xác thực
```
1. Voter có private_key và public_key
2. Tạo vote_data = "voter_id:proposal_id:election_id"
3. Sign: signature = RSA_sign(vote_data, private_key)
4. Verify: is_valid = RSA_verify(vote_data, signature, public_key)
5. Nếu valid → Ghi vào blockchain
```

### Xem trong UI
- Voter → Click "📊 Xem trạng thái phiếu"
- Hiển thị signature của phiếu
- Admin → Tab "👥 Cử tri" → Xem public key

### Code minh họa
```python
# Generate keys
private_key, public_key = generate_key_pair()

# Sign vote
signature = sign_vote(private_key, vote_data)

# Verify
is_valid = verify_signature(public_key, vote_data, signature)
```

## 4. Immutability (Tính bất biến)

### Trong ứng dụng
- Mỗi block có hash được tính từ tất cả dữ liệu
- Block mới chứa hash của block trước
- Thay đổi bất kỳ dữ liệu nào → hash thay đổi → chain invalid

### Kiểm tra
```python
def is_chain_valid():
    for each block:
        # Kiểm tra hash của block
        if block.hash != calculate_hash(block):
            return False
        
        # Kiểm tra liên kết
        if block.previous_hash != previous_block.hash:
            return False
    return True
```

### Xem trong UI
- Admin → Tab "⛓️ Blockchain"
- Click "🔍 Kiểm tra tính toàn vẹn"
- Nếu ai đó sửa database → Chain invalid

### Demo
1. Bỏ vài phiếu
2. Kiểm tra → Valid ✅
3. Dùng DB Browser sửa voter_id trong blockchain table
4. Kiểm tra lại → Invalid ❌

## 5. Consensus và Validation

### Trong ứng dụng
- Mỗi phiếu phải pass validation trước khi vào blockchain:
  - Voter chưa bỏ phiếu
  - Signature hợp lệ
  - Election đang ở state "Vote"
  - Proposal tồn tại

### Code minh họa
```python
def cast_vote(voter, proposal_id):
    # Validate state
    if election.state != 'Vote':
        return False
    
    # Validate voter
    if voter.voted:
        return False
    
    # Validate signature
    if not verify_signature(...):
        return False
    
    # Add to blockchain
    blockchain.add_block(...)
```

## 6. Permissionless vs Permissioned

### Permissionless (Ethereum-like)
**Đặc điểm:**
- Mọi cử tri có thể bỏ phiếu
- Không cần xác thực trước
- Phi tập trung cao
- Trong code: `blockchain_mode = "Permissionless"`

**Trong UI:**
- Cử tri 11-20 (chưa verified) vẫn bỏ phiếu được

### Permissioned (Hyperledger-like)
**Đặc điểm:**
- Chỉ cử tri đã verified mới bỏ phiếu được
- Admin kiểm soát access
- Nhanh hơn, bảo mật hơn
- Trong code: `blockchain_mode = "Permissioned"`

**Trong UI:**
- Cử tri 11-20 (chưa verified) bị chặn khi bỏ phiếu

### Code minh họa
```python
if blockchain_mode == "Permissioned":
    if not voter.verified:
        return False, "Cử tri chưa được xác thực"
```

## 7. One Vote Per Voter

### Trong ứng dụng
- Mỗi voter có flag `voted`
- Sau khi bỏ phiếu, `voted = True`
- Không thể bỏ phiếu lần 2

### Code minh họa
```python
if voter.voted:
    return False, "Bạn đã bỏ phiếu rồi"

# After successful vote
voter.voted = True
db.update_voter(voter)
```

### Xem trong UI
- Voter: Sau khi bỏ phiếu, nút "🗳️ Bỏ phiếu" bị disable
- Admin → Tab "👥 Cử tri" → Cột "Đã bỏ phiếu" hiển thị ✅

## 8. Transparency và Auditability

### Trong ứng dụng
- Mọi phiếu đều được ghi vào blockchain
- Admin có thể xem tất cả blocks
- Có thể trace từng phiếu về voter

### Xem trong UI
- Admin → Tab "⛓️ Blockchain"
- Xem voter_id, proposal_id, signature của mỗi block
- Voter → "📊 Xem trạng thái phiếu" → Xem block của mình

## 9. Decentralization Levels

### High Decentralization (Permissionless)
- ✅ Không cần permission
- ✅ Mọi người đều tham gia được
- ❌ Chậm hơn
- ❌ Khó kiểm soát

### Moderate Decentralization (Permissioned)
- ✅ Nhanh hơn
- ✅ Kiểm soát access tốt hơn
- ❌ Phụ thuộc vào admin
- ❌ Kém phi tập trung

## 10. Gas Fees và Transaction Cost

### Trong production blockchain
- Mỗi transaction (vote) tốn gas fee
- Voter phải trả phí để ghi vào blockchain
- Fee cao khi network congested

### Trong ứng dụng demo
- Không có gas fee (simplified)
- Nhưng có thể thêm field `transaction_fee` vào Block
- Có thể mô phỏng fee calculation

### Mở rộng (không implement)
```python
class Block:
    ...
    transaction_fee: float  # ETH hoặc token
    gas_used: int          # Gas units
    gas_price: float       # Gwei
```

## 11. Challenges và Limitations

### 11.1. Smart Contract Bugs
**Vấn đề:**
- Bug trong state machine logic
- Lỗi trong vote counting
- Race conditions

**Trong ứng dụng:**
- State machine được test kỹ
- Vote counting có validation
- Single-threaded nên không có race condition

### 11.2. Scalability
**Vấn đề:**
- Blockchain size tăng tuyến tính với số phiếu
- Mỗi node phải lưu toàn bộ chain
- Validation time tăng theo chain length

**Trong ứng dụng:**
- SQLite có giới hạn
- Không có sharding
- Phù hợp cho demo nhỏ (< 10,000 votes)

### 11.3. Privacy
**Vấn đề:**
- Blockchain public → Mọi người xem được ai vote gì
- Cần zero-knowledge proofs để ẩn danh

**Trong ứng dụng:**
- Voter_id và proposal_id đều public
- Không có privacy (simplified)

### 11.4. 51% Attack
**Vấn đề:**
- Nếu ai đó kiểm soát > 50% nodes
- Có thể rewrite blockchain

**Trong ứng dụng:**
- Single node nên không có vấn đề này
- Trong production cần nhiều nodes và consensus

## 12. Mapping với Real Blockchain

### Ethereum
```
Smart Contract = election_service.py (state machine)
Transaction = cast_vote()
Block = Block class
Gas = (không có trong demo)
Consensus = (không có, single node)
```

### Hyperledger Fabric
```
Chaincode = voting_service.py
Channel = Election
Peer = (không có, single node)
Orderer = (không có, single node)
MSP = auth_service.py (membership)
```

## 13. Kết luận

Ứng dụng này thành công mô phỏng:

✅ **Blockchain fundamentals**: Hash, linking, immutability
✅ **Smart contract**: State machine, validation rules
✅ **Cryptography**: RSA keys, digital signatures
✅ **DApp concepts**: Decentralization, transparency
✅ **Access control**: Permissionless vs Permissioned

Những gì không có (do simplified):
❌ Network layer (P2P)
❌ Consensus mechanism (PoW, PoS)
❌ Gas fees
❌ Multiple nodes
❌ Privacy (zero-knowledge)

Đây là nền tảng tốt để học và hiểu DApp voting trước khi làm việc với blockchain thật!
