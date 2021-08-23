
import numpy as np

dt = np.dtype(np.uint16)
dt = dt.newbyteorder('>')
def l(s):
    with open(s,"rb") as file:
        return np.frombuffer(file.read(),dt).reshape((1<<16,4))
a=l("data_file")
b=l("data_file2")
