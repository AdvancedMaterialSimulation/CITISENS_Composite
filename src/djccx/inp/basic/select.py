import re
def select(self,name,type):
    if type == "nset":
        r= [inset for inset in self.nsets
            if inset.name == name]
    elif type == "elset":
        r =[ielset for ielset in self.elsets
            if ielset.name == name]
    elif type == "surface":
        r = [isurf for isurf in self.surfaces
            if isurf.name == name]
    else:
        raise Exception("type must be nset, elset or surface")
    
    if len(r) == 0:
        raise Exception("No existe el "+type+": "+name)
    if len(r) > 1:
        raise Exception("Existe mas de un "+type+": "+name)
    return r[0]


def select_regex(self,regex,type):
    if type == "nset":
        r= [inset for inset in self.nsets
            if re.fullmatch(regex,inset.name)]
    elif type == "elset":
        r =[ielset for ielset in self.elsets
            if re.fullmatch(regex,ielset.name)]
    elif type == "surface":
        r = [isurf for isurf in self.surfaces
            if re.fullmatch(regex,isurf.name)]
    else:
        raise Exception("type must be nset, elset or surface")
    
    if len(r) == 0:
        raise Exception("No existe el "+type+": "+regex)
    return r