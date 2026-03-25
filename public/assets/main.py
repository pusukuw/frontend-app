import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")  # Use a strong secret key in production

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000") # Default to localhost if not set

@app.route("/")
def index():
    """Renders the index page."""
    try:
        response = requests.get(f"{API_BASE_URL}/items")
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        items = response.json()
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching items: {e}", "error")
        items = []
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add_item():
    """Adds a new item to the backend."""
    name = request.form.get("name")
    description = request.form.get("description")

    if not name or not description:
        flash("Name and description are required.", "error")
        return redirect(url_for("index"))

    try:
        payload = {"name": name, "description": description}
        headers = {'Content-type': 'application/json'}
        response = requests.post(f"{API_BASE_URL}/items", data=json.dumps(payload), headers=headers)
        response.raise_for_status()

        flash("Item added successfully!", "success")
    except requests.exceptions.RequestException as e:
        flash(f"Error adding item: {e}", "error")

    return redirect(url_for("index"))


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    """Deletes an item from the backend."""
    try:
        response = requests.delete(f"{API_BASE_URL}/items/{item_id}")
        response.raise_for_status()
        flash("Item deleted successfully!", "success")
    except requests.exceptions.RequestException as e:
        flash(f"Error deleting item: {e}", "error")

    return redirect(url_for("index"))

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    """Edits an existing item."""
    if request.method == "GET":
        try:
            response = requests.get(f"{API_BASE_URL}/items/{item_id}")
            response.raise_for_status()
            item = response.json()
            return render_template("edit.html", item=item)
        except requests.exceptions.RequestException as e:
            flash(f"Error fetching item for edit: {e}", "error")
            return redirect(url_for("index"))
    elif request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name or not description:
            flash("Name and description are required.", "error")
            return redirect(url_for("edit_item", item_id=item_id))

        try:
            payload = {"name": name, "description": description}
            headers = {'Content-type': 'application/json'}
            response = requests.put(f"{API_BASE_URL}/items/{item_id}", data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            flash("Item updated successfully!", "success")
            return redirect(url_for("index"))
        except requests.exceptions.RequestException as e:
            flash(f"Error updating item: {e}", "error")
            return redirect(url_for("edit_item", item_id=item_id))

if __name__ == "__main__":
    app.run(debug=True)