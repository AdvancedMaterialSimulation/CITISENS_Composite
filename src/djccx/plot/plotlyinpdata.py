
import plotly.graph_objs as go

def plotlyinpdata(mesh,xlim=None,ylim=None):

    xD = mesh['xi']
    yD = mesh['yi']
    zD = mesh['zi']
    ivalues = mesh['i']
    jvalues = mesh['j']
    kvalues = mesh['k']
    
    data=go.Mesh3d(
        x=xD, # x-coordinates of vertices
        y=yD, # y-coordinates of vertices
        z=zD, # z-coordinates of vertices
        # i, j and k give the vertices of triangles
        # here we represent the 4 triangles of the tetrahedron surface
        i=ivalues,
        j=jvalues,
        k=kvalues,
        name=mesh['names'][0],
        showscale=True,
        colorscale='Jet'    )
    

    return data