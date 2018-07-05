from PersistenFetcher import PersistentFetcher
from dataProvider import DataProvider
from networkGenerator import generate
from math import isnan as nan
import math
print("lets go")
fetcher = PersistentFetcher("/home/ps/PycharmProjects/evo-feature-engineer/data")
dataProvider = DataProvider(fetcher)
data = dataProvider.getData(None, None)
net = generate(data, 9)
lRate, oscillations, lwp, mse = 0.001, 0, True, 101
iters = 0
while (mse > 1 and iters < 10):
    print("ITERATION: ", iters)
    sum_e = 0
    nans = 0
    for d in data:
        lRate, oscillations, lwp, e = net.interation(d.x, d.y, lRate, oscillations, lwp)
        if (nan(e)):
            nans +=1
        else:
            sum_e += e
    iters += 1
    valids = len(data) - nans
    mse = sum_e / (valids) if valids > 0 else -1
    print("NaNs: ", nans)
    print("mean absolute error: ", math.sqrt(mse))

mean = sum([d.y for d in data]) / len(data)
print("Mean ", mean)
var = sum([(d.y - mean)**2 for d in data]) / len(data)
print("Standard variantion, " ,math.sqrt(var))
print("Variance ,", var)
pred = net.predict(data[0].x)
print("predicted :", pred)
print("actual: ", data[0].y)
