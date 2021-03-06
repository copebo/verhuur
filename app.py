from flask import Flask, request, jsonify

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=['GET'])
def home():
    return jsonify(message = "API is online")

@app.route("/api/v1/bedrijven/all", methods=['GET'])
def bedrijf_all():

    try:
        # Verbinden
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        # Opbouwen SQL
        cur.execute("SELECT * FROM bedrijf;")
        conn.commit()

        resultaten = cur.fetchall()

        bedrijven = []

        for resultaat in resultaten:
            bedrijven.append( { 
                "ID": resultaat[0], 
                "Bedrijfsnaam": resultaat[1] 
            } )

        return jsonify(bedrijven)

    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return jsonify(message = "Overzicht laden niet gelukt"), 404

    finally:
        # closing database connection
        if (conn):
            cur.close()
            conn.close()


@app.route("/api/v1/bedrijven/", methods=['GET'])
def bedrijf():
    
    if 'id' in request.args:
        id = request.args['id']
        if id:
            id = str(id)

            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')

                cur = conn.cursor()
                cur.execute("SELECT * FROM bedrijf WHERE idbedrijf = %s ;", (id,))
                conn.commit()

                resultaat = cur.fetchone()
                bedrijf = []

                bedrijf.append( { 
                    "ID": resultaat[0], 
                    "Bedrijfsnaam": resultaat[1] 
                } )

                return jsonify(bedrijf)

            except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    return jsonify(message = "Geen bedrijf gevonden met id "+ id), 404

            finally:
                # closing database connection
                if (conn):
                    cur.close()
                    conn.close()
                    print("PostgreSQL connection is closed \n")

        else:
            return jsonify(message = "Geen id meegegeven"), 404

    else:
        return jsonify(message = "Geen id meegegeven"), 404



@app.route("/api/v1/bedrijven/", methods=['POST'])
def bedrijf_toevoegen():

    # Request data
    bedrijf = request.get_json()

    bedrijfsnaam = bedrijf['bedrijfsnaam']
    idbedrijf = bedrijf['idbedrijf']

    #Transform data
    idbedrijf = int(idbedrijf)
    bedrijfsnaam = str(bedrijfsnaam)

    try:
        # Verbinden
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("INSERT INTO bedrijf (idbedrijf,bedrijfsnaam) VALUES(%s,%s);", (idbedrijf, bedrijfsnaam))
        conn.commit()

        return jsonify(insertID = str(cur.lastrowid))

    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return jsonify(message = "Toevoegen niet gelukt"), 404

    finally:
        # closing database connection
        cur.close()
        conn.close()



@app.route("/api/v1/bedrijven/", methods=['DELETE'])
def bedrijf_verwijderen():

    if 'id' in request.args:

        id = request.args['id']
        # print(id)
        
        if id:

            try:
                # Verbinden
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()

                # Opbouwen SQL
                cur.execute("DELETE FROM bedrijf WHERE idbedrijf = %s ;", (id,))
                
                conn.commit()
                
                if cur.rowcount == 1:
                    return jsonify(message = "Bedrijf met id "+ str(id) +" verwijderd")
                else :
                    return jsonify(message = "Geen bedrijf met id "+ str(id) +" gevonden")


            except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    return jsonify(message = "Verwijderen niet gelukt"), 404

            finally:
                # closing database connection
                if (conn):
                    cur.close()
                    conn.close()
                    # print("PostgreSQL connection is closed \n")

        else:
            return jsonify(message = "Geen id meegegeven"), 404

    else:
        return jsonify(message = "Geen id meegegeven"), 404
