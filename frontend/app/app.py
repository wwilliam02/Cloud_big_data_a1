from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

#Home route
@app.route('/')
def home():
    return render_template("index.html")

def greet():
    data = request.get_json()
    name = data.get("name", "World")
    return jsonify({"message":f"Hello, {name}!"})

if