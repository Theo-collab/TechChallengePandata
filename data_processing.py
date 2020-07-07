#!/usr/bin/env python
# coding: utf-8

# Libraries
import pandas as pd
import moxing as mox
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import json
import codecs
import os

# See available data in the parallel file system
mox.file.shift('os', 'mox')
print(os.listdir('s3://mountpoint'))


def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma


# Weather
def get_weather_to_df(city):
    input_address = 's3://mountpoint/WEATHER_'
    
    input_address = input_address+city    
        
    empty_line = []
    with open(input_address) as json_data:
        data = json.load(json_data)
    # add city to line
    empty_line.append(city)
    # add only 2 days forecast with description and temp to line
    for i in range(3):
        empty_line.append(data['daily'][i]['temp']['day'])
        empty_line.append(data['daily'][i]['weather'][0]['description'])

    empty_frame = pd.DataFrame([empty_line], 
                               columns=['city','day0Temp', 'day0descr', 
                                        'day1Temp', 'day1descr', 
                                        'day2Temp', 'day2descr'])
    return(empty_frame)

# Berlin workaround
BerlinCW = get_weather_to_df('berlin')
BerlinFK = get_weather_to_df('berlin')
BerlinLi = get_weather_to_df('berlin')
BerlinMH = get_weather_to_df('berlin')
BerlinMi = get_weather_to_df('berlin')
BerlinNe = get_weather_to_df('berlin')
BerlinPa = get_weather_to_df('berlin')
BerlinRD = get_weather_to_df('berlin')
BerlinSp = get_weather_to_df('berlin')
BerlinSZ = get_weather_to_df('berlin')
BerlinTS = get_weather_to_df('berlin')
BerlinTK = get_weather_to_df('berlin')
# BerlinCW, BerlinFK, BerlinLi, BerlinMH, BerlinMi, BerlinNe, BerlinPa, BerlinRD, BerlinSp, BerlinSZ, BerlinTS, BerlinTK

BerlinCW = BerlinCW.replace('berlin','Berlin Charlottenburg-Wilmersdorf')
BerlinFK = BerlinFK.replace('berlin','Berlin Friedrichshain-Kreuzberg')
BerlinLi = BerlinLi.replace('berlin','Berlin Lichtenberg')
BerlinMH = BerlinMH.replace('berlin','Berlin Marzahn-Hellersdorf')
BerlinMi = BerlinMi.replace('berlin','Berlin Mitte')
BerlinNe = BerlinNe.replace('berlin','Berlin Neukölln')
BerlinPa = BerlinPa.replace('berlin','Berlin Pankow')
BerlinRD = BerlinRD.replace('berlin','Berlin Reinickendorf')
BerlinSp = BerlinSp.replace('berlin','Berlin Spandau')
BerlinSZ = BerlinSZ.replace('berlin','Berlin Steglitz-Zehlendorf')
BerlinTS = BerlinTS.replace('berlin','Berlin Tempelhof-Schöneberg')
BerlinTK = BerlinTK.replace('berlin','Berlin Treptow-Köpenick')

# run it for all cities we want to showcase
frames = [get_weather_to_df('berlin'), get_weather_to_df('munich'), 
          get_weather_to_df('nuernberg'), get_weather_to_df('hongkong'), 
          BerlinCW, BerlinFK, BerlinLi, BerlinMH, BerlinMi, BerlinNe, 
          BerlinPa, BerlinRD, BerlinSp, BerlinSZ, BerlinTS, BerlinTK]
result_weather = pd.concat(frames)

# common identifier and solving Berlin problem
result_weather = result_weather.replace('munich','München')
result_weather = result_weather.replace('nuernberg','Nürnberg')
result_weather = result_weather.replace('hongkong','Hong Kong')

##################################
# final dataframe: result_weather#
##################################


# ICU
def list_parser(lst):
    
    info_list = list()
    for i in range(len(lst)):
        raw = lst[i].split()
        state = raw[0]
        free = int(raw[-2])
        ratio = round(int(raw[-2]) / int(raw[-1]), 3)
        info_list.append([state, free, ratio])
    
    return info_list

