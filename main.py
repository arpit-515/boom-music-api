from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/audio", methods=["GET"])
def get_audio():
    video_id = request.args.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"url": info["url"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "🎶 Boom Music API Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

