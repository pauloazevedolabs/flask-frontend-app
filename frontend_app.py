import os
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

BACKEND_URL = "http://10.0.0.4:5000/api/data"  # Private VM IP

@app.route("/")
def home():
    try:
        response = requests.get(BACKEND_URL, timeout=5)
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    html = """
    <h1>Data from VM Backend</h1>
    <pre>{{ data }}</pre>
    """
    return render_template_string(html, data=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
