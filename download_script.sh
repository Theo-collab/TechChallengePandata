#!/bin/bash

# README:
#
# change the location after cd like:
# cd /where/ever/you/want
#
# change file permissions before using with:
# chmod +x download_skript.sh
#
# --- 
# we can schedule this script at 1:10 am with e.g. crontab with:
# crontab -e
# 10 1 * * * ./download_skript.sh
#
# alternatively we can use a while loop with a 24h sleep at the end

# move to the correct location
cd /root/TechChall/data

# get most recent ICU data
curl -o ICU-$(date "+%Y-%m-%d") --location --request GET 'https://www.intensivregister.de/api/public/intensivregister'
# update most recent ICU data
curl --location --request GET 'https://www.intensivregister.de/api/public/intensivregister' > ICU

# get most recent RKI data
curl -o RKIjson-$(date "+%Y-%m-%d") --location --request GET 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=cases,deaths,cases_per_100k,BL,BL_ID,county,cases_per_population,last_update,cases7_per_100k,recovered,OBJECTID&returnGeometry=false&outSR=4326&f=json'
# update most recent RKI data
curl --location --request GET 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=cases,deaths,cases_per_100k,BL,BL_ID,county,cases_per_population,last_update,cases7_per_100k,recovered,OBJECTID&returnGeometry=false&outSR=4326&f=json' > RKIjson

# get most recent RKI data - CSV version
curl -o RKIcsv-$(date "+%Y-%m-%d") --location --request GET 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv'
# update most recent RKI data - CSV version
curl --location --request GET 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv' > RKIcsv

# ICU by Bundesland
curl --location --request GET 'https://diviexchange.z6.web.core.windows.net/laendertabelle1.svg' > ICU.svg
inkscape ICU.svg --export-png=ICU.png
tesseract ICU.png ICU

# weather data from openweather API
# Munich
curl --location --request GET 'api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly&units=metric&appid=f05227b503da5eab599a2252ca7e2187&lat=48.13743&lon=11.57549' > WEATHER_munich
# Berlin
curl --location --request GET 'api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly&units=metric&appid=f05227b503da5eab599a2252ca7e2187&lat=52.520008&lon=13.404954' > WEATHER_berlin
# Nuernberg
curl --location --request GET 'api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly&units=metric&appid=f05227b503da5eab599a2252ca7e2187&lat=49.460983&lon=11.061859' > WEATHER_nuernberg
# HongKong
curl --location --request GET 'api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly&units=metric&appid=f05227b503da5eab599a2252ca7e2187&lat=22.302711&lon=114.177216' > WEATHER_hongkong