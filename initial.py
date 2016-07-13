import re
import math
import json
import string
import numpy as np
from sklearn.preprocessing import normalize
from difflib import SequenceMatcher
import nltk


##### PART 1 ##########


ingredientsfile = open("recipe_ingredients.json", "r")
file = open("recipe_ingredients_parsed_with_units.json", "w")

conversions = {'ounce': 1, 'pound': 16, 'cup': 8, 'tablespoon': 0.5, 'teaspoon': 0.16666}

counter = 0
for line in ingredientsfile:
	matchObj = re.match( r'.*\"quantity\": \"([^\"]*)\".*', line)
	if matchObj:
		quantitywithingredient = matchObj.group(1)
		matchObj2 = re.match( r'([\s*|\/*|.|[0-9]*]*)(.*)', quantitywithingredient)
		if matchObj2:
			numbers = matchObj2.group(1)
			numbers=numbers.strip()
			initial_numbers_list = numbers.split(' ')
			numbers_list = []
			for i in initial_numbers_list:
				if i != "":
					numbers_list.append(i)
			if len(numbers_list) == 1:
				if "/" in numbers_list[0]:
					fraction = numbers_list[0].split('/')
					amount = float(fraction[0]) / float(fraction[1])
				else:
					amount = float(numbers_list[0])
			elif len(numbers_list) == 2:
				if "/" in numbers_list[0]:
					amount_f = numbers_list[0].split('/')
					amount = float(amount_f[0])/float(amount_f[1])
					amount = amount * float(numbers_list[1])
				elif "/" in numbers_list[1]:
					amount = float(numbers_list[0])
					additional_f = numbers_list[1].split('/')
					additional = float(additional_f[0])/float(additional_f[1])
					amount = amount + additional
				else:
					amount = float(numbers_list[0]) * float(numbers_list[1])
			elif len(numbers_list) == 3:
				if "/" in numbers_list[0]:
					first_fraction = numbers_list[0].split('/')
					amount = float(first_fraction[0])/float(first_fraction[1])
				else:
					amount = float(numbers_list[0])
				additional = float(numbers_list[1])
				fraction = numbers_list[2].split('/')
				additional = additional + float(fraction[0])/float(fraction[1])
				amount = amount * additional
			else:
				amount = float(numbers_list[0])*(float(numbers_list[1]) + float(numbers_list[1]) + float(numbers_list[2]))

			amount = round(amount, 2)
			amount_integer = int(math.floor(amount))
			amount_decimal = (amount - math.floor(amount))
			amount_decimal = round(amount_decimal, 2)

			amount_string = ""
			if amount_integer != 0:
				amount_string += str(amount_integer)

			#To convert back into fractions, I first consider all common fractions like 1/2, 1/4, 1/3, 2/3, 1/8, etc
			if amount_decimal == 0.5:
				amount_string += " 1/2"
			elif amount_decimal == 0.25:
				amount_string += " 1/4"
			elif amount_decimal == 0.75:
				amount_string += " 3/4"
			elif amount_decimal == 0:
				amount_string = amount_string
			elif amount_decimal == 0.33 or amount_decimal == 0.34:
				amount_string += " 1/3"
			elif amount_decimal == 0.13 or amount_decimal == 0.12:
				amount_string += " 1/8"
			elif amount_decimal == 0.37 or amount_decimal == 0.38:
				amount_string += " 3/8"
			elif amount_decimal == 0.62 or amount_decimal == 0.63:
				amount_string += " 5/8"
			elif amount_decimal == 0.87 or amount_decimal == 0.88:
				amount_string += " 7/8"
			elif amount_decimal == 0.66 or amount_decimal == 0.67:
				amount_string += " 2/3"
			else:
				#The remaining cases will come from odd cases such as 
				#"1/2 17.3 ounce package frozen puff pastry sheets (1 sheet), thawed" - decimal ends in 0.65.
				#In this case, I just leave it as a decimal. I think this is more user-friendly for these specific cases.
				amount_string = str(amount)
				

			amount_string = amount_string.strip(' ')
			replacewith = "\"quantity\": \"" + amount_string + "\", " + "\"unit\": \"" + matchObj2.group(2) + "\""
			num = re.sub(r'\"quantity\": \"[^\"]*\"', replacewith, line)
			
			unit_assignment = "NA"

			unit_words = matchObj2.group(2).split(' ')
			for word in unit_words:
				if "ounce" in word or "oz" in word:
					unit_assignment = "ounce"
					break
				if "pound" in word or "lb" in word:
					unit_assignment = "pound"
					break
				if "cup" in word:
					unit_assignment = "cup"
					break
				if "tablespoon" in word or "tbsp" in word:
					unit_assignment = "tablespoon"
					break
				if "teaspoon" in word or "tsp" in word:
					unit_assignment = "teaspoon"

			if unit_assignment != "NA":
				multiplier = conversions[unit_assignment]
				number_of_ounces = multiplier * amount
				num = re.sub(r'}', ", \"ounces\": \"" + str(number_of_ounces) + "\"}", num)
				#Suggestion: At this point, I think it would be good to change the "unit" element in the database to
				#the unit_assignment variable. This will clean up the database considerably
			else:
				#In this case, the unit did not have measurement. Example: "1 Egg", or "2 medium carrots". In this
				#case, just let "ounces" equal the amount, so that when we add them together in the shopping list,
				#the amounts will be added correctly. 
				num = re.sub(r'}', ", \"ounces\": \"" + str(amount) + "\"}", num)
			print (num)
			file.write(num)
		else:
			print "error: no second match"
	else:
		if counter == 0:
			file.write("[\n")
			counter = 1
		else:
			file.write("]\n")

