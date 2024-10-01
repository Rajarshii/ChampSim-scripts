## Example Usage of the scripts

### create_jobs.py
---
#### Create sweep scripts for ChampSim :
####    1. tlist: workloads (must include the number of warmpup and simulation instructions)
####    2. exp: experiment champsim binaries
####    3. outdir: root directory of the experiments. The scripts creates this directory and sub-directories for each experiment 


```
python3 create_jobs_v2.py --tlist demo_tlist.txt --exp demo_exp.txt --outdir dummy
```

---

###  gen_trace_combinations.py
---
#### Generate Trace Combinations for ChampSim :


```
python3 gen_trace_combinations.py -t testlist -mc 1 -c 8 -u 0 -M 250 -tl 8cor
```
