import psycopg2
import psycopg2.extras
from flask import Flask

app = Flask(__name__)

app.secret_key = "super secret key"

DB_HOST = "localhost"
DB_NAME = "frm-patients"
DB_USER = "postgres"
DB_PASS = "2002"

conn = psycopg2.connect(host=DB_HOST, password=DB_PASS, dbname=DB_NAME, user=DB_USER)

