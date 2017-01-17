
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[1]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[14]:

def answer_one():
    #df.index.name = 'Country'
    newdf = df.loc[[df['Gold'].idxmax()]]
    newdf.index.name = 'Country'
    #print(newdf['Gold'].index.values)
    #print(newdf)
    list1 = newdf['Gold'].index.values
    str1 = ''.join(list1)
    return str1
answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[16]:

def answer_two():
    df['Difference'] = 0
    for index, row in df.iterrows():
        difference = abs(int(row['Gold']) - int(row['Gold.1']))
        df.set_value(index,'Difference',difference)
    
    newdf = df.loc[[df['Difference'].idxmax()]]    
    newdf.index.name = 'Country'
    list1 = newdf['Gold'].index.values
    str1 = ''.join(list1)
    return str1

answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[24]:

def answer_three():
    candidate = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    candidate['Difference'] = 0.0
    for index, row in candidate.iterrows():
        difference = abs(int(row['Gold']) - int(row['Gold.1'])) / int(row['Gold.2'])
        candidate.set_value(index,'Difference',difference)
    
    newdf = candidate.loc[[candidate['Difference'].idxmax()]]    
    newdf.index.name = 'Country'
    list1 = newdf['Gold'].index.values
    str1 = ''.join(list1)
    return str1

answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*

# In[6]:

def answer_four():
    df['Points'] = 0
    for index, row in df.iterrows():
        points = int(row['Gold.2'])*3 + int(row['Silver.2'])*2 + int(row['Bronze.2'])*1
        df.set_value(index,'Points',points)
       
    target = df['Points']
    #print(len(target))
    return target

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[3]:

census_df = pd.read_csv('census.csv')
census_df.head()
#census_df


# In[84]:

def answer_five():
    global census_df
    global candidate
    global newdf
    candidate = census_df.copy()
    candidate = candidate[candidate['SUMLEV'] == 50]
    #candidate = candidate.set_index('STNAME')
    
    newdf = candidate.copy()
    newdf['Total'] = newdf['COUNTY'].groupby(newdf['STNAME']).transform(sum)
    newdf2 = newdf.loc[newdf['Total'].idxmax()]
    return newdf2['STNAME']

answer_five()


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[7]:

def answer_six():
    candidate = census_df.copy()
    candidate = candidate[candidate['SUMLEV'] == 50]
    
    candidate = candidate.sort_values(by = ['STNAME','CENSUS2010POP'], ascending = False)
    candidate = candidate.groupby('STNAME').head(3)
    
    target = candidate.groupby('STNAME').sum().sort_values(by = 'CENSUS2010POP', ascending = False)
    return target.head(3).index.tolist()

answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[4]:

def answer_seven():
    candidate = census_df.copy()
    candidate = candidate[candidate['SUMLEV'] == 50]
    
    candidate['Population Change'] = abs(candidate['POPESTIMATE2015'] - candidate['POPESTIMATE2014'])+abs(candidate['POPESTIMATE2014'] - candidate['POPESTIMATE2013'])+abs(candidate['POPESTIMATE2013'] - candidate['POPESTIMATE2012'])+abs(candidate['POPESTIMATE2012'] - candidate['POPESTIMATE2011'])+abs(candidate['POPESTIMATE2011'] - candidate['POPESTIMATE2010'])
    
    target = candidate['CTYNAME'][candidate['Population Change'] == max(candidate['Population Change'])]
    return target.tolist()[0]

answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[ ]:

def answer_eight():
    candidate = census_df.copy()
    candidate = candidate[candidate['SUMLEV'] == 50]
    
    return "YOUR ANSWER HERE"

