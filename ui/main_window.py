"""Main window for the voting DApp"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget,
                               QLabel, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.login_dialog import LoginDialog
from ui.voter_view import VoterView
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
        self.setMinimumSize(1200, 800)
        
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
        self.stacked_widget.addWidget(self.welcome_page)
    
    def create_welcome_page(self):
        """Create welcome page"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("🗳️ DApp Voting System")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Hệ thống bỏ phiếu phi tập trung dựa trên Blockchain")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        
        info = QLabel(
            "✨ Minh bạch • Bảo mật • Phi tập trung\n\n"
            "Sử dụng công nghệ blockchain và chữ ký số\n"
            "để đảm bảo tính toàn vẹn của mỗi lá phiếu"
        )
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName("infoLabel")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(info)
        
        widget.setLayout(layout)
        return widget
    
    def show_login(self):
        """Show login dialog"""
        dialog = LoginDialog(self)
        if dialog.exec() == LoginDialog.Accepted:
            self.current_role = dialog.user_role
            
            if self.current_role == "Admin":
                self.show_admin_view()
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
    
    def show_voter_view(self, voter):
        """Show voter view"""
        self.current_user = voter
        
        # Remove old voter view if exists
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        voter_view = VoterView(voter, self.voting_service, self.election_service)
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
        
        admin_view = AdminView(self.voting_service, self.election_service, self.auth_service)
        admin_view.logout_signal.connect(self.logout)
        self.stacked_widget.addWidget(admin_view)
        self.stacked_widget.setCurrentWidget(admin_view)
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.current_role = None
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.show_login()
