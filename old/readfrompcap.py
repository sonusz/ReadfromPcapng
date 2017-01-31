import subprocess
import sys
import os
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
#import csv

class pcapfile: #used to get data from buffered file, or the original pcapng file. usage:a=pcapfile('filepath'); a.getdata('column','filter')
	def __init__(self, file_path):
		self.filepath=os.path.abspath(file_path)
		self.dirname=os.path.dirname(file_path)
		self.basename=os.path.basename(file_path)
		self.name_without_ext=os.path.splitext(self.basename)[0]
		self.new_png=os.path.join(self.dirname,self.name_without_ext+'.png')
	def read_from_pcap(self,columns,filter_str):
		syscmd="tshark -r \""+str(self.filepath)+"\" -Y \""+str(filter_str)+"\" -T fields"
		for column_name in columns:
			syscmd=syscmd+" -e \"frame."+str(column_name)+"\""
		print syscmd
		process=subprocess.Popen(syscmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = process.communicate()
		column=out.splitlines()
		i=0
		for line in column:
			column[i]=line.split()
			i=i+1
		return column
	def getdata(self,columns,filter_str): #e.g. getdata(['time_delta_displayed'],'ip.src==192.168.0.196&&ip.dst==192.64.172.182')
		self.datafile=os.path.join(self.dirname,self.name_without_ext+'_'+str(columns)+'.csv')
		try:
			csvfile=open(self.datafile,'rb')
			try:
				out=csvfile.read()
				csvfile.close()
				column=out.splitlines()		
				i=0
				for line in column:
					column[i]=line.split()
					i=i+1
				if len(column)==0:
					column=self.read_from_pcap(columns,filter_str)
					csvfile=open(self.datafile,'wb')
					csvfile.write("\n".join("\t".join(line)for line in array))
					csvfile.close()
			except:
				print "Unexpected error:", sys.exc_info()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			column=self.read_from_pcap(columns,filter_str)
			csvfile=open(self.datafile,'wb')
			csvfile.write("\n".join(column))
			csvfile.close()
			#print column
		except:
			print "Unexpected error 2:", sys.exc_info()[0]
		return column
