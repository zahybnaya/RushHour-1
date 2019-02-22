# get moves for every valid subject
# includes successful and unsuccessful trials
import json
import numpy as np

movefile = '/Users/chloe/Documents/RushHour/exp_data/moves.json'
outmovefile = '/Users/chloe/Documents/RushHour/exp_data/moves_filtered.json'
outfile = '/Users/chloe/Documents/RushHour/exp_data/'
# valid subjects
sublist = np.load('/Users/chloe/Documents/RushHour/exp_data/valid_sub.npy').astype(str)
sublist_flag = [False] * len(sublist)
out_data = []
print(sublist)


def all_moves():
	# load data
	with open(movefile) as f:
		for line in f:
			cur_line = json.loads(line)
			cur_sub = cur_line['subject']
			# print(cur_sub)
			if cur_sub in sublist:
				out_data.append(cur_line)
				sublist_flag[sublist.index(cur_sub)] = True
				print(cur_sub)
	# check unused subject
	for i in range(0, len(sublist_flag)):
		if not sublist_flag[i]:
			print('never used', sublist[i])
			print(i)
	print('data loaded')
	# write to file
	outfile = open(outmovefile, 'w+')
	for i in range(0, len(out_data)):
		json.dump(out_data[i], outfile)
		outfile.write('\n')





# execution
all_moves()



