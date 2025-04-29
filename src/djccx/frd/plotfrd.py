import numpy as np
import pandas as pd
import plotly.graph_objects as go

def plotfrd(out,facecolor=None):


    mesh = out["mesh"]
    out = out["data"]

    x = out["x"].values
    y = out["y"].values
    z = out["z"].values


    i_values = []
    j_values = []
    k_values = []

    faces = np.array([[1,2,3],
                      [1,2,4],
                      [1,3,4],
                      [2,3,4]]) -1
    for iface in faces:
        i = mesh[:,iface[0]]
        j = mesh[:,iface[1]]
        k = mesh[:,iface[2]]
        id_nodes = out["node"].values
        id_nodes_aux = np.arange(1,len(id_nodes)+1)
        df_aux = pd.DataFrame({"id_nodes":id_nodes,"id_nodes_aux":id_nodes_aux})
        # index id_nodes
        df_aux.index = df_aux["id_nodes"]

        i = df_aux.loc[i]["id_nodes_aux"].values
        j = df_aux.loc[j]["id_nodes_aux"].values
        k = df_aux.loc[k]["id_nodes_aux"].values

        i_values.append(i)
        j_values.append(j)
        k_values.append(k)
    
    i = np.concatenate(i_values)
    j = np.concatenate(j_values)
    k = np.concatenate(k_values)
    # plotly 

    fig = go.Figure(data=[
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            opacity=1,
            facecolor=facecolor
        )
    ])

    # aspet ratio
    fig.update_layout(scene_aspectmode='data')
    fig.show()
