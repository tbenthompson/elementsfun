from node import Node
from triangle import Triangle

def generateNodes(size, start, inc):
    nodes = []
    for i in range(0, size[0]):
        node_row = []
        for j in range(0,size[1]):
            x = start[0] + inc[0] * i
            y = start[1] + inc[1] * j
            n = Node((x, y), (i,j))
            node_row.append(n)
        nodes.append(node_row)
    return nodes

def getBoundaries(nodes):
    boundary_nodes =  []
    boundary_nodes.extend(nodes[0])
    boundary_nodes.extend(nodes[-1])
    boundary_nodes.extend([n[0] for n in nodes[1:-1]])      
    boundary_nodes.extend([n[-1] for n in nodes[1:-1]])  
    for b in boundary_nodes:
        b.setBoundaryType('dirichlet') 
    return boundary_nodes

def generateTriangles(nodes, size):
    triangles = []
    for i in range(1, size[0]):
        for j in range(1, size[1]):
            #this should grab a square 2x2 subset of the nodes to the upper left of the current position
            node_set = [sublist[j-1:j+1] for sublist in nodes[i-1:i+1]]
            #TODO: Check whether the direction on the triangles is correct. I believe the rotational direction is important in these problems...
            tri1 = Triangle(node_set[0][0], node_set[1][0], node_set[0][1])
            tri2 = Triangle(node_set[1][0], node_set[1][1], node_set[0][1])
            triangles.append(tri1)
            triangles.append(tri2)
    return triangles
    
def generateRectangularMesh(size, start, inc):
    nodes = generateNodes(size, start, inc)
    boundary_nodes = getBoundaries(nodes)
    triangles = generateTriangles(nodes, size)
    flattened_nodes = [item for sublist in nodes for item in sublist]
    return (flattened_nodes, boundary_nodes, triangles)
    
