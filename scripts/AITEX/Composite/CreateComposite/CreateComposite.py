import os

from ..CreateYarns.CreateYarns import CreateYarns
from ..CreateComposite.CreateBox import CreateBox
from ..CreateComposite.CreateBoxMirror import CreateBoxMirror

def CreateComposite(params_yarns,output_folder):


    h = params_yarns['h']
    r = params_yarns['r']
    interface_factor = params_yarns['interface_factor']

    hmin = 2*r*interface_factor
    if h <= hmin:
        raise ValueError('The height of the composite must be greater than 2*r*interface_factor. The current value is h = %f and hmin = %f' % (h,hmin))

    CreateYarns(params_yarns,os.path.join(*output_folder))
    
    mirror = params_yarns['mirror']
    if mirror:
        CreateBoxMirror(params_yarns,output_folder)
    else:
        CreateBox(params_yarns,output_folder)
    
    return params_yarns