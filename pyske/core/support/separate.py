from pyske.core.list.slist import SList

def distribute_tree(lt, n):
	sum3 = lambda x,y,z : x+y+z
	total_size = lt.map(lambda x : 1, lambda x : 1).reduce(sum3, lambda x : x, sum3, sum3, sum3)
	avg_elements = int(total_size / n)

	# Definition of global_index and distribution 

	global_index = SList([])
	distribution = SList([])

	for i in range(n):
		distribution.append(0)

	current_pid = 0
	nb_segs = 1
	seg = lt[0]
	seg_length = seg.length()
	acc_size = seg_length
	global_index.append((0, seg_length))

	for seg_i in range(1, lt.length()):
		seg = lt[seg_i]
		curr_seg_length = seg.length()
		if current_pid == n - 1:
			# We need to give all the rest to the last processor
			if seg_i == lt.length() - 1:
				distribution[current_pid] = (nb_segs + 1)
				global_index.append((acc_size, curr_seg_length))
			else :
				nb_segs += 1
				curr_seg_length = seg.length()
				global_index.append((acc_size, curr_seg_length))
				acc_size = acc_size + curr_seg_length
		else:
			if seg_i == lt.length() - 1:
				distribution[current_pid] = (nb_segs + 1)
				global_index.append((acc_size, seg.length()))
			else:
				curr_seg_length = seg.length()
				if abs(avg_elements - (acc_size + curr_seg_length)) > abs(avg_elements - acc_size) :
					distribution[current_pid] = nb_segs
					global_index.append((0, curr_seg_length))
					acc_size = curr_seg_length
					nb_segs = 1
					current_pid += 1
				else:
					nb_segs += 1
					global_index.append((acc_size, curr_seg_length))
					acc_size = acc_size + curr_seg_length

	return distribution, global_index






