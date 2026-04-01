"""Voter view for casting votes and viewing results"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QGroupBox, QTextEdit, QHeaderView)
from PySide6.QtCore import Qt, Signal
from models.voter import Voter
from services.voting_service import VotingService
from services.election_service import ElectionService
from utils.constants import ElectionState

class VoterView(QWidget):
    """View for voters to cast votes"""
    
    logout_signal = Signal()
    
    def __init__(self, voter: Voter, voting_service: VotingService, 
                 election_service: ElectionService):
        super().__init__()
        self.voter = voter
        self.voting_service = voting_service
        self.election_service = election_service
        self.selected_proposal_id = None
        self.current_election = None
        self.has_voted_current_election = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        self.header = QLabel(f"👤 Xin chào, {self.voter.full_name}")
        self.header.setObjectName("subtitleLabel")
        layout.addWidget(self.header)
        
        # Election info
        self.election_info_group = QGroupBox("🗳️ Thông tin cuộc bầu cử")
        election_info_layout = QVBoxLayout()
        election_info_layout.setSpacing(8)
        
        self.election_title_label = QLabel("Đang tải...")
        self.election_title_label.setObjectName("valueLabel")
        self.election_state_label = QLabel("")
        self.election_state_label.setObjectName("infoLabel")
        
        election_info_layout.addWidget(self.election_title_label)
        election_info_layout.addWidget(self.election_state_label)
        self.election_info_group.setLayout(election_info_layout)
        layout.addWidget(self.election_info_group)
        
        # Voter info - Grid layout for better alignment
        self.info_group = QGroupBox("📋 Thông tin cử tri")
        info_grid = QVBoxLayout()
        info_grid.setSpacing(8)
        
        # Create info rows with consistent formatting
        id_row = QHBoxLayout()
        id_label = QLabel("Mã cử tri:")
        id_label.setObjectName("infoLabel")
        id_label.setMinimumWidth(150)
        self.voter_id_label = QLabel(str(self.voter.id))
        self.voter_id_label.setObjectName("valueLabel")
        id_row.addWidget(id_label)
        id_row.addWidget(self.voter_id_label)
        id_row.addStretch()
        
        weight_row = QHBoxLayout()
        weight_label = QLabel("Quyền biểu quyết:")
        weight_label.setObjectName("infoLabel")
        weight_label.setMinimumWidth(150)
        self.weight_label = QLabel(str(self.voter.weight))
        self.weight_label.setObjectName("valueLabel")
        weight_row.addWidget(weight_label)
        weight_row.addWidget(self.weight_label)
        weight_row.addStretch()
        
        status_row = QHBoxLayout()
        status_text = QLabel("Trạng thái:")
        status_text.setObjectName("infoLabel")
        status_text.setMinimumWidth(150)
        status = "✅ Đã bỏ phiếu" if self.voter.voted else "⏳ Chưa bỏ phiếu"
        self.status_label = QLabel(status)
        self.status_label.setObjectName("valueLabel")
        status_row.addWidget(status_text)
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        
        verified_row = QHBoxLayout()
        verified_text = QLabel("Quyền bầu cử:")
        verified_text.setObjectName("infoLabel")
        verified_text.setMinimumWidth(150)
        if self.voter.verified:
            verified = "✅ Có quyền bầu cử"
            verified_style = "color: #10b981;"
        else:
            verified = "❌ Chưa được xác thực"
            verified_style = "color: #ef4444;"
        self.verified_label = QLabel(verified)
        self.verified_label.setObjectName("valueLabel")
        self.verified_label.setStyleSheet(verified_style)
        verified_row.addWidget(verified_text)
        verified_row.addWidget(self.verified_label)
        verified_row.addStretch()
        
        info_grid.addLayout(id_row)
        info_grid.addLayout(weight_row)
        info_grid.addLayout(status_row)
        info_grid.addLayout(verified_row)
        
        self.info_group.setLayout(info_grid)
        layout.addWidget(self.info_group)
        
        # Proposals table
        proposals_group = QGroupBox("🎯 Danh sách ứng viên")
        proposals_layout = QVBoxLayout()
        
        self.proposals_table = QTableWidget()
        self.proposals_table.setColumnCount(3)
        self.proposals_table.setHorizontalHeaderLabels(["ID", "Ứng viên", "Mô tả"])
        self.proposals_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.proposals_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.proposals_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.proposals_table.setColumnWidth(1, 200)
        self.proposals_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.proposals_table.setSelectionMode(QTableWidget.SingleSelection)
        self.proposals_table.setAlternatingRowColors(True)
        self.proposals_table.verticalHeader().setVisible(False)
        self.proposals_table.setMinimumHeight(200)
        self.proposals_table.itemSelectionChanged.connect(self.on_proposal_selected)
        proposals_layout.addWidget(self.proposals_table)
        
        proposals_group.setLayout(proposals_layout)
        layout.addWidget(proposals_group)
        
        # Vote button
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.vote_btn = QPushButton("🗳️ Bỏ phiếu")
        self.vote_btn.setObjectName("successButton")
        self.vote_btn.clicked.connect(self.cast_vote)
        self.vote_btn.setEnabled(False)
        self.vote_btn.setMinimumHeight(40)
        
        self.status_btn = QPushButton("📊 Xem trạng thái phiếu")
        self.status_btn.clicked.connect(self.view_vote_status)
        self.status_btn.setMinimumHeight(40)
        
        self.results_btn = QPushButton("📈 Xem kết quả")
        self.results_btn.clicked.connect(self.view_results)
        self.results_btn.setMinimumHeight(40)
        
        logout_btn = QPushButton("🚪 Đăng xuất")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout_signal.emit)
        logout_btn.setMinimumHeight(40)
        
        button_layout.addWidget(self.vote_btn)
        button_layout.addWidget(self.status_btn)
        button_layout.addWidget(self.results_btn)
        button_layout.addStretch()
        button_layout.addWidget(logout_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.load_proposals()
    
    def refresh_voter_info(self):
        """Refresh voter information display"""
        self.header.setText(f"👤 Xin chào, {self.voter.full_name}")
        self.voter_id_label.setText(str(self.voter.id))
        self.weight_label.setText(str(self.voter.weight))
        
        if self.voter.verified:
            verified = "✅ Có quyền bầu cử"
            verified_style = "color: #10b981;"
        else:
            verified = "❌ Chưa được xác thực"
            verified_style = "color: #ef4444;"
        self.verified_label.setText(verified)
        self.verified_label.setStyleSheet(verified_style)
        
        # Update status for current election
        self.update_voter_status_for_current_election()
    
    def load_proposals(self):
        """Load proposals into table"""
        election = self.election_service.get_current_election()
        if not election:
            self.proposals_table.setRowCount(0)
            self.election_title_label.setText("Không có cuộc bầu cử nào")
            self.election_state_label.setText("")
            return
        
        self.current_election = election  # Store current election
        
        # Update election info
        self.election_title_label.setText(f"📌 {election.title}")
        state_text = f"Trạng thái: {election.state}"
        if election.state == "Vote":
            state_text += " (Đang bỏ phiếu)"
            self.election_state_label.setStyleSheet("color: #10b981;")
        elif election.state == "Done":
            state_text += " (Đã kết thúc)"
            self.election_state_label.setStyleSheet("color: #94a3b8;")
        else:
            self.election_state_label.setStyleSheet("color: #f59e0b;")
        self.election_state_label.setText(state_text)
        
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        self.proposals_table.setRowCount(len(proposals))
        
        for row, proposal in enumerate(proposals):
            self.proposals_table.setItem(row, 0, QTableWidgetItem(str(proposal.id)))
            self.proposals_table.setItem(row, 1, QTableWidgetItem(proposal.candidate_name))
            self.proposals_table.setItem(row, 2, QTableWidgetItem(proposal.description))
        
        # Update voter info based on current election
        self.update_voter_status_for_current_election()
    
    def update_voter_status_for_current_election(self):
        """Update voter status specifically for current election"""
        if not hasattr(self, 'current_election') or not self.current_election:
            return
        
        # Check if voter has voted for THIS election
        if self.voter.voted and self.voter.selected_proposal_id:
            proposals = self.voting_service.db_manager.get_all_proposals(self.current_election.id)
            proposal_ids = [p.id for p in proposals]
            self.has_voted_current_election = self.voter.selected_proposal_id in proposal_ids
        else:
            self.has_voted_current_election = False
        
        # Update status label
        if self.has_voted_current_election:
            status = "✅ Đã bỏ phiếu (cuộc bầu cử này)"
        elif self.voter.voted:
            status = "⏳ Chưa bỏ phiếu (cuộc bầu cử này)"
        else:
            status = "⏳ Chưa bỏ phiếu"
        self.status_label.setText(status)
    
    def on_proposal_selected(self):
        """Handle proposal selection"""
        selected_rows = self.proposals_table.selectedItems()
        # Enable vote button if:
        # 1. A proposal is selected
        # 2. Voter has NOT voted for current election yet
        if selected_rows and not self.has_voted_current_election:
            self.selected_proposal_id = int(selected_rows[0].text())
            self.vote_btn.setEnabled(True)
        else:
            self.vote_btn.setEnabled(False)
    
    def cast_vote(self):
        """Cast vote for selected proposal"""
        if not self.selected_proposal_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ứng viên")
            return
        
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào đang diễn ra")
            return
        
        # Confirm vote
        reply = QMessageBox.question(
            self, "Xác nhận",
            f"Bạn có chắc muốn bỏ phiếu cho ứng viên ID {self.selected_proposal_id}?\n"
            "Hành động này không thể hoàn tác!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.voting_service.cast_vote(
                self.voter, self.selected_proposal_id, election
            )
            
            if success:
                QMessageBox.information(self, "Thành công", message)
                self.voter = self.voting_service.db_manager.get_voter_by_id(self.voter.id)
                self.vote_btn.setEnabled(False)
                self.refresh_voter_info()  # Refresh voter info only
            else:
                QMessageBox.warning(self, "Lỗi", message)
    
    def view_vote_status(self):
        """View voter's vote status on blockchain for current election"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào")
            return
        
        # Check if voter has voted for current election
        if not self.has_voted_current_election:
            QMessageBox.information(self, "Trạng thái phiếu bầu", 
                                   f"Bạn chưa bỏ phiếu cho cuộc bầu cử:\n{election.title}")
            return
        
        # Get vote status from blockchain
        status = self.voting_service.get_voter_vote_status(self.voter)
        
        if status:
            # Verify this vote belongs to current election
            proposal = status['proposal']
            if proposal and proposal.election_id == election.id:
                msg = f"""
🗳️ Cuộc bầu cử: {election.title}

📦 Block Index: {status['block_index']}
⏰ Timestamp: {status['timestamp']}
🎯 Ứng viên: {proposal.candidate_name}
🔐 Chữ ký: {status['signature'][:50]}...
#️⃣ Hash: {status['hash'][:50]}...

✅ Phiếu của bạn đã được ghi vào blockchain!
                """
                QMessageBox.information(self, "Trạng thái phiếu bầu", msg)
            else:
                QMessageBox.information(self, "Trạng thái phiếu bầu", 
                                       f"Bạn chưa bỏ phiếu cho cuộc bầu cử:\n{election.title}")
        else:
            QMessageBox.information(self, "Trạng thái phiếu bầu", 
                                   f"Bạn chưa bỏ phiếu cho cuộc bầu cử:\n{election.title}")
    
    def view_results(self):
        """View election results with chart"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure
        
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào")
            return
        
        if election.state != ElectionState.DONE:
            QMessageBox.information(self, "Thông báo", 
                                   "Kết quả chưa được công bố")
            return
        
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        if not proposals:
            QMessageBox.information(self, "Thông báo", "Không có ứng viên nào")
            return
            
        proposals.sort(key=lambda p: p.vote_count, reverse=True)
        total_votes = sum(p.vote_count for p in proposals)
        
        # Create dialog with chart
        dialog = QDialog(self)
        dialog.setWindowTitle("📊 Kết quả bầu cử")
        dialog.setMinimumSize(800, 600)
        layout = QVBoxLayout()
        
        # Create matplotlib figure
        fig = Figure(figsize=(8, 6), facecolor='#1e293b')
        canvas = FigureCanvasQTAgg(fig)
        ax = fig.add_subplot(111)
        
        # Prepare data
        names = [p.candidate_name for p in proposals]
        votes = [p.vote_count for p in proposals]
        percentages = [(v / total_votes * 100) if total_votes > 0 else 0 for v in votes]
        
        # Create bar chart
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
        bars = ax.barh(names, percentages, color=colors[:len(names)])
        
        # Customize chart
        ax.set_xlabel('Phần trăm (%)', color='#f8fafc', fontsize=12, fontweight='bold')
        ax.set_title('Kết quả bầu cử', color='#60a5fa', fontsize=16, fontweight='bold', pad=20)
        ax.set_facecolor('#0f172a')
        ax.tick_params(colors='#f8fafc', labelsize=10)
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', alpha=0.2, color='#334155')
        
        # Add percentage labels on bars
        for i, (bar, pct, vote) in enumerate(zip(bars, percentages, votes)):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                   f'{pct:.1f}% ({vote} phiếu)',
                   ha='left', va='center', color='#f8fafc', fontsize=10, fontweight='600')
        
        ax.set_xlim(0, max(percentages) * 1.2 if percentages else 100)
        fig.tight_layout()
        
        layout.addWidget(canvas)
        
        # Add winner info
        if election.winner_id:
            winner = next((p for p in proposals if p.id == election.winner_id), None)
            if winner:
                winner_label = QLabel(f"🏆 Người chiến thắng: {winner.candidate_name}")
                winner_label.setObjectName("subtitleLabel")
                winner_label.setStyleSheet("color: #10b981; padding: 10px;")
                layout.addWidget(winner_label)
        
        # Add close button
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setMinimumHeight(40)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
