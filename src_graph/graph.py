from collections import defaultdict
import codecs
import matplotlib.pyplot as plt
import pylab as P
import numpy as np
import networkx as nx
import time
import matplotlib.dates as mdates
from datetime import datetime as d
from scipy.stats.stats import pearsonr, spearmanr

#import stats_about_tweet_data as stat

WORKING_FOLDER = "filter_more_20_tweets/"

f_in = WORKING_FOLDER + "tweets_with_usrs_with_more_than_20_tweets.dat"
f_out = WORKING_FOLDER + "graph_data.tab"
SEC_IN_DAY = 86400

f_out_one_side_inter = WORKING_FOLDER + "one_side_interaction_graph_more_5_tweets.tab"
f_out_reciprocal_inter = WORKING_FOLDER + "reciprocal_interaction_graph_more_5_tweets.tab"
f_in_SR_graph = WORKING_FOLDER + "graph_data_with_SR.tab"

'''
take the most requent edges, a.k.a. user pairs
that interacted the most
and let's print their interaction over time
---------------------------------
siledubh	kismit1496	461
KeithHagel	WayneHagel	265
pgnimmo	tcl189	223
tcl189	pgnimmo	220
garywright13	DarrenLA	152
xBon_Bonx	Elisha_Ro_Tii	87
jucksonline	Saydoh	85
'''

G = nx.DiGraph()
graph_with_SR = defaultdict(list)
one_side_interaction = defaultdict(list)
reciprocal_interaction = defaultdict(list)

def read_in_graph_with_time(f_in):
	global G
	cnt_all_tweets = 0
	#filtered_lst = stat.filter_users()
	found_usrs = defaultdict(int)
	user_tweets = defaultdict(list)
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		# the code loops through the input, collects tweets for each user into a dict
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	line = line.split()
	    	user1 = line[0]
	    	user2 = line[1]
	    	found_usrs[user1] = 1
	    	found_usrs[user2] = 1
	    	epoch_time = float(line[4])
	    	if G.has_edge(user1,user2):
	    		G[user1][user2]['weight'] += 1
	    		G[user1][user2]['time_line'].append(epoch_time)
	    	else:
	    		G.add_edge(user1, user2, weight=1, time_line = [epoch_time])
	print "Read ENG tweets: ", cnt_all_tweets
	#print len(filtered_lst), sum(found_usrs.values())

def graphs_stats():
	print "Created directed graph, with: ", G.number_of_nodes(), "nodes; and: ", G.number_of_edges(), " edges."
	print "7 maximum degrees of nodes: ", sorted(nx.degree(G).values())[-7:]
	print "7 maximum indegrees of nodes: ", sorted(G.in_degree().values())[-7:]
	print "7 maximum outdegrees of nodes: ", sorted(G.out_degree().values())[-7:]
	print "Connected components: ", len(nx.connected_components(G.to_undirected()))
	i = 0
	print "7 maximum connected components: "
	for el in sorted(nx.connected_components(G.to_undirected()), key=lambda x: len(x), reverse=True):
		i+=1
		print len(el)
		if i==7: break
	#nx.draw(G)
	#plt.show()
	

def plot_2_usr_interaction(usr1, usr2):
	interaction1, interaction2 = find_interaction(usr1, usr2)
	plot_timeline_epoch(usr1, usr2, interaction1, interaction2)

