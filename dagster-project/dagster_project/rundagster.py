import pandas as pd
import requests
import os

from dagster  import job, MetadataValue, Output, asset

def get_domain(url):
    return url.split("://")[1].split("/")[0]

@asset
def get_domain_of_url():
    curpath = os.getcwd()
    #print(curpath)
    data = pd.read_csv(f'{curpath}//DATA//original.csv')
    data['domain_of_url'] = data['url'].apply(get_domain)
    data.to_csv(f'{curpath}//DATA//result1.csv')
    return data

@job
def run_dagster():
    get_domain_of_url()