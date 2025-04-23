import numpy as np
def grid_section(x0, y0, z0,vec_z, vec_x,d,r,rho=4):

    lx = d + 2*r
    np_x = int(lx*rho) 
    x_span = np.linspace(-(d+2*r)/2,(d+2*r)/2,np_x)

    ly = 2*r
    np_y = int(ly*rho)
    y_span = np.linspace(-r,r,np_y)

    X,Y = np.meshgrid(x_span,y_span)
    X = X.flatten()
    Y = Y.flatten()


    idx = ((X-d/2)**2 + Y**2 > r**2) 
    idx_2 = X > d/2 

    idx = idx * idx_2
    X = X[~idx]
    Y = Y[~idx]

    idx = ((X+d/2)**2 + Y**2 > r**2) 
    idx_2 = X < -d/2 

    idx = idx * idx_2
    X = X[~idx]
    Y = Y[~idx]
    Z = 0*X 

    # ===================================

    vec_z = vec_z / np.linalg.norm(vec_z)
    vec_x = vec_x / np.linalg.norm(vec_x)


    vec_y = np.cross(vec_z, vec_x)
    vec_y = vec_y / np.linalg.norm(vec_y)

    vec_x = np.cross(vec_y, vec_z)
    vec_x = vec_x / np.linalg.norm(vec_x)


    rot = np.column_stack((vec_x, vec_y, vec_z))
    tr = np.array([x0,y0,z0])

    points = np.vstack((X, Y, Z)).T  # This creates a (N, 3) array where each row is a point
    transformed_points = np.dot(points, rot.T) + tr  # Rotate and translate all points

    X, Y, Z = transformed_points[:, 0], transformed_points[:, 1], transformed_points[:, 2]

    return X,Y,Z

