#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import csv
import time
import datetime
import tempfile
import pandas as pd

if sys.version_info[0] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

class InputError(Exception):
    """Exception raised for errors in the input."""
    pass

def daymet_timeseries(lat=36.0133, lon=-84.2625, start_year=2012, end_year=2014, 
                      as_dataframe=True, download_dname=None, verbose=False):
    '''Download a Daymet timeseries for a single location as either a local csv or pandas dataframe

    Keyword arguments:
    lat -- geographic latitude of location for timeseries,  must be within Daymet extent
    long -- geographic longitude of location for timeseries,  must be within Daymet extent
    start_yr -- timeseris will begin on January 1st of this year ( >= 1980)
    end_yr -- timeseris will end on December 31st of this year ( < Current year)
    as_dataframe -- if True return a pandas data frame of the timesereis
                    if False return a local path to the CSV downloaded
    download_dname -- The local directory to save the downloaded csv into
                    if none specified saves the file into the temp workspace
                    returned by tempfile.gettempdir()
    '''
    max_year = datetime.datetime.now().year - 1 
    MIN_YEAR = 1980 #The begining of the Daymet time series

    if start_year < MIN_YEAR:
        raise InputError("start_yr specified ({}) is before the start of data period, {}".format(start_year, MIN_YEAR))
    if end_year > max_year:
        raise InputError("end_yr specified ({}) is after the end of data period".format(end_year))
    if not download_dname:
        download_dname = tempfile.gettempdir() 
    if not os.path.exists(download_dname):
        raise InputError("The directory fof downloading data does not exist on the filesysptem ({})".format(download_dname))
    
    year_range = ",".join([str(i) for i in range(start_year, end_year+1)])

    # create download string / url
    TIMESERIES_URL = "https://daymet.ornl.gov/single-pixel/api/data?lat={lat}&lon={lon}&vars=tmax,tmin,dayl,prcp,srad,swe,vp&year={year_range}"
    timeseries_url = TIMESERIES_URL.format(lat=lat, lon=lon, year_range=year_range)
      
    if verbose:
        print("Daymet webservice URL:\n{}".format(timeseries_url))
        
    # create filename for the output file
    daymet_file = "Daymet_{}_{}_{}_{}.csv".format(lat, lon, start_year, end_year) 
    daymet_file = os.path.join(download_dname, daymet_file)
    
    if verbose:
        print("File downloaded to:\n{}".format(daymet_file))

    # download the daymet data (if available), depending
    # on the python version you need to trap an http error
    try:
        urlretrieve(timeseries_url, daymet_file)
    except:
        if os.path.isfile(daymet_file):
            os.remove(daymet_file)

        raise NameError("You requested data is outside DAYMET coverage, the file is empty --> check coordinates!")

    # check if the file can be read (if not raise error)
    try:
        df = pd.read_csv(daymet_file, header=6)
    except:
        if os.path.isfile(daymet_file):
            os.remove(daymet_file)

        raise NameError("You requested data is outside DAYMET coverage, the file is empty --> check coordinates!")
 
    if as_dataframe:
        df.index = pd.to_datetime(df.year.astype(int).astype(str) + '-' + df.yday.astype(int).astype(str), format="%Y-%j")
        df.columns = [c[:c.index('(')].strip() if '(' in c else c for c in df.columns ]
        return df
    else:
        return daymet_file


def download_Daymet(site="Daymet",lat=36.0133,lon=-84.2625,start_yr=1980,end_yr=2012, as_dataframe=True):
    """
    Function to read download daymet data for a single pixel location
    """
    
    # calculate the end of the range of years to download
    max_year = int(time.strftime("%Y"))-2

    # check validaty of the range of years to download
    # I'm not sure when new data is released so this might be a
    # very conservative setting, remove it if you see more recent data
    # on the website
    if start_yr >= 1980 & end_yr <= max_year:        
    
        # if the year range is valid, create a string of valid years
        year_range = range(start_yr, end_yr)
    
        # convert to string and strip the brackets and spaces
        year_range = str(year_range).strip('[]')
        year_range = year_range.replace(' ','')

        # create download string / url
        download_string = "https://daymet.ornl.gov/single-pixel/api/data?lat=my_lat&lon=my_lon&vars=tmax,tmin,dayl,prcp,srad,swe,vp&year=year_range"
  
        # substitute input variables in download string
        download_string = download_string.replace("my_lat",str(lat))
        download_string = download_string.replace("my_lon",str(lon))
        download_string = download_string.replace("year_range",year_range)
  
        # create filename for the output file
        daymet_file = str(site)+"_"+str(start_yr)+"_"+str(end_yr)+'.csv' 
  
        # download the daymet data (if available), depending
        # on the python version you need to trap an http error
        try:
            urlretrieve(timeseries_url, daymet_file)
        except:
            if os.path.isfile(daymet_file): 
                os.remove(daymet_file)
            raise NameError("You requested data is outside DAYMET coverage, the file is empty --> check coordinates!")

        # check if the file can be read (if not raise error)
        try:
            df = pd.read_csv(daymet_file, header=6)
        except:
            if os.path.isfile(daymet_file):
                os.remove(daymet_file)
            raise NameError("You requested data is outside DAYMET coverage, the file is empty --> check coordinates!")
 
        if as_dataframe:
            df.index = pd.to_datetime(df.year.astype(int).astype(str) + '-' + df.yday.astype(int).astype(str), format="%Y-%j")
            df.columns = [c[:c.index('(')].strip() if '(' in c else c for c in df.columns ]
            return df
        else:
            return daymet_file

    else:
        raise NameError("Year values are out of range!")

if __name__ == "__main__":
    
    # set maximum year -- or update according to the website's
    # info
    max_year = int(time.strftime("%Y"))-2

    # create empty matrix
    sites = []   
    
    # the file name with sites should be the first argument to the
    # program executed without the python command
    my_sites_file = sys.argv[1]

    # do a basic check to see if the file exists, does not check if it
    # is comma separated or contains the correct data, you are on your own
    # there
    if os.path.isfile(my_sites_file):    
        with open(my_sites_file, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                sites.append(row)
    
    for site in sites:
        try:
            download_Daymet(site=str(site[0]),lat=site[1],lon=site[2],start_yr=1980,end_yr=max_year)
        except NameError:
            print("Error: check error messages!")
            
            # uncomment if you want extensive debugging info
            # raise 
