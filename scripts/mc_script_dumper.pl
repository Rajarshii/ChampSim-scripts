my @benchmarks = ("~pgratz/dpc3_traces/607.cactuBSSN_s-2421B.champsimtrace.xz" , 
                  "~pgratz/dpc3_traces/628.pop2_s-17B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/654.roms_s-842B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/603.bwaves_s-3699B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/621.wrf_s-575B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/620.omnetpp_s-874B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/649.fotonik3d_s-1176B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/644.nab_s-5853B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/627.cam4_s-573B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/623.xalancbmk_s-700B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/619.lbm_s-4268B.champsimtrace.xz",
                  "~pgratz/dpc3_traces/602.gcc_s-734B.champsimtrace.xz",
		          "~pgratz/dpc3_traces/605.mcf_s-665B.champsimtrace.xz",
);                  
my $sets = 100;
my $numbers_per_set = 4;
my $max_number = 13;
my %benchmark_set_unique;
my @mix_t;
my @mix;
for ($i = 0; $i < $sets; $i++) {
    my %benchmark_set_choose;
    
    my $benchmark_set_unique_tag;
    my @benchmark_set_choose_keys;
    
    while (keys %benchmark_set_choose < $numbers_per_set) {
        my $random_number = int(rand($max_number)) + 1;
        $benchmark_set_choose{$random_number} = 1;
    }
    @benchmark_set_choose_keys = sort keys %benchmark_set_choose;
    $benchmark_set_unique_tag = $benchmark_set_choose_keys[3]*1000 + $benchmark_set_choose_keys[2]*100 + $benchmark_set_choose_keys[1]*10 + $benchmark_set_choose_keys[0];
    if($benchmark_set_unique{$benchmark_set_unique_tag} == 1){
        redo;
    } else{
        $benchmark_set_unique{$benchmark_set_unique_tag} = 1;
    }
    #print "1---",join(",", keys %benchmark_set_choose)," $benchmark_set_unique_tag\n";
    $mix_t[$i] = [keys %benchmark_set_choose];
    #print ("*********************\n");
    
}

for($i=0; $i < $sets ; $i++){
    for($j=0; $j < $numbers_per_set; $j++){
    	$mix[$i][$j] = $mix_t[$i][$j]-1;
    }
}

#my @prefetcher = ("no", "ip_stride", "next_line", "spp_dev", "va_ampm_lite");
my @prefetcher = ("no", "ip_stride", "spp_dev");

foreach $prefetcher_name (@prefetcher){
    for($i=1 ; $i<=100 ; $i++){
        $filename = "$prefetcher_name/mix$i.sh";
        #print "attempt to write to $filename\n";
        
        open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";  
        
        print $fh "#!/bin/bash\n";
        print $fh "#SBATCH --job-name=mc_$prefetcher_name\_$i\_$mix[$i-1][0]-$mix[$i-1][1]-$mix[$i-1][2]-$mix[$i-1][3]   # Job name\n";
        print $fh "#SBATCH --mail-type=END,FAIL         # Mail Events (NONE,BEGIN,FAIL,END,ALL)\n";
        print $fh "#SBATCH --mail-user=rdas40\@tamu.edu   # Replace with your email address\n";
        print $fh "#SBATCH --ntasks=1                   # Run on a single CPU\n";
        print $fh "#SBATCH --time=12:00:00              # Time limit hh:mm:ss\n";
        print $fh "#SBATCH --output=pref_research/results/$prefetcher_name/serial_test_%j.log  # Standard output and error log\n";
        print $fh "#SBATCH --qos=grad                   # Change to ugrad for undergrads\n";
        print $fh "#SBATCH --partition=non-gpu          # This job does not use a GPU\n";

        print $fh "echo \"mix$i for multicore $mix[$i-1][0]-$mix[$i-1][1]-$mix[$i-1][2]-$mix[$i-1][3]\"\n";
        print $fh "bin/multi_core/champsim_mc_$prefetcher_name \\\n";
        print $fh "  --warmup_instructions 50000000 \\\n";
        print $fh "  --simulation_instructions 150000000 \\\n";
        print $fh "  $benchmarks[$mix[$i-1][0]] \\\n";
        print $fh "  $benchmarks[$mix[$i-1][1]] \\\n";
        print $fh "  $benchmarks[$mix[$i-1][2]] \\\n";
        print $fh "  $benchmarks[$mix[$i-1][3]] \\\n";
        print $fh "  > pref_research/results/$prefetcher_name/mix$i\_mc_$mix[$i-1][0]_$mix[$i-1][1]_$mix[$i-1][2]_$mix[$i-1][3].txt\n";



    }
}