file.close()


### PART 2 #####















quant_list = list()
other_words = list()

with open('quantities.txt','r') as fquant:
   read_data = fquant.read().strip()
   for word in read_data.split():
      quant_list.append("^[0-9]+.*" + word)
      other_words.append(word)

fquant.close()


with open('other_words.txt','r') as other:
   read_data = other.read().strip()
   for word in read_data.split():
	other_words.append(word)

other.close()

quant_regex =  "s*|".join(quant_list)
quant_regex = "(" + quant_regex + "s*|^[0-9]+\s)"
quant_regex_sub = quant_regex + "s*|^[0-9]+"


file = open("recipe_ingredients_trimmed.json", "w")
ingredientsjson = open("recipe_ingredients_parsed_with_units.json", "r")
counter = 0
for line in ingredientsjson:
	matchObj = re.match(r'.*\"detail\": \"([^\"]*)\".*', line)
	if matchObj:
		#print matchObj.group(1)

		detail_without_parentheses = re.sub(r'\([^)]*\)', "", matchObj.group(1))
		#print detail_without_parentheses
		detail_words = detail_without_parentheses.split(' ')
		real_detail_words = []
		for i in detail_words:
			if i != "":
				real_detail_words.append(i)

		new_detail = ""
		for i in real_detail_words:
			new_detail += i + ' '

		#print new_detail
		new_detail = new_detail.strip(' ')

		replacewith = "\"detail\": \"" + new_detail + "\""

		num = re.sub(r'\"detail\": \"[^\"]*\"', replacewith, line)
		# print num
		# file.write(num)




		if re.search(quant_regex,new_detail) != None:
		   m = re.match(quant_regex, new_detail)
		   quantity = m.group(0)
		   ingredient = re.sub(re.escape(quantity),'',new_detail)

		   #Remove other descriptive words from ingredient
		   for word in other_words:
			wordregex = re.compile(r'\b%s\b' % re.escape(word))
			ingredient = re.sub(wordregex,'',ingredient)
		   ingredient = re.sub(r',\s*$','',ingredient)
		   ingredient = ingredient.strip()


		replacewith = "\"ingredient\": \"" + ingredient + "\""

		num = re.sub(r'\"ingredient\": \"[^\"]*\"', replacewith, num)
		file.write(num)



	else:
		if counter == 0:
			file.write("[\n")
			counter = 1
		else:
			file.write("]\n")
file.close()









##### PART 3 ######

















ingredientsjson = open("recipe_ingredients_trimmed.json", "r")
file = open("recipe_ingredients_6_3_16.json", "w")

