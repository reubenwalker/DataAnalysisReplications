#cd db
#IMPORTANT: Use python < 3.0
import pandas as pd
#Ushahidi is a non-profit software company that enables crowdsourcing of data
    #from natural disasters and geopolitical events via text message
    #Many data sets then published on the website:
    #Doesn't seem to be true anymore. They might be here:
    #https://old.datahub.io/dataset/ushahidi
#Data for the 2010 Haiti earthquake crisis and aftermath
data = pd.read_csv('datasets/Haiti/Haiti.csv')
data
#Each row represents a report sent from someone's mobile phone indicating an emergency
    #Each has an associated timestamp and location as lat. and long.
data[['INCIDENT DATE', 'LATITUDE', 'LONGITUDE']][:10]
#CATEGORY field contains a comma-separated list of codes indicating type of message
data['CATEGORY'][:6]
#Some of the categories are missing. 
#Calling .describe shows that there are some aberrant locations:
data.describe()
#Nead to clean latitudes to be within 18 and 20
#Clean longitudes to be within -75 and -70
data = data[(data.LATITUDE > 18) & (data.LATITUDE < 20) &
            (data.LONGITUDE > -75) & (data.LONGITUDE < -70)
            & data.CATEGORY.notnull()]
data.describe()

#We might want to do some analysis of the data by category, 
    #but each category field might have multiple categories
#Additionally, each category has a code plus an English and a French name.
#First, need two functions to get a list of all the categories 
    #and to split each category into a code and an English name:
def to_cat_list(catstr):
    stripped = (x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]

def get_all_categories(cat_series):
    cat_sets = (set(to_cat_list(x)) for x in cat_series)
    return sorted(set.union(*cat_sets))

def get_english(cat):
    code, names = cat.split('.')
    if '|' in names:
        names = names.split(' | ')[1]
    return code, names.strip()

#Test it out!
#Does get_english do what you would expect?
get_english('2. Urgences logistiques | Vital Lines')

#Now make a dict mapping code to name because we'll use the code for analysis
    #We'll use this when adorning plots
    #Note the use of a generator expression in lieu of a list comprehension
all_cats = get_all_categories(data.CATEGORY)
#Generator Expression
english_mapping = dict(get_english(x) for x in all_cats)
english_mapping['2a'] #'Food Shortage'
english_mapping['6c'] #'Earthquake and aftershocks'

#There are many ways to go about augmenting the data set 
    #to be able to easily select records by category.
    #One way is to add indicator (or dummy) columns
    #To do that, extract unique category codes 
        #and construct a dataframe of zeros having those as its columns and 
        #the same index as data.
def get_code(seq):
    return [x.split('.')[0] for x in seq if x]

all_codes = get_code(all_cats)
code_index = pd.Index(np.unique(all_codes))
dummy_frame = pd.DataFrame(np.zeros((len(data), len(code_index))),
                           #index=data.index,
                           columns=code_index)
#Now we want to set the appropriate entries of each row to 1
    #and join it with the data:
i = []
#dummy_frame
for row, cat in zip(dummy_frame.index, data.CATEGORY):
    codes = get_code(to_cat_list(cat))
    i.append(row)
    dummy_frame.iloc[row][codes] = 1
#This syntax isn't working anymore because .ix is deprecated
#Wow that took forever. 
    #In order to make it iterable, your solution was to:
        #Set the dummy_frame to the dimensions of the data
        #Use a default index so that it was iterable
        #Iterate through the matrix with the category headings.
        #NOW we'll set the index to that of the data.
        #.ix seemed like a handy tool. Wonder why they deprecated it.
dummy_frame.index = data.index

#The following took seemingly infinite time. 
    #Over ten million combinations, for sure. 3569 x 3569
#for row in data.index:
#    for cat in data.CATEGORY:
#        codes = get_code(to_cat_list(cat))
#        #print(row)
#        dummy_frame.iloc[row][codes] = 1

#Then we rejoin the dummy_frame to the data:
data = data.join(dummy_frame.add_prefix('category_'))

#Plot time!
#We have spatial data, so it would be cool to plot the data by category on a map of Haiti.
#The basemap toolkit, a matplotlib add-on, enables plottind 2D data on maps in python
#After some trial and error, this draws a simple black and white map of haiti.
#Basemap doesn't seem to be Python 3.0 compatible.
#I installed mpl_toolkits from git clone https://github.com/rveciana/BasemapTutorial.git 
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#Error, only crude, low, and intermediate resolution datasets are installed by default
def basic_haiti_map(ax=None, lllat=17.25, urlat=20.25,
                    lllon=-75, urlon=-71):
    # create polar stereographic Basemap instance.
    m = Basemap(ax=ax, projection='stere',
                lon_0 = (urlon + lllon) / 2,
                lat_0 = (urlat + lllat) / 2,
                llcrnrlat=lllat, urcrnrlat=urlat,
                llcrnrlon=lllon, urcrnrlon=urlon,
                resolution='i') #was 'f', not available, now 'i' for 'intermediate'
    #draw coastlines, state and country boundaries, edge of map
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    return m

#So this returned Basemap object now knows how to transform coordinates onto the canvas.
#The following code plots the data observations for a number of report categories:
#For each category:
    #Filter down the data set to the coordinates labeled in that category.
    #Plot a Basemap on the appropriate subplot,
    #Transform the coordinates,
    #Plot the points using Basemap's plot method
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,10))
fig.subplots_adjust(hspace=0.05, wspace=0.05)
to_plot = ['2a', '1', '3c', '7a']
lllat=17.25; urlat=20.25; lllon=-75; urlon=-71

for code, ax in zip(to_plot, axes.flat):
    m = basic_haiti_map(ax, lllat=lllat, urlat=urlat,
                        lllon=lllon, urlon=urlon)
    cat_data = data[data['category_%s' % code] == 1]
    #This notation seems extremely important to master.
    
    
    #Compute map proj coordinates
    x, y = m(cat_data.LONGITUDE, cat_data.LATITUDE)
    
    m.plot(x, y, 'k.', alpha=0.5)
    ax.set_title('%s: %s' % (code, english_mapping[code]))

#Basemap allows you to overlap additional map data which comes from what are called shapefiles
#Downloaded a shapefile with roads in Port-au-prince (cegrp.cga.harvard.edu/haiti/?q=resources_data
#Basemap object conveniently has a readshapefile method

#PortAuPrince: 18.533333, -72.333336
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12,10))
fig.subplots_adjust(hspace=0.05, wspace=0.05)
code = '2a'
lllat=18.33; urlat=18.83; lllon=-72.58; urlon=-72.08

m = basic_haiti_map(axes, lllat=lllat, urlat=urlat,
                    lllon=lllon, urlon=urlon)
cat_data = data[data['category_%s' % code] == 1]
#This notation seems extremely important to master.


#Compute map proj coordinates
x, y = m(cat_data.LONGITUDE, cat_data.LATITUDE)
axes.set_title('%s: %s in Port-au-Prince' % (code, english_mapping[code]))
m.plot(x, y, 'k.', alpha=0.5)
shapefile_path = 'datasets/Haiti/PortAuPrince_Roads/PortAuPrince_Roads'
m.readshapefile(shapefile_path, 'roads')


