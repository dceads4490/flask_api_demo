# flask_api_tst/app.py
from flask import Flask, request, jsonify, make_response
import requests
# Import the database driver and shapefile library
import psycopg2
import psycopg2.pool
import shapefile
import socket
import time
import os
from envs import env
import logging
import sys
log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

app = Flask(__name__)


def postgress_wait():
    port = 5432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(('postgres', port))
            s.close()
            break
        except socket.error as ex:
            log.info("Waiting for postgress")
            time.sleep(1)


def init_db_pool():
    global pool
    postgres_db=env('POSTGRES_DB')
    postgres_user=env('POSTGRES_USER')
    postgres_password=env('POSTGRES_PASSWORD')
    log.info("Going to print env")
    log.info(postgres_db)
    log.info(postgres_user)
    log.info(postgres_password)
    pool = psycopg2.pool.SimpleConnectionPool(1, 20, host="postgres", 
            database=env('POSTGRES_DB'), 
            user=env('POSTGRES_USER'), 
            password=env('POSTGRES_PASSWORD'))

postgress_wait()
init_db_pool()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def hello():
    results='No Parameter provided'

    return results

@app.route('/state_locator/',methods=['PUT','GET'])
def state_loc():
    query_parameters = request.args
    addr = query_parameters.get('addr')

    if addr:
        addr_str=addr
        api_key=env('GOOGLE_API_KEY')
        if api_key != "":
            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' +addr_str+ '&key='+ env('GOOGLE_API_KEY'))
        else:
            log.error("SUPPORT: Place Google API key into .env file")
            return make_response(jsonify({'error': 'No Google API key found'}), 404)
        
        json_payload=response.json()
        results_lng=str(json_payload['results'][0]['geometry']['location']['lng'])
        results_lat=str(json_payload['results'][0]['geometry']['location']['lat'])
    if not (addr):
       return make_response(jsonify({'error': 'No Address supplied'}), 404)


    # Get database connection
    connection = pool.getconn()

    # Get the database cursor to execute queries
    cursor = connection.cursor()
    query = 'select name from tl_2019_us_state where st_contains(geom,st_point('+results_lng+','+results_lat+'));'
    cursor.execute(query)
    row=cursor.fetchone();
    log.info(query)
    log.info("value=["+row[0]+"]")
    cursor.close()
    #Close connection
    pool.putconn(connection)

#    return jsonify(row)
    return row[0]



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



