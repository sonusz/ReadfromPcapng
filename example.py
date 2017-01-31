#!/usr/bin/env python
"""
Example code for ECE 8930 second assignment
"""
import read_pcap
import time_series
import rand_arr_time

def example1():
    """
    Example usage of read_pcap.py
    """
    files='*.pcap*'
    columns=['frame.time_relative'] # Time since reference or first frame
    filter_str=''
    output_file='a.txt'
    data=read_pcap.read_pcap_files(files, columns, filter_str, output_file)# Get packet arrive time, the output is a list of string
    arrive_time=[float(item[0]) for item in data]   # Format the list of strings to a list of floating numbers
    return arrive_time

def example2():
    """
    Example usage of rand_arr_time.py
    """
    arrive_time=rand_arr_time.rand_arr_time(6,100000,1000)  # Get packet arrive time, with option 2, 100000 packets, expected in 1000 seconds.
    return arrive_time

def example3():
    """
    Plot time series using arriving time
    """
    arrive_time=example2()                      # Get packets arrive time using example1
    time_series.plot_time_series(arrive_time)   # Plot time series using packets arrive time

def main():
    example3()

if __name__ == '__main__':
    main()