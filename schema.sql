DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS requests;
DROP TABLE IF EXISTS offers;

CREATE TABLE patients (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE requests (
  id SERIAL PRIMARY KEY NOT NULL,
  medicament TEXT NOT NULL,
  quant INT NOT NULL,
  type TEXT NOT NULL,
  status INT NOT NULL,
  ID_patient TEXT NOT NULL,
  name TEXT NOT NULL,
  contact TEXT NOT NULL,
  FOREIGN KEY (ID_patient) REFERENCES patients(id)
);

CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    medicament text NOT NULL,
    quant integer NOT NULL,
    type text NOT NULL,
    price numeric NOT NULL,
    status integer NOT NULL,
    id_request integer NOT NULL,
    FOREIGN KEY (id_request) REFERENCES requests(id)
)