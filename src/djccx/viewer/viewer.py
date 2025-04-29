import threading
from IPython.display import clear_output

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parametrized
def luncher(func,viewer,stopper=lambda:False):
    def wrapper():
        t = threading.Thread(target=func)
        t.start()
        elapsed = 0
        p = {"nlines_showed":0}
        while t.is_alive() and not stopper():
            elapsed += 1
            viewer(elapsed,p)
        if stopper():
            # kill thread
            print("Simulation failed")
            raise Exception("Simulation failed by stopper function")
    return wrapper

