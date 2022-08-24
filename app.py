
# from asyncio.windows_events import NULL

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

@app.route("/patients/report",methods=['GET'])
def repor_all():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "select id_patient, count(id_patient) AS ""quant_total"",(select count(status) from requests where status = 1) AS ""quant_andamento"",(select count(status) from requests where status = 2) AS ""quant_concluido"",(select count(status) from requests where status = 3) AS ""quant_cancelado"" FROM requests group by id_patient"
    cur.execute(s)
    list_report = cur.fetchall()
    x = "select * from requests"
    cur.execute(x)
    list_request = cur.fetchall()
    list = []
    list_req = []
    confirm = 0
    canceled = 0
    progress = 0
    for row in list_report:
        list.append(dict(row))
    for row in list_request:
        list_req.append(dict(row))    
    
    for row in list:
        row['quant_andamento'] = 0
        row['quant_cancelado'] = 0
        row['quant_concluido'] = 0

    for row in list:
        confirm = 0
        canceled = 0
        progress = 0
        for i in list_req:

            if(row['id_patient'] == i['id_patient'] and i['status'] == 1):
                print('1')
                print(row['id_patient'])
                progress += 1
                row['quant_andamento'] = progress
            if(row['id_patient'] == i['id_patient'] and i['status'] == 2):
                print('2')
                print(row['id_patient'])
                confirm += 1
                row['quant_concluido'] = confirm
                    
            if(row['id_patient'] == i['id_patient'] and i['status'] == 3):
                print('3')
                print(row['id_patient'])
                canceled += 1
                row['quant_cancelado'] = canceled
        
       


    if list_report:

        return jsonify(list),200
    else:

        return jsonify({"error": "No report"}),400   


@app.route("/patients/<string:id>",methods=['GET'])
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
        id = request_data['id']
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
            cur.execute("INSERT INTO patients (id, name, email) VALUES (%s,%s,%s)", (id, name, email))
            conn.commit()
            return jsonify({"success": 'Patients'}), 201
    
@app.route("/patients/<string:id>",methods=['PUT'])
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

@app.route("/patients/<string:id>",methods=['DELETE'])
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

@app.route("/patients/<string:fk_id>/requests",methods=['GET'])
def get_requests_allP(fk_id):
    l = request.args.get('limit', default='NULL')
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM requests WHERE id_patient = %s ORDER BY id DESC LIMIT {}'.format(l), (fk_id,))
    data = cur.fetchall()
    list = []
    for row in data:
        list.append(dict(row))
    cur.close()
    if len(list) == 0:
        return jsonify({"error": "No requests found"})
    else:
        return jsonify(list),200


@app.route("/patients/requests/<int:id>/status",methods=['PATCH'])
def update_request_esP(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PATCH':
        request_data = request.get_json()
        status = request_data['status']
        # print(status)
        s = "SELECT * FROM requests"
        cur.execute(s)
        list_requests = cur.fetchall()
        list = []
        for row in list_requests:
            list.append(dict(row))
        for i in list:
            i.get('id')
            if i.get('id') == id: 
                cur.execute("UPDATE requests SET status = %s WHERE id = %s", (status,id), )
                conn.commit()
                return jsonify({'success': 'Requests'}), 200
        else:
            return jsonify({'error': 'Invalid'}), 400
    

@app.route("/patients/<string:fk_id>/requests",methods=['POST'])
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

@app.route("/patients/requests/<int:id>",methods=['PUT'])
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
    
@app.route("/patients/requests/<int:id>",methods=['DELETE'])
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
        return jsonify(list), 200

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
        quant = request_data['quant']
        type = request_data['type']
        price = request_data['price']
        status = request_data['status']
        id_request = fk_id # Essa variável vai receber o fk_id
        s = "SELECT * FROM requests"
        cur.execute(s)
        list_patients = cur.fetchall()
        list = []
        for row in list_patients:
            list.append(dict(row))
        for i in list:
            if i.get('id') == fk_id:  
                cur.execute("INSERT INTO offers (medicament, quant,type, price, status, id_request) VALUES (%s,%s, %s, %s, %s, %s);", (medicament,quant, type, price, status, id_request))
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


@app.route("/patients/offers/<int:id>/status",methods=['PATCH'])
def update_offers_esP(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PATCH':
        request_data = request.get_json()
        status = request_data['status']
        print(id)
        s = "SELECT * FROM offers"
        cur.execute(s)
        list_offers = cur.fetchall()
        list = []
        for row in list_offers:
            list.append(dict(row))
        for i in list:
            i.get('id')
            if i.get('id_request') == id: 
                cur.execute("UPDATE offers SET status = %s WHERE id_request = %s", (status,id), )
                conn.commit()
                return jsonify({'success': 'offers'}), 200
        else:
            return jsonify({'error': 'Invalid'}), 400

@app.route("/patients/offers/<int:id>/price",methods=['PATCH'])
def update_price_esP(id):
     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     if request.method == 'PATCH':
        request_data = request.get_json()
        price = request_data['price']
        print(price)
        s = "SELECT * FROM offers"
        cur.execute(s)
        list_offers = cur.fetchall()
        list = []
        for row in list_offers:
            list.append(dict(row))
        for i in list:
            i.get('id')
            if i.get('id_request') == id: 
                cur.execute("UPDATE offers SET price = %s WHERE id_request = %s", (price,id), )
                conn.commit()
                return jsonify({'success': 'offers'}), 200
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

@app.route("/requests/auditoria", methods=['GET'])
def get_auditoria():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM customer_auditoria"
    cur.execute(s)
    list_offers = cur.fetchall()
    list = []
    for row in list_offers:
        list.append(dict(row))
    if list_offers:
        return jsonify(list), 200
    else: 
        return jsonify(list), 200

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
    
    app.run(debug=True,host="0.0.0.0")
