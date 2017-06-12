a = [1, 5, 4, 2, 3]
print(a[0], a[-1])

# Prints: 1,3

a[4] = a[2] + a[-2]
print(a)

# Prints: [1,5,4,2,6]

print(len(a))

# Prints: 5

print(4 in a)

# Prints: True

a[1] = [a[1], a[0]]
print(a)

# Prints: [1.[5,1],4,2,3]



def remove_all(el, lst):

#Removes all instances of el from lst.
#Given: x = [3, 1, 2, 1, 5, 1, 1, 7]
#Usage: remove_all(1, x)
#Would result in: [3, 2, 5, 7]

	while True:
		try:
			if lst.index(el):
				lst.remove(el)
		except ValueError:
			return lst

			

def add_this_many(x, y, lst):

#Adds y to the end of lst the number of times x occurs in lst.
#Given: lst = [1, 2, 4, 2, 1]
#Usage: add_this_many(1, 5, lst)
#Results in: [1, 2, 4, 2, 1, 5, 5]

	count =0
	for i in range(len(lst)):
		if x == lst[i]:
			count=count+1
	for z in range(count):
		lst.append(y)
	return lst



#### 1.3 Slicing
#Like tuples, lists also support slicing notation, allowing you to retrieve multiple elements of a list at once. Slicing a list returns a new list. Slicing has the following syntax:
#lst[start:end:interval]
#where start, end, and interval are integers. The slice includes the element at start and every interval elements up to but not including the element at end. It is legal to omit one or more of start, end, and incr; they default to 0, `len(lst)`, and 1, respectively. Start and end can be negative, meaning you count from the end.



a = [0, 1, 2, 3, 4, 5, 6]
print(a[1:4])

# Prints: [1, 2, 3]

print(a[1:6:2])

# Prints: [1, 3, 5]

print(a[:4]) # equivalent to a[0:4]
# Prints: [0, 1, 2, 3]

print(a[3:]) # equivalent to a[3:len(a)]
# Prints: [3, 4, 5, 6]

print(a[1:4:]) # equivalent to a[1:4:1] or a[1:4] 
# Prints: [1, 2, 3]

print(a[-1:])
# Prints: [6]



#**`D:`**  What would Python print?



a = [3, 1, 4, 2, 5, 3]
print(a[:4])
# Prints: [3,1,4,2]

print(a)
# Prints: [3, 1, 4, 2, 5, 3]

print(a[1::2])
# Prints: [1,2,3]

print(a[:])
# Prints: [3, 1, 4, 2, 5, 3]

print(a[4:2])
# Prints: []

print(a[1:-2])
# Prints: [1,4,2]

print(a[::-1])
# Prints: [3, 5, 2, 4, 1, 3]



#### 1.4 For loops
#There are two main methods of looping through lists.
#- `for el in lst` → loops through the elements in lst
#- `for i in range(len(lst))` → loops through the valid, positive indices of lst
#If you do not need indices, looping over elements is usually more clear. Let's try this out.



#**`E:`**  Let's reverse Python lists in place, meaning mutate the passed in list itself, instead of returning a new list.
#We didn't discuss this in class directly, so feel free to use google. Why is the "in place" solution preferred?



def reverse(lst):
#Reverses lst in place. 
#Given: x = [3, 2, 4, 5, 1] 
#Usage: reverse(x)
#Results: [1, 5, 4, 2, 3]
	mid = int(len(lst)/2)
	h =0
	t=len(lst)-1
	for i in range(mid):
		temp = lst[h]
		lst[h] = lst[t]
		lst[t]=temp
		h=h+1
		t=t-1
	return lst



#**`F.`** Write a function that rotates the elements of a list to the right by `k`. Elements should not ”fall off”; they should wrap around the beginning of the list. `rotate` should return a new list. To make a list of `n` `0's`,you can do this: `[0] * n`



