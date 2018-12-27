#!/usr/bin/env python
# coding: utf-8

# This project will explore a sample of German Ebay auto classifieds.  The data needs to be cleaned and then analyzed.  This project should help me to practice and better understand the details of working with pandas and cleaning data.

# In[86]:


import pandas as pd
import numpy as np

autos = pd.read_csv("autos.csv", encoding = "Latin-1")


# In[87]:


autos


# In[88]:


autos.info()
autos.head()


# There are a few fields which have null values that need to be cleared up.  Going to need to clean the price column, odometer column, and possibly the dateCreated/LastSeen Columns.

# In[89]:


autos.columns


# In[90]:


cols = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
       'last_seen']
autos.columns = cols
autos.head()


# These changes were made to make some of the more obscure or long names easier to work with.  dateCreated for example, it is fairly obscure what this field actually meant, could it be when the car was produced or some other information, or could it be when the ad was created.  By changing the name to ad_created it makes it much easier to quickly understand what this field is meant to be.

# In[91]:


autos.describe()


# It appears as if the nrOfPictures field is always 0.  This field can be dropped.
# 
# There are some strange values in the registration_year field since the min is 1000 and the max is 9999 and a car could not be registered for 7000+ years from now.
# 
# There are also some strange values in the powerPS field since a car shouldnt be able to have 17700 PS of power so some rows may need to be removed.
# 
# As I stated earlier, it appears the price and odometer fields which are currently strings will need to be cleaned and converted to floats/ints.
# 
# Again, if we want to sort by date of posting or date last seen we will need to clean those fields and convert the dates to ints.

# In[92]:


autos['price'] = (autos['price']
                  .str.replace('$','')
                  .str.replace(',','')
                  .astype(float)
                 )

autos['odometer'] = (autos['odometer']
                     .str.replace('km','')
                     .str.replace(',','')
                     .astype(float)
                    )
autos.rename({'odometer': 'odometer_km'}, axis = 1, inplace = True)
autos.head()

autos = autos.drop(columns='nr_of_pictures')


# In[93]:


autos = autos[autos['price'].between(0,350000)]
autos['price'].describe()

autos = autos[autos['registration_year'].between(1900,2017)]


# The odometer appears to follow a standard pattern with no outliers.  However, the price had some inconsistencies.  There were a few listings that had prices well into the millions and while some extremely high end cars can get into that range it is very uncommon to see them on a site like Ebay instead of at an auction.  I capped the max price to 350000 which is the last value in the somewhat reasonable range.  The next value is 990000, nearly 3x the price.  I also left in all the cars that cost 0 dollars because it is not too uncommon  for an old beatup car to be given away for free to someone that wants to fix it up.
# 
# It appears that for the prices, most of them are $3000 or less.  Most of the Mileage is 150000.

# In[94]:


(autos['date_crawled']
 .value_counts(normalize=True, dropna=False)
 .sort_index(ascending=False)
)


# The pages appear to have been crawled over the span of about a month.  Not many listings were crawled at the same time since there are 48200 unique date times that listings were crawled.

# In[95]:


(autos['ad_created']
 .value_counts(normalize=True, dropna=False)
)


# Most of the listings appear to have been created in march and april, when the listings were crawled.  However the earliest ones were created nearly a year before the crawling.  

# In[96]:


(autos['last_seen']
 .value_counts(normalize=True, dropna=False)
 #.sort_index(ascending=False)
)


# Most listings were last seen around the end of the scraping period.  However, there were still a lot of listings that ended throughout the period.

# In[97]:


autos['registration_year'].describe()


# After cleaning the data, most cars were registered before 2008.  The mean registration year is 2003 and only 25% were registered before 1999.

# In[98]:


autos['registration_year'].value_counts(normalize = True) * 100


# The most popular year of car being sold is 2000 with 2005 and 1999 just under 1% behind.

# In[99]:


brand_counts = autos["brand"].value_counts(normalize=True)
top_20_brands = brand_counts.index[:20]
print(top_20_brands)

'''I am using the top 20 brands because that gives a good representation of
not only the largest brands but some of the smaller brands.'''    

top_brands_mean_price = {}
top_brands_mean_mileage = {}

for brand in top_20_brands:
    selected_rows = autos[autos['brand'] == brand]
    top_brands_mean_price[brand] = selected_rows['price'].mean()
    top_brands_mean_mileage[brand] = selected_rows['odometer_km'].mean()
    
top_brands_mean_mileage


# Mini has the best resale price of the top 20 brands.  BMW, Audi, and Mercedes all have good resale value and are close to equal.

