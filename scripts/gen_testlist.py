#!/usr/bin/python3
import argparse
import os
import sys
import traceback

def parse_raw_traces(filename) :
    with open(filename,'r') as f:
        lines = f.readlines()
    mixes = []
    count_mix = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        mix = {}
        args = []
        trc_elem = line.split()
        if len(set(trc_elem)) == 1:
            name = "x11"
        else: 
            name = "mix_{}".format(count_mix)
            count_mix+=1
            mix["NAME"] = name
        for tr in trc_elem:
            args.append(tr)
        mix["TRACE"] = ' '.join(args)
        mixes.append(mix)
    return mixes

def main():
    # parse the arguments
    parser = argparse.ArgumentParser(description="Creating tlist File from Traces",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t","--traces",default=None,help="List of Traces")
    args = vars(parser.parse_args())

    trace_file = args["traces"]

    if "TRACE_SRC" not in os.environ:
        print("TRACE_SRC not set")
        sys.exit(1)


    try:
        trace_info = parse_raw_traces(trace_file)
    except Exception as e:
        print("Error parsing the trace file")
        traceback.print_exc()
        sys.exit(1)


    for trace in trace_info:
        trace_name = trace["NAME"]
        trace_mix = trace["TRACE"]
        cmdline = "NAME={}\nTRACE={}\nKNOBS=\n".format(trace_name,trace_mix)
        print(cmdline)

if __name__=="__main__":
    main()
    




