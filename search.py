import re
from scipy import spatial
import csv
import nltk
import numpy as np
import itertools
from sklearn.preprocessing import normalize
from difflib import SequenceMatcher


## INPUT INFORMATION ##
## INPUT FILE IS "search_dv.txt" and "search_input.txt"
## search_input.txt must have all words on one line, seperated by single spaces

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def cosine_similarity(arr1, arr2):
	return 1 - spatial.distance.cosine(arr1, arr2)


file = open("search_dv.txt", "r")


raw_description_vectors = []

for line in file:
	newline = line.strip(' ').strip('\n').split(' ')
	#print newline
	raw_description_vectors.append(newline[:-1])
#print raw_description_vectors
description_vectors = []
for line in raw_description_vectors:
	description_vectors.append(map(float, line))

#output the recipe_id and recipe names of the most similar recipes
file.close()


#print matrix

def extract_nouns(line):
    tokens = nltk.word_tokenize(line)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word,pos in tagged         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == '')]
    downcased = [x.lower() for x in nouns]
    joined = " ".join(downcased).encode('utf-8')
    return joined


# recipesjson = open("recipes.json", "r")
# meal_types_names = []
# meal_type_vector = []
# recipe_names = []
# recipe_name_list = []
# recipe_nouns_list = []
# recipe_nouns = []
# for line in recipesjson:
# 	matchObj = re.match(r'.*\"recipe_name\": \"([^\"]*)\".*', line)
# 	if matchObj:
# 		recipe_names.append(matchObj.group(1))
# 		#print matchObj.group(1)
# 		noun_list =  extract_nouns(matchObj.group(1))
# 		for word in noun_list.split(' '):
# 			if word not in recipe_nouns_list:
# 				recipe_nouns_list.append(word)
# 		current_nouns = noun_list.split(' ')
# 		recipe_nouns.append(current_nouns)
# 		if matchObj.group(1).split(' ')[-1] not in recipe_name_list:
# 			recipe_name_list.append(matchObj.group(1).split(' ')[-1])
# 	matchObj2 = re.match(r'.*\"meal_type\": \"([^\"]*)\".*', line)
# 	if matchObj2:
# 		if matchObj2.group(1) not in meal_types_names:
# 			meal_types_names.append(matchObj2.group(1))
# 		meal_type_vector.append(matchObj2.group(1))



# recipe_nouns_matrix = np.zeros((len(mass_fractions_matrix), len(recipe_nouns_list)))
# for i,l in enumerate(recipe_nouns):
# 	for j,k in enumerate(recipe_nouns_list):
# 		for m in l:
# 			if m == k:
# 				recipe_nouns_matrix[i, j] = 0.3



names = open("ingredient_frequencies.txt", "r")

ingredients = []
for line in names:
	newline = line.strip('\n')
	ingredients.append(newline)
#print(len(recipe_nouns_list))
#print (len(ingredients))

recipe_nouns_list = open("names.txt", "r")



for i in recipe_nouns_list:
	j = i.strip('\n')
	ingredients.append(j)


#print(len(ingredients))
#description_vectors = np.column_stack((mass_fractions_matrix, recipe_nouns_matrix))





















#for i,j in enumerate(recipe_names):
#	print i, j





user_query = np.zeros((len(ingredients)))
#print user_query
y = []
file = open("search_input.txt", "r")


for line in file:
	y.extend(line.strip('\n').strip(' ').split(' '))

file.close()


#y = str(x).strip('\n').split(' ')
for cur_ingred in y:
	count = 0
	for i,j in enumerate(ingredients):
		cur_similar = similar(cur_ingred, j)
		if cur_similar > 0.75:
			user_query[i] = 1
			count= count + 1
			#print (cur_ingred, "matched with", ingredients[i])
	#if count == 0:
	#	print (cur_ingred, "did not match with anything")

#print ingredients
#print len(ingredients)

cosine_distances = []

for j,i in enumerate(description_vectors):
	cosine_distances.append(cosine_similarity(map(float, user_query), map(float, i)))
	#print cosine_similarity(map(float, mass_fractions_matrix[0]), map(float, i))

cosine_distances = np.asarray(cosine_distances)
order = cosine_distances.argsort()
file = open("search_output.txt", "w")
for i in order[-11:][::-1][1:]:
	file.write(str(i))
	file.write('\n')

file.close()
	#print recipe_names[i]+ ": Meal Type: " + meal_type_vector[i]
	#ingr_list = []
	# for k,j in enumerate(description_vectors[i,]):
	# 	if j > 0:
	# 		ingr_list.append(ingredients[k])
	# print ingr_list
	#print ingredients[matrix[i,] > 0]
	#print recipe_nouns[i]
	#print cosine_similarity(map(float, user_query), map(float, description_vectors[i]))