# source like: 's3://mountpoint/ICU.txt'
def get_ICU(source):
    with codecs.open(source, 'r', 'UTF-8') as reader:
        text = reader.read()
        
    text = text.replace("\r", "")
    text = text.replace("Wirttemberg", "Württemberg")
    text = text.replace("Thiringen", "Thüringen")
    text = text.replace(".", "")
    text = text.replace(",", "")
    
    text2 = text.split("\n\n \n\nDie dargestellten Zahlen ")[0]
    text2= text2.split('Summe')[1]
    
    raw_info= text2.split('\n', 1)[1]
    raw_info_list = raw_info.split('\n')
    
    info_list = list_parser(raw_info_list)
    
    headers = ['State', 'Free Beds', 'Occupancy Ratio']
    
    df = pd.DataFrame(info_list, columns=headers)
    return df

result_ICU = get_ICU('s3://mountpoint/ICU.txt')

###############################
# final dataframe: result_ICU #
###############################


# Clustering + RKI

# Jenks Natural Breaks Optimization
# Jenks Natural Breaks is a clustering algorithm which is used on sorted 1-D data. This is done by seeking to 
# minimize each class's average deviation from the class mean, while maximizing each class's deviation from 
# the means of the other groups. In other words, the method seeks to reduce the variance within classes and 
# maximize the variance between classes.[1]
#
# [1]. https://en.wikipedia.org/wiki/Jenks_natural_breaks_optimization

def get_jenks_breaks(data_list, number_class):
    #data_list.sort()
    mat1 = []
    for i in range(len(data_list) + 1):
        temp = []
        for j in range(number_class + 1):
            temp.append(0)
        mat1.append(temp)
    mat2 = []
    for i in range(len(data_list) + 1):
        temp = []
        for j in range(number_class + 1):
            temp.append(0)
        mat2.append(temp)
    for i in range(1, number_class + 1):
        mat1[1][i] = 1
        mat2[1][i] = 0
        for j in range(2, len(data_list) + 1):
            mat2[j][i] = float('inf')
    v = 0.0
    for l in range(2, len(data_list) + 1):
        s1 = 0.0
        s2 = 0.0
        w = 0.0
        for m in range(1, l + 1):
            i3 = l - m + 1
            val = float(data_list[i3 - 1])
            s2 += val * val
            s1 += val
            w += 1
            v = s2 - (s1 * s1) / w
            i4 = i3 - 1
            if i4 != 0:
                for j in range(2, number_class + 1):
                    if mat2[l][j] >= (v + mat2[i4][j - 1]):
                        mat1[l][j] = i3
                        mat2[l][j] = v + mat2[i4][j - 1]
        mat1[l][1] = 1
        mat2[l][1] = v
    k = len(data_list)
    kclass = []
    for i in range(number_class + 1):
        kclass.append(min(data_list))
    kclass[number_class] = float(data_list[len(data_list) - 1])
    count_num = number_class
    while count_num >= 2:  # print "rank = " + str(mat1[k][count_num])
        idx = int((mat1[k][count_num]) - 2)
        # print "val = " + str(data_list[idx])
        kclass[count_num - 1] = data_list[idx]
        k = int((mat1[k][count_num] - 1))
        count_num -= 1
    return kclass


with open('s3://mountpoint/RKIcsv') as a:
    data = pd.read_csv(a)

# To use the selected clustering algorithm, the values have to be sorted, in this case according to the column
# "cases7_per_700k" which is the new cases in last 7 days per 100.000 inhabitants.
data = data.sort_values(by="cases7_per_100k", ascending=False)
data = data.reset_index(drop=True)

breaks = get_jenks_breaks(data["cases7_per_100k"], 3)
for line in breaks:
    plt.plot([line for _ in range(len(data["cases7_per_100k"]))], 'k--')

plt.plot(data["cases7_per_100k"])
plt.grid(True)
plt.show()
breaks.sort(reverse=True)

# We create a new column which contains the information about classes
def break_function(df):
    data = df
    label_col = []
    
    for i in range(data.shape[0]):
        if data["cases7_per_100k"].iloc[i] > breaks[0]:
            label = 3
        elif data["cases7_per_100k"].iloc[i] > breaks[1]:
            label = 2
        else:
            label = 1
        
        label_col.append(label)
    
    return label_col

