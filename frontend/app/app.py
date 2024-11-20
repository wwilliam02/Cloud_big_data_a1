from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

concerts = []

backend_url = "http://backend:8080"

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

    event_data = {
        "artist": data.get("artist"),
        "venue": data.get("venue"),
        "date": data.get("date"),
        "tour": data.get("tour")
    }
    
    # concerts.append(event_data)

    try:
        response = requests.post(url=f"{backend_url}/concert" , json=event_data)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        print("Error adding concert: " + str(e), flush=True)
        return jsonify({"message: failed to add concert": str(e)}), 500
        
    
    # if response.status_code != 201:
    #     print("ERROR", flush=True)
    # else:
    #     print(response.content, flush=True)

    # Respond back to the client
    return jsonify({"message": "Concert added successfully", "data": event_data})
    #return jsonify({"message": "Message sent", "data":event_data})


@app.route("/allConcerts")
def show_all_concerts():

    try:
        response = requests.get(url=f"{backend_url}/allConcerts")
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        return jsonify({"message: failed to show concerts": str(e)}), 500
    
    print(result, flush=True)
    return jsonify(result)



@app.route("/concert/<id>", methods=["DELETE"])
def deleteConcert(id):
    
    try:
        response = requests.delete(url=f"{backend_url}/concert/{id}")
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        print("Error deleting concert: " + str(e), flush=True)
        return jsonify({"message": "Failed to delete concert", "error": str(e)}), 500
    
    return jsonify({"message": f"Concert with ID {id} deleted successfully", "data": result})
    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)