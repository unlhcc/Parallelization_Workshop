#######################################################################
#
#   Exercise:  Scatter/Gather
#
#   Scatter list a to all even processors, assigning its values to the variable mylist
#   Scatter list b to all odd processors, assigning its values to mylist
#   Gather from all processors to create the list [0,1,0,1,2,3,4,9,....]
#
import ipyparallel

#identify the our python engines
rc  =ipyparallel.Client(profile='crestone-cpu')
nengines = len(rc)

#create views into each engine
all_proc  = rc[:]
all_proc.block=True

even_proc = rc[range(0,nengines,2)]
odd_proc  = rc[range(1,nengines,2)]


a = []
b = []
lsize=nengines
for i in range(0,lsize):
	a.append(i)
	b.append(i**2)

all_proc.scatter('mylist',a)
sub_lists = all_proc['mylist']

#Only the hub prints this
print('\n ',nengines," Python engines are active.\n")


print(' ')
for i in range(nengines):
    istr = '{:02d}'.format(i)  # returns a 2-digit string whose value is i
    msg = 'Engine '+istr+':   list segment = '
    print(msg, sub_lists[i])
print(' ')
gathered = all_proc.gather('mylist')
print('Gathered list: ', gathered[:], type(gathered))
