import subprocess
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import csv


class Pcap_File_Reader:  # used to get data from buffered file, or the original pcapng file. usage:a=pcap_file_path('pcap_file_path'); a.read_pcap('data','filter')
    def __init__(self, file_path):
        self.pcap_file_path = os.path.abspath(file_path)
        self.dirname = os.path.dirname(file_path)
        self.basename = os.path.basename(file_path)
        self.name_without_ext = os.path.splitext(self.basename)[0]
        self.png_file_path = os.path.join(self.dirname, self.name_without_ext + '.png')
        self.csv_file_path = os.path.join(self.dirname, self.name_without_ext + '.csv')
        
    def _read_from_pcap(self, columns, filter_str):
        syscmd = 'tshark -r \'' + str(self.pcap_file_path) + '\' -Y \'' + str(filter_str) + '\' -T fields'
        for data_name in columns:
            syscmd = syscmd + ' -e \'' + str(data_name) + '\''
        print syscmd
        process = subprocess.Popen(syscmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        data = out.splitlines()
        i = 0
        for line in data:
            data[i] = line.split()
            i += 1
        return data

    def _create_csv(self,columns,filter_str):
        print 'Read from pcap(ng) file.'
        data = self._read_from_pcap(columns, filter_str)
        print 'Create buffer file.'
        with open(self.csv_file_path, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            all = []
            all.append(columns)
            all+=data
            writer.writerows(all)
        return data

    def _attach_columns_to_csv(self,columns,filter_str):
        print 'here'
        old_data = []           # A list to store old csv
        all = []                # A list to hold everything write back to csv
        with open(self.csv_file_path, 'rb') as csvinput:
            reader = csv.reader(csvinput)
            for row in reader:
                old_data.append(row)
        with open(self.csv_file_path, 'wb') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            row0=old_data.pop(0)     # Read from existing csv file and get the header
            new_columns=[]           # Colunms that doesn't exist in csv file
            columns_dict={}         # Create an index for the return data
            for column in columns:  # Check which columns that are not exist in csv file
                if column not in row0:
                    new_columns.append(column)
                    row0.append(column)
                columns_dict[column]=row0.index(column)
            print 'Read from pcap(ng) file.'
            data = self._read_from_pcap(new_columns, filter_str)
            print 'Add new column to buffer file.'
            all.append(row0)        # Attach the head line
            for i, row in enumerate(old_data):
                row+=data[i]        # Read each line from csv, attach data
                all.append(row)     # Attach new line
                data[i]=[row[columns_dict[column]] for column in columns ]# Replace data[i] with output data according to 'columns'
            writer.writerows(all)
        return data

    def read_pcap(self, columns,
                filter_str):  # e.g. read_pcap(['time_delta_displayed'],'ip.src==192.168.0.196&&ip.dst==192.64.172.182')
        try:
            with open(self.csv_file_path, 'rb') as csvinput:
                reader = csv.reader(csvinput)
                row0 = reader.next()
                columns_dict = {}       # Create an index for the return data
                for column in columns:  # Check which columns that are not exist in csv file
                    if column in row0:
                        columns_dict[column]=row0.index(column)
                    else:
                        data=self._attach_columns_to_csv(columns,filter_str)
                        return data
                data=[]
                print 'Read from buffer file.'
                for row in reader:
                    data.append([row[columns_dict[column]] for column in columns])
            return data
        except IOError as e:
            print 'No buffer file found.'
            data=self._create_csv(columns, filter_str)
            return data
        # print data
        except:
            print 'Unexpected error :', sys.exc_info()

def read_pcap_files(files, columns, filter_str, output_file):
    pcap_files = glob.glob(files)
    data = []                # A list to hold everything write back to csv
    with open(output_file, 'wb') as myfile:
        myfile.write('')
    for pcap_file in pcap_files:
        temp_pcap_file_reader = Pcap_File_Reader(pcap_file)
        temp_array = temp_pcap_file_reader.read_pcap(columns, filter_str)
        data += temp_array
        with open(output_file, 'ab') as myfile:
            myfile.write('\n'.join('\t'.join(line) for line in temp_array))
            myfile.write('\n')
    return data

