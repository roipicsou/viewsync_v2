from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Stockage temporaire de l'écran affiché
current_screen = "default"

@app.route("/set_screen", methods=["POST"])
def set_screen():
    global current_screen
    data = request.json
    if "screen" in data:
        current_screen = data["screen"]
        socketio.emit("screen_update", {"screen": current_screen})  # Notification en temps réel
        return jsonify({"message": "Screen updated", "screen": current_screen})
    return jsonify({"error": "Missing 'screen' parameter"}), 400

@app.route("/get_screen", methods=["GET"])
def get_screen():
    return jsonify({"screen": current_screen})

@socketio.on("connect")
def handle_connect():
    socketio.emit("screen_update", {"screen": current_screen})

if __name__ == "__main__":
    socketio.run(app, debug=True)