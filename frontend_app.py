import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

BACKEND_BASE = "http://10.0.0.4:5000"  # VM private IP

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    message = None

    if request.method == "POST":
        # Handle "Insert" form submission
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
        except Exception as e:
            message = f"❌ Insert failed: {e}"

    # Always fetch the data table
    try:
        r = requests.get(f"{BACKEND_BASE}/api/data", timeout=5)
        r.raise_for_status()
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}

    html = """
    <html>
    <head>
        <title>Azure SQL Demo</title>
        <style>
          body { font-family: Arial; margin: 40px; }
          input { margin: 4px; padding: 6px; }
          button { padding: 6px 10px; }
          pre { background: #f5f5f5; padding: 10px; border-radius: 4px; }
        </style>
    </head>
    <body>
      <h2>Azure SQL Demo App</h2>

      {% if message %}
        <p><b>{{ message }}</b></p>
      {% endif %}

      <form method="POST">
        <input name="first" placeholder="First Name" required>
        <input name="last" placeholder="Last Name" required>
        <input name="dept" placeholder="Department" required>
        <button type="submit">Insert Row</button>
      </form>

      <h3>Table Data</h3>
      <pre>{{ result | tojson(indent=2) }}</pre>
    </body>
    </html>
    """

    return render_template_string(html, result=result, message=message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
