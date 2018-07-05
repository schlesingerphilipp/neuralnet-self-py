import math
class Linear:
    def calc(self, valueWeightTuples):
        return sum([(x * w) for (x,w) in valueWeightTuples])
    def derivative(self, out):
        return 1 #in this context a linear function is no function, as the weights and sum is already in derivative

class Logistic:
    def calc(self, valueWeightTuples):
        z = sum([(x * w) for (x,w) in valueWeightTuples])
        if (z > 100):
            return 1
        elif (z < -100):
            return 0
        return 1 / (1 + math.exp(-1 * z))
    def derivative(self, out):
        return out * (out -1)

