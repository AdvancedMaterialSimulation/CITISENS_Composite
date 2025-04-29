import matplotlib.pyplot as plt
def plot(self,*args,**kwargs):
    plt.plot(self.nodes.df["x"], 
                self.nodes.df["y"], 
                *args, **kwargs)
    
def plot3D(self,ax,*args,**kwargs):
    ax.plot3D(self.nodes.df["x"],
                self.nodes.df["y"],
                self.nodes.df["z"],
                *args,**kwargs)