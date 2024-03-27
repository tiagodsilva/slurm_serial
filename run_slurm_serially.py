import re 
import os 

import argparse 
parser = argparse.ArgumentParser(description='SLURM parser for serial execution') 
parser.add_argument('--file', type=str, required=True)

def parse_slurm_file(filename): 
    with open(filename, 'r') as stream: 
        lines = stream.readlines() 
        assert '#!/bin/bash' in lines[0], f'{filename} doesn'"'"'t start with #!/bin/bash' 
        pattern = r'#SBATCH --array=(\d+)-(\d+)' 
        num_jobs = None 
        for line in lines:
            m = re.search(pattern, line) 
            if m is not None: 
                num_jobs = int(line[m.start(2):].strip()) - int(line[m.start(1):m.start(2)-1])    
                print(num_jobs) 
        assert num_jobs is not None, 'unspecified number of jobs' 

    return num_jobs 

def run_slurm_file(filename): 
    num_jobs = parse_slurm_file(filename) 
    for job_id in range(num_jobs): 
        os.environ['SLURM_ARRAY_TASK_ID'] = str(job_id)  
        os.system(f'bash {filename}') 
    
if __name__ == '__main__': 
    args = parser.parse_args() 
    run_slurm_file(args.file) 

