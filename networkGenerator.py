from network3 import Node, Network
from Functions import Logistic, Linear
import numpy as np
def generate(data, layers):
    nodes = {}
    inputKeys = [key for key in data[0].x]
    lastLayer = []
    for i in range(-1,layers):
        children = ["{}{}".format(i+1,j) for j in range(1,9)] if i+1 < layers else ['out']
        weights = {"{}{}".format(i-1,j) : np.random.rand(1,1)[0][0] for j in range(1,9) } if i > 0  else {key : np.random.rand(1,1)[0][0] for key in inputKeys}
        if i == -1:
            weights = {}
        layer = [Node("{}{}".format(i,j), children, weights, Logistic()) for j in range(1,9)] if i >= 0 else [Node(key, children, weights, Logistic()) for key in inputKeys]
        i = i if i >= 0 else "in"
        nodes[i] = layer
        lastLayer = layer
    nodes['out'] = [Node('out', [], {node.id : np.random.rand(1,1)[0][0] for node in lastLayer}, Linear())]
    nodeMap = {}
    for layerKey in nodes:
        for node in nodes[layerKey]:
            nodeMap[node.id] = node
    return Network(nodeMap)