def save_direction_of_interaction(threshold=0):
	cnt_one_side_inter = 0
	cnt_reciprocal  = 0
	output_file = codecs.open(f_out_one_side_inter,'w', encoding='utf8')
	output_file2 = codecs.open(f_out_reciprocal_inter,'w', encoding='utf8')
	for edge in G.edges_iter(data=True):
		usr1 = edge[0]
		usr2 = edge[1]
		weight = int(edge[2]['weight'])
		interaction1, interaction2 = find_interaction(usr1, usr2)
		if interaction1 is not None and interaction2 is None:
			if weight > threshold:
				cnt_one_side_inter += 1
				output_file.write(usr1 + '\t' + usr2 + '\t' + str(weight) + '\n')
		if interaction1 is None and interaction2 is not None:
			if weight > threshold:
				cnt_one_side_inter +=1
				output_file.write(usr2 + '\t' + usr1 + '\t' + str(weight) + '\n')
		if interaction1 is not None and interaction2 is not None:
			if weight > threshold:
				cnt_reciprocal += 1
				output_file2.write(usr1 + '\t' + usr2 + '\t' + str(weight) + '\n')
	print "Threshold ", threshold, "Found: ", cnt_one_side_inter, " one side interaction edges, and: ", \
	 cnt_reciprocal, " reciprocal edges."
	output_file.close()
	output_file2.close()

def read_in_one_side_interaction():
	global one_side_interaction
	with codecs.open(f_out_one_side_inter, "r", encoding='utf8') as input_file:
		for line in input_file:
			line = line.split()
			usr1 = line[0]
			usr2 = line[1]
			weight = int(line[2])
			one_side_interaction[(usr1,usr2)] = weight

def read_in_reciprocal_interaction():
	global reciprocal_interaction
	with codecs.open(f_out_reciprocal_inter, "r", encoding='utf8') as input_file:
		for line in input_file:
			line = line.split()
			usr1 = line[0]
			usr2 = line[1]
			weight = int(line[2])
			reciprocal_interaction[(usr1,usr2)] = weight

def read_in_graph_with_SR():
	global graph_with_SR
	with codecs.open(f_in_SR_graph, "r", encoding='utf8') as input_file:
		for line in input_file:
			line = line.split()
			usr1 = line[0]
			usr2 = line[1]
			weight = int(line[2])
			SR = line[3]
			if SR == 'None' or SR == '-1':
				continue
			SR = float(SR)
			graph_with_SR[(usr1,usr2)] = (weight, SR)
	#return graph_with_SR


def find_interaction(usr1, usr2):
	if G.has_edge(usr1, usr2):
		interaction1 = G[usr1][usr2]['time_line']
	else:
		interaction1 = None
	if G.has_edge(usr2, usr1):
		interaction2 = G[usr2][usr1]['time_line']
	else:
		interaction2 = None
	if interaction1 or interaction2:
		return interaction1, interaction2
	print "No interaction found."
	return None, None

def extract_daily_interaction(interaction):
	tweets_per_day = defaultdict(int)
	days = [mdates.epoch2num(long(el - el%SEC_IN_DAY)) for el in interaction]
	days = set(days)
	for day in days:
		tweets_per_day[day] = sum(1 for el in interaction if mdates.epoch2num(long(el - el%SEC_IN_DAY)) == day)
	return tweets_per_day

def plot_timeline_epoch(usr1, usr2, interaction1=None, interaction2=None):
	print "########## Plotting for ", usr1, usr2, "###################"
	if interaction1 is not None:
		tweets_per_day1 = extract_daily_interaction(interaction1)
		plt.plot_date(x=tweets_per_day1.keys(), y=tweets_per_day1.values(), fmt=u'b*')
		print usr1, len(tweets_per_day1.keys()), sorted(tweets_per_day1.keys())
	if interaction2 is not None:
		#print usr2, len(interaction2)
		tweets_per_day2 = extract_daily_interaction(interaction2)
		plt.plot_date(x=tweets_per_day2.keys(), y=tweets_per_day2.values(), fmt=u'xr')
	if interaction1 is not None and interaction2 is not None:
		print usr1, usr2
		plt.title("Mentions 2 users: from " + usr1 + " (blue); from " + usr2 + " (red).")
	elif interaction1 is not None:
		plt.title("Mentions from " + usr1 + " to " + usr2 + ".")
	elif interaction2 is not None:
		plt.title("Mentions from " + usr2 + " to " + usr1 + ".")
	else:
		print "No interaction between 2 users to be plotted."
		return
	plt.xticks(rotation=70)
	plt.ylabel("# tweets per day")
	plt.grid(True)
	plt_name = WORKING_FOLDER + "2_usr_interaction/interaction_" + usr1 + "_and_" + usr2 + ".png"
	plt.savefig(plt_name, bbox_inches='tight', dpi=440)
	print "########## Plotting DONE for ", usr1, usr2, "###############"
	plt.clf()
	

