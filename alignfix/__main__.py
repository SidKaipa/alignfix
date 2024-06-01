#!/usr/bin/env python
import argparse
import numpy as np
from suffix_arr import SA
from alignment import Alignment
from pyfaidx import Fasta
import os
import sys
import time
def print_error(msg):
    """
   Writing an error message

   Parameters
   ----------
   msg : string
       the error message to be printed
   Returns
   -------
   void
   """
    sys.stderr.write("[ERROR]: {msg}\n".format(msg=msg))
    sys.exit(1)
def output_benchmark(file, time_reading, time_aligning, query_count, query_failures):
    """
    Outputs the benchmark results

    Parameters
    ----------
    file: string
        The path to the output benchmark file
    time_reading: float
        The time taken to read the inputs
    time_aligning: float
        The time taken to align the inputs
    query_count: int
        The number of queries in the inputs
    query_failures: int
        The number of queries that failed to align in the inputs
    Returns
    -------
    void
    """
    if not "\\" in file:
        directory = os.getcwd()
    else:
        directory = os.path.dirname(file)
    if not os.path.isdir(directory):
        print_error("Directory {directory} does not exist".format(directory=directory))
        sys.exit(1)

    total_time = time_reading + time_aligning
    percent_aligned = float(query_count - query_failures) / float(query_count)
    with open(file, 'w') as f:
        f.write('Time to Read Input: {:.2f} s\n'.format(time_reading))
        f.write('Time to Align: {:.2f} seconds\n'.format(time_aligning))
        f.write('Total Time: {:.2f} seconds\n'.format(time_reading + time_aligning))
        f.write('Number of queries that failed: {:d}\n'.format(query_failures))
        f.write('Percent of queries that aligned: {:.2f}\n'.format(percent_aligned))
    print(total_time)
    return

def extractDatabase(file):
    """
    Extracting the database

    Parameters
    ----------
    file: string
        The path to the input genome file
    Returns
    -------
    database: string
        the contents of the genome file concatenated into a string
    """
    if not os.path.exists(file):
        print_error("The input genome file does not exist!")
    database = ''
    with open(file, "r") as f:
        for line in f:
            if '>' in line:
                continue
            database += line.strip()
    return database
def write_alignment(o_file, name, alignment, query_count, start, end):
    """
    Writing an alignment to an output file

    Parameters
    ----------
    0_file : string
        The path to the output alignment file
    name : string
        The name of the query
    alignment : Alignment
        The alignment to be written
    Returns
    -------
    void
    """
    if not "\\" in o_file:
        directory = os.getcwd()
    else:
        directory = os.path.dirname(o_file)
    if not os.path.isdir(directory):
        print_error("Directory {directory} does not exist".format(directory=directory))
        sys.exit(1)

    if query_count == 1:
        with open(o_file, "w") as f:
            f.write(">" + name + "\n")
            f.write(alignment[2] + "\n")
            f.write(alignment[1] + "\n")
            f.write("Score: " + str(alignment[0]) + "\n")
            f.write("Start position in database sequence: " + str(start) + '\n')
            f.write("End position in database sequence: " + str(end) + '\n')
        f.close()
        return

    with open(o_file, "a") as f:
        f.write(">" + name + "\n")
        f.write(alignment[2] + "\n")
        f.write(alignment[1] + "\n")
        f.write("Score: " + str(alignment[0]) + "\n")
        f.write("Start position in database sequence: " + str(start) + '\n')
        f.write("End position in database sequence: " + str(end) + '\n')
    f.close()
    return
def write_failure(o_file, name, query_count):
    """
    Writing a failing alignment to an output file (query not found)

    Parameters
    ----------
    0_file : string
        The path to the output alignment file
    name : string
        The name of the query
    Returns
    -------
    void
    """
    if not "\\" in o_file:
        directory = os.getcwd()
    else:
        directory = os.path.dirname(o_file)
    if not os.path.isdir(directory):
        print_error("Directory {directory} does not exist".format(directory=directory))
        sys.exit(1)

    if query_count == 1:
        with open(o_file, "w") as f:
            f.write(">" + name + "\n")
            f.write("Query not found!!")
            f.write("Query not found!!")
            f.write("Score: " + str(-1) + "\n")
        f.close()
        return

    with open(o_file, "a") as f:
        f.write(">" + name + "\n")
        f.write("Query not found!!)
        f.write("Query not found!!")
        f.write("Score: " + str(-1) + "\n")
    f.close()
    return

def main():

    # parser
    parser = argparse.ArgumentParser(prog='alignfix',
                                     description='A seed and extends aligner.\n\nThis program aligns queries against a genome using a seed-and-extend approach. It takes a genome file, a query file, and produces an output file with the alignments.',
                                     epilog='''\
                                     additional information:
                                        version: 0.1
                                     ''')

    # genome
    parser.add_argument('-g', '--genome', help='Path to the genome file', required=True)

    #query
    parser.add_argument('-q', '--query', help='Path to the query file', required=True)

    #output file
    parser.add_argument('-o', '--output', help='Path to the output file', required=True)

    # benchmark file
    parser.add_argument('-b', '--benchmark', help='Path to the benchmark file', required=False)

    args = parser.parse_args()

    # Check if the required arguments are provided
    if not args.genome or not args.query or not args.output:
        parser.print_help()
        print_error("Please provide a genome file, a query file, and an output file.")
        return 1

    # benchmark values
    query_count = 0
    query_failures = 0
    time_reading = 0
    time_aligning_outputting = 0

    # start time for reading
    start_reading = time.time()


    # queries -> pyfaidx
    if not os.path.exists(args.query):
        print_error("The input query file does not exist!")
    queries = Fasta(args.query)

    # database
    database = extractDatabase(args.genome)
    sa = SA(database)

    # end time for reading
    end_reading = time.time()
    time_reading += end_reading - start_reading

    # starting time for aligning
    start_alignment = time.time()

    for query in queries.keys():

        query_count += 1

        seeds = None
        for i in range(0, len(queries[query]) - 15 + 1):
            seeds = sa.Seeds(str(queries[query][i:i + 15]))
            if -42 in seeds and -69 in seeds:
                continue
            else:
                break

        # check seed exists
        if seeds is None:
            query_name = query
            write_failure(args.output, query_name, query_count)
            query_failures += 1
            continue

        # calculating the optimal alignment given our set of seeds
        max_score = -9999
        best_alignment = None
        start = -1
        end = -1
        for seed in seeds:
            r = int(len(queries[query]) * 2)
            if seed - (r//2) < 0:
                db_small = database[:int(seed + (r//2))]
                shifted_seed = int(seed)
            elif seed + (r//2) > len(database):
                db_small = database[int(seed - (r//2)):]
                shifted_seed = int(seed - (r//2))
            else:
                db_small = database[int(seed - (r // 2)) : int(seed + (r // 2))]
                shifted_seed = int(len(db_small) - (r // 2))
            l = 15
            a = Alignment(db_small, str(queries[query]), shifted_seed, l, r)

            if a.upper_alignment == -1:
                query_name = query
                write_failure(args.output, query_name, query_count)
                query_failures += 1
                continue

            results = a.Align()
            if results[0] > max_score:
                best_alignment = results
                start = seed - best_alignment[3]
                end = seed + best_alignment[4] + 15

        print("Processed " + str(query_count) + " so far")
        # writing results to output file
        if best_alignment is not None:
            query_name = query
            write_alignment(args.output, query_name, best_alignment, query_count, start, end)
            query_name = ''
            best_alignment = None
        else:
            query_name = query
            write_failure(args.output, query_name, query_count)
            query_failures += 1
            query_name = ''

    #ending time for alignment
    end_alignment = time.time()
    time_aligning_outputting += end_alignment - start_alignment

    #output benchmark file
    if args.benchmark:
        output_benchmark(args.benchmark, time_reading, time_aligning_outputting, query_count, query_failures)

    return 0
                
if __name__ == "__main__":
    main()
