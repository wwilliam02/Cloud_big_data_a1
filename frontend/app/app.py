from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

concerts = []

backend_url = "http://localhost:8080"

#Home route
@app.route('/')
def home():
    try:
        response = requests.get(backend_url)
        response.raise_for_status()
        # concerts = response.json()
        print(response.content, flush=True)
    except requests.RequestException as e:
        print(f"Error connecting to backend: {e}", flush=True)
        # concerts = []


    return render_template("index.html")

@app.route("/addConcert", methods=["POST"])
def addConcert():
    data = request.get_json()
    #format and send to backend

    artist = data.get("artist")
    venue = data.get("venue")
    date = data.get("date")
    tour = data.get("tour")


    event_data = {
        "id":len(concerts) + 1,
        "artist": artist,
        "venue": venue,
        "date": date,
        "tour": tour
    }
    
    concerts.append(event_data)

    #send event_data to backend...
    # concerts.append(event_data)

    #  # Process the data (you could store it in a database or just print it for now)
    # print(f"Artist: {artist}, Venue: {venue}, Date: {date}, Tour: {tour}", flush=True)

    # url = backend_url + "/concert"

    try:
        response = requests.post(url=f"{backend_url}/concert" , json=event_data)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        print("Error adding concert: " + e, flush=True)
        return jsonify({"message: failed to add concert"}), 500
        
    
    # if response.status_code != 201:
    #     print("ERROR", flush=True)
    # else:
    #     print(response.content, flush=True)

    # Respond back to the client
    return jsonify({"message": result, "data": event_data})
    #return jsonify({"message": "Message sent", "data":event_data})
    



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)