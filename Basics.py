#!/usr/bin/env python
# coding: utf-8

# In[53]:


import csv
f = open("guns.csv")
csvreader = csv.reader(f)
data = list(csvreader)

print(data[:5])


# In[54]:


headers = data[0]
data = data[1:]
print(headers)
print(data[:5])


# In[55]:


years = [row[1] for row in data]
year_counts = {}
for year in years:
    if year in year_counts:
        year_counts[year] += 1
    else:
        year_counts[year] = 1
print(year_counts)


# In[56]:


import datetime
dates = [datetime.datetime(year = int(row[1]), month = int(row[2]), day = 1) for row in data]
print(dates[:5])
date_counts = {}
for date in dates:
    if date in date_counts:
        date_counts[date] += 1
    else:
        date_counts[date] = 1
        
print(date_counts)
        


# In[57]:


sex_counts = {}
race_counts = {}
for row in data:
    if row[5] in sex_counts:
        sex_counts[row[5]] += 1
    else:
        sex_counts[row[5]] = 1
    
    if row[7] in race_counts:
        race_counts[row[7]] += 1
    else:
        race_counts[row[7]] = 1
        
print(race_counts)
print(sex_counts)
        


# Most Shooting deaths are White males

# In[58]:


g = open("census.csv")
census = list(csv.reader(g))
print(census)


# In[59]:


mapping = {}
mapping["White"] = int(census[1][10])
mapping["Hispanic"] = int(census[1][11])
mapping["Black"] = int(census[1][12])
mapping["Native American/Native Alaskan"] = int(census[1][13])
mapping["Asian/Pacific Islander"] = int(census[1][14]) + int(census[1][15])

race_per_hundredk = {}

for race in race_counts:
    race_per_hundredk[race] = race_counts[race] / mapping[race]
    race_per_hundredk[race] *= 100000
    
print(race_per_hundredk)
    


# In[60]:


intents = [row[3] for row in data]
races = [row[7] for row in data]

homicide_race_counts = {}
for i, race in enumerate(races):
    if intents[i] == "Homicide":
        if race in homicide_race_counts:
            homicide_race_counts[race] += 1
        else:
            homicide_race_counts[race] = 1
            
for race in homicide_race_counts:
    homicide_race_counts[race] = homicide_race_counts[race] / mapping[race]
    homicide_race_counts[race] *= 100000
    
print(homicide_race_counts)
            


# In[61]:


accidental_race_counts = {}
for i, race in enumerate(races):
    if intents[i] == "Accidental":
        if race in accidental_race_counts:
            accidental_race_counts[race] += 1
        else:
            accidental_race_counts[race] = 1
            
for race in accidental_race_counts:
    accidental_race_counts[race] = accidental_race_counts[race] / mapping[race]
    accidental_race_counts[race] *= 100000
    
print(accidental_race_counts)


# In[62]:


suicide_race_counts = {}
for i, race in enumerate(races):
    if intents[i] == "Suicide":
        if race in suicide_race_counts:
            suicide_race_counts[race] += 1
        else:
            suicide_race_counts[race] = 1
            
for race in suicide_race_counts:
    suicide_race_counts[race] = suicide_race_counts[race] / mapping[race]
    suicide_race_counts[race] *= 100000
    
print(suicide_race_counts)


# In[ ]:




