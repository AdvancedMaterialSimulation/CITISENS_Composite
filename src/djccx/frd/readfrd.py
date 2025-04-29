import numpy as np
import pandas as pd
from djccx.frd.measurements import von_misses,principal_stress

def parseblock(block_data):
    headers = [ line for line in block_data if line.startswith(" -5") ]
    headers = [ line.split()[1] for line in headers ]
    headers.insert(0,"node")

    data = [ line for line in block_data if line.startswith(" -1") ]
    data = [ line.replace("-"," -").replace("E -","E-") for line in data ]
    data = [ line for line in data ]
    data = [ line.split()[1:] for line in data ]
    data = np.array(data,dtype=float)

    # if data is empty, return empty dataframe
    # Esto paso por que si los datos son todo ceros
    # Calculix no los escribe en el archivo .frd
    # y en el archivo .frd solo se escribe el header
    # agregamos esta linea para que no falle
    if len(data) == 0:
        return pd.DataFrame(columns=headers)
    ncol = len(data[0])
    data = pd.DataFrame(data,columns=headers[:ncol])
    # node is a integer
    data["node"] = data["node"].astype(int)

    r = {
        "data":data,
        "step": block_data[1].split(),
    }
    return r


def parsenodes(nodes):
    # select the lines that start with " -1"
    nodes = [ line for line in nodes if line.startswith(" -1") ]
    nodes = [ line for line in nodes if line.startswith(" -1") ]
    nodes = [ line.replace("-"," -").replace("E -","E-") for line in nodes ]
    nodes = [ line.split()[1:] for line in nodes ]
    nodes = np.array(nodes,dtype=float)
    nodes = pd.DataFrame(nodes,columns=["node","x","y","z"])
    #id integer, x float, y float, z float
    nodes["node"] = nodes["node"].astype(int)
    return nodes
# ==========
# readfrd
# ==========
def readfrd(file,remove_fail_steps=True,add_compute=True):

    
    lines = open(file).readlines()
    # search " -3" in the file, this is the end of blocks. 
    # de line mush start with " -3"
    idx = [ i for i, line in enumerate(lines) if line.startswith(" -3") ]
    # add zero at the begining
    idx.insert(0,0)

    blocks = [ lines[idx[i]:idx[i+1]] for i in range(len(idx)-1) ]

    nodes = parsenodes(blocks[0])
    blocks_out = []
    for i in range(2,len(blocks)):
        parseb = parseblock(blocks[i])
        if len(parseb) > 0:
            blocks_out.append(parseb)



    steps       = [ b["step"] for b in blocks_out ]
    blocks_data = [ b["data"] for b in blocks_out ]



    tot_steps = [ i[2:] for i in steps]
    # i[1] fix width str 
    name_steps = [ "step_"+str(i[1]).zfill(2)+"_"+str(i[0]).zfill(2) 
                  for i in tot_steps]
    name_steps = np.array(name_steps)
    name_steps_u = np.unique(name_steps)

    indexs = [np.where(name_steps == i)[0] for i in name_steps_u]

    blocks_out_list = []
    for id,name in zip(indexs,name_steps_u):
        blocks_out_list.append([ blocks_data[j] for j in id])
    
    blocks_out_list_merged = []
    for blocks_out in blocks_out_list:
        # append columns to nodes (pandas dataframe)
        blocks_out = pd.concat(blocks_out,axis=1)
        # nodes columns are repeated, so we drop all but the first
        blocks_out = blocks_out.loc[:,~blocks_out.columns.duplicated()]
        # add nodes x y z columns to blocks
        blocks_out = pd.merge(blocks_out,nodes,on="node")
        # re order columns to have node, x, y, z, and then the rest
        cols = list(blocks_out.columns)
        cols = cols[:1] + cols[-3:] + cols[1:-3]
        blocks_out = blocks_out[cols]

        blocks_out.index = blocks_out["node"]
        blocks_out_list_merged.append(blocks_out)

    # 
    mesh = blocks[1]
    mesh = [ line for line in mesh if line.startswith(" -2") ]
    mesh = [ line.replace(" -2","") for line in mesh ]
    # split 
    mesh = [ line.split() for line in mesh ]
    mesh = np.array(mesh,dtype=int)
    #mesh = mesh[:,:3]
    # 
    out = dict()
    out["data"] = blocks_out_list_merged[-1]
    out["mesh"] = mesh
    out["steps"] = name_steps_u
    out["data_blocks"] = blocks_out_list_merged

    # 
    # borramos el ultimo si no existe tension
    if remove_fail_steps:
        last_block = out["data_blocks"][-1]
        if not "SXX" in last_block.keys():
            out["data_blocks"].pop(-1)
            out["data"] = out["data_blocks"][:-1]
            out["steps"] = out["steps"][:-1]

    if add_compute:
        von_misses(out)
        principal_stress(out)

    return out