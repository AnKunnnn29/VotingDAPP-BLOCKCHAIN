"""Enhanced Voter view with voting history and multiple elections support"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QGroupBox, QTextEdit, QHeaderView,
                               QTabWidget, QDialog)
from PySide6.QtCore import Qt, Signal
from models.voter import Voter
from services.voting_service import VotingService
from services.election_service import ElectionService
from utils.constants import ElectionState
from datetime import datetime

class VoterViewEnhanced(QWidget):
    """Enhanced view for voters with history and multiple elections"""
    
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
        """Initialize the UI with tabs"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        self.header = QLabel(f"👤 Xin chào, {self.voter.full_name}")
        self.header.setObjectName("subtitleLabel")
        layout.addWidget(self.header)
        
        # Create tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_current_election_tab(), "🗳️ Cuộc bầu cử hiện tại")
        tabs.addTab(self.create_voting_history_tab(), "📜 Lịch sử bỏ phiếu")
        tabs.addTab(self.create_all_elections_tab(), "📋 Tất cả cuộc bầu cử")
        layout.addWidget(tabs)
        
        # Logout button
        logout_btn = QPushButton("🚪 Đăng xuất")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout_signal.emit)
        logout_btn.setMinimumHeight(40)
        layout.addWidget(logout_btn)
        
        self.setLayout(layout)
    
    def create_current_election_tab(self):
        """Create tab for current election voting"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Election info
        self.election_info_group = QGroupBox("🗳️ Thông tin cuộc bầu cử")
        election_info_layout = QVBoxLayout()
        
        self.election_title_label = QLabel("Đang tải...")
        self.election_title_label.setObjectName("valueLabel")
        self.election_state_label = QLabel("")
        self.election_state_label.setObjectName("infoLabel")
        
        election_info_layout.addWidget(self.election_title_label)
        election_info_layout.addWidget(self.election_state_label)
        self.election_info_group.setLayout(election_info_layout)
        layout.addWidget(self.election_info_group)
        
        # Voter info
        self.info_group = QGroupBox("📋 Thông tin cử tri")
        info_grid = QVBoxLayout()
        
        # Status row
        status_row = QHBoxLayout()
        status_text = QLabel("Trạng thái:")
        status_text.setObjectName("infoLabel")
        status_text.setMinimumWidth(150)
        self.status_label = QLabel("⏳ Chưa bỏ phiếu")
        self.status_label.setObjectName("valueLabel")
        status_row.addWidget(status_text)
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        
        info_grid.addLayout(status_row)
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
        
        self.vote_btn = QPushButton("🗳️ Bỏ phiếu")
        self.vote_btn.setObjectName("successButton")
        self.vote_btn.clicked.connect(self.cast_vote)
        self.vote_btn.setEnabled(False)
        self.vote_btn.setMinimumHeight(40)
        
        self.status_btn = QPushButton("📊 Xem trạng thái phiếu")
        self.status_btn.clicked.connect(self.view_vote_status)
        self.status_btn.setMinimumHeight(40)
        
        button_layout.addWidget(self.vote_btn)
        button_layout.addWidget(self.status_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_current_election()
        return widget
    
    def create_voting_history_tab(self):
        """Create tab showing voting history"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📜 Lịch sử bỏ phiếu của bạn")
        title.setObjectName("subtitleLabel")
        layout.addWidget(title)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Cuộc bầu cử", "Thời gian", "Ứng viên đã chọn", "Block #", "Trạng thái", "Kết quả"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Interactive)
        self.history_table.setColumnWidth(1, 150)
        self.history_table.setColumnWidth(2, 150)
        self.history_table.setColumnWidth(5, 150)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setMinimumHeight(300)
        self.history_table.doubleClicked.connect(self.view_history_detail)
        layout.addWidget(self.history_table)
        
        # Info label
        info_label = QLabel("💡 Nhấp đúp vào dòng để xem chi tiết")
        info_label.setObjectName("infoLabel")
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_voting_history)
        refresh_btn.setMinimumHeight(40)
        
        export_btn = QPushButton("📥 Xuất lịch sử")
        export_btn.clicked.connect(self.export_history)
        export_btn.setMinimumHeight(40)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_voting_history()
        return widget
    
    def create_all_elections_tab(self):
        """Create tab showing all elections"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("📋 Tất cả các cuộc bầu cử")
        title.setObjectName("subtitleLabel")
        layout.addWidget(title)
        
        # Elections table
        self.elections_table = QTableWidget()
        self.elections_table.setColumnCount(6)
        self.elections_table.setHorizontalHeaderLabels([
            "ID", "Tên cuộc bầu cử", "Trạng thái", "Thời gian bắt đầu", "Bạn đã bỏ phiếu", "Người thắng"
        ])
        self.elections_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.elections_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.elections_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.elections_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        self.elections_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.elections_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Interactive)
        self.elections_table.setColumnWidth(2, 120)
        self.elections_table.setColumnWidth(3, 150)
        self.elections_table.setColumnWidth(5, 150)
        self.elections_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.elections_table.setAlternatingRowColors(True)
        self.elections_table.verticalHeader().setVisible(False)
        self.elections_table.setMinimumHeight(300)
        self.elections_table.doubleClicked.connect(self.view_election_detail)
        layout.addWidget(self.elections_table)
        
        # Info label
        info_label = QLabel("💡 Nhấp đúp vào dòng để xem chi tiết cuộc bầu cử")
        info_label.setObjectName("infoLabel")
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_all_elections)
        refresh_btn.setMinimumHeight(40)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_all_elections()
        return widget
    
    def load_current_election(self):
        """Load current election and proposals"""
        election = self.election_service.get_current_election()
        if not election:
            self.proposals_table.setRowCount(0)
            self.election_title_label.setText("Không có cuộc bầu cử nào")
            self.election_state_label.setText("")
            return
        
        self.current_election = election
        
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
        
        # Load proposals
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        self.proposals_table.setRowCount(len(proposals))
        
        for row, proposal in enumerate(proposals):
            self.proposals_table.setItem(row, 0, QTableWidgetItem(str(proposal.id)))
            self.proposals_table.setItem(row, 1, QTableWidgetItem(proposal.candidate_name))
            self.proposals_table.setItem(row, 2, QTableWidgetItem(proposal.description))
        
        # Update voter status
        self.update_voter_status_for_current_election()
    
    def load_voting_history(self):
        """Load voting history from blockchain"""
        # Get all elections
        all_elections = self.voting_service.db_manager.get_all_elections()
        
        # Get voter's votes from blockchain
        history_data = []
        for election in all_elections:
            vote_block = self.voting_service.blockchain.get_vote_by_voter_and_election(
                self.voter.id, election.id
            )
            
            if vote_block:
                # Get proposal info
                proposal = self.voting_service.db_manager.get_all_proposals(election.id)
                proposal_name = "N/A"
                for p in proposal:
                    if p.id == vote_block.proposal_id:
                        proposal_name = p.candidate_name
                        break
                
                # Get winner info
                winner_name = "Chưa công bố"
                if election.winner_id:
                    for p in proposal:
                        if p.id == election.winner_id:
                            winner_name = f"🏆 {p.candidate_name}"
                            break
                
                history_data.append({
                    'election': election.title,
                    'timestamp': vote_block.timestamp,
                    'proposal': proposal_name,
                    'block_index': vote_block.index,
                    'status': "✅ Đã xác nhận",
                    'winner': winner_name
                })
        
        # Update table
        self.history_table.setRowCount(len(history_data))
        for row, data in enumerate(history_data):
            self.history_table.setItem(row, 0, QTableWidgetItem(data['election']))
            self.history_table.setItem(row, 1, QTableWidgetItem(data['timestamp']))
            self.history_table.setItem(row, 2, QTableWidgetItem(data['proposal']))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(data['block_index'])))
            self.history_table.setItem(row, 4, QTableWidgetItem(data['status']))
            self.history_table.setItem(row, 5, QTableWidgetItem(data['winner']))
    
    def load_all_elections(self):
        """Load all elections"""
        all_elections = self.voting_service.db_manager.get_all_elections()
        
        self.elections_table.setRowCount(len(all_elections))
        for row, election in enumerate(all_elections):
            # Check if voter voted in this election
            vote_block = self.voting_service.blockchain.get_vote_by_voter_and_election(
                self.voter.id, election.id
            )
            voted_status = "✅ Đã bỏ phiếu" if vote_block else "❌ Chưa bỏ phiếu"
            
            # Get winner
            winner_name = "Chưa công bố"
            if election.winner_id:
                proposals = self.voting_service.db_manager.get_all_proposals(election.id)
                for p in proposals:
                    if p.id == election.winner_id:
                        winner_name = p.candidate_name
                        break
            
            self.elections_table.setItem(row, 0, QTableWidgetItem(str(election.id)))
            self.elections_table.setItem(row, 1, QTableWidgetItem(election.title))
            self.elections_table.setItem(row, 2, QTableWidgetItem(election.state))
            start_time = election.start_time.strftime('%Y-%m-%d %H:%M') if election.start_time else "N/A"
            self.elections_table.setItem(row, 3, QTableWidgetItem(start_time))
            self.elections_table.setItem(row, 4, QTableWidgetItem(voted_status))
            self.elections_table.setItem(row, 5, QTableWidgetItem(winner_name))
    
    def update_voter_status_for_current_election(self):
        """Update voter status for current election"""
        if not self.current_election:
            return
        
        existing_vote = self.voting_service.blockchain.get_vote_by_voter_and_election(
            self.voter.id, self.current_election.id
        )
        self.has_voted_current_election = existing_vote is not None
        
        if self.has_voted_current_election:
            status = "✅ Đã bỏ phiếu (cuộc bầu cử này)"
        else:
            status = "⏳ Chưa bỏ phiếu"
        self.status_label.setText(status)
    
    def on_proposal_selected(self):
        """Handle proposal selection"""
        selected_rows = self.proposals_table.selectedItems()
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
                self.update_voter_status_for_current_election()
                self.load_voting_history()  # Refresh history
            else:
                QMessageBox.warning(self, "Lỗi", message)
    
    def view_vote_status(self):
        """View vote status on blockchain"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào")
            return
        
        if not self.has_voted_current_election:
            QMessageBox.information(self, "Trạng thái phiếu bầu", 
                                   f"Bạn chưa bỏ phiếu cho cuộc bầu cử:\n{election.title}")
            return
        
        status = self.voting_service.get_voter_vote_status(self.voter)
        
        if status:
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
    
    def view_history_detail(self):
        """View detailed history of selected vote"""
        selected_row = self.history_table.currentRow()
        if selected_row < 0:
            return
        
        election_name = self.history_table.item(selected_row, 0).text()
        block_index = int(self.history_table.item(selected_row, 3).text())
        
        # Get block from blockchain
        block = self.voting_service.blockchain.chain[block_index]
        
        # Get election
        all_elections = self.voting_service.db_manager.get_all_elections()
        election = None
        for e in all_elections:
            if e.title == election_name:
                election = e
                break
        
        if not election:
            return
        
        # Get proposal
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        proposal = None
        for p in proposals:
            if p.id == block.proposal_id:
                proposal = p
                break
        
        # Show detail dialog
        msg = f"""
📋 Chi tiết phiếu bầu

🗳️ Cuộc bầu cử: {election.title}
📝 Mô tả: {election.description}
⛓️ Chế độ: {election.blockchain_mode}

🎯 Ứng viên đã chọn: {proposal.candidate_name if proposal else 'N/A'}
📝 Mô tả ứng viên: {proposal.description if proposal else 'N/A'}

📦 Thông tin Block:
- Index: {block.index}
- Timestamp: {block.timestamp}
- Hash: {block.hash[:64]}...
- Previous Hash: {block.previous_hash[:64]}...
- Nonce: {block.nonce}
- Difficulty: {block.difficulty}
- Miner: {block.miner}

🔐 Chữ ký số: {block.signature[:100]}...

✅ Phiếu bầu đã được xác thực và ghi vào blockchain!
        """
        
        QMessageBox.information(self, "Chi tiết phiếu bầu", msg)
    
    def view_election_detail(self):
        """View detailed info of selected election"""
        selected_row = self.elections_table.currentRow()
        if selected_row < 0:
            return
        
        election_id = int(self.elections_table.item(selected_row, 0).text())
        election = self.voting_service.db_manager.get_election_by_id(election_id)
        
        if not election:
            return
        
        # Get proposals
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        
        # Check if voted
        vote_block = self.voting_service.blockchain.get_vote_by_voter_and_election(
            self.voter.id, election.id
        )
        
        voted_info = "❌ Bạn chưa bỏ phiếu trong cuộc bầu cử này"
        if vote_block:
            for p in proposals:
                if p.id == vote_block.proposal_id:
                    voted_info = f"✅ Bạn đã bỏ phiếu cho: {p.candidate_name}"
                    break
        
        # Get winner
        winner_info = "Chưa công bố"
        if election.winner_id:
            for p in proposals:
                if p.id == election.winner_id:
                    winner_info = f"🏆 {p.candidate_name} ({p.vote_count} phiếu)"
                    break
        
        msg = f"""
📋 Chi tiết cuộc bầu cử

🗳️ Tên: {election.title}
📝 Mô tả: {election.description}
🔄 Trạng thái: {election.state}
⛓️ Chế độ: {election.blockchain_mode}
⏰ Bắt đầu: {election.start_time.strftime('%Y-%m-%d %H:%M:%S') if election.start_time else 'N/A'}
⏰ Kết thúc: {election.end_time.strftime('%Y-%m-%d %H:%M:%S') if election.end_time else 'N/A'}

👥 Số ứng viên: {len(proposals)}
🗳️ Tổng số phiếu: {sum(p.vote_count for p in proposals)}

{voted_info}

🏆 Người chiến thắng: {winner_info}
        """
        
        QMessageBox.information(self, "Chi tiết cuộc bầu cử", msg)
    
    def export_history(self):
        """Export voting history to file"""
        import json
        from datetime import datetime
        
        # Get all elections
        all_elections = self.voting_service.db_manager.get_all_elections()
        
        # Collect history
        history = []
        for election in all_elections:
            vote_block = self.voting_service.blockchain.get_vote_by_voter_and_election(
                self.voter.id, election.id
            )
            
            if vote_block:
                proposals = self.voting_service.db_manager.get_all_proposals(election.id)
                proposal_name = "N/A"
                for p in proposals:
                    if p.id == vote_block.proposal_id:
                        proposal_name = p.candidate_name
                        break
                
                history.append({
                    'election_id': election.id,
                    'election_title': election.title,
                    'election_description': election.description,
                    'voted_at': vote_block.timestamp,
                    'proposal_id': vote_block.proposal_id,
                    'proposal_name': proposal_name,
                    'block_index': vote_block.index,
                    'block_hash': vote_block.hash,
                    'signature': vote_block.signature
                })
        
        # Export to JSON
        filename = f"voting_history_{self.voter.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'voter_id': self.voter.id,
            'voter_name': self.voter.full_name,
            'exported_at': datetime.now().isoformat(),
            'total_votes': len(history),
            'voting_history': history
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(self, "Thành công", 
                                   f"Đã xuất lịch sử bỏ phiếu ra file:\n{filename}")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể xuất file: {str(e)}")
