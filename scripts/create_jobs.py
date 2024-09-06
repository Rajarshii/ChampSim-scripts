#!/usr/bin/python3

import os
import sys
import argparse
import traceback

def parse_exp(filename):
    with open(filename,'r') as f:
        lines = f.readlines()

    exp_configs = {}
    exps = []
    exp = {}

    for elem in lines:
        elem = elem.strip()

        if not elem:
            continue
        if elem.startswith('#'):
            continue

        tokens = elem.split()
        if tokens[1] == "=":
            exp_configs[tokens[0]] = ' '.join(tokens[2:])
        else:
            exp["NAME"] = tokens[0]
            args = []

            for token in tokens[1:]:
                if token.startswith('$'):
                    token = token.replace('$','').replace('(','').replace(')','')
                    if token in exp_configs:
                        args.append(exp_configs[token])
                    else:
                        raise ValueError(f"{token} is not defined before exp {tokens[0]}")
                else:
                    args.append(token)
            exp["KNOBS"] = ' '.join(args)
            exps.append(exp)
            exp = {}
    return exps


def parse_trace(filename) :
    with open(filename,'r') as f:
        lines = f.readlines()

    trace_info = []
    rec = {}

    for elem in lines:
        elem = elem.strip()

        if elem:
            idx = elem.find('=')
            key = elem[:idx].strip()
            value = elem[idx+1:].strip()

            if key == "NAME":
                if rec:
                    trace_info.append(rec)
                    rec = {}
            rec[key] = value;                
    if rec:
        trace_info.append(rec)
    return trace_info


# Parse the parameters
parser = argparse.ArgumentParser(description="Creating Jobs for ChampSim",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t","--tlist",default=None,help="Trace List")
parser.add_argument("-c","--config",default=None,help="Experiment configurations")
parser.add_argument("-x","--exe",default=None,help="Executable file")
parser.add_argument("-l","--local",default=1,help="Local(1) or slurm(0) runs")
args = vars(parser.parse_args())

# Setup the parameters
tlist_file = args["tlist"]
exe = args["exe"]
conf_file = args["config"]
loc = args["local"]

if "CHAMPSIM_HOME" not in os.environ:
    print("CHAMPSIM_HOME not set")
    sys.exit(1)

if "TRACE_SRC" not in os.environ:
    print("TRACE_SRC not set")
    sys.exit(1)

if not tlist_file:
    print("tlist file not provided")
    sys.exit(1)

if not conf_file:
    print("configuration file not present")
    sys.exit(1)

if not exe:
    print("Executable file not present")
    sys.exit(1)


# Parsing trace and experiment info
try:
    trace_info = parse_trace(tlist_file)
    exp_info = parse_exp(conf_file)
except Exception as e:
    print("Error parsing trace or experiment info:", e)
    traceback.print_exc()
    sys.exit(1)

for trace in trace_info:
    trace_name = trace["NAME"]

for exp in exp_info:
    exp_name = exp["NAME"]
    exp_knobs = exp["KNOBS"]

for trace in trace_info:
    for exp in exp_info:
        exp_name = exp["NAME"]
        exp_knobs = exp["KNOBS"]
        trace_name = trace["NAME"]
        trace_input = trace["TRACE"]
        trace_knobs = trace["KNOBS"]
        #print(trace_input)
        if loc == 1:
            cmdline = "{} {} {} {} > {}_{}.out 2>&1".format(exe,exp_knobs,trace_knobs,trace_input,trace_name,exp_name)
        else: 
            slurm_cmd = "sbatch --mincpus 1 -c 1 -J {}_{} -o {}_{}.out -e {}_{}.err wrapper ".format(trace_name,exp_name,trace_name,exp_name,trace_name,exp_name)
            cmdline = slurm_cmd + "{} {} {} {}".format(exe,exp_knobs,trace_knobs,trace_input)
        cmdline = cmdline.replace("$(CHAMPSIM_HOME)",os.environ['CHAMPSIM_HOME'])
        cmdline = cmdline.replace("$(TRACE_SRC)",os.environ['TRACE_SRC'])
        cmdline = cmdline.replace("$(TRACE)",trace_name)
        cmdline = cmdline.replace("$(EXP)",exp_name)

        print(cmdline)
