
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def get_grid(p):
    x = np.unique(np.array([n.pos[0] for n in p.nodes]))
    y = np.unique(np.array([n.pos[1] for n in p.nodes]))
    X, Y = np.meshgrid(x, y)
    return X, Y


def view_rectangular_grid_solution(size, p, U, g):
    width = size[0]
    height = size[1]
    X,Y = get_grid(p)
    Z = np.zeros(X.shape)
    for i in range(0,width):
        for j in range(0,height):
            node = p.findNodeAtIndex(i,j)
            if node.isDirichlet():
                Z[i,j] = g[node.boundary_node_index]                
            else:    
                Z[i,j] = U[node.free_node_index]
    show_plot(X,Y,Z)
    return Z

def show_plot(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X, Y, Z, cmap=matplotlib.cm.coolwarm)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
