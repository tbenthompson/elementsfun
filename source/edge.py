class Edge(object):        
    #DON'T CALL THIS DIRECTLY, USE newEdge
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        
    def node1(self):
        return self.nodes[0]
    
    def node2(self):
        return self.nodes[1]
