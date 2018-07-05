from random import randint
from math import isnan as nan
printOut = False
printW = True
printD = False
printT = False
class Node:
    def __init__(self, id, children, weights, function):
        self.id = id
        self.parents = [key for key in weights]
        self.children = children
        self.weights = weights
        self.function = function
        self.delta_E_out = False
        self.out = False
        self.hasNan = False
    def delta_E(self, target, nodes, inputs):
        if (self.delta_E_out != False):
            return self.delta_E_out
        if (len(self.children) == 0):
            self.delta_E_out = target - self.getOut(inputs, nodes)
            if (printOut):
                print("\nout: ", self.out)
            if (printD):
                print("\nDELTA:: ", self.delta_E_out)
        else:
            self.delta_E_out = self.function.derivative(self.out) * sum(nodes[i].delta_E(target, nodes, inputs) for i in self.children)
        return self.delta_E_out

    def cleanUp(self):
        self.delta_E_out = False
        self.out = False


    def getOut(self, inputs, nodes):
        if (self.out != False):
            return self.out
        if (len(self.parents) == 0):
            self.out = inputs[self.id]
        else:
            valueWeightTuples = [(nodes[i].getOut(inputs, nodes), self.weights[i]) for i in self.parents]
            self.out = self.function.calc(valueWeightTuples)
            self.hasNan = False
            if (nan(self.out)):
                print("NAN in ", self.id)
                self.hasNan = True
                self.out = 0
        return self.out

    def delta_Wi(self, inputs, nodes, target, i):
        if (i not in inputs):
            inputs[i] = nodes[i].getOut(inputs, nodes)
        delta =  inputs[i] * self.delta_E(target, nodes, inputs)
        return delta


class Network:
    def __init__(self, nodes):
        self.nodes = nodes

    def interation(self, inputs, target, lRate, oscillations, lwp):
        if (printT):
            print("in: ", inputs, " target: ", target)
        for i in self.nodes:
            node = self.nodes[i]
            weightsOld = node.weights
            node.weights = {
            parentNodeId: node.weights[parentNodeId] + (lRate * node.delta_Wi(inputs, self.nodes, target, parentNodeId))
            for parentNodeId in node.weights}
            for id in node.weights:
                if (nan(node.weights[id])):
                    print("NaN WEight ", id)
                    node.weights[id] = 0
        for i in self.nodes:
            if (i == 'out'):
                out = self.nodes[i]
                if (out.hasNan):
                    e = float('nan')
                else:
                    try:
                        e = (target - out.out) ** 2
                    except OverflowError:
                        e = float('nan')
                if (lwp and out.delta_E_out < 0):
                    lwp = False
                    oscillations += 1
                elif (not lwp and out.delta_E_out > 0):
                    lwp = True
                    oscillations += 1
            self.nodes[i].cleanUp()
        if (oscillations > 5):
            lRate *= 0.9
            oscillations = 0
        return (lRate, oscillations, lwp, e)


    def predict(self, inputs):
        for i in self.nodes:
            self.nodes[i].cleanUp()
        return self.nodes['out'].getOut(inputs, self.nodes)
