from read_pcap import *
#files = '/Users/s/Dropbox/research/SideChannelDetect/16PMUs_Wireshark/*.pcapng'#
#
#a = readpcap_file_paths(files, ['frame.time_epoch', 'ip.src'], 'ip.dst==130.127.88.235',
#                  '/Users/s/Dropbox/research/SideChannelDetect/16PMUs_Wireshark/training_data.txt')
## a=pcap_file_path('/Users/s/Google Drive/research/SideChannelDetect/data/lol/lol_April5.pcapng')
#a = pcap_file_path('/Users/s/Dropbox/research/SideChannelDetect/16PMUs_Wireshark/2015Dec_00001_20151214150440.pcapng')
## array=a.read_pcap(['frame.len','frame.time_delta_displayed'],'ip.src==192.168.0.196&&ip.dst==192.64.172.182')
#array = a.read_pcap(['frame.time_delta_displayed', 'ip.src'], 'ip.dst==130.127.88.235')
#x = [float(line[0]) for line in array]
#y = [float(line[1]) for line in array]
#nbins = 1000
#H, xedges, yedges = np.histogram2d(x, y, bins=nbins)
#Hmasked = np.ma.masked_where(H == 0, H)  # Mask pixels with a value of zero
#plt.pcolormesh(xedges, yedges, Hmasked)
#plt.show()
#
#
#def plt_hist(array):
#    array = [float(x) for x in array]
#    # print out
#    # print 'hehe'
#    plt.hist(array, 1000, range=[-0.0005, 0.1])
#    plt.show()
#    # plt.savefig(self.png_file_path)
#    plt.close('all')

def main():
    files='*.pcap*'
    columns=['frame.time_delta_displayed', 'frame.len']
    filter_str='!(ip.dst==127.0.0.1)'
    output_file='a.txt'
    data=read_pcap_files(files, columns, filter_str, output_file)

if __name__ == '__main__':
    main()