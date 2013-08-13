import unittest
from math import *
from problem import Problem
from mesh_gen import generateRectangularMesh
from view_solution import view_rectangular_grid_solution, get_grid, show_plot
import numpy as np
#   I TOOK THIS EXAMPLE FROM THE GOCKENBACH BOOK, HERE IS THE ORIGINAL ACCOMPANYING TEXT
#   This script demonstrates the use of the Fem code to
#   solve the BVP
#
#          -div(k*grad u)=f in Omega,
#                       u=g on Gamma_1,
#                 k*du/dn=h on Gamma_2.
#
#   Here Omega is the unit square, Gamma_1 consists of
#   the top and left edges of the square and Gamma_2 is
#   the remainder of the boundary (the bottom and right
#   edges).  The coefficient is k(x,y)=1+x^2*y, and
#   f, g, h are chosen so that the exact solution is
#   u(x,y)=exp(2*x)*(x^2+y^2).

#   This routine is part of the MATLAB Fem code that
#   accompanies "Understanding and Implementing the Finite
#   Element Method" by Mark S. Gockenbach (copyright SIAM 2006).


class TestKnownProblem(unittest.TestCase):
    def testKnownProblem(self):
        def f(x,y):
            return -2*x*y*(2*exp(2*x)*(x**2+y**2)+2*exp(2*x)*x)-(1+x**2*y)*(4*exp(2*x)*(x**2+y**2)+8*exp(2*x)*x+2*exp(2*x))-2*x**2*exp(2*x)*y-2*(1+x**2*y)*exp(2*x)
        
        def k(x,y):
            return 1+x**2*y
        
        def u(x,y):
            return exp(2*x)*(x**2+y**2)
        
        def ux(x,y):
            return 2*exp(2*x)*(x**2+y**2)+2*exp(2*x)*x
        
        def uy(x,y):
            return 2*exp(2*x)*y
            
        ewidth = 30
        eheight = 30
        xwidth = 2.
        ywidth = 2.
        ll = (-1.,-1.)
        
        [nodes, boundary_nodes, tris] = generateRectangularMesh((ewidth, eheight), ll, (xwidth/(ewidth-1),ywidth/(eheight-1)))
        p = Problem(nodes, boundary_nodes, tris)
        # U, g = p.solve(lambda x,y: cos(x*y*pi) - 0.5, lambda x,y: 1, lambda x,y: 0, ux)
        Uest, g = p.solve(f, k, u, ux)
        Utrue = [u(n.pos[0],n.pos[1]) for n in p.free_nodes] 
        # view_rectangular_grid_solution((ewidth, eheight), p, Uest, g)
        # view_rectangular_grid_solution((ewidth, eheight), p, Utrue, g)
        error = np.sqrt(np.sum((Utrue - Uest) ** 2))
        print error
        self.assertTrue(error < 0.5)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestKnownProblem))
    unittest.TextTestRunner(verbosity=2).run(suite)       
    
        
