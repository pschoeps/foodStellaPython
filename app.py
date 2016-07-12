
from flask import Flask, request
from flask_restful import Resource, Api

import re
import math
import json
import string
import numpy as np
from sklearn.preprocessing import normalize
from difflib import SequenceMatcher
import nltk


ingredientsfile = open("recipe_ingredients.json", "r")

class Parse_Data(Resource):
    def get(self):
        return request.args.get('username')

app = Flask(__name__)
api = Api(app)

api.add_resource(Parse_Data, '/parse')



if __name__ == '__main__':
    app.run(debug=True)