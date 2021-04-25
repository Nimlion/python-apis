from flask import Flask, request, jsonify
import sqlalchemy as db

app = Flask(__name__)

# database setup
engine = db.create_engine('mysql://user:password@localhost/database')
connection = engine.connect()
metadata = db.MetaData()
table = db.Table('jongere', metadata, autoload=True, autoload_with=engine)


# GET request that selects all rows from the table
# Followed by returning all rows one by one in json
@app.route('/', methods=['GET'])
def query_records():
    proxy = connection.execute(db.select([table]))
    result = proxy.fetchall()
    return jsonify({'result': [dict(row) for row in result]})


# PUT request to update a record in the table
# Starts by retrieving the id from the arguments in the URL
# Checks if the id isn't empty
# Then gets the body and checks if all values are present
# Lastly it executes the update query on the id
@app.route('/', methods=['PUT'])
def update_record():
    rec_id = request.args.get('id')
    if rec_id is None:
        return jsonify({"error": "please provide a id"})
    record = request.json
    if 'achternaam' not in record or 'inschrijfdatum' not in record or 'jongerecode' not in record or \
            'roepnaam' not in record or 'tussenvoegsel' not in record:
        return jsonify({"error": "please provide all values"})
    query = db.update(table).values(record).where(table.columns.jongerecode == rec_id)
    connection.execute(query)
    return jsonify({"status": "successfully updated record"})


# POST request that places a new record into the table
# Starting with getting the body and checking if all values are present
# Then it executes the insert query
@app.route('/', methods=['POST'])
def create_record():
    record = request.json
    if 'achternaam' not in record or 'inschrijfdatum' not in record or 'jongerecode' not in record or \
            'roepnaam' not in record or 'tussenvoegsel' not in record:
        return jsonify({"error": "please provide all values"})
    query = db.insert(table)
    connection.execute(query, [record])
    return jsonify({"status": "successfully added new record"})


# DELETE request that deletes a record from the table
# Starts by retrieving the id from the arguments in the URL
# And then executes the delete query on all records with the id
@app.route('/', methods=['DELETE'])
def del_record():
    rec_id = request.args.get('id')
    if rec_id is None:
        return jsonify({"error": "please provide a id"})
    query = db.delete(table).where(table.columns.jongerecode == rec_id)
    connection.execute(query)
    return jsonify({"status": "successfully deleted record"})


app.run(debug=True)
