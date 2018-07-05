import urllib.request
import json

from requests import HTTPError


def getSeriesIds(search_text = False, realtime_start= False, realtime_end= False):
    endpoint = "series/search"
    params = makeParams(None, search_text=search_text, realtime_start=realtime_start, realtime_end=realtime_end)
    return makeRequest(endpoint, params)['seriess']

def getObservations(id, observation_start= False, observation_end= False):
    endpoint = "series/observations"
    params = makeParams(id=id, observation_start=observation_start, observation_end=observation_end)
    return makeRequest(endpoint, params)['observations']


def makeParams(id=None, search_text=None, realtime_start=None, realtime_end=None, observation_start=None, observation_end=None):
    params = ""
    if (id):
        params += "&series_id=" + id
    if (search_text):
        params += "&search_text=" + search_text
    if (realtime_start):
        params += "&realtime_start=" + realtime_start
    if (realtime_end):
        params += "&realtime_end=" + realtime_end
    if (observation_start):
        params += "&observation_start=" + observation_start
    if (observation_end):
        params += "&observation_end=" + observation_end
    return params

def makeRequest(endpoint, params):
    url = "https://api.stlouisfed.org/fred/" + endpoint + "?file_type=json&api_key=29a9fb85f111c9bafaba7882cf57c4ca" + params
    try:
        content = urllib.request.urlopen(url).read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(url)
        raise e

#print(getSeriesIds(search_text="trade",observation_start="2018-01-01", observation_end="2018-06-06"))