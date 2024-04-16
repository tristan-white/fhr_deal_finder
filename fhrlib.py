import requests
import time
import json
import datetime
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import cloudscraper

SLEEPTIME = 10
US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]
REGIONS = [
    "United States", "South America", "Europe", "Asia Pacific", "Middle East", "Middle East and Africa"
]
URL = 'https://www.amextravel.com/api/hotel_searches'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Cache-control': 'no-store, max-age=0',
    'Pragma': 'no-cache',
    'Origin': 'https://www.amextravel.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
}
DATA = {
    "hotel_search": {
        "end_date": "",
        "hotel_ids": [],
        "hotel_search_rooms_attributes": [
            {
                "child_ages": [],
                "number_adults": 2,
                "number_children": 0
            }
        ],
        "is_dateless": False,
        "location_name": "",
        "location_type": "STATE",
        "location_xid": "",
        "modifier": "FHR",
        "order_by": 66,
        "referrer": "",
        "start_date": "",
        "user_timezone": "UTC-04:00",
        "sort_direction": 2
    },
    "partner_programs": ""
}

def formatReqData(start_date: str, region: str=None, state: str=None, city: str = None) -> dict:
    req_data = DATA.copy()
    if city:
        assert city[0].isupper() and city[1:].islower()
        assert state in US_STATES
        location_name = f"{city}, {state}, United States"
        req_data["hotel_search"]["location_type"] = "CITY"
    elif state:
        assert state in US_STATES
        location_name = f"{state}, United States"
        req_data["hotel_search"]["location_type"] = "STATE"
    else:
        assert region in REGIONS
        location_name = region
        req_data["hotel_search"]["location_type"] = "REGION"


    req_data["hotel_search"]["start_date"] = start_date.isoformat()
    req_data["hotel_search"]["location_name"] = location_name
    end_date = start_date + datetime.timedelta(days=1)
    req_data["hotel_search"]["end_date"] = end_date.isoformat()
    return req_data

"""
Get json data about hotels in a state.
This function makes a request to amextravel.com, receives json, then 
"""
def getStateJsonForDate(url: str, req_json: dict) -> dict:
    holdUp() # prevent throttling:

    scraper = cloudscraper.create_scraper()

    response = scraper.post(url, headers=HEADERS, json=req_json, allow_redirects=True)
    if response.status_code == 512:
        # no hotels for this night
        return {}
    if response.status_code != 200:
        print(f"Unexpected response code: {response.status_code}")
    try:
        state_data = json.loads(response.text)
    except:
        print("Unable to convert reponse text to json.")
        print(f"Response code: {response.status_code}")
        print("Reponse text:\n\n")
        print(response.text)
        exit(1)
    return state_data

def getRegionJsonForDate(URL: str, req_data: dict):
    holdUp() # prevent throttling
    r1 = requests.post(URL, headers=HEADERS, json=req_data, allow_redirects=True)
    holdUp() # prevent throttling

    if r1.status_code != 200:
        print(f"Unexpected response code: {r1.status_code}")
    r1_json = json.loads(r1.text)
    id = r1_json['id']

    r2 = requests.get(url=f"{URL}/{id}?promotion_token=&extlink=&size=1000", headers=HEADERS, cookies=r1.cookies, allow_redirects=True)
    region_data = json.loads(r2.text)
    return region_data
    
def jsonToDataFrame(json_input: dict) -> pd.DataFrame:
    ret = []
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    i = datetime.datetime.fromisoformat(json_input["start_date"]).weekday()
    day = weekdays[i]
    for h in json_input["hotels"]:
        ret.append(
            {
                "name": h["name"],
                "date": json_input["start_date"],
                "weekday": day,
                "location": json_input["location_name"],
                "lowest_rate": "",
                "taxes_and_fees": "",
                "city": h["address"]["city_name"],
                "state": h["address"]["state_province_code"],
                "latitude": h["geocoding"]["latitude"],
                "longitude": h["geocoding"]["longitude"],
            }
        )
        if h["availability_status"] == "AVAILABLE":
            ret[-1]["lowest_rate"] = h["room_with_all_rates"]["lowest_nightly_rate"]["cents"] // 100
            ret[-1]["taxes_and_fees"] = h["room_with_all_rates"]["display_rate"]["total_taxes_and_fees"]["cents"] // 100
    return pd.DataFrame(ret)

def holdUp():
    return
    # prevent throttling
    print("Waiting momentarily to prevent throttling...", end="", flush=True)
    for i in range(SLEEPTIME):
        print(".", end="", flush=True)
        time.sleep(1)
    print()

# returns a dataframe with price info for the location across the dates
def getDfForDatesInLoc(state: str, start_date: datetime.date, end_date: datetime.date, city: str=None, fname: str=None, region: str=None) -> pd.DataFrame:
    assert start_date >= datetime.date.today()
    assert end_date > start_date

    eta = SLEEPTIME * (end_date - start_date).days / 60
    if region:
        eta *= 2
    print(f"Estimated search time: {eta} minutes.\n")

    df = pd.DataFrame()
    while (start_date != end_date):
        print(f"Getting data for {start_date}")
        # format request data
        req_data = formatReqData(start_date, region, state, city)
        # make request
        if not state:
            response_json = getRegionJsonForDate(URL, req_data)
        else:
            response_json = getStateJsonForDate(URL, req_data)
        if not response_json:
            continue
        # convert response json to dataframe
        cur_df = jsonToDataFrame(response_json)
        if cur_df.empty == True:
            continue
        # update df
        df = pd.concat([df, cur_df], ignore_index=False)
        # save dataframe to csv file
        if fname:
            df.to_csv(fname, index=False)

        # increment date
        start_date += datetime.timedelta(days=1)
    return df 

def dfToFig(df: pd.DataFrame) -> go.Figure:
    fig = px.line(df, x="date", y="lowest_rate", color="name", symbol="name", 
                  hover_data=["taxes_and_fees", "city", "state", "weekday"])
    cur = datetime.datetime.now().date().isoformat()
    start = df.iloc[0]['date']
    end = df.iloc[-1]['date']
    fig.update_layout(title_text=f"Data Queried on {cur} for {start} to {end}")
    return fig

def csvToFig(filename: str) -> go.Figure:
    df = pd.read_csv(filename)
    return dfToFig(df)