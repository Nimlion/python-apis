from flask import Flask, request, jsonify

app = Flask(__name__)

personal_db = [{'name': 'Jamie', 'email': 'Jamie.Oliver@outlook.com'},
               {'name': 'John', 'email': 'John.Travolta@outlook.com'},
               {'name': 'Bloomberg', 'email': 'Mr.Bloomberg@outlook.com'},
               {'name': 'Mike', 'email': 'Mike.Tyson@outlook.com'},
               {'name': 'Tony', 'email': 'Tony.Stark@outlook.com'},
               {'name': 'Thor', 'email': 'Thor.Oddison@outlook.com'},
               {'name': 'Donald', 'email': 'Donald.Duck@outlook.com'}]


@app.route('/', methods=['GET'])
def query_records():
    if request.json is None:
        return jsonify({"status": "ID couldn't be found"})
    rec_id = request.json.get('id')
    if rec_id >= len(personal_db) or rec_id < -abs(len(personal_db)):
        return jsonify({"status": "ID out of range"})
    return jsonify(personal_db[rec_id])


@app.route('/', methods=['PUT'])
def update_record():
    rec_id = int(request.args.get('id'))
    if rec_id is None:
        return jsonify({"error": "please provide a id"})
    if rec_id >= len(personal_db) or rec_id < -abs(len(personal_db)):
        return jsonify({"status": "ID out of range"})
    record = request.json
    if 'name' not in record:
        return jsonify({"error": "please provide a name"})
    if 'email' not in record:
        return jsonify({"error": "please provide a email"})
    personal_db[rec_id] = record
    return jsonify(personal_db)


@app.route('/', methods=['POST'])
def create_record():
    record = request.json
    if 'name' not in record:
        return jsonify({"error": "please provide a name"})
    if 'email' not in record:
        return jsonify({"error": "please provide a email"})
    personal_db.append(record)
    return jsonify(personal_db)


@app.route('/', methods=['DELETE'])
def del_record():
    rec_id = int(request.args.get('id'))
    if rec_id is None:
        return jsonify({"error": "please provide a id"})
    if rec_id >= len(personal_db) or rec_id < -abs(len(personal_db)):
        return jsonify({"status": "ID out of range"})
    del personal_db[rec_id]
    return jsonify(personal_db)


app.run(debug=True)
