from flask import Flask, request, jsonify
import db
    
app = Flask(__name__)

@app.route("/patients",methods=['GET'])
def get_patients():
    patients = db.query_db('select * from patients')
    return jsonify(patients),200

@app.route("/patients/<int:id>",methods=['GET'])
def get_patient_id(id):
    patients = db.query_db('select * from patients where id = ' + str(id))
    return jsonify(patients),200

@app.route("/patients",methods=['POST'])
def add_patients():
    if request.is_json:
        patient = request.get_json()
        id = db.insert((patient['name'],patient['email']))
        return 201
    return {"error": "Request must be JSON"}, 415

@app.route("/patients/<int:id>",methods=['PUT'])
def put_patient(id):
    if request.is_json:
        patient = request.get_json()
        idr = db.put((patient["name"], patient["email"], id))
        return 200
    return {"error": "Request must be JSON"}, 415

@app.route("/patients/<int:id>",methods=['DELETE'])
def delete_patient(id):
    
    id = db.delete(int(id))
    return 200
        
@app.route("/patients/requests",methods=['GET'])
def get_requests():
    requests = db.query_db('select * from requests')
    return jsonify(requests),200

@app.route("/patients/<int:fk_id>/requests",methods=['GET'])
def get_requests_allP(fk_id):
    requests = db.query_db('select * from requests where ID_patient = ' + str(fk_id))
    return jsonify(requests),200

@app.route("/patients/<int:fk_id>/requests/<int:id>",methods=['GET'])
def get_request_esP(fk_id,id):
    requests = db.query_db('select * from requests where ID_patient = ' + str(fk_id) + " and id = " + str(id))
    return jsonify(requests),200

@app.route("/patients/<int:fk_id>/requests",methods=['POST'])
def add_request(fk_id):
    if request.is_json:
        requests = request.get_json()
        id = db.insertR((requests['medicament'],requests['quant'],requests['type'],requests['status'],fk_id))
        return 201
    return {"error": "Request must be JSON"}, 415

@app.route("/patients/<int:fk_id>/requests/<int:id>",methods=['PUT'])
def put_request(fk_id,id):
    if request.is_json:
        requests = request.get_json()
        idr = db.putR((requests['medicament'],requests['quant'],requests['type'],requests['status'],id,fk_id))
        return 200
    return {"error": "Request must be JSON"}, 415

@app.route("/patients/<int:fk_id>/requests/<int:id>",methods=['DELETE'])
def delete_request(fk_id,id):

    id = db.deleteR((int(id),int(fk_id)))
    return 200

if __name__ == '__main__':
    init_db = False
    
    db.init_app(app)
    
    if init_db:
        with app.app_context():
            db.init_db()
    
    app.run(debug=True,host="0.0.0.0", port=8090)
