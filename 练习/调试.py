
(pdb) 1
import pdb

def pdb_test(arg):
    for i in range(arg):
        print(i)
    return(arg)
pdb.run("pdb_test(3)")
