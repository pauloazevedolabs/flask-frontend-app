from flask import Flask

app = Flask(__name__)

# Health check endpoint
@app.route("/health")
def health():
    return "OK", 200

# Simple test page
@app.route("/")
def index():
    return "Frontend running!", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
