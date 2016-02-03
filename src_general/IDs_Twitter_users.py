
from collections import defaultdict
import json
import codecs

f_in = "CV_usrs_v2.json"
f_out = "user_IDs.dat"





# for a faster processing for all user pairs, we do not want to query MongoDB for the text 
# more than once for one user; so here we read in all the precaclculated user CVs.
def read_all_user_CVs(f_in):

	user_ids = defaultdict(int)
	cnt = 0

	with open(f_in) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        user_ids[cnt] = usr
	        if cnt % 10000 == 0:
	        	print cnt, usr
	        cnt += 1

	return user_ids

def save_usr_IDs(user_ids, f_out):

	with codecs.open(f_out,'w', encoding='utf8') as f:
		for usr in user_ids.keys():
			f.write(str(usr) + '\t' + str(user_ids[usr]) + '\n')



def main():
	user_ids = read_all_user_CVs(f_in)
	save_usr_IDs(user_ids, f_out)



main()

