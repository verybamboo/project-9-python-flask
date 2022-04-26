from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('dinosaurs', user="verybamboo",
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Dinosaur(BaseModel):
    name = CharField()
    diet = CharField()
    length = CharField()
    weight = CharField()


db.connect()
db.drop_tables([Dinosaur])
db.create_tables([Dinosaur])

Dinosaur(name='Tyrannosaurus-Rex', diet='Carnivore',
         length='12.4 Meters', weight='8.4 Metric Tons').save()
Dinosaur(name='Allosaurus', diet='Carnivore',
         length='9.7 Meters', weight='2.5 Metric Tons').save()
Dinosaur(name='Triceratops', diet='Herbivore',
         length='8 Meters', weight='9 Metric Tons').save()
Dinosaur(name='Shantungosaurus', diet='Herbivore',
         length='14.7 Meters', weight='16 Metric Tons').save()
Dinosaur(name='Stegosaurus', diet='Herbivore',
         length='9 Meters', weight='7 Metric Tons').save()
Dinosaur(name='Dreadnoughtus', diet='Herbivore',
         length='26 Meters', weight='49 Metric Tons').save()
Dinosaur(name='Apatosaurus', diet='Herbivore',
         length='23 Meters', weight='45 Metric Tons').save()


app = Flask(__name__)


@app.route('/dinosaur/', methods=['GET', 'POST'])
@app.route('/dinosaur/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Dinosaur.get(Dinosaur.id == id)))
        else:
            dinosaurList = []
            for dinosaur in Dinosaur.select():
                dinosaurList.append(model_to_dict(dinosaur))
            return jsonify(dinosaurList)

    if request.method == 'PUT':
        return 'PUT request'

    if request.method == 'POST':
        new_dinosaur = dict_to_model(Dinosaur, request.get_json())
        new_dinosaur.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        return 'DELETE request'

    app.run(debug=True)
