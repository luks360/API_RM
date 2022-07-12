import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE = 'database.db'

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def insert(args=()):
    sql = ''' INSERT INTO patients(name,email)
              VALUES(?,?) '''
    cur = get_db().cursor()
    cur.execute(sql, args)
    get_db().commit()
    return cur.lastrowid

def put(args=()):
    sql = ''' UPDATE patients SET name = ?, email = ? WHERE id = ? '''
    cur = get_db().cursor()
    cur.execute(sql, (args[0],args[1],args[2],))
    get_db().commit()
    return cur.lastrowid

def delete(args=()):
    sql = ''' DELETE FROM patients WHERE id = ? '''
    cur = get_db().cursor()
    cur.execute(sql, (args,))
    get_db().commit()
    return cur.lastrowid

def insertR(args=()):
    sql = ''' INSERT INTO requests(medicament,quant,type,status,ID_patient)
              VALUES(?,?,?,?,?) '''
    cur = get_db().cursor()
    cur.execute(sql, args)
    get_db().commit()
    return cur.lastrowid

def putR(args=()):
    sql = ''' UPDATE requests SET medicament = ?, quant = ?, type = ?, status = ? WHERE id = ? AND ID_patient = ?'''
    cur = get_db().cursor()
    cur.execute(sql, (args[0],args[1],args[2],args[3],args[4],args[5],))
    get_db().commit()
    return cur.lastrowid

def deleteR(args=()):
    sql = ''' DELETE FROM requests WHERE id = ? AND ID_patient = ? '''
    cur = get_db().cursor()
    cur.execute(sql, (args[0],args[1],))
    get_db().commit()
    return cur.lastrowid

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = [dict((cur.description[i][0], value) \
       for i, value in enumerate(row)) for row in cur.fetchall()]
   
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

if __name__ == "__main__":

    init_db_command()