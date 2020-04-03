#!/usr/bin/env python
# coding: utf-8

# In[256]:


#Answer1
import urllib.request
import csv

yelp_restaurant_url = "https://www.yelp.com/biz/j-wata-temaki-bar-san-diego-2?osq=restaurant"
source_code = urllib.request.urlopen(yelp_restaurant_url).read().decode('utf-8')

Author = []
Review = []
Restaurant = []
Restaurant1= []
counter = 0

while True:
    #getting restaurant name
    index1 = source_code.find('itemprop="aggregateRating"')
    source1 = source_code[index1:]
    index2 = source1.find('itemprop="name" content="')+25
    source2 = source1[index2:]
    index3 = source2.find('/>')-2
    Restaurant.append(source2[:index3])
    
    while source2.find('itemprop="review"') != -1:
        #getting author and their review
        source3 = source2[source2.find('itemprop="review"'):]
        index4 = source3.find('itemprop="author" content="')+27
        index6 = source3.find('itemprop="description"')+23
        source4 = source3[index4:]
        source5 = source3[index6:]
        index6 = source5.find('<p>')
        index5 = source4.find('>')-1
        Review.append(source5[:index6])
        Author.append(source4[:index5])
        #updating source code for next review
        source2 = source5
        
    #getting the subsequent page URL from the source code    
    index7 = source_code.find('link rel="next" href=')+22
    source6 = source_code[index7:]
    index8 = source6.find('>')-3
    new_url = source6[:index8]
    new_url = new_url.replace('&amp;','&')
    
    if counter == -1:
        break
    
    #updating source code for next page iteration
    source_code = urllib.request.urlopen(new_url).read().decode('utf-8')
    if source_code.find('link rel="next" href=') == -1:
        counter = -1
        
Restaurant[0] = Restaurant[0].replace('&amp;','&')
for i in list(range(len(Author))):
    Restaurant1.append(Restaurant[0])
    
for i in list(range(len(Author))):
    Review[i] = Review[i].replace('\n\n','\n')

#importing csv
from itertools import zip_longest
d = [Restaurant1, Author, Review]
export_data = zip_longest(*d, fillvalue = '')
with open('Files_Directory/hw4.csv', 'w', encoding='utf-8', newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("restaurant name", "reviewer's name", "review text"))
      wr.writerows(export_data)
myfile.close()

