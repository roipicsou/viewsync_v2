import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
import socketio
import requests

# Importation des écrans du main.py
from screens.clock_screen import ClockScreen

class WebSocketThread(QThread):
    screen_updated = pyqtSignal(str)

    def run(self):
        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            print("Connected to server")

        @self.sio.on("screen_update")
        def on_screen_update(data):
            screen = data.get("screen", "clock")
            self.screen_updated.emit(screen)

        self.sio.connect("http://127.0.0.1:5000")
        self.sio.wait()

class ViewSyncClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ViewSync Client")
        self.showFullScreen()
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.screens = {
            "clock": ClockScreen(),
            #"youtube": YouTubeScreen()
        }
        
        for screen in self.screens.values():
            self.stack.addWidget(screen)
        
        self.thread = WebSocketThread()
        self.thread.screen_updated.connect(self.update_screen)
        self.thread.start()
        
        self.init_screen()
    
    def init_screen(self):
        try:
            response = requests.get("http://127.0.0.1:5000/get_screen")
            if response.status_code == 200:
                self.update_screen(response.json()["screen"])
        except requests.exceptions.RequestException:
            print("Failed to load initial screen")
    
    def update_screen(self, screen_name):
        if screen_name in self.screens:
            self.stack.setCurrentWidget(self.screens[screen_name])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ViewSyncClient()
    client.show()
    sys.exit(app.exec())