def rotate(lst, k):
#Return a new list, with the same elements of lst, rotated to the right k.
#Given: x = [1, 2, 3, 4, 5]
#Usage: rotate(x, 3)
#Results: [3, 4, 5, 1, 2]

	k=k%len(lst)
	revLst = []
	Len=len(lst)
	for i in range(Len):
		revLst.append(lst[((Len-k)+i)%Len])
	return revLst



## 2 Dictionaries
#Recall that dictionaries are data structures that map keys to values. Dictionaries are usually unordered (unlike real-world dictionaries) – in other words, the key-value pairs are not arranged in the dictionary in any particular order. Let's look at an example:

superbowls = {'joe montana': 4, 'tom brady':3, 'joe flacco': 0}
#print(superbowls['tom brady'])
# Prints: 3

superbowls['peyton manning'] = 1
#print(superbowls)
# Prints: {'peyton manning': 1, 'tom brady': 3, 'joe flacco': 0, 'joe montana': 4}

superbowls['joe flacco'] = 1
#print(superbowls)
# Prints:{'peyton manning': 1, 'tom brady': 3, 'joe flacco': 1, 'joe montana': 4}
#Dictionaries are indexed with similar syntax as sequences, only they use keys, which can be any immutable value, not just numbers. Dictionaries themselves are mutable; we can add, remove, and change entries after creation. There is only one value per key, however, in a dictionary (we call this _injective_ or one-to-one).



#**`H:`**  Continuing from above, what would Python print?

print('colin kaepernick' in superbowls)
#Prints: False

print(len(superbowls))
#Prints: 4

print(superbowls['peyton manning'] == superbowls['joe montana'])
#Prints: False

superbowls[('eli manning', 'giants')] = 2
print(superbowls)
#Prints: Prints:{'peyton manning': 1, 'tom brady': 3, 'joe flacco': 1, 'joe montana': 4, ('eli manning', 'giants') : 2}

#superbowls[3] = 'cat'
#print(superbowls)
#Prints: Error


superbowls[('eli manning', 'giants')] =  superbowls['joe montana'] + superbowls['peyton manning']
print(superbowls)
#Prints: Prints:{'peyton manning': 1, 'tom brady': 3, 'joe flacco': 1, 'joe montana': 4, ('eli manning', 'giants') : 5

#superbowls[['steelers', '49ers']] = 11
#print(superbowls)
#Prints: Error



#Dictionaries in general can be arbitrarily deep, meaning their values can be dictionaries themselves. Let's get practice traversing these deep structures. To do so, we'll need to know a couple more things about dictionaries.
#To iterate over a dictionary's keys:
#`for k in d.keys(): ...`
#and to remove an entry:
#`del dictionary[key]`



#**`I:`**  Given a dictionary replace all occurrences of x as the value with y.




def replace_all(d, x, y):
#Replaces all values of x with y. 
#Given: d = {1: {2:3, 3:4}, 2:{4:4, 5:3}} 
#Usage: replace_all(d,3,1)
#Results: {1: {2: 1, 3: 4}, 2: {4: 4, 5: 1}} 
	for subd in d:
		for k,v in d[subd].items():
			if v == x:
				d[subd][k]=y
	return d




#**`J:`**  Given a (non-nested) dictionary delete all occurences of a value. You cannot delete items in a dictionary as you are iterating through it (google :) ).



def rm(d, x):
#Removes all pairs with value x. 
#Given:  d = {1:2, 2:3, 3:2, 4:3}
#Usage:  rm(d,2)
#Results: {2:3, 4:3}
	toDel=[]
	for k,v in d.items():
		if v == x:
			toDel.append(k)
	for i in toDel:
		del d[i]
	return d

print(remove_all(1,[3, 1, 2, 1, 5, 1, 1, 7]))
print(add_this_many(1,5,[1,2,4,2,1]))
print(reverse([3, 2, 4, 5, 1]))
print(rotate([1,2,3,4,5],3))
print(replace_all({1: {2:3, 3:4}, 2:{4:4, 5:3}},3,1))
print(rm({1:2, 2:3, 3:2, 4:3},2))