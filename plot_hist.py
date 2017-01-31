import subprocess
import sys
import os
#from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
#import csv
import glob
from scipy.cluster.vq import vq, kmeans, whiten

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
			del column[0]
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

def getKmeans(pcap_files,columns,filter_str):	
	centers=[[],[],[],[]]
	for pcap_file in pcap_files:
		temp_pcap_file=pcapfile(pcap_file)
		temp_array=temp_pcap_file.getdata(columns,filter_str)
		temp_array=[float(x[0]) for x in temp_array]
		features=np.array(temp_array)
		tk=kmeans(features,2)
#		print tk[0]
		ttk=tk[0].tolist()
		ttk.sort()
		centers[0].append(ttk[0])
		centers[1].append(ttk[1])
		breakpoint=0.5*(ttk[0]+ttk[1])
		ta=[]
		tb=[]
		for x in temp_array:
			if x<=breakpoint:
				ta.append(x)
			elif x>breakpoint:
				tb.append(x)
		ta=np.array(ta)
		centers[2].append(np.std(ta))
		tb=np.array(tb)
		centers[3].append(np.std(tb))
	return centers

def getKmean_all(pcap_files,columns,filter_str):
	clusters=[]
	array=[]
	for pcap_file in pcap_files:
		temp_pcap_file=pcapfile(pcap_file)
		temp_array=temp_pcap_file.getdata(columns,filter_str)
		temp_array=[float(x[0]) for x in temp_array]
		array=array+temp_array
	features=np.array(array)
	tk=kmeans(features,2)
#	print tk[0]
	ttk=tk[0].tolist()
	ttk.sort()
	breakpoint=0.5*(ttk[0]+ttk[1])
	clusters.append(ttk[0])
	clusters.append(ttk[1])
	ta=[]
	tb=[]
	for x in array:
		if x<=breakpoint:
			ta.append(x)
		elif x>breakpoint:
			tb.append(x)
	ta=np.array(ta)
	clusters.append(np.std(ta))
	tb=np.array(tb)
	clusters.append(np.std(tb))
	clusters.append(len(ta))
	clusters.append(len(tb))
	return clusters

files=glob.glob('week*')
#a=readpcapfiles(files,['frame.time_epoch','ip.src'],'ip.dst==130.127.88.235','training_data.txt')
#a=readpcapfiles(files,['frame.time_epoch','ip.src'],'ip.dst==130.127.88.235','training_data.txt')
#a=readpcapfiles(files,['frame.time_delta_displayed'],'ip.src==130.127.88.170','training_data.txt')
#a=readpcapfiles(files,['frame.time_delta_displayed'],'frame.len == 430 and ip.dst==192.168.0.165','training_data2.txt')
a=readpcapfiles(files,['frame.time_delta_displayed'],'','all.txt')
#a=[float(x[0]) for x in a if float(x[0])<0.15]
a=[float(x[0]) for x in a]
plt.hist(a[0:108000],100,range=[0.00, 0.1])
plt.xlabel('Delta Time (Second)')
plt.ylabel('Number of Packets')
plt.show()

c=getKmeans(files,['frame.time_delta_displayed'],'')
H=range(len(c[0]))

H=range(len(c[0][0:168]))
plt.plot(H,c[0][0:168],label="Certer of cluster \'a\'")
plt.plot(H,c[1][0:168],label="Certer of cluster \'b\'")
plt.xlabel('Time(Hour)')
plt.ylabel('K-Means Clustering Center')
plt.legend(loc='upper left')
plt.ylim([0,1])
plt.show()

plt.plot(H,c[2][0:168],label="Standard deviation of cluster \'a\'")
plt.plot(H,c[3][0:168],label="Standard deviation of cluster \'b\'")
plt.xlabel('Time(Hour)')
plt.ylabel('K-Means Clustering Standard Deviation')
plt.legend(loc='upper left')
plt.ylim([0,1])
plt.show()


d=getKmean_all(files,['frame.time_delta_displayed'],'')

plt.hist(b,100,range=[0.00, 0.5])
plt.xlabel('Delta Time (Second)')
plt.ylabel('Number of Packets')
plt.show()

