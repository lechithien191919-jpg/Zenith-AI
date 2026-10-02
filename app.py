import os
from flask import Flask, render_template, request, jsonify
from database import init_db
from data import get_or_create_user, get_chat_history, save_chat_message
from ai import generate_ai_response

app = Flask(__name__)

with app.app_context():
    init_db()

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_history", methods=["GET"])
def load_history():
    user_ip = get_client_ip()
    get_or_create_user(user_ip)
    history = get_chat_history(user_ip, limit=20)
    formatted_history = [{"role": role, "content": content} for role, content in history]
    return jsonify({"history": formatted_history})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    if not user_msg:
        return jsonify({"error": "Nội dung không được để trống"}), 400

    user_ip = get_client_ip()
    get_or_create_user(user_ip)
    history = get_chat_history(user_ip, limit=10)

    ai_reply = generate_ai_response(history, user_msg)

    save_chat_message(user_ip, "user", user_msg)
    save_chat_message(user_ip, "model", ai_reply)

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
