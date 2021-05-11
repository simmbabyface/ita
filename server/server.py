# -*- coding:utf-8 -*-

import bottle_pgsql
import datetime
import collections
import json
import os
# import jwt
# import logging.config
import psycopg2
# import uuid
from bottle import HTTPError, request, response, run, Bottle, static_file, redirect
# from datetime import datetime, timedelta

# logging.config.dictConfig(json.load(open('logging.json', 'rb')))

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

app = Bottle()
plugin = bottle_pgsql.Plugin('dbname=ita user=babyface password=5555 host=localhost port=5432')
app.install(plugin)

@app.get('/sample')
def sample_redirect():
    redirect('/#sample')

@app.get('/chemical')
def chemical_redirect():
    redirect('/#chemical')

@app.get('/assay')
def chemical_redirect():
    redirect('/#assay')

@app.get('/sampleItem')
def sample_item_redirect():
    redirect('/#sampleItem')

@app.get('/sampleItem/<sample_id>')
def sample_item_param_redirect(sample_id):
    redirect('/#sampleItem/' + sample_id)

@app.get('/chemicalItem')
def chemical_item_redirect():
    redirect('/#chemicalItem')

@app.get('/chemicalItem/<chemical_id>')
def chemical_item_param_redirect(chemical_id):
    redirect('/#chemicalItem/' + chemical_id)

@app.get('/assayItem')
def assay_item_redirect():
    redirect('/#assayItem')

@app.get('/assayItem/<assay_id>')
def assay_item_param_redirect(assay_id):
    redirect('/#assayItem/' + assay_id)


@app.route('/')
def server_static_index(filename="index.html"):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), '..', 'client'))

@app.route('/<filename:path>')
def server_static(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), '..', 'client'))

@app.get('/get_all_assay_names_keyed_by_toxicities')
def get_all_assay_names_keyed_by_toxicities_handler(db):
    response_dict = collections.defaultdict(list)
    db.execute('SELECT toxicity, assay_name FROM assay')
    for row in db.fetchall():
        response_dict[row['toxicity']].append(row['assay_name'])
    return json.dumps(response_dict)

@app.get('/get_all_biological_process_targets_keyed_by_toxicities')
def get_all_biological_process_targets_keyed_by_toxicities_handler(db):
    response_dict = collections.defaultdict(list)
    db.execute('SELECT toxicity, biological_process_target FROM assay')
    for row in db.fetchall():
        response_dict[row['toxicity']].append(row['biological_process_target'])
    return json.dumps(response_dict)

@app.get('/get_all_sample_types')
def get_all_sample_types_keyed_by_toxicities_handler(db):
    response_dict = collections.defaultdict(list)
    db.execute('SELECT DISTINCT sample_type FROM sample')
    for row in db.fetchall():
        response_dict['sample_type'].append(row['sample_type'])
    return json.dumps(response_dict)

@app.post('/search_sample')
def search_sample_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    start_time = data['start_time']
    end_time = data['end_time']
    sample_type = data['type']
    assay = data['assay']
    toxicity = data['toxicity']
    # cas = data['cas']

    constraint_sample = []
    constraint_assay = []
    constraint_variables = []
    if start_time != '':
        constraint_sample.append('sampling_time >= %s')
        constraint_variables.append(start_time)
    if end_time != '':
        constraint_sample.append('sampling_time <= %s')
        constraint_variables.append(end_time)
    if sample_type != '':
        constraint_sample.append('sample_type = %s')
        constraint_variables.append(sample_type)

    if assay != '':
        constraint_assay.append('assay_name = %s')
        constraint_variables.append(assay)
    if toxicity != '':
        constraint_assay.append('toxicity = %s')
        constraint_variables.append(toxicity)

    query = 'SELECT DISTINCT s.sample_id, s.sampling_name, s.sampling_location, s.sampling_time, s.sample_type FROM ( SELECT * FROM sample'
    if len(constraint_sample) > 0:
        query += ' WHERE ' + ' AND '.join(constraint_sample)
    query += ') AS s INNER JOIN sample_assay ON s.sample_id = sample_assay.sample_id INNER JOIN ('
    query += 'SELECT * FROM assay'
    if len(constraint_assay) > 0:
        query += ' WHERE ' + ' AND '.join(constraint_assay)
    query += ') AS a ON sample_assay.assay_id = a.assay_id;'
    db.execute(query, tuple(constraint_variables))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/search_assay')
def search_assay_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    biological_process_target = data['biological_process_target']
    toxicity = data['toxicity']

    constraint_assay = []
    constraint_variables = []
    if biological_process_target != '':
        constraint_assay.append('biological_process_target = %s')
        constraint_variables.append(biological_process_target)
    if toxicity != '':
        constraint_assay.append('toxicity = %s')
        constraint_variables.append(toxicity)

    query = 'SELECT * FROM assay'
    if len(constraint_assay) > 0:
        query += ' WHERE ' + ' AND '.join(constraint_assay)
    query += ';'
    db.execute(query, tuple(constraint_variables))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/search_chemical')
