from flask import Flask, request, jsonify, Response
import yt_dlp
import requests
import os

app = Flask(__name__)

@app.route("/stream", methods=["GET"])
def stream():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio[ext=webm]/bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info['url']

        def generate():
            with requests.get(stream_url, stream=True, headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.youtube.com"
            }) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        yield chunk

        # Serve the stream with appropriate content type
        return Response(generate(), content_type='audio/webm')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "🎶 Boom Music API Running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
