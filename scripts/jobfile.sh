#
#Traces
#    ligra_BellmanFord.com-lj.ungraph.gcc_6.3.0_O3.drop_1750M.length_250M
#
# Experiment configurations
#    nopref: --warmup_instructions=100000000 --simulation_instructions=500000000 --config=$(CHAMPSIM_HOME)/config/nopref.ini
#    spp: --warmup_instructions=100000000 --simulation_instructions=500000000 --l2c_prefetcher_types=spp_dev2 --config=$(CHAMPSIM_HOME)/config/spp_dev2.ini
#
#
#
#
/home/das/ChampSim_base/ChampSim/bin/champsim --warmup_instructions=100000000 --simulation_instructions=500000000 --config=/home/das/ChampSim/config/nopref.ini --warmup_instructions=100000000 --simulation_instructions=150000000 /home/das/ChampSim/traces/ligra_BellmanFord.com-lj.ungraph.gcc_6.3.0_O3.drop_1750M.length_250M.champsimtrace.xz > ligra_BellmanFord.com-lj.ungraph.gcc_6.3.0_O3.drop_1750M.length_250M_nopref.out 2>&1
/home/das/ChampSim_base/ChampSim/bin/champsim --warmup_instructions=100000000 --simulation_instructions=500000000 --l2c_prefetcher_types=spp_dev2 --config=/home/das/ChampSim/config/spp_dev2.ini --warmup_instructions=100000000 --simulation_instructions=150000000 /home/das/ChampSim/traces/ligra_BellmanFord.com-lj.ungraph.gcc_6.3.0_O3.drop_1750M.length_250M.champsimtrace.xz > ligra_BellmanFord.com-lj.ungraph.gcc_6.3.0_O3.drop_1750M.length_250M_spp.out 2>&1
