from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# # in-memory storage for concerts
# concerts = []
client = MongoClient("mongodb://localhost:27017")
db = client.concerts_db # Database
concerts_collection = db.concerts # collection

@app.route("/")
def home():
    """
    A simple home route to provide a basic message or interface.
    """
    return jsonify({"message": "Welcome to the Concert Management API"})




@app.route("/concert", methods=["POST"])
def addConcert():
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
        "tour": tour,
    }
    result = concerts_collection.insert_one(concert)

    return jsonify({"message": "Concert added successfully", "id": str(result.inserted_id)}), 201


# get:/concert/<concert_id>/
@app.route("/concert/<int:id>", methods=["GET"])
def getConcert(id: int):
    #concert_id = request.args.get("id")
    # concert_id = id
    # if not concert_id:
    #     return jsonify({"error": "Conncert ID is required"}), 400
    
    try:
        concert = concerts_collection.find_one({"_id":ObjectId(id)})
        if not concert:
            return jsonify({"error": "Concert not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid concert ID"}), 400
    
 # Convert ObjectId to string for JSON serialization
    concert["_id"] = str(concert["_id"])

    return jsonify({"data": concert}), 200

@app.route("/allConcerts", methods=["GET"])
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
    app.run(host="0.0.0.0", port=8000)