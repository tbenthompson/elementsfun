from edge import Edge
from node import Node
import numpy as np

class Triangle(object):
    def __init__(self, node1, node2, node3):
        self.nodes = [node1, node2, node3]
        #TODO: When triangles share an edge should it be ensured to be unique?
        self.edges = [Edge(node1, node2), Edge(node2, node3), Edge(node3, node1)]
    
    def isNodeMember(self, node):
        return node in self.nodes
    
    def getEdges(self, node):
        edge_set = []
        for e in self.edges:
            if node in e.nodes:
                edge_set.append(e)
        return edge_set
    
    def getCornerCoords(self):
        return np.array([n.pos for n in self.nodes])
    
    def getArea(self):
        return 0.5 * abs(np.linalg.det(np.vstack([self.getCornerCoords().T,np.ones((1,3))])))  
    
    def getCentroid(self):
        return sum(self.getCornerCoords())/3.

    #this if n1 and n2 are not nodes of this triangle, this function returns node1, careful!
    #if this function returns "None", then two of the nodes in the triangle are the same, this is also a big problem!
    def getThirdNode(self, n1, n2):
        if self.nodes[0] is not n1 and self.nodes[0] is not n2:
            return self.nodes[0]
        if self.nodes[1] is not n1 and self.nodes[1] is not n2:
            return self.nodes[1]
        if self.nodes[2] is not n1 and self.nodes[2] is not n2:
            return self.nodes[2]
        return None
