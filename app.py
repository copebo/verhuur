from flask import Flask, request, jsonify

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)
app.config["DEBUG"] = True

cur = conn.cursor()
cur.execute("SELECT * FROM bedrijven;")
resultaten = cur.fetchone()
conn.commit()

# Close communication with the database
cur.close()
conn.close()




@app.route("/", methods=['GET'])
def home():

    return jsonify(resultaten)
    # return jsonify(message = "API is online")




bedrijven = [
    {
        'id': 1,
        'bedrijfsnaam': 'De Koningshoeve Verhuur & Catering',
        'adres' : 'Botweg 1b, 3286LB Klaaswaal',
        'telefoonnummer' : '0186-579397'
    },
    {
        'id': 2,
        'bedrijfsnaam': 'copebo',
        'adres' : 'Prins Alexanderlaan 91, 2912AK Nieuwerkerk aan den IJssel',
        'telefoonnummer' : '06-12345678'
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

