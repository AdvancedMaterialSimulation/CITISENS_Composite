import os

from ..CreateYarns.CreateYarns import CreateYarns
from .CreateBoxMirror import CreateBoxMirror

def CreateComposite(params_yarns,output_folder):

    CreateYarns(params_yarns,os.path.join(*output_folder))
    CreateBoxMirror(params_yarns,output_folder)
 
    return params_yarns