import numpy as np
import numpy.linalg as la

class Edge(object):        
    #DON'T CALL THIS DIRECTLY, USE newEdge
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        
    def node1(self):
        return self.nodes[0]
    
    def node2(self):
        return self.nodes[1]

    def getNormal(self, triangle):
        v = np.array(self.nodes[0].getVectorTo(self.nodes[1]))
        normal = np.array([v[1], -v[0]]) / la.norm(v)
        thirdNode = triangle.getThirdNode(self.nodes[0],self.nodes[1])
        othervector = np.array(self.nodes[0].getVectorTo(triangle.getThirdNode(self.nodes[0],self.nodes[1])))
        if normal.dot(othervector) >= 0:
            normal = -normal
        return normal

