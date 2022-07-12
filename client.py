import requests
 
api_url = 'http://127.0.0.1:8090/patients'

''' PATIENTS '''

def get():
    response = requests.get(api_url)
    print(response.json())

def get_per_id(id):
    url = api_url+"/"+str(id)
    response = requests.get(url)
    print(response.json()) 

def insert(name, email):
    patient = {"name": name, "email": email}
    response = requests.post(api_url, json=patient)
    print(response.json())

def put(id,name,email):
    url = api_url+"/"+str(id)
    patient = {"name": name, "email": email}
    response = requests.put(url, json=patient)
    print(response.json())

def delete(id):
    url = api_url+"/"+str(id)
    response = requests.delete(url)
    print(response.status_code)

''' REQUESTS '''

def getR():
    url = api_url+"/requests"
    response = requests.get(url)
    print(response.json())

def get_pid_all(pid):
    url = api_url+"/"+str(pid)+"/requests"
    response = requests.get(url)
    print(response.json())

def get_pid_rid(pid,rid):
    url = api_url+"/"+str(pid)+"/requests/"+str(rid)
    response = requests.get(url)
    print(response.json()) 

def insertR(medicament,quant,type,status,fk_id):
    url = api_url+"/"+str(fk_id)+"/requests"
    request = {'medicament':medicament,'quant':quant,'type':type,'status':status}
    response = requests.post(url, json=request)
    print(response.json())

def putR(medicament,quant,type,status,id,fk_id):
    url = api_url+"/"+str(fk_id)+"/requests/"+str(id)
    request = {'medicament':medicament,'quant':quant,'type':type,'status':status}
    response = requests.put(url, json=request)
    print(response.json())

def deleteR(id,fk_id):
    url = api_url+"/"+str(fk_id)+"/requests/"+str(id)
    response = requests.delete(url)
    print(response.status_code)

''' TESTS INSERT PATIENTS '''
# Register a new patient
insert()
insert()

''' TESTS INSERT REQUESTS '''
# Register a new request
insertR()
insertR()

''' TESTS GET PATIENTS '''
# Get all registered patients
get()
# Get a specific patient by id
get_per_id()

''' TESTS GET REQUESTS '''
# Gets all requests registered by patients
getR()
# Gets all requests registered by a specific patient
get_pid_all()
# Get a specific request registered from a specific patient
get_pid_rid(1,3)

''' TESTS PUT PATIENTS '''
# Update patient data
put()

''' TESTS PUT REQUESTS '''
# Update request data
putR()

''' TESTS DELETE REQUESTS '''
# Deletes a specific request by id (it is necessary to inform the patient's id, in addition to the request itself)
deleteR()

''' TESTS DELETE PATIENTS '''
# Delete a patient specified by id
delete()
