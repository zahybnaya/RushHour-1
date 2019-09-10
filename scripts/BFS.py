# BFS model

import MAG, rushhour
import random, sys, copy, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from graphviz import Digraph

# global w0, w1, w2, w3, w4, w5, w6, w7, noise, weights
# w0 = None
# w1 = None
# w2 = None
# w3 = None
# w4 = None
# w5 = None
# w6 = None
# w7 = None
# noise = None
# weights = [w0, w1, w2, w3, w4, w5, w6, w7]
all_instances = ['prb8786', 'prb11647', 'prb21272', 'prb13171', 'prb1707', 'prb23259', 'prb10206', 'prb2834', 'prb28111', 'prb32795', 'prb26567', 'prb14047', 'prb14651', 'prb32695', 'prb29232', 'prb15290', 'prb12604', 'prb20059', 'prb9718', 'prb29414', 'prb22436', 'prb62015', 'prb38526', 'prb3217', 'prb34092', 'prb12715', 'prb54081', 'prb717', 'prb31907', 'prb42959', 'prb79230', 'prb14898', 'prb62222', 'prb68910', 'prb33509', 'prb46224', 'prb47495', 'prb29585', 'prb38725', 'prb33117', 'prb20888', 'prb55384', 'prb6671', 'prb343', 'prb68514', 'prb29600', 'prb23404', 'prb19279', 'prb3203', 'prb65535', 'prb14485', 'prb34551', 'prb72800', 'prb44171', 'prb1267', 'prb29027', 'prb24406', 'prb58853', 'prb24227', 'prb45893', 'prb25861', 'prb15595', 'prb54506', 'prb48146', 'prb78361', 'prb25604', 'prb46639', 'prb46580', 'prb10166', 'prb57223']	

class Node:
	def __init__(self, cl):
		self.__car_list = cl
		self.__children = []
		self.__value = None
		self.__value_bylevel = None
		self.__tag = None
		self.__pos1 = None
		self.__pos2 = None

	def add_child(self, n):
		n.set_parent(self)
		self.__children.append(n)

	def add_move(self, tag, pos1, pos2):
		self.__tag = tag
		self.__pos1 = pos1
		self.__pos2 = pos2
		for car in self.__car_list:
			if car.tag == self.__tag:
				self.__pos1old, self.__pos2old = car.start[0], car.start[1]

	def get_move(self):
		return self.__tag, self.__pos1, self.__pos2, self.__pos1old, self.__pos2old

	def set_parent(self, p):
		self.__parent = p

	def set_value(self, v):
		self.__value = v

	def get_carlist(self):
		return self.__car_list

	def get_red(self):
		for car in self.__car_list:
			if car.tag == 'r':
				return car

	def get_board(self):
		tmp_b, _ = MAG.construct_board(self.__car_list)
		return tmp_b

	def get_value(self):
		if self.__value == None:
			# self.__value, self.__value_bylevel = Value1(self.__car_list, self.get_red())
			self.__value= Manhattan_Value(self.__car_list, self.get_red())
		return self.__value

	def get_value_bylevel(self):
		return self.__value_bylevel

	def get_child(self, ind):
		return self.__children[ind]

	def get_children(self):
		return self.__children

	def find_child(self, c):
		for i in range(len(self.__children)):
			if self.__children[i] == c:
				return i
		return None

	def clean_children(self):
		self.__children = []

	def get_parent(self):
		return self.__parent
	
	def remove_child(self, c):
		for i in range(len(self.__children)):
			if self.__children[i] == c:
				c.parent = None
				self.__children.pop(i)
				return	

	def update_carlits(self, cl):
		self.__car_list = cl
		self.__board, self.__red = MAG.construct_board(self.__car_list)
		# self.__value, self.__value_bylevel = Value1(self.__car_list, self.__red)		
		self.__value, self.__value_bylevel = Manhattan_Value(self.__car_list, self.__red)		

	def print_children(self):
		print('total number of children: '+str(len(self.__children)))
		for i in range(2):
			print('print first two children: '+str(i))
			print(MAG.board_to_str(self.__children[i].get_board()))

	def board_to_str(self):
		tmp_board, tmp_red = MAG.construct_board(self.__car_list)
		out_str = ''
		for i in range(tmp_board.height):
			for j in range(tmp_board.width):
				cur_car = tmp_board.board_dict[(j, i)]
				if cur_car == None:
					out_str += '.'
					if i == 2 and j == 5:
						out_str += '>'
					continue
				if cur_car.tag == 'r':
					out_str += 'R'
				else:
					out_str += cur_car.tag
				if i == 2 and j == 5:
					out_str += '>'
			out_str += '\n'
		return out_str