counter = 0
#edwords = []
#lywords = []
for line in ingredientsjson:
	matchObj = re.match(r'.*\"ingredient\": \"([^\"]*)\".*', line)
	if matchObj:
		#first remove all hyphens
		ingredient = re.sub(r'-', " ", matchObj.group(1))
		#remove beginning commas and spaces
		ingredient = re.sub(r'^,[ |,]*', "", ingredient)
		#if there is an "or", choose the first one
		#remove everything after "with"
		ingredient = re.sub(r' or .*', "", ingredient)
		ingredient = re.sub(r' with .*', "", ingredient)
		#remove the last comma and everything following it
		ingredient = re.sub(r',[^,]*$', "", ingredient)
		#remove any spaces and commas at the end
		ingredient = re.sub(r',[ |,]*$', "", ingredient)
		#remove non-whitespace, non-alphabet characters like "%", "$", etc
		ingredient = re.sub(r'[^A-Za-z_\s]', "", ingredient)
		#remove all extra white spaces on the ends

		ingredient = ingredient.strip(' ')

		real_ingredient_words = []
		for word in ingredient.split(' '):
			if word != "":
				real_ingredient_words.append(word)

		final_ingredient = ""
		for word in real_ingredient_words:
			final_ingredient += word + " "

		final_ingredient = final_ingredient.strip(' ')

		replacewith = "\"ingredient\": \"" + final_ingredient + "\""

		num = re.sub(r'\"ingredient\": \"[^\"]*\"', replacewith, line)
		file.write(num)

		#matchObj2 = re.match(r'.*[ |^](.*)ed[,| |$].*', ingredient)
		#if matchObj2:
	#		if matchObj2.group(1) not in edwords:
		#		edwords.append(matchObj2.group(1))
		#matchObj3 = re.match(r'.*[ |^](.*)ly[,| |$].*', ingredient)
		#if matchObj3:
		#	if matchObj3.group(1) not in lywords:
		#		lywords.append(matchObj3.group(1))

	else:
		if counter == 0:
			file.write("[\n")
			counter = 1
		else:
			file.write("]\n")

file.close()

#for word in edwords:
#	print word + "ed"

#for word in lywords:
#	print word + "ly"
#list of words to also remove:
#en, can, dried, dry, salted, unsalted, a lot of words ending in "ed" and "ly", e.g. studded, coarsely, fine, soft
#drained, cubed 












#### PART 4 #####





def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

ingredientsjson = open("recipe_ingredients_6_3_16.json", "r")

file = open("ingredient_frequencies.txt", "w")
ingredients_list = []

for line in ingredientsjson:
	matchObj = re.match(r'.*\"ingredient\": \"([^\"]*)\".*', line)
	if matchObj:
		if matchObj.group(1).split(' ')[-1] not in ingredients_list:
			ingredients_list.append(str(matchObj.group(1).split(' ')[-1]))

ingredientsjson.seek(0)





vector = np.zeros(len(ingredients_list))


for line in ingredientsjson:
	matchObj = re.match(r'.*\"ingredient\": \"([^\"]*)\".*', line)
	if matchObj:
		matchObj2 = re.match(r'.*\"ounces\": \"([^\"]*)\".*', line)
		if matchObj2:
			for i,j in enumerate(ingredients_list):
				if j == matchObj.group(1).split(' ')[-1]:
					vector[i] += 1

ingredients_list = np.asarray(ingredients_list)
vector = np.asarray(vector)
vector = vector.astype(int)
order = vector.argsort()

matrix = np.column_stack((vector, ingredients_list))




matrix = matrix[order]
matrix = list(matrix)
#print len(matrix)

