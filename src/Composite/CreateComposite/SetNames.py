import os
def SetNames(files_yarns):
    
    names = []
    # only plus
    #files_yarns = [i for i in files_yarns if "plus" in i]

    for file in files_yarns:

        name = os.path.abspath(file).split(os.sep)[-1].split(".")[0]

        # add physical group
        name = name.replace("yarn_","y")
        name = name.replace("layer_","l")
        # if "minus" in name MI prefix
        if "minus" in name:
            name = "MI_"+name
        if "plus" in name:
            name = "PL_"+name
        name = name.replace("_minus","")
        name = name.replace("_plus","")

        names.append(name)

    # sorf 
    names_idx = sorted(range(len(names)), key=lambda k: names[k])
    names = [names[i] for i in names_idx]
    files_yarns = [files_yarns[i] for i in names_idx]


    return names, files_yarns