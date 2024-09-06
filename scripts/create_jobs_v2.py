#!/usr/bin/python3

import os
import sys
import argparse
import traceback

def parse_exp(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Configuration file {filename} not found.")
        sys.exit(1)

    exp_configs = {}
    exps = []

    for elem in lines:
        elem = elem.strip()
        if not elem or elem.startswith('#'):
            continue

        tokens = elem.split()
        if tokens[1] == "=":
            exp_configs[tokens[0]] = ' '.join(tokens[2:])
        else:
            exp = {"NAME": tokens[0], "KNOBS": ' '.join(exp_configs.get(token.replace('$', '').replace('(', '').replace(')', ''), token) for token in tokens[1:])}
            exps.append(exp)

    return exps

def parse_trace(filename):
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Trace list file {filename} not found.")
        sys.exit(1)

    trace_info = []
    rec = {}

    for elem in lines:
        elem = elem.strip()
        if elem:
            idx = elem.find('=')
            key = elem[:idx].strip()
            value = elem[idx+1:].strip()

            if key == "NAME" and rec:
                trace_info.append(rec)
                rec = {}
            rec[key] = value
    if rec:
        trace_info.append(rec)

    return trace_info

def main():
    parser = argparse.ArgumentParser(description="Creating Jobs for ChampSim", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--tlist", required=True, help="Trace List for simulations")
    parser.add_argument("-c", "--config", required=True, help="Experiment configurations")
    parser.add_argument("-x", "--exe", required=True, help="ChampSim executable file")
    parser.add_argument("-l", "--local", type=int, choices=[0, 1], default=1, help="Local(1) or slurm(0) runs")

    args = parser.parse_args()

    if "CHAMPSIM_HOME" not in os.environ or "TRACE_SRC" not in os.environ:
        print("CHAMPSIM_HOME or TRACE_SRC environment variables not set")
        sys.exit(1)

    try:
        trace_info = parse_trace(args.tlist)
        exp_info = parse_exp(args.config)
    except Exception as e:
        print("Error parsing trace or experiment info:", e)
        traceback.print_exc()
        sys.exit(1)

    for trace in trace_info:
        for exp in exp_info:
            cmdline = generate_command(args.exe, exp["KNOBS"], trace["KNOBS"], trace["TRACE"], trace["NAME"], exp["NAME"], args.local)
            print(cmdline)

def generate_command(exe, exp_knobs, trace_knobs, trace_input, trace_name, exp_name, local):
    if local == 1:
        cmdline = f"{exe} {exp_knobs} {trace_knobs} {trace_input} > {trace_name}_{exp_name}.out 2>&1"
    else:
        slurm_cmd = f"sbatch --mincpus 1 -c 1 -J {trace_name}_{exp_name} -o {trace_name}_{exp_name}.out -e {trace_name}_{exp_name}.err wrapper "
        cmdline = slurm_cmd + f"{exe} {exp_knobs} {trace_knobs} {trace_input}"

    cmdline = cmdline.replace("$(CHAMPSIM_HOME)", os.environ['CHAMPSIM_HOME'])
    cmdline = cmdline.replace("$(TRACE_SRC)", os.environ['TRACE_SRC'])
    cmdline = cmdline.replace("$(TRACE)", trace_name)
    cmdline = cmdline.replace("$(EXP)", exp_name)

    return cmdline

if __name__ == "__main__":
    exit(main())