def combine_ingredients(matrix, threshold):
	similarities = {}

	total = 0
	matched = 0

	matched_ingredients = []

	for i in range(0, len(matrix)):
			total += 1
			maxsim = threshold
			maxindex = -1
			for j in range(i+1, len(matrix)):
				if j != i:
					cursim = float(similar(matrix[i][1], matrix[j][1]))
					if cursim > float(maxsim):
						maxsim = cursim
						maxindex = j
			if maxindex != -1:
				matched += 1
				similarities[matrix[i][1]] = matrix[maxindex][1]
				matrix[maxindex][0] = str(int(matrix[i][0]) + int(matrix[maxindex][0]))
				matched_ingredients.append(i)


	output = []
	for i,j in enumerate(matrix):
		if i not in matched_ingredients:
			output.append(j)

	
	instances = []
	for i in output:
		instances.append(i[0])
	instances = np.asarray(instances)
	instances = instances.astype(int)
	order = np.argsort(instances)

	final_output = []
	for i in order:
		final_output.append(output[i])

	return final_output, similarities

#print len(matrix)
matrix, similarities = combine_ingredients(matrix, 0.75)

print similarities

#print len(matrix)
#print similarities

for i in matrix:
	file.write(i[0])
	file.write(' ')
	file.write(i[1])
	file.write("\n")

file.close()
#matrix contains the ingredients in the second column and the number of times that ingredient appears
#in the first column. It is sorted in ascending order by the first column.
ingredientsjson.seek(0)


file = open("recipe_ingredients_6_7_16.json", "w")
counter = 0
for line in ingredientsjson:
	matchObj = re.match(r'.*\"ingredient\": \"([^\"]*)\".*', line)
	if matchObj:
		last_word = matchObj.group(1).split(' ')[-1]
		if last_word in similarities:
			last_word = similarities[last_word]
		num = re.sub(r', \"ounces\"', ', \"abbreviated\": \"' + last_word + '\", \"ounces\"', line)
		file.write(num)
	else:
		if counter == 0:
			file.write('[\n')
			counter = 1
		else:
			file.write(']\n')

file.close()
ingredientsjson.seek(0)

#go through recipe ingredients and create mass fractions vector for each recipe
#ask in email for ideas to standardize more: list of categories, list of ingredients in each category
#combine as much as possible and then ignore ingredients that only appear in one recipe
#the following is a preliminary mass fractions matrix

#first generate list of recipe_id's


ingredients_list = list(ingredients_list)

recipe_ids = []

for line in ingredientsjson:
	matchObj = re.match(r'.*\"recipe_id\": ([^,]*),.*', line)
	if matchObj:
		if matchObj.group(1) not in recipe_ids:
			recipe_ids.append(matchObj.group(1))

ingredientsjson.seek(0)

print recipe_ids

mass_fractions_matrix = np.zeros((len(recipe_ids), len(matrix)))
counter = 0
for line in ingredientsjson:
		matchObj = re.match(r'.*\"ingredient\": \"([^\"]*)\".*', line)
		matchObj2 = re.match(r'.*\"ounces\": \"([^\"]*)\".*', line)
		matchObj3 = re.match(r'.*\"recipe_id\": ([^,]*),.*', line)

		if matchObj:
			if int(matchObj3.group(1)) > 335 and int(matchObj3.group(1)) <= 339:
				counter = 1
			if counter == 1:
				print line
				print matchObj.group(1)
				print matchObj2.group(1)
				print matchObj3.group(1)
			#i = ingredients_list.index(str(matchObj.group(1).split(' ')[-1]))
			for i,j in enumerate(matrix):
				last_word = matchObj.group(1).split(' ')[-1]
				if last_word in similarities:
					last_word = similarities[last_word]
				if j[1] == last_word:
					number_of_ounces = matchObj2.group(1)
					print matchObj3.group(1)
					for k,l in enumerate(recipe_ids):
						if int(l) == int(matchObj3.group(1)):
							if k == 336:
								print k
							mass_fractions_matrix[k, i] += float(number_of_ounces)

#real_mass_fractions_matrix = []


#for i in mass_fractions_matrix:
#	real_mass_fractions_matrix.append(normalize(i, norm='l1'))

#real_mass_fractions_matrix = np.reshape(real_mass_fractions_matrix, (len(recipe_ids), len(ingredients_list)))

mass_fractions_matrix = normalize(mass_fractions_matrix, norm='l1')

#mass_fractions_matrix.tofile("mass_fractions_matrix.txt", sep = " ")


