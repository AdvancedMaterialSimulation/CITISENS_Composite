def CreatePBC_with_tie(self,tie_name,nset,surface,vec):
    #
    ncopy = nset + "_REP"
    inset_rep = self.CreateCopyNset(nameset      = nset,
                                nameset_copy = ncopy,
                                vec          = vec)
    # create a surface with the new nodes
    self.CreateSurfNodeFromNset(inset_rep,"SURFACE_"+ncopy)
    # create tie
    self.CreateTie(tie_name, 
                slave  = "SURFACE_"+ncopy, 
                master = surface)
    
    self.AddEquation(nset,ncopy,type_eq="point2point")