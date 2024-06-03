import os
import re
import matplotlib.pyplot as plt

# Set the paths to the "sim_genome_bench" and "sim_genome" folders
sim_genome_bench_path = "benchmark/sim_genome_bench"
sim_genome_path = "benchmark/sim_genome"

# Get the list of files in the "sim_genome_bench" folder
bench_files = os.listdir(sim_genome_bench_path)

# Sort the files based on the numerical index
bench_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Initialize empty lists to store the total time and sequence lengths
total_times = []
sequence_lengths = []

# Iterate through each file in the sorted order
for file in bench_files:
    # Extract the numerical index from the file name
    index = int(re.search(r'\d+', file).group())
    
    # Open the corresponding "genome{i}.fa" file and read its content
    genome_file = f"genome{index}.fa"
    with open(os.path.join(sim_genome_path, genome_file), "r") as f:
        genome_content = f.read()
    
    # Extract the sequence string from the genome file
    sequence = re.search(r"(?<=\n).*", genome_content, re.DOTALL).group().replace("\n", "")
    sequence_lengths.append(len(sequence))
    
    # Open the "genome_bench{i}.txt" file and read its content
    with open(os.path.join(sim_genome_bench_path, file), "r") as f:
        bench_content = f.read()
    
    # Use regular expression to extract the total time
    match = re.search(r"Total Time: ([\d.]+) seconds", bench_content)
    if match:
        total_times.append(float(match.group(1)))
    else:
        total_times.append(0.0)  # If the line is not found, assume 0 seconds

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(sequence_lengths, total_times, marker="o")
plt.xlabel("Genome Length (bp)")
plt.ylabel("Total Time (seconds)")
plt.title("Genome Length vs Runtime")
plt.grid(True)
plt.tight_layout()
plt.show()