def Value1(car_list2, red):
	'''
	value = w0 * num_cars{MAG-level 0}
		+ w1 * num_cars{MAG-level 1} 
		+ w2 * num_cars{MAG-level 2}  
		+ w3 * num_cars{MAG-level 3} 
		+ w4 * num_cars{MAG-level 4} 
		+ w5 * num_cars{MAG-level 5} 
		+ w6 * num_cars{MAG-level 6}
		+ w7 * num_cars{MAG-level 7}  
		+ noise
	'''
	num_parameters = 8
	value_level = []
	# [w0, w1, w2, w3, w4, w5, w6, w7] = [-1,-1,-1,-1,-1,-1,-1,-1]
	# weights = [w0, w1, w2, w3, w4, w5, w6, w7]
	noise = np.random.normal(loc=mu, scale=sigma)
	value = 0
	# initialize MAG
	my_board2, my_red2 = MAG.construct_board(car_list2)
	new_car_list2 = MAG.construct_mag(my_board2, my_red2)
	# number of cars at the top level (red only)
	value += w0 * 1 
	value_level.append(1)
	# each following level
	for j in range(num_parameters - 1): 
		level = j+1
		new_car_list2 = MAG.clean_level(new_car_list2)
		new_car_list2 = MAG.assign_level(new_car_list2, my_red2)
		cars_from_level = MAG.get_cars_from_level2(new_car_list2, level)
		value += weights[level] * (len(cars_from_level))
		value_level.append(len(cars_from_level))
	return value+noise, value_level


def Manhattan_Value(car_list2, red):
	''' value function is manhattan distance,
		start by converting car_list to instance,
		need to import Zahy's rushhour.py functions
	'''
	h,v = {},{}
	name = ''
	for car in car_list2:
		if car.orientation == 'horizontal':
			h[car.tag] = (car.start[0], car.start[1], car.length)
		elif car.orientation == 'vertical':
			v[car.tag] = (car.start[0], car.start[1], car.length)
	cur_ins = rushhour.RHInstance(h,v,name)
	value = rushhour.min_manhattan_distance_calc(cur_ins)
	print('following board: manhattan distance '+str(value))
	print('board:\n'+Node(car_list2).board_to_str())
	return -value






def DropFeatures(delta):
	pass


def Lapse(probability=0.1): 
	''' return true with a probability '''
	return random.random() < probability


def Stop(probability=0.1): 
	''' return true with a probability '''
	return random.random() < probability


def Determined(root_node): 
	''' return true if win, false otherwise '''
	return MAG.check_win(root_node.get_board(), root_node.get_red())


def RandomMove(node):
	''' make a random move and return the resulted node '''
	return random.choice(node.get_children())
	

def InitializeChildren(root_node):
	''' initialize the list of children (using all possible moves) '''
	if len(root_node.get_children()) == 0:
		tmp = copy.deepcopy(root_node)
		all_moves = MAG.all_legal_moves(tmp.get_carlist(), tmp.get_red(), tmp.get_board())
		for i, (tag, pos) in enumerate(all_moves):
			new_list, _ = MAG.move2(tmp.get_carlist(), tag, pos[0], pos[1])
			dummy_child = Node(new_list)
			dummy_child.add_move(tag, pos[0], pos[1])
			root_node.add_child(dummy_child)


def SelectNode(root_node):
	''' return the child with max value '''
	n = root_node
	traversed = []
	while len(n.get_children()) != 0:
		n = ArgmaxChild(n)
		traversed.append(n)
	return n, traversed
 

