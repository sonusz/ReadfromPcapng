
a=pcapfile('/Users/s/Google Drive/research/SideChannelDetect/data/lol/lol_April5.pcapng')
array=a.getdata(['len','time_delta_displayed'],'ip.src==192.168.0.196&&ip.dst==192.64.172.182')
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
