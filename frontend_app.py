import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!", 200
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
