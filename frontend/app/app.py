from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

#Home route
@app.route('/')
def home():
    return render_template("index.html")

@app.route("/addConsert", methods=["POST"])
def addConsert():
    data = request.get_json()
    #format and send to backend

    artist = data.get("artist")
    venue = data.get("venue")
    date = data.get("date")
    tour = data.get("tour")


    event_data = {
        "artist": artist,
        "venue": venue,
        "date": date,
        "tour": tour
    }

    #send event_data to backend...
    print(event_data)

     # Process the data (you could store it in a database or just print it for now)
    print(f"Artist: {artist}, Venue: {venue}, Date: {date}, Tour: {tour}")

    # Respond back to the client
    return jsonify({"message": "Event data received successfully", "data": event_data})
    #return jsonify({"message": "Message sent", "data":event_data})
    



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)