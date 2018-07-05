import pandas as pd
import os
import json
from Fetcher import Fetcher

class PersistentFetcher(Fetcher):
    def __init__(self, dataDir):
        self.dataDir = dataDir

    def getPath(self, start, end, suffix):
        return "{}/features{}_{}.{}".format(self.dataDir, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), suffix)

    def fetchTargets(self, start, end):
        path = self.getPath(start, end, "csv")
        if (os.path.isfile(path) ):
            return pd.read_csv(path)
        else:
            targets = super().fetchTargets(start, end)
            targets.to_csv(path_or_buf=path)
            return targets

    def fetchFeatures(self, start, end):
        path = self.getPath(start, end, "json")
        if (os.path.isfile(path) ):
            with open(path) as data_file:
                return json.load(data_file)
        else:
            features = super().fetchFeatures(start, end)
            with open(path, "w")  as data_file:
                json.dump(features, data_file)
                data_file.close()
                return features