label_col = break_function(data)
label_data = pd.DataFrame(label_col, columns =['Labels']) 
exteded_data = pd.concat([data, label_data], axis=1)

# A new identifier is created to be used later data merging
exteded_data['pfid'] = np.nan
exteded_data["pfid"] = exteded_data["pfid"].fillna(exteded_data["OBJECTID"])

exteded_data['pfid'] = exteded_data['pfid'].apply(lambda x: 'p'+str(int(x)))
    

result_RKI = exteded_data

###############################
# final dataframe: result_RKI #
###############################


# Regulations

# Reading the Document
with codecs.open('s3://mountpoint/b_eng.txt', 'r', 'UTF-8') as reader:
    b_content = reader.read()
with codecs.open('s3://mountpoint/m_eng.txt', 'r', 'UTF-8') as reader:
    m_content = reader.read()

# Helper Functions
# We realised that '§' is used in German legal documents to split the topics, so we also used that character and
# additional conditions (as '§' is not only used in the titles) to split the topics. This is the pattern that for 
# Bavaria
def splitter(text):
    
    rule_list = list()
    flag = True
    i = 1
    
    while flag:
        
        splitted = text.split('§ ' + str(i) + '\r\n', 1)
        if len(splitted) == 1:
            flag = False
        else:
            rule_list.append(splitted[0])  
            text = ''.join(splitted[1:])
            i += 1
            
    print(str(i) + " rules have been extracted")
    return rule_list


# This pattern is used for Berlin
def b_splitter(text):
    
    rule_list = list()
    flag = True
    i = 1
    
    while flag:
        
        splitted = text.split('\r\n§ ', 1)
        if len(splitted) == 1:
            flag = False
        else:
            rule_list.append(splitted[0])  
            text = ''.join(splitted[1:])
            i += 1
            
    #print(str(i) + " rules have been extracted")
    return rule_list


# We created a dictionary, in which we store the titles as keys and the content as values. Content consists of the paragraphs
# after the titles
def title_extractor(rule_list):
    rule_dict = dict()
    for i in range(len(rule_list)):
        elements = rule_list[i].split('\r\n', 1)
        rule_dict[elements[0]] = elements[1].replace('\n', '').replace('\r', '')
    
    #print(str(i) + " key-value pairs have been created")
    return rule_dict

# Calling the helper functions
# Defined helper functions are called. 
rule_list = splitter(m_content)
rule_list_b = b_splitter(b_content)

rule_list = rule_list[1:]
rule_list_b = rule_list_b[1:]

rule_dict = title_extractor(rule_list)
rule_dict_b = title_extractor(rule_list_b)

# print extracted titles from Bavaria regulations text
print('extracted titles from Bavaria regulations')
print(rule_dict .keys())

# print extracted titles from Berlin regulations text
print('extracted titles from Berlin regulations:')
print(rule_dict_b .keys())

# Functions for Rule Extarcting
# To extract the information about the distance, the following logic is used: There has to be the word "distance" within the
# respective paragraph which gives the information that we are looking for, and there has to be numeric value which quantifies 
# the distance measure. So we check for the numeric information, and extract the numeric information closest to the given word,
# which is in this case "distance".
def number_finder(rule_text, word):
    word_list = rule_text.split()
    num = word_list.index(word)
    index_list = list()
    
    for i in range(len(word_list)):
        if word_list[i].replace('.','',1).isdigit():
            index_list.append(i)
            
    min_index = min(index_list, key=lambda x:abs(x-num))
    
    print(word + ": " + word_list[min_index] )
    return word_list[min_index]


# Here we check, if the given word is used in the respective paragraph. There has to be the word "mask", if there is an
# obligation about wearing a mask
def check_word(rule_text, word):
    if word in rule_text:
        answer = "Yes"
    else:
        answer = "No"
        
    print(answer + ' ' + word)
    return answer

# Explanation: 
# Manual inspection has to be done for this part. By manual inspection, we can see which part in the text file 
# contains the respective  rule. Then we use the "rule extraction" functions to extract the rules and convert 
# them to first a Pandas DataFrame and then to a CSV file.

