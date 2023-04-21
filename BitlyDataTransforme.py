#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import re, datetime
import  sys
import getopt
import time
import argparse
import pathlib
#record start time


st = time.time()
# def myfunc(argv):
#
#     arg_unix = ""
#     arg_help  = "{0} Enter script name followd by path to JSON file and/or -U to convert time stamp to unix format".format(argv[0])
#
#
#     try:
#         opts, args = getopt.getopt(argv[2:], "hu", ["help","unix"])
#     except:
#         print(arg_help)
#         sys.exit(2)
#
#     for opt, arg in opts:
#         if opt in ("-h", "--help"):
#             print(arg_help)  # print the help message
#             sys.exit(2)
#         elif opt in ("-u", "--unix"):
#             arg_unix = True
#
#     return arg_unix
# unix = myfunc(sys.argv)
# json_file = sys.argv[1]

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Enter the right path to json fie")
parser.add_argument("-u", "--unix", action="store_true" , default=False)
args = parser.parse_args()
unix =""
if args.unix:
    unix =True

json_file = args.file

temp_df = pd.read_json(json_file, lines=True)


# create empty dataframe
BitlyDF = pd.DataFrame()


# extract browser

def extract_browser(string):
    browser_regex = r'([A-Za-z]+.[0-9]+\.[0-9]+)'
    match = re.search(browser_regex, string)
    if match:
        return match.group(1)
    else:
        return "NotFound"


BitlyDF['web_browser'] = temp_df['a'].apply(extract_browser)


# extract OS
def extract_os(string):
    os_regex = r'\((Windows|Macintosh|Ubuntu)[^)]+\)'
    # os_regex = r'\(([^)]*?)\)'
    match = re.search(os_regex, string)
    if match:
        return match.group(1)
    else:
        return "NotFound"


BitlyDF['operating_sys'] = temp_df['a'].apply(extract_os)


# extract  URL where user come from
def extract_url(string):
    url_regex = r'([A-Za-z]+(\.[A-Za-z]+)+)'
    match = re.search(url_regex, string)
    if match:
        return match.group(1)
    else:
        return "NotFound"


BitlyDF['from_url'] = temp_df['r'].apply(extract_url)

# extract URL where the user headed to
BitlyDF['to_url'] = temp_df['u'].apply(extract_url)


# extract city where request come from
def extract_city(string):
    city_regex = r'([^"]*)'
    match = re.search(city_regex, str(string))
    if match:
        return match.group(1)
    else:
        return 'NotFound'


BitlyDF['city'] = temp_df['cy'].apply(extract_city)


# extract the longitude
def extract_longt(string):
    longt_regex = r'([0-9]+\.[0-9]+)'

    match = re.search(longt_regex, str(string))
    if match:
        return match.group(1)
    else:
        return "NotFound"


BitlyDF['longitude'] = temp_df['ll'].apply(extract_longt)


# extract latitude
def extract_latt(string):
    latt_regex = r',\s(-?[0-9]+\.[0-9]+)'

    match = re.search(latt_regex, str(string))
    if match:
        return match.group(1)
    else:
        return "NotFound"


BitlyDF['latitude'] = temp_df['ll'].apply(extract_latt)


# extract time zone
def extract_tmzn(string):
    time_regex = r'([^"]*)'
    match = re.search(time_regex, str(string))
    if match:
        tz = match.group(1).replace("_", "")
        if tz != "":
            return tz
    else:
        return "NotFound"


BitlyDF['time_zone'] = temp_df['tz'].apply(extract_tmzn)

# extract Time when the request started
def extract_t(string):
    tin_regex = r'([0-9]+)'
    match = re.search(tin_regex, str(string))

    if match:
        timestamp = datetime.datetime.fromtimestamp(int(match.group(1)))
        if unix:
            return int(timestamp.timestamp())
        else:
            return timestamp.strftime('%Y/%m/%d %H:%M:%S')

    else:
        return "NotFound"

BitlyDF['time_in'] = temp_df['t'].apply(extract_t)

# extract Time when the request is ended
BitlyDF['time_out'] = temp_df['hc'].apply(extract_t)


count_rows = len(BitlyDF)
print(count_rows, ' row converted')
csvname =re.search(r'([A-Za-z0-9]+)' , json_file)
csvname = csvname.group(1)+'.csv'
BitlyDF.to_csv(csvname)

print('CSV File Saved at -->', pathlib.Path().resolve())
# record end time of excutoin
et = time.time()
print('CPU excution time = ', round((et-st)*1000,2) , ' mille Seconds')

