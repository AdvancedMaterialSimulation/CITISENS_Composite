import os

from ..CreateYarns.CreateYarns import CreateYarns
from .CreateBox import CreateBox

def CreateComposite(params_yarns,output_folder):

    CreateYarns(params_yarns,os.path.join(*output_folder))
    
    CreateBox(params_yarns,output_folder)
    
    return params_yarns