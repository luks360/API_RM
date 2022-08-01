import requests

api_url = 'http://127.0.0.1:5000/patients'

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
    sucess = response.json()
    print(sucess["sucess"])

def put(id,name,email):
    url = api_url+"/"+str(id)
    patient = {"name": name, "email": email}
    response = requests.put(url, json=patient)
    sucess = response.json()
    print(sucess["sucess"])

def delete(id):
    url = api_url+"/"+str(id)
    response = requests.delete(url)
    sucess = response.json()
    print(sucess["sucess"])

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
    sucess = response.json()
    print(sucess["sucess"])

def putR(medicament,quant,type,status,id,fk_id):
    url = api_url+"/"+str(fk_id)+"/requests/"+str(id)
    request = {'medicament':medicament,'quant':quant,'type':type,'status':status}
    response = requests.put(url, json=request)
    sucess = response.json()
    print(sucess["sucess"])

def deleteR(id,fk_id):
    url = api_url+"/"+str(fk_id)+"/requests/"+str(id)
    response = requests.delete(url)
    sucess = response.json()
    print(sucess["sucess"])


''' TESTS INSERT PATIENTS '''
# Register a new patient
# insert("Lucas","lucas@gmail.com")
# insert("Sebastião", "sebastiao@gmail.com")
# insert("Demetrios", "demetrios@gmail.com")
# insert("Raphael", "raphael@gmail.com")
# insert("Jefferson", "jefferson@gmail.com")

''' TESTS INSERT REQUESTS '''
# Register a new request
# insertR("A",1,"gotas",1,1)
# insertR("B",2,"comprimido",1,1)
# insertR("C",2,"gotas",1,2)
# insertR("D",2,"comprimido",1,2)
# insertR("E",2,"gotas",1,3)
# insertR("F",2,"comprimido",1,3)
# insertR("G",2,"gotas",1,4)
# insertR("H",2,"comprimido",1,4)
# insertR("I",2,"gotas",1,5)
# insertR("J",2,"comprimido",1,5)

''' TESTS GET REQUESTS '''
# Gets all requests registered by patients
# getR()
# Gets all requests registered by a specific patient
# get_pid_all(3)
# Get a specific request registered from a specific patient
# get_pid_rid(1,2)

''' TESTS PUT REQUESTS '''
# Update request data
# putR("Bo",5,"gotas",2,2,1)

''' TESTS DELETE REQUESTS '''
# Deletes a specific request by id (it is necessary to inform the patient's id, in addition to the request itself)
# deleteR(2,1)
