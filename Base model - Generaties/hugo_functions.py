# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 09:52:03 2016

@author: hdevos
"""

# %% --- Functions: ---



def read_cmd_line(pop_1_filenm, pop_2_filenm, fig, parms):
    import getopt
    import sys
    myopts, args = getopt.getopt(sys.argv[1:],"p1:p2:f:prm:")
    for o, a in myopts:     #o = option, a = argument
        if o == '-p1':
            pop_1_filenm = a
        elif o == '-p2':
            pop_2_filenm = a
        elif o == '-f':
            fig = a
        elif o == "-prm":
            parms = a
    
    return pop_1_filenm, pop_2_filenm, fig, parms


def read_cmd_line2(pop_1_filenm, pop_2_filenm, fig, pop1_size, pop2_size):
    import getopt
    import sys
    myopts, args = getopt.getopt(sys.argv[1:],"p1:p2:f:ps1:ps2")
    for o, a in myopts:     #o = option, a = argument
        if o == '-p1':
            pop_1_filenm = a
        elif o == '-p2':
            pop_2_filenm = a
        elif o == '-f':
            fig = a
        elif o == 'ps1':
            pop1_size = a
        elif o == 'ps2':
            pop2_size = a
    
    return pop_1_filenm, pop_2_filenm, fig, pop1_size, pop2_size


def update_logfile(logfile, bookkeeping):
    logfile_df = pd.read_csv(logfile, delimiter = ";")
    
    
    now = dtm.datetime.now()
    now_iso = now.isoformat()
    
    output = ("|".join([str(round(i,4)) for i in bookkeeping])).strip("\n")
    
    logfile_df.loc[len(logfile_df)] = [now_iso, NR_OF_EXEMPLARS, POPULATION_SIZE, NR_OF_INTERACTIONS, output]
    
    logfile_df.to_csv(logfile, sep = ";", encoding='utf-8', index = False)