def ExpandNode(node, threshold):
	''' create all possible nodes under input node, 
	cut the ones below threshold '''
	if len(node.get_children()) == 0:
		InitializeChildren(node)
	Vmax = MaxChildValue(node)
	for child in node.get_children():
		if abs(child.get_value() - Vmax) > threshold:
			node.remove_child(child)
	return ArgmaxChild(node)


def Backpropagate(this_node, root_node):
	''' update value back until root node '''
	this_node.set_value(MaxChildValue(this_node))
	if this_node != root_node:
		Backpropagate(this_node.get_parent(), root_node)


def MaxChildValue(node): 
	''' return the max value from node's children '''
	Vmax = -float('inf')
	for child in node.get_children():
		if Vmax < child.get_value():
			Vmax = child.get_value()
	return Vmax


def ArgmaxChild(root_node): 
	''' return the child with max value '''
	maxChild = None
	for child in root_node.get_children():
		if maxChild == None:
			maxChild = child
		elif maxChild.get_value() < child.get_value():
			maxChild = child
	return maxChild


def MakeMove(state, delta=0, gamma=0.1, theta=float('inf')):
	''' returns an optimal move to make next, given current state '''
	root = state # state is already a node
	InitializeChildren(root)
	if Lapse():
		print('Random move made')
		return RandomMove(root), [], []
	else:
		DropFeatures(delta)
		# debug = 0
		considered_node = [] # nodes already traversed along the branch in this ieration
		considered_node2 = [] # new node expanded along the branch in this iteration
		while not Stop(probability=gamma) and not Determined(root):
			n, traversed = SelectNode(root)
			considered_node.append(traversed)
			# debug += 1
			n2 = ExpandNode(n, theta)
			considered_node2.append(n2)
			Backpropagate(n, root)
	return ArgmaxChild(root), considered_node, considered_node2


def estimate_prob(root_node, exp_str='', iteration=1000):
	''' Estimate the probability of next possible moves given the root node '''
	InitializeChildren(root_node)
	frequency = [0] * len(root_node.get_children())
	for i in range(iteration):
		new_node, _, _ = MakeMove(root_node)
		child_idx = root_node.find_child(new_node)
		frequency[child_idx] += 1
	
	frequency = np.array(frequency, dtype=np.float32)/iteration
	chance = float(1)/float(len(frequency))

	sol_idx = None
	sol_value_level = None
	for i in range(len(root_node.get_children())):
		if root_node.get_child(i).board_to_str() == exp_str:
			sol_idx = i
			sol_value_level = root_node.get_child(i).get_value_bylevel()

	return root_node.get_children(), frequency, sol_idx, sol_value_level, chance


def solution_prob(instance):
	''' print probability of selecting solution moves 
		at each position along the optimal solution '''
	ins_dir = '/Users/chloe/Documents/RushHour/exp_data/data_adopted/'
	ins_file = ins_dir + instance + '.json'
	solution = np.load('/Users/chloe/Documents/RushHour/exp_data/' + instance + '_solution.npy')
	print('instance '+instance)
	print('optimal solution length '+str(len(solution)))
	sol_prob = []
	chance = []
	sol_vlevel = []

	# construct initial state/node
	initial_car_list, initial_red = MAG.json_to_car_list(ins_file)
	initial_board, initial_red = MAG.construct_board(initial_car_list)
	print('Initial board:\n'+MAG.board_to_str(initial_board))
	initial_node = Node(initial_car_list)

	cur_node = initial_node
	cur_carlist = initial_car_list
	
	for i in range(len(solution)):
		sol = solution[i]
		car_to_move = sol[0]
		if car_to_move == 'R':
			car_to_move = 'r'
		move_by = int(sol[2:])
		cur_carlist, _ = MAG.move_by(cur_carlist, car_to_move, move_by)
		if i == len(solution)-1:
			cur_carlist, _ = MAG.move2(cur_carlist, car_to_move, 4, 2)
		cur_board, _ = MAG.construct_board(cur_carlist)
		sol_board_str = MAG.board_to_str(cur_board)
		# print('solution child\n'+sol_board_str)
		_, frequency, sol_idx, v_level, ch= estimate_prob(cur_node, sol_str=sol_board_str)
		cur_node = cur_node.get_child(sol_idx)
		sol_prob.append(frequency[sol_idx])
		sol_vlevel.append(v_level)
		chance.append(ch)

	return sol_prob, sol_vlevel, chance
	
	

