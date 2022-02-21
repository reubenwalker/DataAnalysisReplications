#cd db
import pandas as pd
import json
db = json.load(open('datasets/usda_food/database.json'))
len(db)
#Each entry in db is a dict containing all the data for a single food.
	#The 'nutrients' field is a list of dicts, one for each nutrients
db[0].keys()
db[0]['nutrients'][0]
nutrients = pd.DataFrame(db[0]['nutrients'])
nutrients[:7]
#When converting to a DataFrame, specify a list of fields to extract:
    #take food names, group, id, and manufacturer
info_keys = ['description', 'group', 'id', 'manufacturer']
info = pd.DataFrame(db, columns=info_keys)
info[:5]
#Distribution of food groups with value_counts
pd.value_counts(info.group)[:10]
#To do some analysis on the nutrient data,
    #Assemble the nutrients for each food into a single large table.
    #Several steps:
        #1. Convert each list of nutrients to a DataFrame
        #2. Add a column for the food "id"
        #3. Append the DataFrame to a list
        #4. Concatenate them together with .concat


nutrients = []
summed = 0
for rec in db:
    #1. Convert each list of nutrients to a DataFrame
    fnuts = pd.DataFrame(rec['nutrients'])
    #summed += len(fnuts)
    #print(len(fnuts))
    #2. Add a column for the food "id"
    fnuts['id'] = rec['id']
    #3. Append the DataFrame to a list
    nutrients.append(fnuts)
#At this point, we have a list of Dataframes
#4. Concatenate them together with .concat
nutrients = pd.concat(nutrients, axis=0, ignore_index=True)
#389355 non-null Series:
    #Value, units, description, group, id
#There are duplicates
nutrients.duplicated().sum() #14719
#Let's drop duplicates
nutrients = nutrients.drop_duplicates()
#Let's rename group and description, to clarify:
col_mapping = {'description' : 'food',
               'group'       : 'fgroup'}
info = info.rename(columns=col_mapping, copy=False)
col_mapping = {'description' : 'nutrient',
               'group'       : 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)
#So we've removed all of the nutrient information
#We can now (re)merge nutrients and info
ndata = pd.merge(nutrients, info, on='id', how='outer') 
ndata.iloc[30000]
#Slice, dice, and aggregate can be used on this dataset later
#Plot of median values by food group and nutrient type:
result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
result['Zinc, Zn'].sort_values().plot(kind='barh', title='Foods high in zinc')
#Can find out which food is most dense in each nutrient:
by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])
get_maximum = lambda x: x.xs(x.value.idxmax())
get_minimum = lambda x: x.xs(x.value.idxmin())
max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]
#make the food a little smaller:
max_foods.food = max_foods.food.str[:50]