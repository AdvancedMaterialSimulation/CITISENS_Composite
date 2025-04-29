import numpy as np
import pandas as pd

def read_dat(dat_file):
    
    lines = open(dat_file).readlines()

    lines = [ line for line in lines 
                   if "S T E P"   not in line ]
    lines = [ line for line in lines 
                   if "INCREMENT"   not in line ]
    lines = [ line for line in lines
                   if "\n" != line ]
    # remove "\n"
    
    # separate by enpty lines
    # find empty lines index
    indx = [i for i, s in enumerate(lines) 
              if "for set" in s ]
    # add last line
    indx.append(len(lines))
    lines_list = [lines[indx[i]:indx[i+1]] for i in range(len(indx)-1)]
    # append the last lines

    lines_list.append(lines[indx[-1]+1:])
    r_list = []
    for i in range(0,len(indx)-1):
            header = lines_list[i][0]
            headers_split = header.split() 
            name_table = headers_split[0]
            time_table = headers_split[-1]
            # find set name in list 
            id_set = [i for i, s in enumerate(headers_split) 
                    if s.startswith("set")][0]
            set_name = headers_split[id_set+1]
            # remove in header all before "(" and after ")"
            vars = header[header.find("(")+1:header.find(")")]
            vars = vars.replace(" ","").split(",")
            data    = lines_list[i][1:]
            #
            data_np = np.array([line.split() 
                                for line in data]).astype(float)
            # create a dataframe
            if data_np.shape[1] > len(vars):
                    # in vars node id is not included
                    vars = ["nid"] + vars

            df = pd.DataFrame(data_np,columns=vars)
            # first is the integer 
            df[vars[0]] = df[vars[0]].astype(int)

            r = {
                    "time": time_table,
                    "set": set_name,
                    "df": df,
                    "name": name_table,
            }
            r_list.append(r)
    return r_list