import subprocess
import sys
import os
from copy import deepcopy

class pcapfile: #used to get data from buffered file, or the original pcapng file. usage:a=pcapfile('filepath'); a.getdata('column')
	def __init__(self, file_path):
		self.filepath=os.path.abspath(file_path)
		self.dirname=os.path.dirname(file_path)
		self.basename=os.path.basename(file_path)
		self.name_without_ext=os.path.splitext(self.basename)[0]
#		self.datafile=os.path.join(self.dirname,self.name_without_ext+'.csv')
	def read_from_pcap(self,column_name):
#		syscmd="tshark -r \""+str(self.filepath)+"\" -Y \"(frame.number>1000)&&(esp||synphasor)&&((eth.src == 00:30:a7:07:9e:de)||(eth.dst == 00:30:a7:07:9e:df)||(eth.src == 00:30:a7:07:9f:26))\" -T fields -e  \"frame."+str(column_name)+"\" "
		syscmd="tshark -r \""+str(self.filepath)+"\" -Y \"((esp||synphasor)&&(eth.src == 00:30:a7:07:9e:de)&&((frame.len == 486 || frame.len == 278 || frame.len == 422 || frame.len == 582 || frame.len == 726 || frame.len == 886 || frame.len == 1046 || frame.len == 1190 || frame.len == 1350 || frame.len == 1510 || frame.len == 1654)))||(ip.src == 192.168.65.2)\" -T fields -e  \"frame."+str(column_name)+"\" "
		process=subprocess.Popen(syscmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = process.communicate()
		column=out.splitlines()
		return column
	def getdata(self,column_name): #e.g. getdata('time_delta_displayed')
		self.datafile=os.path.join(self.dirname,self.name_without_ext+'_'+str(column_name)+'.csv')
		try:
			csvfile=open(self.datafile,'rb')
			try:
				out=csvfile.read()
				csvfile.close()
				column=out.splitlines()
				if len(column)==0:
					column=self.read_from_pcap(column_name)
					csvfile=open(self.datafile,'wb')
					csvfile.write("\n".join(column))
					csvfile.close()
			except:
				print "Unexpected error:", sys.exc_info()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			column=self.read_from_pcap(column_name)
			csvfile=open(self.datafile,'wb')
			csvfile.write("\n".join(column))
			csvfile.close()
			#print column
		except:
			print "Unexpected error 2:", sys.exc_info()[0]
		#column = map(float, column) #convert type if necessary
		return column

