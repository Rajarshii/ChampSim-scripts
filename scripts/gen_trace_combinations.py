from itertools import combinations
import argparse
import sys
import os
import re
import csv

# Custom file writer
def list_writer(list_input):
    print("Writing to File")
    with open("output.traces",'w+') as f:
        for items in list_input:
            f.write("%s\n" %items)

# custom csv writer
def csv_writer(list_input,filename,delim):
    print("Writing to csv")
    with open(filename,"w") as f:
        wr = csv.writer(f,delimiter=delim)
        wr.writerows(list_input)
    f.close()

# validate traces exist
def validate_traces(src_dir,trace_list):
    print("validating traces")
    for trace in trace_list:
        trace_path = os.path.join(src_dir, trace)
        if not os.path.exists(trace_path):
            raise FileNotFoundError(f"file {trace_path} does not exist.")

# Generate trace combinations
def gen_trace_combinations(src_dir,trace_list,cores,uniform,start,max_combinations):
    print("Generating Traces.")
    
    validate_traces(src_dir,trace_list)

    trace_combinations = []

    if cores <= 0:
        raise ValueError(f"Number of cores must be more than one")
    else:
        if not uniform:
            trace_combinations = list(combinations(trace_list,cores))
        else:
            trace_combinations = [[trace] * cores for trace in trace_list]
        
        # TODO add check for range of slicing        
        trace_combinations = trace_combinations[start:start+max_combinations:]

    for i in range(len(trace_combinations)):
        trace_combinations[i] = [f"{src_dir}/{trace}" for trace in trace_combinations[i]]

    return trace_combinations

# Parse the original list of traces
def parse_trace_list(tracelist,multicore,cores,uniform,start,max_combinations):
    print("parsing trace list")

    if multicore > 1 and cores <= 1:
        raise ValueError(f"Core count {cores} should be > 1 for multicore traces")

    # Read the trace list file
    with open(tracelist, 'r') as f:
        lines = f.readlines()

    # Extract SRCDIR and traces
    src_dirs = {}
    traces = []
    dir = ""

    for line in lines:
        line = line.strip()
        if line.startswith("SRCDIR="):
            output = re.search("=(.*)",line)
            if output != None: dir = output.group(1)           
            src_dirs[dir] = []            
        elif line and not src_dirs:
            print("Error: No SRCDIR specified for tests")
            sys.exit(1)            
        elif line:
            src_dirs[dir].append(line)            


    if not src_dirs:
        print("Error: SRCDIR not specified in the trace list file.")
        sys.exit(1)

    for [src_dir,trace_list] in src_dirs.items():
        traces = gen_trace_combinations(src_dir, trace_list,cores,uniform,start,max_combinations)
    csv_writer(traces,"output.tlist"," ")

# format tests
def format_tests(testlist) :
    #print("Formatting tests")
    with open(testlist,'r') as f:
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

        with open("traces.mix",'w+') as f:
            for trace in mixes:
                trace_name = trace["NAME"]
                trace_mix = trace["TRACE"]
                cmdline = "NAME={}\nTRACE={}\nKNOBS=\n".format(trace_name,trace_mix)                
                f.write(f"{cmdline}\n")


def main() :
    print("Script to Generate Tests from Traces")
    parser = argparse.ArgumentParser(description="Creating Jobs for ChampSim", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t","--trace",default=None,help="Original traces to generate trace mixes")
    parser.add_argument("-mc","--multicore",type=int,choices=[0, 1],default=0,help="Multi-core(1) or Single core(0) simulations")
    parser.add_argument("-c","--cores",type=int,default=1,help="Number of cores")
    parser.add_argument("-u","--uniform",type=int,choices=[0, 1],default=0,help="When Multi-core=1 determine if simulation runs the same (0) or different(1) traces on all cores")
    parser.add_argument("-s","--start",type=int,default=0,help="Start offset for multicore simulations")
    parser.add_argument("-M","--max",type=int,default=200,help="Maximum number of combinations generated for multicore simulations")
    parser.add_argument("-tl","--tests",default=None,help="Generate formatted testlist file for use by create_jobs")

    args = parser.parse_args()

    print(f"""Generating traces with the following configurations:\n
          multicore = {args.multicore}\n
          cores = {args.cores}\n
          uniform = {args.uniform}
        """)
    
    if not args.trace and not args.tests:
        print("neither trace file nor test list not provided")
        sys.exit(1)
    
    if args.trace and args.tests:
        parse_trace_list(args.trace,args.multicore,args.cores,args.uniform,args.start,args.max)
        format_tests("output.tlist")
    elif args.trace:
        parse_trace_list(args.trace,args.multicore,args.cores,args.uniform,args.start,args.max)
    elif args.tests:
        format_tests(args.tests)
            

if __name__=="__main__":
    main()