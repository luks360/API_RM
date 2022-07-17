from flask import Flask, request, jsonify
import db
    
app = Flask(__name__)

@app.route("/patients",methods=['GET'])
def get_patients():
    patients = db.get()
    return jsonify(patients),200

@app.route("/patients/<int:id>",methods=['GET'])
def get_patient_id(id):
    patients = db.getId(id)
    return jsonify(patients),200

@app.route("/patients",methods=['POST'])
def add_patients():
    if request.is_json:
        patient = request.get_json()
        id = db.insert((patient['name'],patient['email']))
        return {"sucess":"Paciente criado (id: "+str(id)+")."},201

@app.route("/patients/<int:id>",methods=['PUT'])
def put_patient(id):
    if request.is_json:
        patient = request.get_json()
        db.put((patient["name"], patient["email"], id))
        return {"sucess":"Paciente do id: "+str(id)+" foi alterado"},200

@app.route("/patients/<int:id>",methods=['DELETE'])
def delete_patient(id):
    db.delete(int(id))
    return {"sucess":"Paciente de id: "+str(id)+" foi deletado"},200
        
@app.route("/patients/requests",methods=['GET'])
def get_requests():
    requests = db.getR()
    return jsonify(requests),200

@app.route("/patients/<int:fk_id>/requests",methods=['GET'])
def get_requests_allP(fk_id):
    requests = db.getIdAllR(fk_id)
    return jsonify(requests),200

@app.route("/patients/<int:fk_id>/requests/<int:id>",methods=['GET'])
def get_request_esP(fk_id,id):
    requests = db.getIdR((fk_id,id))
    return jsonify(requests),200

@app.route("/patients/<int:fk_id>/requests",methods=['POST'])
def add_request(fk_id):
    if request.is_json:
        requests = request.get_json()
        id = db.insertR((requests['medicament'],requests['quant'],requests['type'],requests['status'],fk_id))
        return {"sucess":"Requisição criada (id: "+str(id)+")."},201

@app.route("/patients/<int:fk_id>/requests/<int:id>",methods=['PUT'])
def put_request(fk_id,id):
    if request.is_json:
        requests = request.get_json()
        db.putR((requests['medicament'],requests['quant'],requests['type'],requests['status'],id,fk_id))
        return {"sucess":"Requisição do paciente de id: "+str(fk_id)+" alterada (id da requisição: "+str(id)+")."},200

@app.route("/patients/<int:fk_id>/requests/<int:id>",methods=['DELETE'])
def delete_request(fk_id,id):

    db.deleteR((int(id),int(fk_id)))
    return {"sucess":"Requisição do paciente de id: "+str(fk_id)+" foi deletada (id da requisição: "+str(id)+")"},200

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
    
    app.run(debug=True,host="0.0.0.0", port=8090)
