from flask import Flask, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=['GET'])
def home():
    return jsonify("Message","Gelukt")

