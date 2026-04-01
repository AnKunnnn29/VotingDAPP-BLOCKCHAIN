"""Modern stylesheet for the application"""

MAIN_STYLE = """
QMainWindow {
    background-color: #0f172a;
}

QDialog {
    background-color: #0f172a;
}

QWidget {
    font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
    font-size: 10pt;
    color: #f8fafc;
}

QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #60a5fa;
    color: white;
}

QPushButton:pressed {
    background-color: #2563eb;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
}

QPushButton#successButton {
    background-color: #10b981;
}

QPushButton#successButton:hover {
    background-color: #34d399;
}

QPushButton#dangerButton {
    background-color: #ef4444;
}

QPushButton#dangerButton:hover {
    background-color: #f87171;
}

QPushButton#warningButton {
    background-color: #f59e0b;
}

QPushButton#warningButton:hover {
    background-color: #fbbf24;
}

QLineEdit, QTextEdit, QSpinBox, QComboBox {
    padding: 10px;
    border: 1px solid #334155;
    border-radius: 6px;
    background-color: #1e293b;
    color: #f8fafc;
    selection-background-color: #3b82f6;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #3b82f6;
    background-color: #0f172a;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    selection-background-color: #3b82f6;
}

QLabel {
    color: #f8fafc;
}

QLabel#titleLabel {
    font-size: 24pt;
    font-weight: bold;
    color: #60a5fa;
}

QLabel#subtitleLabel {
    font-size: 16pt;
    font-weight: bold;
    color: #60a5fa;
    padding: 10px 0;
}

QLabel#infoLabel {
    color: #94a3b8;
    font-size: 10pt;
}

QLabel#valueLabel {
    color: #f8fafc;
    font-size: 11pt;
    font-weight: 600;
    padding: 5px 0;
}

QTableWidget {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: transparent;
    color: #f8fafc;
    selection-background-color: #3b82f6;
    alternate-background-color: #0f172a;
}

QTableWidget::item {
    padding: 12px 8px;
    border-bottom: 1px solid #334155;
}

QTableWidget::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
    font-weight: 600;
}

QTableWidget::item:hover {
    background-color: rgba(59, 130, 246, 0.2);
}

QHeaderView::section {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 12px 10px;
    border: none;
    border-bottom: 2px solid #334155;
    font-weight: bold;
}

QTabWidget::pane {
    border: 1px solid #334155;
    background-color: #1e293b;
    border-radius: 8px;
    padding: 5px;
}

QTabBar::tab {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
}

QTabBar::tab:selected {
    background-color: #1e293b;
    color: #60a5fa;
    border-bottom: 2px solid #3b82f6;
}

QTabBar::tab:hover:!selected {
    background-color: #1e293b;
    color: #f8fafc;
}

QGroupBox {
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 16px;
    padding-top: 16px;
    font-weight: bold;
    background-color: #1e293b;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    color: #60a5fa;
    background-color: #0f172a;
    border-radius: 4px;
    left: 10px;
}

QMessageBox {
    background-color: #1e293b;
}

QMessageBox QLabel {
    color: #f8fafc;
}

QScrollBar:vertical {
    border: none;
    background-color: #0f172a;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #475569;
}

QScrollBar:horizontal {
    border: none;
    background-color: #0f172a;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #334155;
    border-radius: 4px;
    min-width: 20px;
}

QProgressBar {
    border: 1px solid #334155;
    border-radius: 8px;
    text-align: center;
    background-color: #0f172a;
    color: #f8fafc;
    height: 20px;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #3b82f6, stop: 1 #60a5fa);
    border-radius: 6px;
}
"""