np.savetxt("mass_fractions_matrix.txt", mass_fractions_matrix)
#for i in mass_fractions_matrix:
	#print i

print mass_fractions_matrix[336]
print mass_fractions_matrix[333]

recipe_ids = np.asarray(recipe_ids)

mass_fractions_matrix_with_ids = np.column_stack((recipe_ids, mass_fractions_matrix))
#for i in mass_fractions_matrix_with_ids:
#	print i

































### Create description vectors files###

mass_fractions = open("mass_fractions_matrix.txt")


mass_fractions_matrix = []
for line in mass_fractions:
	mass_fractions_matrix.append(line.split(' '))



def cosine_similarity(arr1, arr2):
	return 1 - spatial.distance.cosine(arr1, arr2)

def extract_nouns(line):
    tokens = nltk.word_tokenize(line)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word,pos in tagged         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == '')]
    downcased = [x.lower() for x in nouns]
    joined = " ".join(downcased).encode('utf-8')
    return joined


recipesjson = open("recipes.json", "r")
meal_types_names = []
meal_type_vector = []
recipe_names = []
recipe_name_list = []
recipe_nouns_list = []
recipe_nouns = []
for line in recipesjson:
	matchObj = re.match(r'.*\"recipe_name\": \"([^\"]*)\".*', line)
	if matchObj:
		recipe_names.append(matchObj.group(1))
		#print matchObj.group(1)
		noun_list =  extract_nouns(matchObj.group(1))
		for word in noun_list.split(' '):
			if word not in recipe_nouns_list:
				recipe_nouns_list.append(word)
		current_nouns = noun_list.split(' ')
		recipe_nouns.append(current_nouns)
		if matchObj.group(1).split(' ')[-1] not in recipe_name_list:
			recipe_name_list.append(matchObj.group(1).split(' ')[-1])
	matchObj2 = re.match(r'.*\"meal_type\": \"([^\"]*)\".*', line)
	if matchObj2:
		if matchObj2.group(1) not in meal_types_names:
			meal_types_names.append(matchObj2.group(1))
		meal_type_vector.append(matchObj2.group(1))

#lambdamt is the weight of the meal type  - how much we want to weight meal type 
lambdamt = 0.5
#lambdadt is the weight of the dish type - how much we want to weight dish type
lambdadt = 0.7
#lambdant is the weight of the nouns in the recipe names
lambdant = 0.5
# print recipe_nouns
# print recipe_nouns_list
# print len(recipe_nouns)
# print len(recipe_nouns_list)


recipe_nouns_matrix = np.zeros((len(mass_fractions_matrix), len(recipe_nouns_list)))
for i,l in enumerate(recipe_nouns):
	for j,k in enumerate(recipe_nouns_list):
		for m in l:
			if m == k:
				recipe_nouns_matrix[i, j] = lambdant

meal_type_matrix = np.zeros((len(mass_fractions_matrix), len(meal_types_names)))
for i, l in enumerate(meal_type_vector):
	for j,k in enumerate(meal_types_names):
		if k == l:
			meal_type_matrix[i, j] = lambdamt
			break

dish_type_matrix = np.zeros((len(mass_fractions_matrix), len(recipe_name_list)))
for i, l in enumerate(recipe_names):
	for j, k in enumerate(recipe_name_list):
		if k.split(' ')[-1] == l:
			dish_type_matrix[i,j] = lambdadt
			break
description_vectors = np.column_stack((mass_fractions_matrix, meal_type_matrix, recipe_nouns_matrix))
print description_vectors

file = open("recommender_dv.txt", "w")
for line in description_vectors:
	for i in line:
		file.write(str(i).strip('\n'))
		file.write(' ')
	file.write('\n')

# np.savetxt("recommender_dv.txt", description_vectors)

description_vectors = np.column_stack((mass_fractions_matrix, recipe_nouns_matrix))



file = open("search_dv.txt", "w")
for line in description_vectors:
	for i in line:
		file.write(str(i).strip('\n'))
		file.write(' ')
	file.write('\n')
# np.savetxt("search_dv.txt", description_vectors)