# Munich rules
m1 = number_finder(rule_dict['General rule of social distancing, mouth and nose cover'], "distance")
m2 = number_finder(rule_dict['Gastronomy'], "distance")
m3 = check_word(rule_dict['Trade and service companies'], 'mask')
m4 = number_finder(rule_dict['Gastronomy'], "distance")

m_dict = {'State': 'Bayern',
          'General Distance': [m1],
         'Distance in Restaurants': [m2],
         'Masks in Supermarkets': [m3]}
df_m = pd.DataFrame(m_dict, )

# Berlin rules
b1 = number_finder(rule_dict_b['1 Basic Obligations'], "distance")
b2 = number_finder(rule_dict_b['6 Restaurants and Hotels'], "distance")
b3 = check_word(rule_dict_b['2 Compliance with Hygiene Rules'], 'shop')

b_dict = {'State': 'Berlin',
          'General Distance': [b1],
         'Distance in Restaurants': [b2],
         'Masks in Supermarkets': [b3]}
df_b = pd.DataFrame(b_dict, )

result_regulations = pd.concat([df_m , df_b], ignore_index=True)


#######################################
# final dataframe: result_regulations #
#######################################



# Pandascore
def Pandascore(RKI_data,ICU_data):
    rki=RKI_data
    icu=ICU_data

    RKI=pd.concat([rki[["GEN","BL"]], -standardization(rki[["death_rate","cases","deaths","cases7_per_100k"]])], axis=1)
    RKI.columns = ['City','State','Death_rate','Cases','Deaths','Cases7_per_100k']
    ICU=pd.concat([icu['State'], standardization(icu[['Free Beds','Occupancy Ratio']])], axis=1)
    x=pd.merge(RKI,ICU,on='State')
    x['other']=standardization(np.sum(x[['Death_rate','Cases','Deaths','Free Beds','Occupancy Ratio']],axis=1))
    X=x[['City','State','Cases7_per_100k','other']]
    data_new=X[['Cases7_per_100k','other']]
    
    kmeans = KMeans(n_clusters=10)
    kmeans.fit(data_new)
    y_kmeans = kmeans.predict(data_new)
    
    data_new_array=data_new.values
    #plt.scatter(data_new_array[:, 0], data_new_array[:, 1], c=y_kmeans, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    #plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.3);
    
    a=np.sum(centers,axis=1)
    order=np.argsort(a)
    
    pandascore=[]
    for i in range(len(y_kmeans)):
        for j in range(len(order)):
            if y_kmeans[i]==order[j]:
                pandascore.append(j+1)
                
    result_pandascore=pd.DataFrame(result_RKI['GEN'])
    result_pandascore['pandascore']=pandascore
    
    return result_pandascore


result_pandascore = Pandascore(result_RKI,result_ICU)


######################################
# final dataframe: result_pandascore #
######################################

result_pandascore.head(5)


# Combine all into One dataframe
# result_weather, result_RKI, result_regulations, result_ICU
# save
def csv_and_save(dataframe):
    output_address1 = 's3://mountpoint/data-processing/dashboard_data/COMBINED_DATA.csv'
    output_address2 = 's3://datatc2020/processed_data_dashboard/COMBINED_DATA.csv'
    with mox.file.File(output_address1, 'w') as file:
        dataframe.to_csv(file)
    with mox.file.File(output_address2, 'w') as file:
        dataframe.to_csv(file)
    return('saved data to: ', output_address1, 'AND ', output_address2)

# merge all dataframes to one result
# result_ICU['State'] mit result_RKI['BL']
# result_regulations['State'] mit result_RKI['BL']
# result_weather['city'] mit result_RKI['GEN']
result_merge = pd.merge(result_RKI, result_ICU, left_on='BL', right_on='State')
result_merge = pd.merge(result_merge, result_regulations, left_on='BL', right_on='State', how='left')
result_merge = pd.merge(result_merge, result_weather, left_on='GEN', right_on='city', how='left')
result_merge = pd.merge(result_merge, result_pandascore, left_on='GEN', right_on='GEN', how='left')

csv_and_save(result_merge)

