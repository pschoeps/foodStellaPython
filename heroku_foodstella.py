import os
import psycopg2
import urlparse
import pandas as pd

from datetime import datetime
startTime = datetime.now()

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse('postgres://hbdckqqdlvllpv:syQoGQmxTy1I6lk2TVjIIGe7tu@ec2-54-83-56-31.compute-1.amazonaws.com:5432/daekr1h951bd7e')

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

# Get table names in the database
cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cur.fetchall():
    print(table)

# Get recipe table
cur = conn.cursor()
cur.execute("""SELECT * FROM recipes""")
recipeTable = cur.fetchall()

cur2 = conn.cursor()
cur2.execute("""select column_name from information_schema.columns where
table_name='recipes'""")
recipes_cols_tmp = cur2.fetchall()
recipes_cols = [i[0] for i in recipes_cols_tmp]
dt = pd.DataFrame(recipeTable, columns=recipes_cols)
dt.shape

# Splitting ingredient detail into different entries
import json
import re
import string

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

fout = open('recipe_ingredients_test.json','w')

quant_regex =  "s*|".join(quant_list)
quant_regex = "(" + quant_regex + "s*|^[0-9]+\s)"
quant_regex_sub = quant_regex + "s*|^[0-9]+"


# Start cleaning details in dataframe
recipes_file = open('recipeWebsite_beef.json','rU')
a = []
for line in recipes_file:
  a.append(json.loads(line))

dt = pd.DataFrame(a)
def split_ingredient(data):
  for ingredient_detail in data['recipe_ingredients'].split('\n'):
    m = re.match(r'^[0-9]+',ingredient_detail)
    if m == None:
      continue
    ingredient_num = m.group(0)
    ingredient_detail = re.sub(r'^[0-9]*:\s','',ingredient_detail)
    if re.search(quant_regex,ingredient_detail) != None:
      m = re.match(quant_regex, ingredient_detail)
      quantity = m.group(0)
      ingredient = re.sub(re.escape(quantity),'',ingredient_detail)

      #Remove other descriptive words from ingredient
      for word in other_words:
        wordregex = re.compile(r'\b%s\b' % re.escape(word))
        ingredient = re.sub(wordregex,'',ingredient)
      ingredient = re.sub(r',\s*$','',ingredient)
      ingredient = ingredient.strip()
      ingredient_info = {'ingredient_id': ingredient_num,
              'recipe_id': data['recipe_id'],
              'ingredient': ingredient,
              'quantity': quantity,
              'detail': ingredient_detail}

      fout.write(json.dumps(ingredient_info))
      fout.write('\n')

## Write to recipe_ingredient
dt.apply(split_ingredient, axis = 1)
recipes_file.close()
fout.close()

print datetime.now() - startTime