# In[100]:


bmp_series = pd.Series(top_brands_mean_price)
bmm_series = pd.Series(top_brands_mean_mileage)

mileage_and_prices = pd.DataFrame(bmp_series, columns = ['mean_price'])
mileage_and_prices['mean_mileage'] = bmm_series

mileage_and_prices


# Part of the reason Mini's are so valuable is because they have the least average miles.  If Mini's average mileage were closer to the 130000 miles of BMW, Audi, and Mercedes I would expect it to be equal or less than their average prices.
# 
# It also appears that most the cars being sold have between 100000 and 130000 miles.

# In[101]:


autos


# In[102]:


autos = autos.replace('andere','other')
autos['seller'] = autos['seller'].str.replace('privat','private').str.replace('gewerblich','commercial')

autos['offer_type'] = autos['offer_type'].str.replace('Angebot','offer').str.replace('Gesuch','Auction')

autos['vehicle_type'] = (autos['vehicle_type']
                         .str.replace('kleinwagen','compact car')
                         .str.replace('kombi', 'station wagon')
                        )

autos['gearbox'] = autos['gearbox'].str.replace('manuell','manual').str.replace('automatik','automatic')

autos['fuel_type'] = (autos['fuel_type']
                      .str.replace('benzin','gasoline')
                      .str.replace('elektro','electric')
                      )

autos['unrepaired_damage'] = autos['unrepaired_damage'].str.replace('nein','no').str.replace('ja','yes')


# Converted all the German words to English here.

# In[103]:


autos['date_crawled'] = autos['date_crawled'].str.split(n=1,expand=True).iloc[:,0].str.replace('-','')
autos['ad_created'] = autos['ad_created'].str.split(n=1,expand=True).iloc[:,0].str.replace('-','')
autos['last_seen'] = autos['last_seen'].str.split(n=1,expand=True).iloc[:,0].str.replace('-','')


# In[104]:


mileage_groups = autos['odometer_km'].value_counts().index

mean_price_for_mileage = {}

for mileage in mileage_groups:
    selected_rows = autos[autos['odometer_km'] == mileage]
    mean_price_for_mileage[mileage] = selected_rows['price'].mean()
    
mean_price_for_mileage


# The price of a vehicle on average drops $1300 ever 10000km for the first 100000km, then it drops less aggresively at a rate of $850 per 10000km over 100000km.  For some reason cars with only 5000km on them are very cheap.  Perhaps a lot of cars in the 5000km have unrepaired damage.

# In[105]:


for mileage in [5000.0,10000.0]:
    selected_rows = autos[autos['odometer_km'] == mileage]
    print(mileage)
    print(selected_rows['unrepaired_damage'].value_counts(normalize = True))


# My previous hypothesis was correct, out of the cars in the 5000km category 20.25% of them have damage.  While in the 10000km only 3.75% of the cars have damage.  Lets look at what damage does to a vehicle's valuation.

# In[111]:


mean_price_for_mileage_undamaged = {}
mean_price_for_mileage_damaged = {}

for mileage in mileage_groups:
    selected_rows_undamaged = autos[(autos['odometer_km'] == mileage) & (autos['unrepaired_damage'] == 'no')]
    mean_price_for_mileage_undamaged[mileage] = selected_rows_undamaged['price'].mean()
    selected_rows_damaged = autos[(autos['odometer_km'] == mileage) & (autos['unrepaired_damage'] == 'yes')]
    mean_price_for_mileage_damaged[mileage] = selected_rows_damaged['price'].mean()
    
mean_price_undamaged_series = pd.Series(mean_price_for_mileage_undamaged)
mean_price_damaged_series = pd.Series(mean_price_for_mileage_damaged)

damage_vs_undamaged = pd.DataFrame(mean_price_undamaged_series, columns = ['mean_price_undamaged'])
damage_vs_undamaged['mean_price_damaged'] = mean_price_damaged_series
damage_vs_undamaged['price_difference'] = damage_vs_undamaged['mean_price_undamaged'] - damage_vs_undamaged['mean_price_damaged']
damage_vs_undamaged['damaged_percent_value_of_undamged'] = (damage_vs_undamaged['mean_price_damaged'] / damage_vs_undamaged['mean_price_undamaged']) * 100
damage_vs_undamaged


# As can be seen in the chart above, selling a damaged car causes a huge drop in price.  You can see that the fewer miles on a car, the more of the value you lose when a car is sold damaged.  There is almost a $20000 difference between damaged and
