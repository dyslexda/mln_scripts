import time, csv, sys, random, os
from pa_sim import *

def main():
    brc = sys.argv[1]
    result = sys.argv[2]
    vari = pa_simulator(brc,result)
    print(vari.sim_count())

if __name__ == "__main__":
    main()