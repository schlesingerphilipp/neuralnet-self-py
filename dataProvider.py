from datetime import datetime
from datetime import date
import json
def mapByDate(tenObs):
    map = {}
    for id in tenObs:
        features = tenObs[id]
        observations = [OneObservation(feature, id) for feature in features]
        obs = [o for o in observations if o.val is not None]

        for o in obs:
            if (o.date not in map):
                map[o.date] = []
            map[o.date].append(o)
    return map

class OneObservation:
    def __init__(self, obs, id):
        self.id = id
        try:
            self.val = float(obs['value'])
        except ValueError:
            self.val = None
            print("illegal value: ", obs['value'])
        self.date = datetime.strptime(obs['date'],"%Y-%m-%d")
class Target:
    def __init__(self, target, d):
        self.open = target['Open']
        self.close = target['Close']
        self.date = d


class Observation:
    def __init__(self, obs, target, keys, date):
        self.x = {key:None for key in keys}
        for o in obs:
            self.x[o.id] = o.val
        self.y = target['Open']
        self.date = date

def zipTarget(obsMap, targetMap, keys):
    obs = []
    for date in obsMap:
        if date in targetMap:
            obs.append(Observation(obsMap[date], targetMap[date], keys, date))
    return sorted(obs, key= lambda x: x.date)

def mapTarget(df):
    jsonstr = df.to_json()
    map = json.loads(jsonstr)
    #{un:{30:"",28:""
    m = {}
    for fieldName in map:
        field = map[fieldName]
        for index in field:
            if index not in m:
                m[index] = {}
            m[index][fieldName] = field[index]
    mapByDate = {}
    for index in m:
        entry = m[index]
        datestr = entry["Unnamed: 0"]
        ymd, hms = datestr.split(" ")
        d = datetime.strptime(ymd, "%Y-%m-%d")
        del entry["Unnamed: 0"]
        mapByDate[d] = entry
    return mapByDate

def combineData(features, targets):
    datedFeatures = mapByDate(features)
    targetMap = mapTarget(targets)
    keys = [id for id in features]
    data = zipTarget(datedFeatures, targetMap, keys)
    fillEmpty(data, keys)
    return data
def fillEmpty(data, keys):
    lastValues = {key:None for key in keys}
    fillWith(data, lastValues)
    reversed = sorted(data, key=lambda x: x.date, reverse = True)
    fillWith(reversed, lastValues)
    for d in reversed:
        for i in d.x:
            if (d.x[i] is None):
                d.x[i] = 0
    return sorted(reversed, key=lambda x: x.date, reverse = False)

def fillWith(data, lastValues):
    for d in data:
        for i in d.x:
            if (d.x[i] is not None):
                lastValues[i] = d.x[i]
            else:
                d.x[i] = lastValues[i]
    return data
class DataProvider:
    def __init__(self, fetcher):
        self.fetcher = fetcher
    def getData(self, fromDate, toDate):
        end = toDate if toDate is not None else datetime.today()
        start = fromDate if fromDate is not None else date(end.year - 1, end.month, end.day)
        features = self.fetcher.fetchFeatures(start, end)
        targets = self.fetcher.fetchTargets(start, end)
        return combineData(features, targets)