def search_chemical_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    cas = data['cas']
    sample_type = data['type']
    assay = data['assay']
    toxicity = data['toxicity']
    smiles = data['smiles']

    constraint_sample = []
    constraint_assay = []
    constraint_chemical = []
    constraint_variables = []        
    if cas != '':
        constraint_chemical.append('cas = %s')
        constraint_variables.append(cas)
    if smiles != '':
        constraint_chemical.append('canonical_smiles = %s')
        constraint_variables.append(smiles)
    if sample_type != '':
        constraint_sample.append('sample_type = %s')
        constraint_variables.append(sample_type)
    if assay != '':
        constraint_assay.append('assay_name = %s')
        constraint_variables.append(assay)
    if toxicity != '':
        constraint_assay.append('toxicity = %s')
        constraint_variables.append(toxicity)

    query = 'SELECT DISTINCT c.chemical_id, c.chemical_name, c.molecular_formula, c.CAS FROM ( SELECT * FROM chemical'
    if len(constraint_chemical) > 0:
        query += ' WHERE ' + ' AND '.join(constraint_chemical)
    query += ') AS c INNER JOIN sample_chemical ON c.chemical_id = sample_chemical.chemical_id INNER JOIN ( SELECT * FROM sample'
    if len(constraint_sample) > 0:
        query += ' WHERE ' + ' AND '.join(constraint_sample)
    query += ') AS s ON sample_chemical.sample_id = s.sample_id INNER JOIN chemical_assay ON c.chemical_id = chemical_assay.chemical_id INNER JOIN ( SELECT * FROM assay'
    if len(constraint_assay) > 0:
        query += ' WHERE ' + ' AND '.join(constraint_assay)
    query += ') AS a ON chemical_assay.assay_id = a.assay_id;'
    db.execute(query, tuple(constraint_variables))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/sample_detail')
def sample_detail_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM sample WHERE sample_id = %s;', (data['sample_id'], ))
    row = db.fetchone()
    return json.dumps(row, default=datetime_handler)

@app.post('/sample_assay')
def sample_assay_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM sample_assay WHERE sample_id = %s;', (data['sample_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)    

@app.post('/sample_chemical')
def sample_chemical_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM sample_chemical WHERE sample_id = %s;', (data['sample_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/sample_chemical_component')
def sample_chemical_component_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM sample_chemical JOIN (SELECT component_id, chemical_id FROM component_chemical) AS a USING(chemical_id) WHERE sample_id = %s;', (data['sample_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/chemical_detail')
def chemical_detail_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM chemical WHERE chemical_id = %s;', (data['chemical_id'], ))
    row = db.fetchone()
    return json.dumps(row, default=datetime_handler)

@app.post('/chemical_assay')
def chemical_assay_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM chemical_assay WHERE chemical_id = %s;', (data['chemical_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/chemical_sample')
def chemical_sample_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM sample_chemical WHERE chemical_id = %s;', (data['chemical_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/assay_detail')
def assay_detail_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM assay WHERE assay_id = %s;', (data['assay_id'], ))
    row = db.fetchone()
    return json.dumps(row, default=datetime_handler)

@app.post('/assay_chemical')
def assay_chemical_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM chemical_assay WHERE assay_id = %s;', (data['assay_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/assay_component')
def assay_component_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM component_assay WHERE assay_id = %s;', (data['assay_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

@app.post('/assay_sample')
def assay_sample_handler(db):
    response.headers['Content-Type'] = 'application/json'
    try:
        data = request.json
    except HTTPError as e:
        response.status = 400
        return {'error': 'HTTP Error'}

    if data is None:
        response.status = 400
        return {'error': 'empty request body'}

    db.execute('SELECT * FROM sample_assay WHERE assay_id = %s;', (data['assay_id'], ))
    rows = db.fetchall()
    return json.dumps(rows, default=datetime_handler)

    # start_time: start_time,
    #         end_time: end_time,
    #         type: type,
    #         assay: assay,
    #         toxicity: toxicity,
    #         cas: cas

    # try:
    #     current_hand = HandPoker.from_dict(data['current_hand'])
    #     to_place_pokers = set(data['to_place_pokers'])
    #     usable_pokers = set(data['usable_pokers'])
    #     time_limit = float(data['time_limit'])
    #     round_id = data['round_id']
    #     if 'client_version' not in data:  # no client version should be developer test call
    #         data['client_version'] = 'none'
    # except TypeError as e:
    #     logger.error(f'TypeError: {e.args}')
    #     response.status = 400
    #     return {'error': 'incorrect parameters'}
    # except KeyError as e:
    #     logger.error(f'Missing Key: {e.args}')
    #     response.status = 400
    #     return {'error': 'incorrect parameters'}
    # except HandPokerException:
    #     logger.error(f'Error parsing current hand: {data["current_hand"]}')
    #     response.status = 400
    #     return {'error': 'incorrect parameters'}

    # new_hand = poker_agent.plan(current_hand, to_place_pokers, usable_pokers, time_limit)
    # response_dict = new_hand.to_dict()

    # if len(to_place_pokers) == 5:  # 新的一轮
    #     response_dict['round_id'] = str(uuid.uuid4())
    # else:
    #     response_dict['round_id'] = round_id

    # logger.info(f'Input: {data}, Output: {response_dict}')
    # return json.dumps(response_dict)


