### Web-Scrapper cli application

## Description

this application is designed to scrap 2 websites [databasesets.com](https://tun.databasesets.com/) and [ecoles](https://www.ecoles.com.tn/) to collect data about primary schools in Tunisia.
the output data is in a csv file contains (school name, Private or Public, Quality).

## Dependencies
`beautifulsoup4` `requests`
```shell
  pip3 install beautifulsoup4 requests
  # or
  pip install beautifulsoup4 requests 
```

## How to use
```shell
    # to start collection data 
    python get_data.py # by default data will be found in $(pwd)/data/output.csv
    
    # to run cmd in silent mode
    python get_data.py --silent
    
    python get_data.py --speed=1 # select speed from 1,2,3 the smallest the fastest

```