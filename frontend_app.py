import os
from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

BACKEND_BASE = "http://10.0.0.4:5000"  # VM private IP

# ---------- Insert Page ----------
@app.route("/", methods=["GET", "POST"])
def insert_page():
    message = None
    if request.method == "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        dept = request.form.get("dept")
        try:
            r = requests.post(
                f"{BACKEND_BASE}/api/insert",
                json={"FirstName": first, "LastName": last, "Department": dept},
                timeout=5
            )
            r.raise_for_status()
            message = "✅ Row inserted successfully!"
            return redirect(url_for("table_page"))  # redirect after insert
        except Exception as e:
            message = f"❌ Insert failed: {e}"

    html = """
    <html>
    <head><title>Insert Employee</title></head>
    <body>
      <h2>Insert Employee</h2>
      {% if message %}<p><b>{{ message }}</b></p>{% endif %}
      <form method="POST">
        <input name="first" placeholder="First Name" required>
        <input name="last" placeholder="Last Name" required>
        <input name="dept" placeholder="Department" required>
        <button type="submit">Insert Row</button>
      </form>
      <p><a href="{{ url_for('table_page') }}">View Employees Table</a></p>
    </body>
    </html>
    """
    return render_template_string(html, message=message)

# ---------- Table Page ----------
@app.route("/table")
def table_page():
    try:
        r = requests.get(f"{BACKEND_BASE}/api/data", timeout=5)
        r.raise_for_status()
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}

    html = """
    <html>
    <head><title>Employees Table</title></head>
    <body>
      <h2>Employees Table</h2>
      <pre>{{ result | tojson(indent=2) }}</pre>
      <p><a href="{{ url_for('insert_page') }}">Insert Another Employee</a></p>
    </body>
    </html>
    """
    return render_template_string(html, result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
