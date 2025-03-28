from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QFont

class ClockScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: black; color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Label pour afficher l'heure
        self.label = QLabel()
        self.label.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Timer pour mettre à jour l'heure chaque seconde
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Mettre à jour chaque seconde

        self.update_time()  # Mise à jour initiale

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.label.setText(current_time)