def plot_trial(this_w0=0, this_w1=0, this_w2=0, this_w3=-1, this_w4=0, this_w5=0, this_w6=0, this_w7=0, this_mu=0, this_sigma=1):
	''' show movie of the model's consideration of next moves (with tree expansion)
		based on subject's current position from a trial'''
	global w0, w1, w2, w3, w4, w5, w6, w7, mu, sigma, weights
	w0 = this_w0
	w1 = this_w1
	w2 = this_w2
	w3 = this_w3
	w4 = this_w4
	w5 = this_w5
	w6 = this_w6
	w7 = this_w7
	mu = this_mu
	sigma = this_sigma
	weights = [w0, w1, w2, w3, w4, w5, w6, w7]
	trial_start = 2 # starting row number in the raw data
	trial_end = 20 # ending row number in the raw data
	global plot_tree_flag # whether to visialize the tree at the same time
	plot_tree_flag = True
	sub_data = pd.read_csv('/Users/chloe/Desktop/trialdata_valid_true_dist7_processed.csv')
	dir_name = '/Users/chloe/Desktop/RHfig/' # dir for new images
	os.chdir(dir_name)

	# construct initial node
	first_line = sub_data.loc[trial_start-2,:]
	instance = first_line['instance']
	ins_dir = '/Users/chloe/Documents/RushHour/exp_data/data_adopted/'
	ins_file = ins_dir + instance + '.json'
	initial_car_list, initial_red = MAG.json_to_car_list(ins_file)
	initial_board, initial_red = MAG.construct_board(initial_car_list)
	initial_node = Node(initial_car_list)
	print('Initial board:\n'+initial_node.board_to_str())
	
	# initialize parameters
	cur_node = initial_node
	cur_carlist = initial_car_list
	move_num = 1 # move number in this human trial
	img_count = 0 # image count



	# every move in the trial
	for i in range(trial_start-1, trial_end-2):
		
		# plot text
		plot_blank(instance, img_count, text='Move Number '+str(move_num), color='orange')
		# initialize tree plot if required
		if plot_tree_flag:
			dot = Digraph(comment='Test Tree', format='jpg', strict=True)
			dot.attr(size='8,8', fixedsize='true')
			# dot.attr('node', shape='circle', fixedsize='true', width='0.9')
			dot.node(str(id(initial_node)), str(initial_node.get_value()))
			plot_blank(instance, img_count, text='Move Number '+str(move_num), color='orange', imgtype='tree')
		# increment image number
		img_count += 1
		# plot blank space
		plot_blank(instance, img_count, text='Initial Board', color='orange')
		if plot_tree_flag:
			plot_blank(instance, img_count, text='Initial Board', color='orange', imgtype='tree')
		img_count += 1
		# plot initial board
		plot_state(cur_node, instance, img_count)
		if plot_tree_flag:
			dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
		img_count += 1
		# sys.exit()


		# load data from datafile
		print('Move number '+str(move_num))
		row = sub_data.loc[i, :]
		piece = row['piece']
		move_to = row['move']


		# run model to make one decision (which contains many iterations)
		selectedmove, considered, considered2 = MakeMove(cur_node)
		print('Initial board:\n'+initial_node.board_to_str())
		print('move made:\n'+selectedmove.board_to_str())
		total_iteration = len(considered2)
		cur_iteration_num = 1 # initialize iteration count


		# plot each itertaion seperately
		if considered == []:
			# plot text
			plot_blank(instance, img_count, text='Random Move', color='green')
			if plot_tree_flag:
				plot_blank(instance, img_count, text='Random Move', color='green', imgtype='tree')
			img_count += 1
		for pos, pos2 in zip(considered, considered2): # if any iteration is considered
			# plot text
			plot_blank(instance, img_count, text='Iteration '+str(cur_iteration_num)+'/'+str(total_iteration), color='blue')
			if plot_tree_flag:
				plot_blank(instance, img_count, 
						text='Iteration '+str(cur_iteration_num)+'/'+str(total_iteration), 
						color='blue', imgtype='tree')
			cur_iteration_num += 1
			img_count += 1
			# plot board
			plot_state(cur_node, instance, img_count) # initial state
			if plot_tree_flag:
				dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
			img_count += 1
			# plot the node traversed along the selected branch in this iteration
			tree_cur = cur_node
			for pos_cur in pos: 
				plot_state(pos_cur, instance, img_count)
				if plot_tree_flag:
					for child in tree_cur.get_children():
						dot.node(str(id(child)), str(child.get_value()))
						dot.edge(str(id(tree_cur)), str(id(child)))
					dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
					tree_cur = pos_cur
				img_count += 1
			# plot the new node expanded along this branch in this iteration
			plot_state(pos2, instance, img_count)
			if plot_tree_flag:
				for child in tree_cur.get_children():
					dot.node(str(id(child)), str(child.get_value()))
					dot.edge(str(id(tree_cur)), str(id(child)))
				tree_cur = pos2
				for child in tree_cur.get_children():
					dot.node(str(id(child)), str(child.get_value()))
					dot.edge(str(id(tree_cur)), str(id(child)))
				dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
			img_count += 1
			

		# plot selected move 
		plot_blank(instance, img_count, text='Selected Move', color='green')
		if plot_tree_flag:
			plot_blank(instance, img_count, text='Selected Move', color='green', imgtype='tree')
		img_count += 1

		plot_state(cur_node, instance, img_count)
		if plot_tree_flag:
			dot.edge(str(id(initial_node)), str(id(cur_node)), color='red')
			dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
		img_count += 1

		plot_state(selectedmove, instance, img_count)
		if plot_tree_flag:
			dot.edge(str(id(cur_node)), str(id(selectedmove)), color='red')
			dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
		img_count += 1


		# plot actual move made by human 
		plot_blank(instance, img_count, text='Human Move', color='red')
		if plot_tree_flag:
			plot_blank(instance, img_count, text='Human Move', color='red', imgtype='tree')
		img_count += 1

		plot_state(cur_node, instance, img_count)
		if plot_tree_flag:
			dot.edge(str(id(initial_node)), str(id(cur_node)), color='red')
			cur_node2 = cur_node
			dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
		img_count += 1

		cur_carlist, _ = MAG.move(cur_carlist, piece, move_to)
		cur_board, _ = MAG.construct_board(cur_carlist)
		cur_node = Node(cur_carlist)
		plot_state(cur_node, instance, img_count)
		if plot_tree_flag:
			dot.edge(str(id(cur_node2)), str(id(cur_node)), color='red')
			dot.render('/Users/chloe/Desktop/RHfig/'+instance+'_'+str(img_count)+'_tree', 
						view=False)
		img_count += 1


		# make movie and save
		move_num += 1
		make_movie(move_num-1, format='avi')
		if plot_tree_flag:
			make_movie(move_num-1, format='avi', imgtype='tree')
		
		sys.exit()
		
		# clean all jpg files after movie done
		test = os.listdir(dir_name)
		for item in test:
		    if item.endswith(".jpg") or item.endswith('tree'):
		        os.remove(os.path.join(dir_name, item))
		






