from random import randint
from network3 import Node, Network
from math import isnan as nan
nodes = []
nodes.append(Node('out', [], {1:2, 2:-2,3:0.1}))
nodes.append(Node(1, ['out'], {11:2}))
nodes.append(Node(2, ['out'], {11:4,22:3}))
nodes.append(Node(3, ['out'], {22:-1}))
nodes.append(Node(11, [1,2], {}))
nodes.append(Node(12, [2,3],{}))
nodes.append(Node(13, [2,3],{}))
nodes.append(Node(14, [2,3],{}))
nodes.append(Node(15, [2,3],{}))
nodes.append(Node(16, [2,3],{}))

net = Network({node.id : node for node in nodes})
targetFunc = lambda X : 3 * X[0] - 2 * (2*X[0] + 3* X[1]) + 10 * X[1]
X = [[randint(0,9),randint(0,9)] for x in range(1,500)]
lRate, oscillations, lwp, mse = 1, 0, True, 101
iters = 0
while (mse > 100 and iters < 10):
    print("ITERATION: ", iters)
    sum_e = 0
    nans = 0
    for i in range(0, len(X)):
        inputs = {11:X[i][0], 22:X[i][1]}
        lRate, oscillations, lwp, e = net.interation(inputs, targetFunc(X[i]), lRate, oscillations, lwp)
        if (nan(e)):
            nans +=1
        else:
            sum_e += e
    iters += 1
    valids = len(X) - nans
    mse = sum_e / (valids) if valids > 0 else -1
    print("NaNs: ", nans)
    print("mse: ", mse)
if (False):
    for key in net.nodes:
        node = net.nodes[key]
        print("Node: ", node.id)
        print("Ws: ", node.weights)