import subprocess
import sys
import os
#from copy import deepcopy
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
			syscmd=syscmd+" -e \""+str(column_name)+"\""
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
		self.datafile=os.path.join(self.dirname,self.name_without_ext+'_'+str(columns)+'.txt')
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
					csvfile.write("\n".join("\t".join(line)for line in column))
					csvfile.close()
			except:
				print "Unexpected error:", sys.exc_info()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			column=self.read_from_pcap(columns,filter_str)
			csvfile=open(self.datafile,'wb')
			csvfile.write("\n".join("\t".join(line)for line in column))
			csvfile.close()
			#print column
		except:
			print "Unexpected error 2:", sys.exc_info()[0]
		return column

def readpcapfiles(pcap_files,columns,filter_str,output_file):
	array=[]
	for pcap_file in pcap_files:
		temp_pcap_file=pcapfile(pcap_file)
		temp_array=temp_pcap_file.getdata(columns,filter_str)
		array=array+temp_array
		with open(output_file, "ab") as myfile:
			myfile.write("\n".join("\t".join(line)for line in temp_array))
	return array

def readdatafile(pcap_files,columns,filter_str,output_file):
	array=[]
	for pcap_file in pcap_files:
		temp_pcap_file=pcapfile(pcap_file)
		temp_array=temp_pcap_file.getdata(columns,filter_str)
		array=array+temp_array
		with open(output_file, "ab") as myfile:
			myfile.write("\n".join("\t".join(line)for line in temp_array))
	return array


import glob
files=glob.glob('/Users/s/Google Drive/research/SideChannelDetect/16PMUs_Wireshark/*.pcapng')


a=readpcapfiles(files,['frame.time_epoch','ip.src'],'ip.dst==130.127.88.235','/Users/s/Google Drive/research/SideChannelDetect/16PMUs_Wireshark/training_data.txt')
#a=pcapfile('/Users/s/Google Drive/research/SideChannelDetect/data/lol/lol_April5.pcapng')
a=pcapfile('/Users/s/Google Drive/research/SideChannelDetect/16PMUs_Wireshark/2015Dec_00001_20151214150440.pcapng')
#array=a.getdata(['frame.len','frame.time_delta_displayed'],'ip.src==192.168.0.196&&ip.dst==192.64.172.182')
array=a.getdata(['frame.time_delta_displayed','ip.src'],'ip.dst==130.127.88.235')
x=[float(line[0]) for line in array]
y=[float(line[1]) for line in array]
nbins = 1000
H, xedges, yedges = np.histogram2d(x,y,bins=nbins)
Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
plt.pcolormesh(xedges,yedges,Hmasked)
plt.show()

def plt_hist(array):
	array=[float(x) for x in array]
	#print out
	#print "hehe"
	plt.hist(array,1000,range=[-0.0005, 0.1])
	plt.show()
	#plt.savefig(self.new_png)
	plt.close('all')