def save_graph_data(f_out):
	output_file = codecs.open(f_out, 'w', encoding='utf8')
	for e in sorted(G.edges_iter(data=True), key=lambda x: x[2], reverse=True):
		#print e[0] + '\t' + e[1] + '\t' + str(e[2]['weight'])
		output_file.write(e[0] + '\t' + e[1] + '\t' + str(e[2]['weight']) + '\n')
	output_file.close()

# Could add MEDIAN here
def explore_SR_of_interaction_direction():
	SR_reciprocal_interaction = 0
	cnt_reciprocal_with_SR = 0
	for k in reciprocal_interaction.iterkeys():
		if k in graph_with_SR.keys():
			cnt_reciprocal_with_SR += 1
			SR_reciprocal_interaction += graph_with_SR[k][1]
	print "Average SR between the users with reciprocal mentions: ", SR_reciprocal_interaction / cnt_reciprocal_with_SR 
	print "Total: ", len(reciprocal_interaction.keys()), ". Found with SR: ", cnt_reciprocal_with_SR
	SR_one_side_interaction = 0
	cnt_one_side_with_SR = 0
	for k in one_side_interaction.iterkeys():
		if k in graph_with_SR.keys():
			cnt_one_side_with_SR += 1
			SR_one_side_interaction += graph_with_SR[k][1]
	print "Average SR between the users with unidirectional mentions: ", SR_one_side_interaction / cnt_one_side_with_SR
	print "Total: ", len(one_side_interaction.keys()), ". Found with SR: ", cnt_one_side_with_SR

# Do people who are more SR-related on Twitter also more talk to each other, i.e. mention each other?
def interaction_vs_SR(threshold = 0):
	SR_vec = []
	weight_vec = []
	read_in_graph_with_SR()
	for k in graph_with_SR.keys():
		w = float(graph_with_SR[k][0])
		sr = float(graph_with_SR[k][1])
		print k, w, sr
		if w > threshold and sr > 0:
			weight_vec.append(w)
			SR_vec.append(sr)
	print "Interaction," + str(threshold) + " threshold " + "vs. SR Pearson " , pearsonr(SR_vec, weight_vec)
	print
	print "Interaction," + str(threshold) + " threshold " + "vs. SR Spearman ", spearmanr(SR_vec, weight_vec)

####################################
# when G needed
####################################
# read_in_graph_with_time(f_in)
####################################

#############################
# plotting user interaction
#############################
'''
usr1_lst = ["siledubh", "KeithHagel", "pgnimmo", "garywright13", "xBon_Bonx", "jucksonline", "Kiss_nd_makeup"]
usr2_lst = ["kismit1496", "WayneHagel", "tcl189", "DarrenLA", "Elisha_Ro_Tii", "Saydoh", "JimmytHeGreeKK"]

for (usr1, usr2) in zip(usr1_lst, usr2_lst):
	plot_2_usr_interaction(usr1, usr2)
'''
############################
# general staff
############################
'''
read_in_graph_with_time(f_in)
graphs_stats()
save_graph_data(f_out)
'''
#################################
# direction of interaction
#################################
'''
read_in_graph_with_time(f_in)
save_direction_of_interaction(5)
'''
'''
read_in_one_side_interaction()
read_in_reciprocal_interaction()
read_in_graph_with_SR()
explore_SR_of_interaction_direction()
'''
#################################
# interaction vs. SR
#################################
#interaction_vs_SR(10)