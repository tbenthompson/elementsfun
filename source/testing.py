from math import floor
import unittest
from test_known_problem import TestKnownProblem
from scipy import sparse
import numpy as np

from problem import Problem
from node import Node
from edge import Edge
from triangle import Triangle
from mesh_gen import generateRectangularMesh

class TestPyFEMur(unittest.TestCase):    
    def testDirichletFunction(self):
        d = Node((2,3), (0,0))
        self.assertEqual(d.evaluateWith(lambda x,y: x*y), 6)
        self.assertRaises(Exception, d.evaluateWith, d, lambda x: x)
    
    def testProblemCalcConstrainedNodeIndices(self):
        width = 4
        height = 4
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        self.assertEqual(len(p.boundary_nodes), 12)
        for i in range(0, 12):
            self.assertEqual(p.boundary_nodes[i].boundary_node_index, i)        
            
    
    def testProblemCalcFreeNodes(self):
        width = 4
        height = 4
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        self.assertEqual(len(p.free_nodes), 4)
        for i in range(0, 4):
            self.assertEqual(p.free_nodes[i].free_node_index, i)        
    
    def testProblemGetDirichlet(self):
        width = 3
        height = 3
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        data = p.getDirichletData(lambda x,y: x*y)
        self.assertEqual(data[0], 0)
        self.assertEqual(4 in data, True)
        self.assertEqual(2 in data, True)
    
    def testProblemCalcBasisGradient(self):
        coords = np.array([[0.,0.],[ 0.0625,0.    ],[ 0.,0.0625]])
        bg = Problem._calcBasisGradient(coords)
        self.assertTrue((bg == np.array([[512.,-256.,-256.],[-256.,256.,0.], [-256.,0.,256.]])).all())
    
    def testEdgeNormal(self):
        a = Node((0,0),(0,0))
        b = Node((1,0),(0,0))
        c = Node((0,1),(0,0))
        t = Triangle(a, b, c)
        xaxisedge = t.edges[0]
        reversedxaxisedge = Edge(xaxisedge.nodes[1], xaxisedge.nodes[0])
        diagonaledge = t.edges[1]
        yaxisedge = t.edges[2]
        self.assertTrue((xaxisedge.getNormal(t) == (0, -1)).all())
        self.assertTrue((reversedxaxisedge.getNormal(t) == (0, -1)).all())

    def testTriangleArea(self):
        t = Triangle(Node((1,1),(0,0)), Node((0,0),(0,0)), Node((1,0),(0,0)))
        self.assertEqual(t.getArea(), 0.5)
        
    def testProblemStiffness(self):
        width = 3
        height = 3
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        stiffness = p.getStiffnessMatrix(lambda x,y: x*y).toarray()
        self.assertEqual(stiffness[0,0], 34.0/9.0)
    
    def testProblemStiffness2(self):
        width = 4
        height = 4
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        K = p.getStiffnessMatrix(lambda x,y: x*y)
        self.assertTrue((sparse.triu(K, 1).T.toarray() == sparse.tril(K,-1).toarray()).all())
        width = 5
        height = 5
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        K = p.getStiffnessMatrix(lambda x,y: x*y)
        self.assertTrue((sparse.triu(K, 1).T.toarray() == sparse.tril(K,-1).toarray()).all())
    
    def testProblemLoad(self):
        width = 10
        height = 10
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        p = Problem(nodes, boundary_nodes, tris)
        f = p.getLoad(lambda x,y: x+y, lambda x,y: x*y, map(lambda x: 0, p.boundary_nodes))
#        print f
        #TODO: HOW TO TEST?
#        self.assertTrue((sparse.triu(K, 1).T.toarray() == sparse.tril(K,-1).toarray()).all())
        
    
    def testRectangularMeshGen(self):
        width = 4
        height = 4
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        for i in range(0, len(nodes)):
            node = nodes[i]
            self.assertEqual(node.pos[0], floor(i / float(height)))
            self.assertEqual(node.pos[1], i % height)
            if node not in boundary_nodes:
                tri_count = 0
                edges = []
                for t in tris:
                    if t.isNodeMember(node):
                        tri_count = tri_count + 1
                        new_edges = t.getEdges(node)
                        self.assertEqual(len(new_edges), 2)
                        if new_edges[0] not in edges:
                            edges.append(new_edges[0])
                        if new_edges[1] not in edges:
                            edges.append(new_edges[1])
                    else:
                        self.assertEqual(len(t.getEdges(node)), 0)
                #each node should be in 6 triangles, 2 to the upper right, 2 to the lower left, and one to the upper left and lower right
                #and 6 unique edges, or 12 total edges
#                print node.pos, count
                self.assertEqual(tri_count, 6)
                self.assertEqual(len(edges), 12)
    
    def testRectangularMeshGenSimpleTriangles(self):
        width = 2
        height = 2
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        for n in nodes:
            count = 0
            for t in tris:
                if n in t.nodes:
                    count = count + 1
            if n.pos[0] == n.pos[1]:
                #upper left or lower right corner node
                self.assertEqual(count, 1)
            else:
                self.assertEqual(count, 2)
   
    def testRectangularMeshGenSimpleTriangles2(self):
        width = 2
        height = 3
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (0,0), (1,1))
        self.assertEqual(len(tris), 4)
        correct_tri_counts = {
            str((0,0)): 1,
            str((0,1)): 3,
            str((0,2)): 2,
            str((1,0)): 2,
            str((1,1)): 3,
            str((1,2)): 1
        }
#        print [n.pos for t in tris for n in t.nodes]
        for n in nodes:
            count = 0
            for t in tris:
                if n in  t.nodes:
                    count = count + 1
#            print n.pos, count
            self.assertEqual(count, correct_tri_counts[str(n.pos)])
      
   
    def testRectangularMeshGenPositioning(self):                
        width = 2
        height = 1
        [nodes, boundary_nodes, tris] = generateRectangularMesh((width, height), (5, 0), (10, 0))
        self.assertEqual(nodes[0].pos, (5, 0))
        self.assertEqual(nodes[1].pos, (15, 0))

    def testTriangleThirdNode(self):
        n1 = Node((0,0),1)
        n2 = Node((1,1),2)
        n3 = Node((0,1),3)
        t = Triangle(n1, n2, n3)
        self.assertEqual(n1, t.getThirdNode(n2,n3))
        self.assertEqual(n2, t.getThirdNode(n1,n3))
        self.assertEqual(n3, t.getThirdNode(n1,n2))

        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPyFEMur))
    suite.addTest(unittest.makeSuite(TestKnownProblem))
    unittest.TextTestRunner(verbosity=2).run(suite)
