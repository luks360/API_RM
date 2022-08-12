import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint

import db
from db import conn

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# Crud de patients
@app.route("/patients",methods=['GET'])
def get_patients():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM patients"
    cur.execute(s)
    list_patients = cur.fetchall()
    list = []
    for row in list_patients:
        list.append(dict(row))
    if list_patients:

        return jsonify(list),200
    else:

        return jsonify({"error": "No patients"}),400    

@app.route("/patients/<int:id>",methods=['GET'])
def get_patient_id(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM patients WHERE id = %s', (id, ))
    data = cur.fetchall()
    list = []
    for row in data:
        list.append(dict(row))
    cur.close()
    if len(list) == 0:
        return jsonify({"error": "No patients found"})
    else:
        return jsonify(list[0]),200

@app.route("/patients",methods=['POST'])
def add_patients():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        request_data = request.get_json()
        name = request_data['name']
        email = request_data['email']
        s = "SELECT * FROM patients"
        cur.execute(s)
        list_patients = cur.fetchall()
        list = []
        for row in list_patients:
            list.append(dict(row))
        for i in list:
            if i.get('email') == email:
                return jsonify({"error": "No patients found"})
        else:
            cur.execute("INSERT INTO patients (name, email) VALUES (%s,%s)", (name, email))
            conn.commit()
            return jsonify({"success": 'Patients'}), 201
    
@app.route("/patients/<int:id>",methods=['PUT'])
def put_patient(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PUT':
        request_data = request.get_json()
        name = request_data['name']
        email = request_data['email']
        s = "SELECT * FROM patients"
        cur.execute(s)
        list_patients = cur.fetchall()
        list = []
        for row in list_patients:
            list.append(dict(row))
        for i in list:
            if i.get('id') == id: 
                cur.execute("UPDATE patients SET name = %s,  email = %s WHERE id = %s", (name, email, id, ))
                conn.commit()
                return jsonify({'success': 'Patients'}), 200
        else:
            return jsonify({'error': 'Invalid'}), 400

@app.route("/patients/<int:id>",methods=['DELETE'])
def delete_patient(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM patients WHERE id = %s RETURNING id;", [id])
    result = cur.fetchall()
    conn.commit()
    if result:
        return jsonify({'success': 'Patients'}), 204
    else:
        return jsonify({'error': 'Invalid'}), 400  

# Crud de requests
@app.route("/patients/requests",methods=['GET'])
def get_requests():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM requests"
    cur.execute(s)
    list_requests = cur.fetchall()
    list = []
    for row in list_requests:
        list.append(dict(row))
    if list_requests:
        return jsonify(list), 200
    else: 
        return jsonify({'error': 'Invalid'}), 400

@app.route("/patients/<int:fk_id>/requests",methods=['GET'])
def get_requests_allP(fk_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM requests WHERE id_patient = %s', (fk_id, ))
    data = cur.fetchall()
    list = []
    for row in data:
        list.append(dict(row))
    cur.close()
    if len(list) == 0:
        return jsonify({"error": "No requests found"})
    else:
        return jsonify(list),200


@app.route("/patients/<int:id>/requests/status",methods=['PATCH'])
def update_request_esP(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PATCH':
        request_data = request.get_json()

        status = request_data['status']
        print(status)
        s = "SELECT * FROM requests"
        cur.execute(s)
        list_requests = cur.fetchall()
        list = []
        for row in list_requests:
            list.append(dict(row))
        for i in list:
            if i.get('id') == id: 
                cur.execute("UPDATE requests SET status = %s WHERE id = %s", (status,id), )
                conn.commit()
                return jsonify({'success': 'Requests'}), 200
        else:
            return jsonify({'error': 'Invalid'}), 400
    

@app.route("/patients/<int:fk_id>/requests",methods=['POST'])
def add_request(fk_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        request_data = request.get_json()
        medicament = request_data['medicament']
        quant = request_data['quant']
        type = request_data['type']
        status = request_data['status']
        id_patient = request_data['id_patient'] # Essa variável vai receber o fk_id
        contact = request_data['contact']
        name = request_data['name']
        s = "SELECT * FROM patients"
        cur.execute(s)
        list_patients = cur.fetchall()
        list = []
        for row in list_patients:
            list.append(dict(row))
        for i in list:
            if i.get('id') == fk_id:  
                cur.execute("INSERT INTO requests (medicament, quant, type, status, id_patient, contact, name) VALUES (%s,%s, %s, %s, %s, %s, %s);", (medicament, quant, type, status, id_patient, contact,name))
                conn.commit()
                return jsonify({"success": 'Patients'}), 201
        else:
            return jsonify({"error": "No patients"}), 400

@app.route("/patients/<int:id>/requests",methods=['PUT'])
def put_request(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PUT':
        request_data = request.get_json()
        medicament = request_data['medicament']
        quant = request_data['quant']
        status = request_data['status']
        type = request_data['type']
        s = "SELECT * FROM requests"
        cur.execute(s)
        list_requests = cur.fetchall()
        list = []
        for row in list_requests:
            list.append(dict(row))
        for i in list:
            if i.get('id') == id: 
                cur.execute("UPDATE requests SET medicament = %s,  quant = %s, status = %s, type = %s WHERE id = %s", (medicament, quant, status, type,id), )
                conn.commit()
                return jsonify({'success': 'Requests'}), 200
        else:
            return jsonify({'error': 'Invalid'}), 400
    
@app.route("/patients/<int:id>/requests",methods=['DELETE'])
def delete_request(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM requests WHERE id = %s RETURNING id;", [id])
    result = cur.fetchall()
    conn.commit()
    if result:
        return jsonify({'success': 'Requests'}), 204
    else:
        return jsonify({'error': 'Invalid'}), 400 

# Crud de offers
@app.route("/requests/offers", methods=['GET'])
def get_offers():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM offers"
    cur.execute(s)
    list_offers = cur.fetchall()
    list = []
    for row in list_offers:
        list.append(dict(row))
    if list_offers:
        return jsonify(list), 200
    else: 
        return jsonify({'error': 'Invalid'}), 400

@app.route("/requests/<int:fk_id>/offers", methods=["GET"])
def get_all_offers_specific(fk_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM offers WHERE id_request = %s', (fk_id, ))
    data = cur.fetchall()
    list = []
    for row in data:
        list.append(dict(row))
    cur.close()
    if len(list) == 0:
        return jsonify({"error": "No offers found"}), 400
    else:
        return jsonify(list),200

@app.route('/requests/<int:fk_id>/offers', methods=['POST'])
def add_offers(fk_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        request_data = request.get_json()
        print(request_data)
        medicament = request_data['medicament']
        type = request_data['type']
        price = request_data['price']
        status = request_data['status']
        id_request = request_data['id_request'] # Essa variável vai receber o fk_id
        s = "SELECT * FROM requests"
        cur.execute(s)
        list_patients = cur.fetchall()
        list = []
        for row in list_patients:
            list.append(dict(row))
        for i in list:
            if i.get('id') == fk_id:  
                cur.execute("INSERT INTO offers (medicament, type, price, status, id_request) VALUES (%s,%s, %s, %s, %s);", (medicament, type, price, status, id_request))
                conn.commit()
                return jsonify({"success": 'offers'}), 201
        else:
            return jsonify({"error": "Invalid"}), 400

@app.route('/requests/<int:id>/offers', methods=['PUT'])
def put_offers(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PUT':
        request_data = request.get_json()
        medicament = request_data['medicament']
        type = request_data['type']
        price = request_data['price']
        status = request_data['status']
        s = "SELECT * FROM offers"
        cur.execute(s)
        list_requests = cur.fetchall()
        list = []
        for row in list_requests:
            list.append(dict(row))
        for i in list:
            if i.get('id') == id: 
                cur.execute("UPDATE offers SET medicament = %s,  type = %s, price = %s, status = %s  WHERE id = %s", (medicament, type, price, status,id), )
                conn.commit()
                return jsonify({'success': 'Offers'}), 200
        else:
            return jsonify({'error': 'Invalid'}), 400

@app.route("/requests/<int:id>/offers",methods=['DELETE'])
def delete_offers(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM offers WHERE id = %s RETURNING id;", [id])
    result = cur.fetchall()
    conn.commit()
    if result:
        return jsonify({'success': 'offers'}), 204
    else:
        return jsonify({'error': 'Invalid'}), 400 

@app.errorhandler(400)
def error_400(e):
    return "solicitação inválida"

@app.errorhandler(401)
def error_401(e):
    return "não autorizado"

@app.errorhandler(403)
def error_403(e):
    return "proibido"

@app.errorhandler(404)
def error_404(e):
    return "Não foi possivel encontrar"

@app.errorhandler(415)
def error_415(e):
    return "tipo de mídia não suportado"

if __name__ == '__main__':
    init_db = False
    
    db.init_app(app)
    
    if init_db:
        with app.app_context():
            db.init_db()
    
    app.run(debug=True,host="0.0.0.0")
