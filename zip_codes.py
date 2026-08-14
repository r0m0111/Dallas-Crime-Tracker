import requests
import json
import datetime



#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

def main():
    ZIP_CODES={}
    MONTHS={1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("www.dallasopendata.com", "rPRXH917VkPlfDQv6olYk5Hx4",
                    username="youremailapi",
                    password="yourpasswordapi",timeout=60)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(www.dallasopendata.com,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.

    x=datetime.datetime.now()

    year1=int(x.strftime("%Y"))
    year2=int(x.strftime("%Y"))

    current_month=int(x.strftime("%m"))
    if(current_month==1):
        current_month=13
        year1=year1-1
        year2=year2-1

    last_month=int(current_month)-1
    if(last_month==1):
        current_month=14
        year2=year2-1

    compare_month=int(current_month)-2




    results = client.get("qv6i-rri7", limit=20000,where=f"month1 = '{MONTHS[last_month]}' AND year1='{year1}'")
    compare = client.get("qv6i-rri7", limit=20000,where=f"month1 = '{MONTHS[compare_month]}' AND year1='{year2}'")
    # print(json.dumps(results,indent=2))



    # Convert to pandas DataFrame
    # results_df = pd.DataFrame.from_records(results)

    # print(results_df["incidentnum"]) #use to_list()

    lastm_crime=0
   
    for i in results:
        
        lastm_crime=lastm_crime+1

        zip_code = i.get("zip_code")

        if not zip_code:
            continue

        if zip_code in ZIP_CODES:
            ZIP_CODES[zip_code] += 1
        else:
            ZIP_CODES[zip_code] = 1

                

    comp_crime=0
    for i in compare:
        comp_crime=comp_crime+1
      

    percent=percent_change(lastm_crime,comp_crime)
    percent=float(percent)

    if(percent<0):
        percent=percent*-1
        print(f"Crime was down {percent:.2f}% in Dallas from {MONTHS[compare_month]} {year2} to {MONTHS[last_month]} {year1}")

    else:
        print(f"Crime was up {percent:.2f}% in Dallas from {MONTHS[compare_month]} {year2} to {MONTHS[last_month]} {year1}")

    max=1
    zip_code=""
    for i in ZIP_CODES:
        if(ZIP_CODES[i]>max):
            max=ZIP_CODES[i]
            zip_code=i
        

    print(f"With zip code {zip_code} being the most active area last month with over {max} reported crimes")

def percent_change(new,original):
    percent= (new-original)

    return (percent/original)*100
    


main()





