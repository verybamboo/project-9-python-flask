from flask import Flask, request, jsonify
from peewee import *
from seed import *
from models import *
from playhouse.shortcuts import model_to_dict, dict_to_model

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def root_api():
    return "This is the root, type in any dinosaur names as the endpoints to see their information or /dinosaur for all dinosaurs."


@app.route('/dinosaur/', methods=['GET', 'POST'])
@app.route('/dinosaur/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Dinosaur.get(Dinosaur.id == id)))
        else:
            dinosaur_list = []
            for dinosaur in Dinosaur.select():
                dinosaur_list.append(model_to_dict(dinosaur))
            return jsonify(dinosaur_list)

    if request.method == 'PUT':
        body = request.get_json()
        Dinosaur.update(body).where(Dinosaur.id == id).execute()
        return "Dinosaur " + str(id) + " has been updated."

    if request.method == 'POST':
        new_dinosaur = dict_to_model(Dinosaur, request.get_json())
        new_dinosaur.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Dinosaur.delete().where(Dinosaur.id == id).execute()
        return "Dinosaur " + str(id) + " deleted."


app.run(debug=True)
