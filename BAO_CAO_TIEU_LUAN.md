# BÁO CÁO TIỂU LUẬN: ỨNG DỤNG BLOCKCHAIN TRONG HỆ THỐNG BỎ PHIẾU ĐIỆN TỬ

## THÔNG TIN CHUNG
- **Môn học:** Công nghệ Blockchain và ứng dụng
- **Sinh viên:** [Tên sinh viên] - MSSV: [Mã số]
- **Giảng viên:** [Tên giảng viên]
- **Thời gian:** Tháng 4/2026

---

## I. TỔNG QUAN HỆ THỐNG

### 1.1. Mục tiêu
Xây dựng hệ thống bỏ phiếu điện tử phi tập trung (DApp) với đầy đủ các thành phần blockchain cốt lõi:
- Blockchain ledger với hash linking và immutability
- Mật mã RSA 2048-bit cho digital signatures  
- Smart contract state machine
- Proof of Work consensus
- Xác thực sinh trắc học (face recognition)

### 1.2. Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.8+
- **GUI Framework:** PySide6 (Qt for Python)
- **Database:** SQLite
- **Cryptography:** RSA 2048-bit, SHA-256
- **Computer Vision:** OpenCV, face recognition

### 1.3. Kiến trúc hệ thống

`
┌─────────────────────────────────────────┐
│  UI LAYER (PySide6)                     │
│  - MainWindow, LoginDialog              │
│  - VoterView, AdminView                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SERVICE LAYER                          │
│  - VotingService                        │
│  - ElectionService (State Machine)      │
│  - CryptoService (RSA, Signatures)      │
│  - AuthService, FaceRecognitionService  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  BLOCKCHAIN LAYER                       │
│  Genesis → Block1 → Block2 → Block3     │
│  (hash_0)  (hash_1) (hash_2) (hash_3)   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  DATABASE LAYER (SQLite)                │
│  - voters, proposals, elections         │
│  - blockchain (JSON serialized)         │
└─────────────────────────────────────────┘
`

---

## II. PHÂN TÍCH CÁC THÀNH PHẦN BLOCKCHAIN

### 2.1. Block Structure (blockchain/block.py)

**Cấu trúc Block:**
