import subprocess
import sys
import os
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from numpy import linspace,hstack
from scipy.stats.kde import gaussian_kde

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
		print len(column)
		i=0
		for line in column:
			column[i]=line.split()
			i=i+1
		print len(column)
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
				#if len(column)==0:
				#	column=self.read_from_pcap(columns,filter_str)
				#	csvfile=open(self.datafile,'wb')
				#	csvfile.write("\n".join("\t".join(line)for line in column))
				#	csvfile.close()
			except:
				print "Unexpected error:", sys.exc_info()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			column=self.read_from_pcap(columns,filter_str)
			csvfile=open(self.datafile,'wb')
			print len(column)
			time.sleep(5)
			tmpdata="\n".join(column)
			csvfile.write(tmpdata)
			csvfile.close()
			#print column
		except:
			print "Unexpected error 2:", sys.exc_info()[0]
		return column


new_png=''
array=[]

for i in range(1,len(sys.argv)):
	filepath=os.path.abspath(sys.argv[i])
	dirname=os.path.dirname(filepath)
	basename=os.path.basename(filepath)
	name_without_ext=os.path.splitext(basename)[0]
	new_png=os.path.join(dirname,name_without_ext+'.png')
	tmppcap=pcapfile(filepath)
	arr=tmppcap.getdata(['time_delta_displayed','len'],'eth.src == a4:1f:72:93:6f:36 && dns')
	#process=subprocess.Popen("tshark -r \""+filepath+"\" -Y \"eth.src == a4:1f:72:93:6f:36 && dns\" -T fields -e  \"frame.time_delta_displayed\" ", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#out, err = process.communicate()
	#returncode = process.returncode
	#arr=[]
	#arr=out.splitlines()
	print len(arr)
	array=array+arr
	#print out
	#print "hehe"

arr=[int(row[1]) for row in array]

plt.hist(arr,150,range=[0, 150])
#plt.plot(x,y3)
plt.savefig(new_png)
plt.close('all')