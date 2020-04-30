from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=['GET'])
def home():
    return jsonify(message = "API is online")


bedrijven = [
    {
        'id': 1,
        'bedrijfsnaam': 'De Koningshoeve Verhuur & Catering',
        'adres' : 'Botweg 1b, 3286LB Klaaswaal'
    },
    {
        'id': 2,
        'bedrijfsnaam': 'copebp',
        'adres' : 'Prins Alexanderlaan 91, 2912AK Nieuwerkerk aan den IJssel'
    },

]

@app.route("/api/v1/bedrijven/all", methods=['GET'])
def bedrijf_all():
    return jsonify(bedrijven)


@app.route("/api/v1/bedrijven/", methods=['GET'])
def bedrijf():
    if 'id' in request.args:
        id = int(request.args['id'])
    else :
        return jsonify(message = "Geen bedrijf gevonden met het id " + str(request.args['id']) )

    results = []

    for bedrijf in bedrijven:
        if bedrijf['id'] == id:
            results.append(bedrijf)

    return jsonify(results)

