from flask import Flask, request, jsonify
from peewee import *
from seed import *
from models import *
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
