from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Always use the database inside the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "automobile.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    return """
    <h1>Welcome to Automobile World!</h1>
    <h2>Backend is working successfully!</h2>
    <p>Python Flask is connected to our application.</p>
    """


@app.route("/book-service", methods=["POST"])
def book_service():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid booking data"}), 400

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    vehicle = data.get("vehicle", "").strip()
    service = data.get("service", "").strip()
    date = data.get("date", "").strip()

    if not all([name, phone, vehicle, service, date]):
        return jsonify({"error": "Please fill in all fields"}), 400

    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO bookings (name, phone, vehicle, service, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, phone, vehicle, service, date)
        )

        connection.commit()

        return jsonify({
            "message": "Service booking saved successfully!"
        }), 201

    except sqlite3.Error:
        app.logger.exception("Database error while saving booking")
        return jsonify({
            "error": "Could not save booking to the database"
        }), 500

    finally:
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)
