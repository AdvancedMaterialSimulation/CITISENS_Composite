import plotly.graph_objects as go
import numpy as np

def plotly(mesh,xlim=None,ylim=None,clim=None):

    xD = mesh['x']
    yD = mesh['y']
    zD = mesh['z']
    magnitud = mesh['magnitud']
    ivalues = mesh['i']
    jvalues = mesh['j']
    kvalues = mesh['k']
    
    fig = go.Figure(data=[
    go.Mesh3d(
        x=xD, # x-coordinates of vertices
        y=yD, # y-coordinates of vertices
        z=zD, # z-coordinates of vertices
        # i, j and k give the vertices of triangles
        # here we represent the 4 triangles of the tetrahedron surface
        i=ivalues,
        j=jvalues,
        k=kvalues,
        intensity=magnitud, # the color is given by the z value
        name='y',
        showscale=True,
        colorscale='Jet',
        cmin=clim[0] if clim is not None else None,  # Set color scale minimum limit
        cmax=clim[1] if clim is not None else None   # Set color scale maximum limit
                    )
])

    # fig size 
    fig.update_layout(width=500, height=500)
    # aspect ratio
    fig.update_layout(scene_aspectmode='data')
    # zoom out 
    # 
    if xlim is not None:
        fig.update_layout(scene_xaxis_range=xlim)
    if ylim is not None:
        fig.update_layout(scene_yaxis_range=ylim)

    
    fig.show()

# round values
    xD = np.round(xD,4)
    yD = np.round(yD,4)
    zD = np.round(zD,4)
    magnitud = np.round(magnitud,4)
