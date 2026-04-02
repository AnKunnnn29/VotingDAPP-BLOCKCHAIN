"""Enhanced login dialog with CCCD and face recognition"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QComboBox, QMessageBox,
                               QWidget, QProgressBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from services.face_recognition_service import FaceRecognitionService
from database.db_manager import DatabaseManager

class LoginDialogWithFace(QDialog):
    """Enhanced login dialog with face recognition"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.face_service = FaceRecognitionService()
        self.user_role = None
        self.user_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Đăng nhập - Hệ thống bầu cử Blockchain")
        self.setMinimumWidth(750)
        self.setMinimumHeight(700)
        
        # Track fullscreen state
        self.is_fullscreen = False
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)
        
        # Add fullscreen button at top right
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        
        self.fullscreen_btn = QPushButton("⛶ Full Screen")
        self.fullscreen_btn.setObjectName("secondaryButton")
        self.fullscreen_btn.setMinimumHeight(35)
        self.fullscreen_btn.setMaximumWidth(140)
        self.fullscreen_btn.setStyleSheet("""
            QPushButton {
                font-size: 9pt;
                font-weight: 600;
                padding: 8px 15px;
            }
        """)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        top_bar.addWidget(self.fullscreen_btn)
        
        main_layout.addLayout(top_bar)
        
        # Content layout with proper spacing
        content_layout = QVBoxLayout()
        content_layout.setSpacing(25)
        
        # Header
        header_container = QWidget()
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(10)
        
        # Icon
        icon_label = QLabel("🔐")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 42pt; padding: 8px;")
        header_layout.addWidget(icon_label)
        
        # Title
        title = QLabel("Đăng nhập hệ thống")
        title.setObjectName("subtitleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16pt;
            font-weight: 700;
            color: #60a5fa;
            padding: 8px 0;
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Xác thực bằng CCCD và khuôn mặt")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 10pt;
            color: #94a3b8;
            padding: 3px;
        """)
        header_layout.addWidget(subtitle)
        
        header_container.setLayout(header_layout)
        content_layout.addWidget(header_container)
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.6), stop:1 rgba(15, 23, 42, 0.8));
                border: 2px solid #1e293b;
                border-radius: 12px;
                padding: 25px;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)
        
        # Role selection
        role_label = QLabel("👤 Vai trò")
        role_label.setStyleSheet("""
            font-size: 10pt;
            font-weight: 600;
            color: #60a5fa;
            padding: 3px 0;
        """)
        form_layout.addWidget(role_label)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Cử tri", "Quản trị viên"])
        self.role_combo.setMinimumHeight(42)
        self.role_combo.setStyleSheet("""
            QComboBox {
                font-size: 10pt;
                padding: 10px 14px;
            }
        """)
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        form_layout.addWidget(self.role_combo)
        
        # CCCD input (for voters)
        self.cccd_label = QLabel("🆔 Số CCCD")
        self.cccd_label.setStyleSheet("""
            font-size: 10pt;
            font-weight: 600;
            color: #60a5fa;
            padding: 3px 0;
        """)
        form_layout.addWidget(self.cccd_label)
        
        self.cccd_input = QLineEdit()
        self.cccd_input.setPlaceholderText("Nhập số CCCD (12 số)")
        self.cccd_input.setMinimumHeight(42)
        self.cccd_input.setMaxLength(12)
        self.cccd_input.setStyleSheet("""
            QLineEdit {
                font-size: 10pt;
                padding: 10px 14px;
            }
        """)
        form_layout.addWidget(self.cccd_input)
        
        # Admin ID input (hidden by default)
        self.admin_label = QLabel("🔑 Mã quản trị")
        self.admin_label.setStyleSheet("""
            font-size: 10pt;
            font-weight: 600;
            color: #60a5fa;
            padding: 3px 0;
        """)
        self.admin_label.hide()
        form_layout.addWidget(self.admin_label)
        
        self.admin_input = QLineEdit()
        self.admin_input.setPlaceholderText("Nhập 'admin'")
        self.admin_input.setMinimumHeight(42)
        self.admin_input.setStyleSheet("""
            QLineEdit {
                font-size: 10pt;
                padding: 10px 14px;
            }
        """)
        self.admin_input.hide()
        form_layout.addWidget(self.admin_input)
        
        # Face recognition button
        self.face_btn = QPushButton("📸 Quét khuôn mặt")
        self.face_btn.setObjectName("warningButton")
        self.face_btn.setMinimumHeight(45)
        self.face_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        self.face_btn.clicked.connect(self.scan_face)
        form_layout.addWidget(self.face_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("""
            font-size: 9pt;
            padding: 10px;
            border-radius: 8px;
        """)
        self.status_label.hide()
        form_layout.addWidget(self.status_label)
        
        form_container.setLayout(form_layout)
        content_layout.addWidget(form_container)
        
        # Info box
        info_box = QLabel("💡 Cử tri: Nhập CCCD và quét khuôn mặt\n💡 Admin: Chọn vai trò Admin và nhập 'admin'\n💡 Chưa có tài khoản? Click 'Đăng ký' bên dưới")
        info_box.setAlignment(Qt.AlignCenter)
        info_box.setWordWrap(True)
        info_box.setStyleSheet("""
            color: #94a3b8;
            font-size: 9pt;
            padding: 12px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 8px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            line-height: 1.4;
        """)
        content_layout.addWidget(info_box)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        register_btn = QPushButton("📝 Đăng ký")
        register_btn.setObjectName("secondaryButton")
        register_btn.setMinimumHeight(45)
        register_btn.setMinimumWidth(140)
        register_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        register_btn.clicked.connect(self.show_register)
        
        self.login_btn = QPushButton("🚀 Đăng nhập")
        self.login_btn.setObjectName("successButton")
        self.login_btn.setMinimumHeight(45)
        self.login_btn.setMinimumWidth(160)
        self.login_btn.setEnabled(False)
        self.login_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        
        cancel_btn = QPushButton("❌ Hủy")
        cancel_btn.setObjectName("dangerButton")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setMinimumWidth(140)
        cancel_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(register_btn)
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        content_layout.addLayout(button_layout)
        
        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # State
        self.face_verified = False
    
    def on_role_changed(self, role):
        """Handle role selection change"""
        if role == "Quản trị viên":
            # Hide voter fields
            self.cccd_label.hide()
            self.cccd_input.hide()
            self.face_btn.hide()
            # Show admin fields
            self.admin_label.show()
            self.admin_input.show()
            self.login_btn.setEnabled(True)
        else:
            # Show voter fields
            self.cccd_label.show()
            self.cccd_input.show()
            self.face_btn.show()
            # Hide admin fields
            self.admin_label.hide()
            self.admin_input.hide()
            self.login_btn.setEnabled(False)
            self.face_verified = False
        
        self.status_label.hide()
    
    def scan_face(self):
        """Handle face scanning"""
        cccd = self.cccd_input.text().strip()
        
        if not cccd:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số CCCD trước")
            return
        
        if len(cccd) != 12 or not cccd.isdigit():
            QMessageBox.warning(self, "Lỗi", "Số CCCD phải có 12 chữ số")
            return
        
        # Find voter by CCCD
        voter = self.find_voter_by_cccd(cccd)
        if not voter:
            QMessageBox.warning(self, "Lỗi", 
                              f"Không tìm thấy cử tri với CCCD: {cccd}\n"
                              "Vui lòng liên hệ quản trị viên để đăng ký.")
            return
        
        # Check if face is registered
        if not self.face_service.has_registered_face(cccd):
            reply = QMessageBox.question(
                self, "Đăng ký khuôn mặt",
                f"CCCD {cccd} chưa đăng ký khuôn mặt.\n"
                f"Bạn có muốn đăng ký ngay không?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.face_service.register_face(cccd, voter.full_name):
                    # Update voter record
                    voter.face_registered = True
                    self.db_manager.update_voter(voter)
                    
                    self.show_status("✅ Đăng ký khuôn mặt thành công!", "success")
                    
                    # Auto verify after registration
                    reply2 = QMessageBox.question(
                        self, "Xác thực ngay",
                        "Đăng ký khuôn mặt thành công!\n\n"
                        "Bạn có muốn xác thực và đăng nhập ngay không?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if reply2 == QMessageBox.Yes:
                        # Verify face immediately
                        self.show_status("🔍 Đang xác thực khuôn mặt...", "info")
                        QTimer.singleShot(100, lambda: self.verify_face_async(cccd, voter))
                else:
                    self.show_status("❌ Đăng ký khuôn mặt thất bại", "error")
            return
        
        # Verify face
        self.show_status("🔍 Đang xác thực khuôn mặt...", "info")
        QTimer.singleShot(100, lambda: self.verify_face_async(cccd, voter))
    
    def verify_face_async(self, cccd, voter):
        """Verify face asynchronously"""
        is_match, confidence = self.face_service.verify_face(cccd)
        
        if is_match:
            self.face_verified = True
            self.user_id = voter.id
            self.user_role = "Voter"
            self.show_status(f"✅ Xác thực thành công! Độ tin cậy: {confidence:.1%}", "success")
            
            # Auto login after successful face verification
            QMessageBox.information(
                self, "Thành công",
                f"Xác thực khuôn mặt thành công!\n"
                f"Độ tin cậy: {confidence:.1%}\n\n"
                f"Đang đăng nhập..."
            )
            
            # Automatically accept the dialog (login)
            self.accept()
        else:
            self.face_verified = False
            self.login_btn.setEnabled(False)
            self.show_status(f"❌ Xác thực thất bại! Độ tin cậy: {confidence:.1%}", "error")
    
    def show_status(self, message, status_type):
        """Show status message"""
        colors = {
            "success": ("background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981;"),
            "error": ("background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444;"),
            "info": ("background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid #3b82f6;")
        }
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            font-size: 10pt;
            font-weight: 600;
            padding: 12px;
            border-radius: 8px;
            {colors.get(status_type, colors['info'])}
        """)
        self.status_label.show()
    
    def find_voter_by_cccd(self, cccd):
        """Find voter by CCCD number"""
        voters = self.db_manager.get_all_voters()
        for voter in voters:
            if voter.cccd == cccd:
                return voter
        return None
    
    def handle_login(self):
        """Handle login button click"""
        role = self.role_combo.currentText()
        
        if role == "Quản trị viên":
            admin_input = self.admin_input.text().strip()
            if admin_input.lower() == "admin":
                self.user_role = "Admin"
                self.user_id = 0
                self.accept()
            else:
                QMessageBox.warning(self, "Lỗi", "Mã quản trị viên không đúng")
        else:
            if not self.face_verified:
                QMessageBox.warning(self, "Lỗi", "Vui lòng quét khuôn mặt để xác thực")
                return
            
            self.user_role = "Voter"
            self.accept()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.is_fullscreen:
            # Exit fullscreen
            self.showNormal()
            self.fullscreen_btn.setText("⛶ Full Screen")
            self.is_fullscreen = False
        else:
            # Enter fullscreen
            self.showFullScreen()
            self.fullscreen_btn.setText("⛶ Exit Full Screen")
            self.is_fullscreen = True
    
    def show_register(self):
        """Show registration dialog"""
        from ui.register_dialog import RegisterDialog
        
        dialog = RegisterDialog(self.db_manager, self)
        if dialog.exec() == RegisterDialog.Accepted:
            QMessageBox.information(
                self, "Thành công",
                "Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ."
            )
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        # ESC to exit fullscreen
        if event.key() == Qt.Key_Escape and self.is_fullscreen:
            self.toggle_fullscreen()
        # F11 to toggle fullscreen
        elif event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)
