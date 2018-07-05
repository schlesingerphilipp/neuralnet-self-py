from fed_data import getSeriesIds, getObservations
from gFinance import getGdata
from stockCrawler import getNASQIds

class Fetcher:
    def __init__(self):
        self.id = "asasdf"

    def fetchFeatures(self, start, end):
        fedEnd = end.strftime("%Y-%m-%d")
        fedStart = start.strftime("%Y-%m-%d")
        series = getSeriesIds(search_text="trade", realtime_start=fedStart, realtime_end=fedEnd)
        features = {series[i]['id']: getObservations(series[i]['id'], fedStart, fedEnd) for i in range(0, 10)}
        return features

    def fetchTargets(self, start, end):
        j = 8
        targetIds = getNASQIds()
        df = getGdata(targetIds[5]['symbol'], 86400, 'NASD', '1Y')
        return df