import os
from flask import Flask, render_template, request, redirect, url_for
import requests


BACKEND_BASE = "http://134.149.58.75:5000"  # VM private IP

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
            return redirect(url_for("table_page"))
        except Exception as e:
            message = f"❌ Insert failed: {e}"
    return render_template("insert.html", message=message)

# ---------- Table Page ----------
@app.route("/table")
def table_page():
    try:
        r = requests.get(f"{BACKEND_BASE}/api/data", timeout=5)
        r.raise_for_status()
        employees = r.json()
    except Exception as e:
        employees = []

    return render_template("table.html", employees=employees)

if __name__ == "__main__":
port = int(os.environ.get("PORT", 8000))
