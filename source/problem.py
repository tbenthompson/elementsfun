from node import Node
from dirichletnode import DirichletNode
import numpy as np
from scipy import sparse
import scipy.sparse.linalg as sparselinalg

class Problem(object):
    def __init__(self, nodes, boundary_nodes, triangles):
        self.nodes = nodes
        self.triangles = triangles
        self.boundary_nodes = boundary_nodes
        self._calcFreeNodesIndices()
        self._calcConstrainedNodesIndices()
        
    def _calcFreeNodesIndices(self):
        self.free_nodes = [n for n in self.nodes if n not in self.boundary_nodes]
        for i in range(0, len(self.free_nodes)):
            self.free_nodes[i].free_node_index = i
    
    def _calcConstrainedNodesIndices(self):
        for i in range(0, len(self.boundary_nodes)):
            self.boundary_nodes[i].boundary_node_index = i
    
    def findNodeAtIndex(self, i,j):
        for n in self.nodes:
            if n.idx[0] == i and n.idx[1] == j:
                return n
        return None
    
    def solve(self, f, k, u, du):
        g = self.getDirichletData(u)
        K = self.getStiffnessMatrix(k)
        f = self.getLoad(f, k, g)
        return (sparselinalg.cg(K, f)[0], g)
        
    def getDirichletData(self, function):
        return np.array([n.evaluateWith(function) for n in self.boundary_nodes if n.isDirichlet() == True])   
        
    @staticmethod
    def _calcBasisGradient(coords):
        coords_matrix = np.hstack([np.ones((3,1)),coords])    
        C = np.linalg.inv(coords_matrix)
        #TODO: I don't understand this line and why it calculates the gradient of the basis
        basis_gradient = C[1:3,:].T.dot(C[1:3,:])
        return basis_gradient
    
    def getStiffnessMatrix(self, k_function):
        K = sparse.lil_matrix((len(self.free_nodes), len(self.free_nodes)))
        for t in self.triangles:
            coords = t.getCornerCoords()
            basis_gradient = self._calcBasisGradient(coords)
#            print basis_gradient
            triarea = t.getArea()
        
            centroid = t.getCentroid()
            intensity = triarea * k_function(centroid[0], centroid[1])
#            print intensity
            for i in range(0,3):
                if t.nodes[i].isBoundary():
                    continue
                for j in range(0,i+1):
                    if t.nodes[j].isBoundary():
                        continue
                    idx1 = t.nodes[i].free_node_index
                    idx2 = t.nodes[j].free_node_index
                    if idx2 < idx1:
                        temp = idx1
                        idx1 = idx2
                        idx2 = temp
                    K[idx1,idx2] += basis_gradient[i,j] * intensity
        K = K + sparse.triu(K,1).T
        return K.tocsr()
    
    #TODO:Write a test for the dirichlet data utilizing part of this function 
    def getLoad(self, f_function, k_function, g):
        f = np.zeros((len(self.free_nodes),1))
        for t in self.triangles:
            coords = t.getCornerCoords()
            triarea = t.getArea()
            centroid = t.getCentroid()
            intensity = triarea * f_function(centroid[0], centroid[1]) / 3
            
            for n in t.nodes:
                if n.isBoundary():
                    continue
                f[n.free_node_index] += intensity
            dirichlet = np.array([n.isDirichlet() for n in t.nodes])
            neumann = np.array([n.isNeumann() for n in t.nodes])
            if dirichlet.any():
                w = np.zeros((3,1))
                for j in range(0,3):
                    if not t.nodes[j].isDirichlet():
                        continue
                    w[j] = g[t.nodes[j].boundary_node_index]
                    
                basis_gradient = self._calcBasisGradient(coords).dot(w)
                intensity = triarea * k_function(centroid[0], centroid[1]) * basis_gradient
                for i in range(0,3):
                    if t.nodes[i].isDirichlet():
                        continue
                    f[t.nodes[i].free_node_index] -= intensity[i]
            # if neumann.any():
                  
        return f
