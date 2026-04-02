"""Main window for the voting DApp"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
                               QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.login_dialog_face import LoginDialogWithFace
from ui.voter_view_enhanced import VoterViewEnhanced
from ui.admin_view import AdminView
from ui.styles import MAIN_STYLE
from services.voting_service import VotingService
from services.election_service import ElectionService
from services.auth_service import AuthService
from database.db_manager import DatabaseManager
from blockchain.blockchain import Blockchain

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.blockchain = self.db_manager.load_blockchain()
        self.voting_service = VotingService(self.db_manager, self.blockchain)
        self.election_service = ElectionService(self.db_manager)
        self.auth_service = AuthService(self.db_manager)
        
        self.current_user = None
        self.current_role = None
        
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("DApp Voting System - Hệ thống bỏ phiếu phi tập trung")
        
        # Set full screen
        self.showMaximized()  # Maximized window
        # Or use self.showFullScreen() for true fullscreen
        
        # Apply stylesheet
        self.setStyleSheet(MAIN_STYLE)
        
        # Central widget with stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Welcome page
        self.welcome_page = self.create_welcome_page()
        self.welcome_page.login_btn.clicked.connect(self.show_login)
        self.stacked_widget.addWidget(self.welcome_page)
    
    def create_welcome_page(self):
        """Create welcome page with blockchain theme"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Blockchain icon/logo area
        logo_container = QWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_layout.setSpacing(15)
        
        # Blockchain visual representation
        chain_visual = QLabel("⛓️ 🔗 ⛓️")
        chain_visual.setAlignment(Qt.AlignCenter)
        chain_visual.setStyleSheet("""
            font-size: 48pt;
            padding: 20px;
        """)
        logo_layout.addWidget(chain_visual)
        
        title = QLabel("🗳️ DApp Voting System")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(title)
        
        subtitle = QLabel("Hệ thống bỏ phiếu phi tập trung dựa trên Blockchain")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(subtitle)
        
        logo_container.setLayout(logo_layout)
        layout.addWidget(logo_container)
        
        # Features section with cards
        features_container = QWidget()
        features_layout = QHBoxLayout()
        features_layout.setSpacing(20)
        
        # Feature 1: Transparency
        feature1 = self.create_feature_card(
            "🔍",
            "Minh bạch",
            "Mọi phiếu bầu được ghi lại\ntrên blockchain công khai"
        )
        features_layout.addWidget(feature1)
        
        # Feature 2: Security
        feature2 = self.create_feature_card(
            "🔐",
            "Bảo mật",
            "Chữ ký số RSA 2048-bit\nđảm bảo tính xác thực"
        )
        features_layout.addWidget(feature2)
        
        # Feature 3: Immutability
        feature3 = self.create_feature_card(
            "⛓️",
            "Bất biến",
            "Dữ liệu không thể thay đổi\nsau khi ghi vào blockchain"
        )
        features_layout.addWidget(feature3)
        
        features_container.setLayout(features_layout)
        layout.addWidget(features_container)
        
        # Technology info
        tech_info = QLabel(
            "💎 Công nghệ: SHA-256 Hash • RSA Digital Signatures • Smart Contract State Machine"
        )
        tech_info.setAlignment(Qt.AlignCenter)
        tech_info.setObjectName("infoLabel")
        tech_info.setStyleSheet("""
            color: #60a5fa;
            font-size: 10pt;
            padding: 20px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(59, 130, 246, 0.3);
        """)
        layout.addWidget(tech_info)
        
        # Login button
        login_btn = QPushButton("🚀 Đăng nhập để bắt đầu")
        login_btn.setObjectName("successButton")
        login_btn.setMinimumHeight(50)
        login_btn.setMinimumWidth(250)
        login_btn.setStyleSheet("""
            QPushButton {
                font-size: 12pt;
                font-weight: 700;
            }
        """)
        # Will be connected later in init_ui
        
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(login_btn)
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)
        
        widget.setLayout(layout)
        widget.login_btn = login_btn  # Store reference
        return widget
    
    def create_feature_card(self, icon, title, description):
        """Create a feature card widget"""
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 36pt; padding: 10px;")
        card_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: 700;
            color: #60a5fa;
            padding: 5px;
        """)
        card_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            font-size: 9pt;
            color: #94a3b8;
            line-height: 1.5;
        """)
        card_layout.addWidget(desc_label)
        
        card.setLayout(card_layout)
        card.setMinimumWidth(200)
        card.setMinimumHeight(200)
        card.setStyleSheet("""
            QWidget#card {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.6), stop:1 rgba(15, 23, 42, 0.8));
                border: 2px solid #1e293b;
                border-radius: 12px;
                padding: 20px;
            }
            QWidget#card:hover {
                border: 2px solid rgba(59, 130, 246, 0.5);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.8), stop:1 rgba(15, 23, 42, 0.9));
            }
        """)
        
        return card
    
    def show_login(self):
        """Show login dialog"""
        dialog = LoginDialogWithFace(self.db_manager, self)
        if dialog.exec() == LoginDialogWithFace.Accepted:
            self.current_role = dialog.user_role
            
            if self.current_role == "Admin":
                # Use secure admin login
                self.show_admin_login()
            else:
                voter = self.db_manager.get_voter_by_id(dialog.user_id)
                if voter:
                    self.show_voter_view(voter)
                else:
                    QMessageBox.warning(self, "Lỗi", 
                        "Cử tri không tồn tại. Vui lòng liên hệ quản trị viên.")
                    self.show_login()
        else:
            self.close()
    
    def show_admin_login(self):
        """Show secure admin login dialog"""
        from ui.admin_login_dialog import AdminLoginDialog
        
        admin_dialog = AdminLoginDialog(self)
        if admin_dialog.exec() == AdminLoginDialog.Accepted:
            admin_data = admin_dialog.get_admin_data()
            if admin_data:
                self.current_user = admin_data
                self.show_admin_view()
        else:
            # Admin cancelled, go back to role selection
            self.show_login()
    
    def show_voter_view(self, voter):
        """Show voter view"""
        self.current_user = voter
        
        # Remove old voter view if exists
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        voter_view = VoterViewEnhanced(voter, self.voting_service, self.election_service)
        voter_view.logout_signal.connect(self.logout)
        self.stacked_widget.addWidget(voter_view)
        self.stacked_widget.setCurrentWidget(voter_view)
    
    def show_admin_view(self):
        """Show admin view"""
        # Remove old admin view if exists
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        admin_view = AdminView(self.voting_service, self.election_service, self.auth_service, self.blockchain)
        admin_view.logout_signal.connect(self.logout)
        self.stacked_widget.addWidget(admin_view)
        self.stacked_widget.setCurrentWidget(admin_view)
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.current_role = None
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.show_login()
