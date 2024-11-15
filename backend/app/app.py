from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

# in-memory storage for concerts
concerts = []

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
        "id": len(concerts) + 1,
        "artist": artist,
        "venue": venue,
        "date": date,
        "tour": tour,
    }
    concerts.append(concert)

    return jsonify({"message": "Concert added successfully"}), 201


# get:/concert/<concert_id>/
@app.route("/concert/<int:id>", methods=["GET"])
def getConcert(id: int):
    #concert_id = request.args.get("id")
    concert_id = id
    if not concert_id:
        return jsonify({"error": "Conncert ID is required"}), 400
    
    try:
        concert_id = int(concert_id)
    except ValueError:
        return jsonify({"error": "Concert ID must be an integer"}), 400
    
    concert = None
    for i in concerts:
        if i["id"] == concert_id:
            concert = i
            break

    if not concert:
        return jsonify({"error":"Concert not found"}), 404

    return jsonify({"data": concert})

@app.route("/allConcerts", methods=["GET"])
def listAllConcerts():
    return jsonify({"concerts": concerts}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)