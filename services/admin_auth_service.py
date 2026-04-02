"""Admin authentication service with multi-layer security"""
import hashlib
import secrets
import sqlite3
import random
from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta

class AdminAuthService:
    """
    Secure admin authentication with:
    - Password hashing (SHA-256 + Salt)
    - 2FA (OTP via console/email)
    - Rate limiting (max login attempts)
    - Account lockout
    - Session management
    - Audit logging
    """
    
    # Security settings
    MAX_LOGIN_ATTEMPTS = 5  # Số lần đăng nhập sai tối đa
    LOCKOUT_DURATION = 15  # Khóa tài khoản 15 phút
    SESSION_TIMEOUT = 30  # Session timeout 30 phút
    OTP_EXPIRY = 5  # OTP hết hạn sau 5 phút
    PASSWORD_MIN_LENGTH = 8
    
    def __init__(self, db_path: str = "voting_dapp.db"):
        self.db_path = db_path
        self.otp_storage = {}  # Temporary OTP storage {username: (otp, expiry)}
        self.init_admin_table()
        self.ensure_default_admin()
    
    def init_admin_table(self):
        """Initialize admin and security tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                created_at TEXT,
                last_login TEXT,
                is_active INTEGER DEFAULT 1,
                require_2fa INTEGER DEFAULT 1,
                failed_login_attempts INTEGER DEFAULT 0,
                locked_until TEXT
            )
        ''')
        
        # Session table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                session_token TEXT UNIQUE,
                created_at TEXT,
                expires_at TEXT,
                ip_address TEXT,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        ''')
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                username TEXT,
                action TEXT,
                details TEXT,
                ip_address TEXT,
                timestamp TEXT,
                success INTEGER,
                FOREIGN KEY (admin_id) REFERENCES admins(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def ensure_default_admin(self):
        """Create default admin if none exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM admins')
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_username = "admin"
            default_password = "Admin@2024"
            
            password_hash, salt = self.hash_password(default_password)
            
            cursor.execute('''
                INSERT INTO admins (username, password_hash, salt, full_name, 
                                   email, created_at, is_active, require_2fa)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (default_username, password_hash, salt, "Administrator", 
                  "admin@voting.local", datetime.now().isoformat(), 1, 1))
            
            conn.commit()
            print("\n" + "="*60)
            print("✅ ĐÃ TẠO TÀI KHOẢN ADMIN MẶC ĐỊNH")
            print("="*60)
            print(f"Username: {default_username}")
            print(f"Password: {default_password}")
            print("\n⚠️  BẢO MẬT:")
            print("1. VUI LÒNG ĐỔI MẬT KHẨU NGAY SAU KHI ĐĂNG NHẬP!")
            print("2. Mật khẩu mới phải có:")
            print("   - Ít nhất 8 ký tự")
            print("   - Chữ hoa, chữ thường, số, ký tự đặc biệt")
            print("3. 2FA (OTP) được bật mặc định")
            print("="*60 + "\n")
        
        conn.close()
    
    def hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password with salt using SHA-256"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        password_salt = f"{password}{salt}"
        password_hash = hashlib.sha256(password_salt.encode()).hexdigest()
        
        return password_hash, salt
    
    def generate_otp(self) -> str:
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def send_otp(self, username: str, email: str = None) -> Tuple[bool, str]:
        """
        Generate and send OTP
        For demo: Display in console
        For production: Send via email/SMS
        """
        otp = self.generate_otp()
        expiry = datetime.now() + timedelta(minutes=self.OTP_EXPIRY)
        
        # Store OTP temporarily
        self.otp_storage[username] = (otp, expiry)
        
        # For demo: Display in console
        print("\n" + "="*50)
        print("🔐 MÃ XÁC THỰC 2FA (OTP)")
        print("="*50)
        print(f"Mã OTP: {otp}")
        print(f"Hết hạn sau: {self.OTP_EXPIRY} phút")
        print("="*50 + "\n")
        
        # TODO: For production, send via email
        # if email:
        #     self.send_otp_email(email, otp)
        
        return True, f"Mã OTP đã được gửi (hiển thị trên console)"
    
    def verify_otp(self, username: str, otp: str) -> Tuple[bool, str]:
        """Verify OTP code"""
        if username not in self.otp_storage:
            return False, "Không tìm thấy mã OTP. Vui lòng đăng nhập lại"
        
        stored_otp, expiry = self.otp_storage[username]
        
        # Check expiry
        if datetime.now() > expiry:
            del self.otp_storage[username]
            return False, "Mã OTP đã hết hạn"
        
        # Verify OTP
        if otp != stored_otp:
            return False, "Mã OTP không đúng"
        
        # OTP valid, remove from storage
        del self.otp_storage[username]
        return True, "Xác thực thành công"
    
    def check_account_locked(self, username: str) -> Tuple[bool, str]:
        """Check if account is locked"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT locked_until, failed_login_attempts 
            FROM admins WHERE username = ?
        ''', (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return False, ""
        
        locked_until, failed_attempts = row
        
        if locked_until:
            lock_time = datetime.fromisoformat(locked_until)
            if datetime.now() < lock_time:
                remaining = (lock_time - datetime.now()).seconds // 60
                return True, f"Tài khoản bị khóa. Thử lại sau {remaining} phút"
            else:
                # Unlock account
                self.unlock_account(username)
        
        return False, ""
    
    def unlock_account(self, username: str):
        """Unlock account and reset failed attempts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE admins 
            SET locked_until = NULL, failed_login_attempts = 0 
            WHERE username = ?
        ''', (username,))
        
        conn.commit()
        conn.close()
    
    def record_failed_login(self, username: str):
        """Record failed login attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE admins 
            SET failed_login_attempts = failed_login_attempts + 1 
            WHERE username = ?
        ''', (username,))
        
        # Check if should lock account
        cursor.execute('''
            SELECT failed_login_attempts FROM admins WHERE username = ?
        ''', (username,))
        
        row = cursor.fetchone()
        if row and row[0] >= self.MAX_LOGIN_ATTEMPTS:
            # Lock account
            lock_until = datetime.now() + timedelta(minutes=self.LOCKOUT_DURATION)
            cursor.execute('''
                UPDATE admins 
                SET locked_until = ? 
                WHERE username = ?
            ''', (lock_until.isoformat(), username))
            
            print(f"\n⚠️  TÀI KHOẢN BỊ KHÓA!")
            print(f"Lý do: Đăng nhập sai {self.MAX_LOGIN_ATTEMPTS} lần")
            print(f"Thời gian khóa: {self.LOCKOUT_DURATION} phút\n")
        
        conn.commit()
        conn.close()
    
    def reset_failed_attempts(self, username: str):
        """Reset failed login attempts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE admins 
            SET failed_login_attempts = 0, locked_until = NULL 
            WHERE username = ?
        ''', (username,))
        
        conn.commit()
        conn.close()
    
    def log_action(self, admin_id: Optional[int], username: str, action: str, 
                   details: str, success: bool, ip_address: str = "127.0.0.1"):
        """Log admin action to audit trail"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO admin_audit_log 
            (admin_id, username, action, details, ip_address, timestamp, success)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (admin_id, username, action, details, ip_address, 
              datetime.now().isoformat(), 1 if success else 0))
        
        conn.commit()
        conn.close()
    
    def authenticate_step1(self, username: str, password: str) -> Tuple[bool, Optional[dict], str]:
        """
        Step 1: Authenticate username and password
        Returns: (success, admin_data, message)
        """
        # Check if account is locked
        is_locked, lock_message = self.check_account_locked(username)
        if is_locked:
            self.log_action(None, username, "LOGIN_ATTEMPT", 
                          "Account locked", False)
            return False, None, lock_message
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, username, password_hash, salt, full_name, email, 
                       is_active, require_2fa
                FROM admins WHERE username = ?
            ''', (username,))
            
            row = cursor.fetchone()
            
            if not row:
                self.log_action(None, username, "LOGIN_ATTEMPT", 
                              "Username not found", False)
                return False, None, "Tên đăng nhập không tồn tại"
            
            admin_id, db_username, db_password_hash, db_salt, full_name, \
                email, is_active, require_2fa = row
            
            if not is_active:
                self.log_action(admin_id, username, "LOGIN_ATTEMPT", 
                              "Account inactive", False)
                return False, None, "Tài khoản đã bị vô hiệu hóa"
            
            # Verify password
            password_hash, _ = self.hash_password(password, db_salt)
            
            if password_hash != db_password_hash:
                self.record_failed_login(username)
                self.log_action(admin_id, username, "LOGIN_ATTEMPT", 
                              "Wrong password", False)
                return False, None, "Mật khẩu không đúng"
            
            # Password correct, reset failed attempts
            self.reset_failed_attempts(username)
            
            admin_data = {
                'id': admin_id,
                'username': db_username,
                'full_name': full_name,
                'email': email,
                'require_2fa': bool(require_2fa)
            }
            
            # If 2FA required, send OTP
            if require_2fa:
                success, message = self.send_otp(username, email)
                if success:
                    self.log_action(admin_id, username, "OTP_SENT", 
                                  "2FA OTP sent", True)
                    return True, admin_data, "REQUIRE_2FA"
                else:
                    return False, None, "Không thể gửi mã OTP"
            else:
                # No 2FA, login successful
                self.complete_login(admin_id, username)
                return True, admin_data, "Đăng nhập thành công"
            
        except Exception as e:
            self.log_action(None, username, "LOGIN_ERROR", str(e), False)
            return False, None, f"Lỗi: {str(e)}"
        finally:
            conn.close()
    
    def authenticate_step2(self, username: str, otp: str, admin_data: dict) -> Tuple[bool, str]:
        """
        Step 2: Verify OTP for 2FA
        Returns: (success, message)
        """
        success, message = self.verify_otp(username, otp)
        
        if success:
            self.complete_login(admin_data['id'], username)
            self.log_action(admin_data['id'], username, "LOGIN_SUCCESS", 
                          "2FA verified", True)
            return True, "Đăng nhập thành công"
        else:
            self.log_action(admin_data['id'], username, "2FA_FAILED", 
                          message, False)
            return False, message
    
    def complete_login(self, admin_id: int, username: str):
        """Complete login process"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update last login
        cursor.execute('''
            UPDATE admins SET last_login = ? WHERE id = ?
        ''', (datetime.now().isoformat(), admin_id))
        
        # Create session
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(minutes=self.SESSION_TIMEOUT)
        
        cursor.execute('''
            INSERT INTO admin_sessions 
            (admin_id, session_token, created_at, expires_at, ip_address, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (admin_id, session_token, datetime.now().isoformat(), 
              expires_at.isoformat(), "127.0.0.1", 1))
        
        conn.commit()
        conn.close()
        
        self.log_action(admin_id, username, "LOGIN_SUCCESS", 
                       "Login completed", True)
    
    def change_password(self, admin_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change admin password with validation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT username, password_hash, salt FROM admins WHERE id = ?
            ''', (admin_id,))
            
            row = cursor.fetchone()
            if not row:
                return False, "Admin không tồn tại"
            
            username, db_password_hash, db_salt = row
            
            # Verify old password
            old_password_hash, _ = self.hash_password(old_password, db_salt)
            if old_password_hash != db_password_hash:
                self.log_action(admin_id, username, "CHANGE_PASSWORD_FAILED", 
                              "Wrong old password", False)
                return False, "Mật khẩu cũ không đúng"
            
            # Validate new password
            is_valid, error_msg = self.validate_password(new_password)
            if not is_valid:
                return False, error_msg
            
            # Hash new password
            new_password_hash, new_salt = self.hash_password(new_password)
            
            # Update password
            cursor.execute('''
                UPDATE admins SET password_hash = ?, salt = ? WHERE id = ?
            ''', (new_password_hash, new_salt, admin_id))
            
            conn.commit()
            
            self.log_action(admin_id, username, "CHANGE_PASSWORD", 
                          "Password changed successfully", True)
            
            return True, "Đổi mật khẩu thành công"
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
        finally:
            conn.close()
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < self.PASSWORD_MIN_LENGTH:
            return False, f"Mật khẩu phải có ít nhất {self.PASSWORD_MIN_LENGTH} ký tự"
        
        if not any(c.isupper() for c in password):
            return False, "Mật khẩu phải có ít nhất 1 chữ HOA"
        
        if not any(c.islower() for c in password):
            return False, "Mật khẩu phải có ít nhất 1 chữ thường"
        
        if not any(c.isdigit() for c in password):
            return False, "Mật khẩu phải có ít nhất 1 chữ SỐ"
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, "Mật khẩu phải có ít nhất 1 ký tự đặc biệt (!@#$%...)"
        
        return True, "Mật khẩu hợp lệ"
    
    def get_audit_log(self, admin_id: Optional[int] = None, limit: int = 100) -> list:
        """Get audit log entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if admin_id:
            cursor.execute('''
                SELECT id, admin_id, username, action, details, ip_address, 
                       timestamp, success
                FROM admin_audit_log 
                WHERE admin_id = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (admin_id, limit))
        else:
            cursor.execute('''
                SELECT id, admin_id, username, action, details, ip_address, 
                       timestamp, success
                FROM admin_audit_log 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                'id': row[0],
                'admin_id': row[1],
                'username': row[2],
                'action': row[3],
                'details': row[4],
                'ip_address': row[5],
                'timestamp': row[6],
                'success': bool(row[7])
            })
        
        return logs
    
    def toggle_2fa(self, admin_id: int, enable: bool) -> Tuple[bool, str]:
        """Enable or disable 2FA for admin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT username FROM admins WHERE id = ?
            ''', (admin_id,))
            
            row = cursor.fetchone()
            if not row:
                return False, "Admin không tồn tại"
            
            username = row[0]
            
            cursor.execute('''
                UPDATE admins SET require_2fa = ? WHERE id = ?
            ''', (1 if enable else 0, admin_id))
            
            conn.commit()
            
            action = "ENABLE_2FA" if enable else "DISABLE_2FA"
            self.log_action(admin_id, username, action, 
                          f"2FA {'enabled' if enable else 'disabled'}", True)
            
            return True, f"Đã {'bật' if enable else 'tắt'} 2FA"
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}"
        finally:
            conn.close()
