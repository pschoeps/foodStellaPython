import re
from scipy import spatial
import csv
import nltk
import numpy as np
import itertools



def cosine_similarity(arr1, arr2):
	return 1 - spatial.distance.cosine(arr1, arr2)

file = open("recommender_input.txt", "r")


for line in file:
	x = int(line)

#print x
file.close()

file = open("recommender_dv.txt", "r")


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
cosine_distances = []

for j,i in enumerate(description_vectors):
	cosine_distances.append(cosine_similarity(map(float, description_vectors[x-1]), map(float, i)))
	#print cosine_similarity(map(float, mass_fractions_matrix[0]), map(float, i))

cosine_distances = np.asarray(cosine_distances)
order = cosine_distances.argsort()

file = open("recommender_output.txt", "w")
for i in order[-11:][::-1][1:]:
	file.write(str(i+1))
	file.write('\n')
	#print cosine_similarity(map(float, description_vectors[x-1]), map(float, description_vectors[i]))
file.close()