def heat_map(this_w0=0, this_w1=-1, this_w2=0, this_w3=0, this_w4=0, this_w5=0, this_w6=0, this_w7=0, this_mu=0, this_sigma=1):
	''' show the model's consideration of immediate next moves 
		by heatmap and arrows,
		based on subject's current position from a trial'''
	pass



def str_to_matrix(string):
	''' convert string of board to a int matrix '''
	matrix = np.zeros((6,6), dtype=int)
	line_idx = 0
	for line in string.split('\n'):
		char_idx = 0
		for char in line:
			if char == '>':
				continue
			elif char == '.':
				matrix[line_idx][char_idx] = -1
			elif char == 'R':
				matrix[line_idx][char_idx] = 0
			else:
				matrix[line_idx][char_idx] = int(char)+1
			char_idx += 1
		line_idx += 1
	return matrix



def plot_state(cur_node, instance, idx, out_file='/Users/chloe/Desktop/RHfig/', imgtype='board'):
	''' visualize the current node/board configuration '''
	matrix = str_to_matrix(cur_node.board_to_str())
	matrix = np.ma.masked_where(matrix==-1, matrix)
	cmap = plt.cm.Set1
	cmap.set_bad(color='white')
	fig, ax = plt.subplots()
	im = ax.imshow(matrix, cmap=cmap)
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			num = matrix[i, j]
			if num == 0:
				num = 'R'
			elif num > 0:
				num -= 1
			else:
				num = ''
			text = ax.text(j, i, num, ha="center", va="center", color="black", fontsize=14)
	plt.savefig(out_file+instance+'_'+str(idx)+'_'+imgtype+'.jpg')
	plt.close()



