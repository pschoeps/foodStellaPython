
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
import urlparse




ingredientsfile = open("recipe_ingredients.json", "r")

class Search(Resource):
    def get(self):
		search_array = []

		output_file = open("search_output.txt", "r")
		for line in output_file:
			x = int(line)
			search_array.append(x)
		output_file.close()

		return search_array

class Recommend(Resource):
	def get(self):
		#recipe = request.args.get('recipe')
		#file = open("recommender_input.txt", "w")
		#file.write(recipe)
		#file.close()
		#import recommender.py

		recommended_array = []

		output_file = open("recommender_output.txt", "r")
		for line in output_file:
			x = int(line)
			recommended_array.append(x)
		output_file.close()

		return recommended_array



app = Flask(__name__)
api = Api(app)

api.add_resource(Search, '/search')
api.add_resource(Recommend, '/recommend')



if __name__ == '__main__':
    app.run(debug=True)