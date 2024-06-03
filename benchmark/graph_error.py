import os
import re
import matplotlib.pyplot as plt

# Set the path to the "sim_error_bench" folder
sim_error_bench_path = "benchmark/sim_error_bench"

# Get the list of files in the folder
files = os.listdir(sim_error_bench_path)

# Sort the files based on the numerical index
files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

# Initialize an empty list to store the percent of aligned queries for each file
aligned_queries_percent = []

# Iterate through each file in the sorted order
for file in files:
    # Open the file and read its content
    with open(os.path.join(sim_error_bench_path, file), "r") as f:
        content = f.read()
        
    # Use regular expression to extract the percent of aligned queries
    match = re.search(r"Percent of queries that aligned: ([\d.]+)", content)
    if match:
        aligned_queries_percent.append(float(match.group(1)))
    else:
        aligned_queries_percent.append(0.0)  # If the line is not found, assume 0% aligned queries

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(range(len(aligned_queries_percent)), aligned_queries_percent, marker="o")
plt.xlabel("Chance of Error (%)")
plt.ylabel("Percent of Aligned Queries")
plt.title("Aligned Queries Error Percentage")
plt.grid(True)
plt.xticks(range(len(aligned_queries_percent)))
plt.tight_layout()
plt.show()