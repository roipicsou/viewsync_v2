import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
import socketio
import requests

class WebSocketThread(QThread):
    screen_updated = pyqtSignal(str)

    def run(self):
        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            print("Connected to server")

        @self.sio.on("screen_update")
        def on_screen_update(data):
            screen = data.get("screen", "default")
            self.screen_updated.emit(screen)

        self.sio.connect("http://127.0.0.1:5000")
        self.sio.wait()

class ViewSyncClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ViewSync Client")
        self.setGeometry(100, 100, 300, 200)
        
        self.label = QLabel("Waiting for updates...", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.thread = WebSocketThread()
        self.thread.screen_updated.connect(self.update_screen)
        self.thread.start()
        
        self.init_screen()
    
    def init_screen(self):
        try:
            response = requests.get("http://127.0.0.1:5000/get_screen")
            if response.status_code == 200:
                self.label.setText(f"Current Screen: {response.json()['screen']}")
        except requests.exceptions.RequestException:
            self.label.setText("Failed to load initial screen")
    
    def update_screen(self, screen):
        self.label.setText(f"Current Screen: {screen}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ViewSyncClient()
    client.show()
    sys.exit(app.exec())