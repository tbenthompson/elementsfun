class Node(object):
    def __init__(self, pos, idx):
        self.pos = pos
        self.idx = idx
        self.boundary = ''
    
    def isBoundary(self):
        return self.isDirichlet() or self.isNeumann()
    
    def isDirichlet(self):
        return self.boundary == 'dirichlet'
    
    def isNeumann(self):
        return self.boundary == 'neumann'
    
    def setBoundaryType(self, name):
        self.boundary = name
    
    def evaluateWith(self, function):
        return function(self.pos[0], self.pos[1])

    def getVectorTo(self, othernode):
        deltax = othernode.pos[0] - self.pos[0]
        deltay = othernode.pos[1] - self.pos[1]
        return [deltax, deltay]