# @app.post('/send_error_report')
# def send_error_report_handler():
#     logger = logging.getLogger('error_report')
#     response.headers['Content-Type'] = 'application/json'
#     try:
#         data = request.json
#     except HTTPError as e:
#         response.status = 400
#         return {'error': 'HTTP Error'}

#     if data is None:
#         response.status = 400
#         return {'error': 'empty request body'}

#     # token verification
#     if 'token' not in data:
#         response.status = 400
#         return {'error': 'empty token'}
#     try:
#         jwt.decode(data['token'], JWT_SECRET, algorithms=['HS256'])
#     except jwt.ExpiredSignatureError:
#         response.status = 400
#         return {'error': 'token expired'}
#     except (jwt.InvalidTokenError, jwt.DecodeError, jwt.InvalidSignatureError):
#         response.status = 400
#         return {'error': 'invalid token'}

#     if 'machine_id' not in data or 'error' not in data:
#         response.status = 400
#         return {'error': 'empty machine id or empty error'}

#     logger.error(f'{data["machine_id"]}: {data["error"]}')
#     return {'success': 1}


# ### Licensing ###

# @app.get('/serial_generator')
# def serial_generator_handler(db):
#     if 'pass' not in request.query or request.query['pass'] != DB_SECRET:
#         response.status = 400
#         return
#     count = int(request.query.get('count', 1))  # support bulk generate
#     result = ""
#     for _ in range(count):
#         db.execute('INSERT INTO license (created_on) VALUES (current_timestamp) RETURNING serial_id;')
#         row = db.fetchone()
#         if row:
#             result += row['serial_id']
#             result += '<br>'
#     return result


# @app.get('/serial_list')
# def serial_list_handler(db):
#     if 'pass' not in request.query or request.query['pass'] != DB_SECRET:
#         response.status = 400
#         return
#     db.execute('SELECT * FROM license;')
#     rows = db.fetchall()
#     if rows:
#         return str(rows)


# @app.get('/register_serial')
# def register_serial_handler(db):
#     response.headers['Content-Type'] = 'application/json'
#     if 'serial_id' not in request.query or 'machine_id' not in request.query or 'client_version' not in request.query:
#         response.status = 400
#         return {'error': 'incorrect parameters'}
#     try:
#         db.execute('SELECT machine_id FROM license WHERE serial_id = %s;', (request.query['serial_id'],))
#         row = db.fetchone()
#         if row:
#             if row['machine_id'] is not None:  # already registered
#                 response.status = 400
#                 return {'error': 'already registered'}
#         else:
#             response.status = 400
#             return {'error': 'invalid serial number'}
#     except psycopg2.DataError:
#             response.status = 400
#             return {'error': 'invalid serial number'}

#     try:
#         db.execute(
#             'UPDATE license SET machine_id = %s, verified_on=current_timestamp, client_version = %s WHERE serial_id = %s;',
#             (request.query['machine_id'], request.query['client_version'], request.query['serial_id'],)
#         )
#         if db.rowcount == 1:
#             return {'success': 1}
#         else:
#             response.status = 500
#             return {'error': 'internal database error'}
#     except psycopg2.DataError:
#             response.status = 500
#             return {'error': 'internal database error'}
#     response.status = 500
#     return {'error': 'internal database error'}


# @app.get('/verify_machine')
# def verify_machine_handler(db):
#     """
#     Verify machine, if success, return access token.
#     """
#     response.headers['Content-Type'] = 'application/json'
#     if 'machine_id' not in request.query:
#         response.status = 400
#         return {'error': 'empty machine_id'}
#     try:
#         db.execute('SELECT serial_id FROM license WHERE machine_id = %s;', (request.query['machine_id'],))
#         row = db.fetchone()
#         if row:
#             return json.dumps({
#                 'token': jwt.encode({'exp': datetime.utcnow() + timedelta(hours=10)}, JWT_SECRET, algorithm='HS256').decode(
#                     'utf-8')
#             })
#         else:
#             response.status = 400
#             return {'error': 'invalid machine_id'}
#     except psycopg2.DataError:
#             response.status = 400
#             return {'error': 'invalid machine_id'}
#     response.status = 400
#     return {'error': 'invalid machine_id'}


if __name__ == '__main__':
    # run(app, host='localhost', port=8080, debug=True, reloader=True)
    run(app, server='auto', host='localhost', port=8080)