import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!", 200
