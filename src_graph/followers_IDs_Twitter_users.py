
from collections import defaultdict
import codecs, os

IN_DIR = "../../../DATA/mention_graph/"
os.chdir(IN_DIR)


F_IN = "followers/FOLLOWERS_ment_users_sorted"
F_OUT = "followers/FOLLOWERS_ment_IDs_sorted"



F_IN_IDs = "followers/user_IDs.dat"
def read_user_IDs():

	user_ids = defaultdict(int)

	with codecs.open(F_IN_IDs,'r', encoding='utf8') as f:
		for line in f:
			line = line.split()
			user_id = line[0]
			user =  line[1]
			user_ids[user] = user_id

	return user_ids


def read_and_save_IDs_followers():

	f2 = open(F_OUT, "w")

	user_ids = read_user_IDs()

	with codecs.open(F_IN,'r', encoding='utf8') as f:	
		cnt = 0
		for line in f:
			if not line.strip():
				continue
			line = line.split()
			userA = line[0]
			userB =  line[1]
			x1 = line[2]
			x2 = line[3]
			ID1 = user_ids[userA]
			ID2 = user_ids[userB]
			SR =  line[2]
			f2.write(ID1 + '\t' + ID2 + '\t' + str(x1) + '\t' + str(x2) + '\n')
			if cnt % 1000 == 0:
				print "Saved ", cnt, " users ", userA, userB
			cnt += 1
				
		print "Saved in", F_OUT 


read_and_save_IDs_followers()
