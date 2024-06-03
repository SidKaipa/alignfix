import os
import re
import matplotlib.pyplot as plt

# Set the paths to the "sim_reads_bench" and "sim_reads" folders
sim_reads_bench_path = "alignfix/benchmark/sim_reads_bench"
sim_reads_path = "alignfix/benchmark/sim_reads"

# Get the list of files in the "sim_reads_bench" folder
bench_files = os.listdir(sim_reads_bench_path)

# Sort the files based on the numerical index
bench_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Initialize empty lists to store the total time and line counts
total_times = []
line_counts = []

# Iterate through each file in the sorted order
for file in bench_files:
    # Extract the numerical index from the file name
    index = int(re.search(r'\d+', file).group())
    
    # Open the corresponding "reads{i}.fa" file and read its content
    reads_file = f"reads{index}.fa"
    with open(os.path.join(sim_reads_path, reads_file), "r") as f:
        reads_lines = f.readlines()
    
    # Count the number of non-empty lines and divide by 2
    line_count = sum(1 for line in reads_lines if line.strip()) // 2
    line_counts.append(line_count)
    
    # Open the "reads_bench{i}.txt" file and read its content
    with open(os.path.join(sim_reads_bench_path, file), "r") as f:
        bench_content = f.read()
    
    # Use regular expression to extract the total time
    match = re.search(r"Total Time: ([\d.]+) seconds", bench_content)
    if match:
        total_times.append(float(match.group(1)))
    else:
        total_times.append(0.0)  # If the line is not found, assume 0 seconds

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(line_counts, total_times, marker="o")
plt.xlabel("Number of Reads")
plt.ylabel("Total Time (seconds)")
plt.title("Number of Reads vs Runtime")
plt.grid(True)
plt.tight_layout()
plt.show()