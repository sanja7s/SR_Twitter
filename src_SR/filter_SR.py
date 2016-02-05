
from collections import defaultdict

f_in = "filter_IDs_SR"
f_out = "filter_IDs_SR_"


def read_filter_save(threshold = 0.95):

	f1 = open(f_in, "r")
	f_out2 = f_out + str(threshold)
	f2 = open(f_out2, "w")
	
	cnt = 0
	for line in f1:	
		cnt += 1 
		line = line.split()
		ID1 = line[0]
		ID2 =  line[1]
		SR =  line[2]
		if float(SR) >= threshold: 
			f2.write(ID1 + '\t' + ID2 + '\t' + SR + '\n')
		if cnt % 100000 == 0:
			print "Saved ", cnt, " users ", ID1, ID2
				
	print "Saved in ", f_out2, " # of connections ", cnt 

def main():

	read_filter_save()


main()

