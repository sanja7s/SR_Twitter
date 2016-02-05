
from collections import defaultdict
import codecs

f_in = "user_IDs.dat"
f_in_SR = "filter_user_SR_part_"
f_out = "filter_IDs_SR"




def read_user_IDs(f_in):

	user_ids = defaultdict(int)

	with codecs.open(f_in,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids


def read_and_save_IDs_SR(f_in_SR, f_out):

	f2 = open(f_out, "w")

	user_ids = read_user_IDs(f_in)
	
	for c in range(8):
		with codecs.open(f_in_SR + str(c),'r', encoding='utf8') as f:	
			cnt = 0
			for line in f:
				line = line.split()
				userA = line[0]
				userB =  line[1]
				ID1 = user_ids[userA]
				ID2 = user_ids[userB]
				SR =  line[2]
				f2.write(ID1 + '\t' + ID2 + '\t' + SR + '\n')
				if cnt % 10000 == 0:
					print "Saved ", cnt, " users ", userA, userB
				cnt += 1
					
			print "Saved in", f_out 

def main():

	read_and_save_IDs_SR(f_in_SR, f_out)


main()