def plot_state_hold(cur_node, instance, idx, out_file='/Users/chloe/Desktop/RHfig/', imgtype='board'):
	''' visualize the current state '''
	matrix = str_to_matrix(cur_node.board_to_str())
	matrix = np.ma.masked_where(matrix==-1, matrix)
	cmap = plt.cm.Set1
	cmap.set_bad(color='white')
	fig, ax = plt.subplots()
	im = ax.imshow(matrix, cmap=cmap)
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			num = matrix[i, j]
			if num == 0:
				num = 'R'
			elif num > 0:
				num -= 1
			else:
				num = ''
			text = ax.text(j, i, num, ha="center", va="center", color="black", fontsize=14)
	plt.savefig(out_file+instance+'_'+str(idx)+'_'+imgtype+'.jpg')
	# plt.show()
	# plt.close()
	return fig, ax



def plot_blank(instance, idx, text, color, out_file='/Users/chloe/Desktop/RHfig/', imgtype='board'):
	''' plot a blank image
		with the entire page filled by one color and a text message '''
	fig, ax = plt.subplots()
	fig.patch.set_facecolor(color)
	fig.patch.set_alpha(0.1)
	ax.patch.set_facecolor(color)
	ax.patch.set_alpha(0.1)
	ax.text(0.3, 0.5, text, fontsize=20)
	ax.grid(False)
	ax.set_xticks([])
	ax.set_yticks([])
	plt.axis('off')
	fig.savefig(out_file+instance+'_'+str(idx)+'_'+imgtype+'.jpg', \
				facecolor=fig.get_facecolor(), edgecolor='none')
	plt.close()



import imageio
from pprint import pprint
import time
import datetime
import cv2
import datetime
def make_movie(move_num, path='/Users/chloe/Desktop/RHfig/', format='gif', imgtype='board'):
	''' make a movie using png files '''
	os.chdir(path)
	if format == 'gif':
		e=sys.exit
		duration = 0.5
		filenames = sorted(filter(os.path.isfile, [x for x in os.listdir(path) if x.endswith('_'+imgtype+'.jpg')]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple()))
		images = []
		for filename in filenames:
			images.append(imageio.imread(filename))
			output_file = 'MOVIE-'+imgtype+'-%s.gif' % (str(move_num)+'-'+datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S'))
		imageio.mimsave(output_file, images, duration=duration)
	elif format == 'avi':
		image_folder = path
		video_name = 'MOVIE-'+imgtype+'-%s.avi' % (str(move_num)+'-'+datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S'))
		images = sorted(filter(os.path.isfile, [x for x in os.listdir(path) if x.endswith('_'+imgtype+'.jpg')]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple()))
		frame = cv2.imread(os.path.join(image_folder, images[0]))
		height, width, layers = frame.shape
		video = cv2.VideoWriter(video_name, 0, 1, (width,height))
		for image in images:
		    video.write(cv2.imread(os.path.join(image_folder, image)))
		cv2.destroyAllWindows()
		video.release()




plot_trial()


# MakeMove()





