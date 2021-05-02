from AVLtree import *
tree=AVLtree()
arr=[1,2,3,4,5,6,7,8,9]
for i in arr:
  tree.insert(i)
 tree.delete(2)
print('after deletion -->')
tree.visualize()
