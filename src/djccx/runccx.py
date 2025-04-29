import os
import time
from djccx.viewer.viewer import luncher
import pandas as pd
import subprocess
import signal
from djccx.check_wine_installed import check_wine_installed
from mpi4py import MPI

path = os.path
if not os.name == "nt":
    exist_wine = check_wine_installed()
    if not exist_wine:
        print("Wine is not installed. Calculix will be run with linux binary")
    else:
        print("Wine is installed. Calculix will be run with windows binary")

file = path.abspath(__file__)
ccx_windows = path.join(path.dirname(file),"bin","ccx_dynamic.exe")
ccx_linux   = path.join(path.dirname(file),"bin","ccx_2.22")

if os.name == "nt":
    ccx = ccx_windows
else:
    if exist_wine:
        ccx = "wine " + ccx_windows
    else:
        cxx = ccx_linux

def runccx(output_folder,
           name_inp,
           OMP_NUM_THREADS  = 8,
           outtxt           = "out.txt",
           mpi              = False,
           mpi_np           = 4):


    # ==============================================================================
    # viewer function
    # ==============================================================================
    def viewer(elapsed,p):
        nlines_showed = p["nlines_showed"]
        outfile = os.path.join(name_inp+".cvg")
        exist = os.path.isfile(outfile)
        if exist:
            lines = open(outfile).readlines()
            nlines = len(lines)
        else:
            lines = ".cvg file not found"
            nlines = 0
        # use div html to show lines
        # mono space
        if nlines_showed < nlines:
            print(lines[p["nlines_showed"]].replace("\n",""))
            p["nlines_showed"] = p["nlines_showed"] + 1
        
        if nlines_showed == 0:
            time.sleep(10)

    # ==============================================================================
    # stopper function
    # ==============================================================================
    
    def stopper():
        cvf_file = name_inp+".cvg"
        try:
            # count lines
            nlines = sum(1 for line in open(cvf_file))
            if nlines < 5:
                return False
            # read last line
            df_cvf = pd.read_csv(cvf_file, sep=r"\s+", header=None,skiprows=4)
            last_row = df_cvf.iloc[-1,:]
            # 0 STEP , 1 INC
            # 2 ATT  , 3 ITER
            # 4 CONT EL (#)
            att = last_row[2]
            # condicion de parada
            if att > att:
                # read pid.txt and kill process
                pid = int(open("pid.txt").read())
                print("Killing process: ",pid)
                os.kill(pid,signal.SIGTERM)
                return True
            else:
                return False
        except:
            print("Error reading cvf file")
            return False
        
    # ==============================================================================
    curr_dir = os.getcwd()
    out_abs = os.path.abspath(output_folder)
    os.chdir(output_folder)

    os.environ["OMP_NUM_THREADS"] = str(OMP_NUM_THREADS)  # Establece el número deseado de hilos

    # ==============================================================================
    # if windows
    if os.name == "nt":
        if mpi:
            # evitamos los problemas con los espacios en blanco
            ccx_path_without_sep = ccx.replace(" ","_SEP_")
            cmd = ccx_path_without_sep+' {}'.format(name_inp)
            # cmd = 'mpiexec -n {} '.format(mpi_np) + cmd
            cmd = 'C:\Program Files\Microsoft MPI\Bin\mpiexec -n {} '.format(mpi_np) + cmd

            
        else:
            cmd = ccx+' {}'.format(name_inp)

    else:   
        # if linux
        cmd = "{} {} > ".format(ccx,name_inp) +outtxt
    # ==============================================================================
    # De esta menra evitamos los probelemas con los espacios en blanco
    # en las direcciones de los archivos
    # ==============================================================================
    cmd_split = cmd.split(" ")
    if mpi:
        cmd_split = [ line.replace("_SEP_"," ") for line in cmd_split
                     ]
    print("Running Calculix at: ",output_folder)
    # show the outpt file 
    print("Output file: ", os.path.join(out_abs,outtxt))
    print("Command:\n",cmd)
    @luncher(viewer,stopper)
    def run():
        stdout = open(outtxt,"w")
        stderr = open("err.txt","w")
        process = subprocess.Popen(cmd_split,
                                    stdout = stdout,
                                    stderr = stderr)
        # save pid in pid.txt
        pid = process.pid
        print("\npid: ",pid,"\n")
        with open("pid.txt","w") as f:
            f.write(str(pid))
        # wait for process to finish
        process.wait()
        
    try:
        run()
        error = 0
    except Exception as e:
        error = 1
        os.chdir(curr_dir)
        raise Exception(e)

    print("Calculix finished\n")
    os.chdir(curr_dir)

    return error,cmd


