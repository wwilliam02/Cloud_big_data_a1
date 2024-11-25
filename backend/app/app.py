from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

app = Flask(__name__)

# Database setup
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.concerts_db 
concerts_collection = db.concerts


@app.route("/")
def home():
    """
    Used for testing frontend com.
    """
    return jsonify({"message": "Welcome to the Concert Management API"})


@app.route("/concert", methods=["POST"])
def addConcert():
    """
    Adds concert to database
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    artist = data.get("artist")
    venue = data.get("venue")
    date = data.get("date")
    tour = data.get("tour")
    
    if not artist or not venue or not date:
        return jsonify({"error": "Artist, Venue and date are required"}), 400
    
    concert = {
        "artist": artist,
        "venue": venue,
        "date": date,
        "tour": tour
    }
 
    try:
        result = concerts_collection.insert_one(concert)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    return jsonify({"message": "Concert added successfully", "id": str(result.inserted_id)}), 201

@app.route("/concert/<id>", methods=["DELETE"])
def deleteConcert(id):
    """
    Delete a single concert from the MongoDB database by its ID.
    """
    try:
        result = concerts_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Concert not found"}), 404
        return jsonify({"message": "Concert deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Invalid concert ID"}), 400

# get:/concert/<concert_id>/
@app.route("/concert/<id>", methods=["GET"])
def getConcert(id: str):
    """
    Fix if we should use it
    """
    try:
        concert = concerts_collection.find_one({"_id":ObjectId(id)})
        if not concert:
            return jsonify({"error": "Concert not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid concert ID"}), 400
    
 # Convert ObjectId to string for JSON serialization
    concert["_id"] = str(concert["_id"])

    return jsonify({"data": concert}), 200

@app.route("/concert", methods=["GET"])
def listAllConcerts():
    """
    Retrieve all concerts from the MongoDB database.
    """
    concerts = []
    for concert in concerts_collection.find():
        concert["_id"] = str(concert["_id"])  # Convert ObjectId to string
        concerts.append(concert)

    return jsonify({"concerts": concerts}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)