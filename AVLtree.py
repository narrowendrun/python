import queue
class AVLNode:
	def __init__(self,data):
		self.data=data
		self.right=None
		self.left=None
		self.parent=None
		self.height=1
class AVLtree:
	def __init__(self):
		self.root=None
	def visualize(self):
		levels=self.printTree('levelorder')
		h=self.root.height
		n1=len(levels[-1])
		n2=len(levels[-1])
		for level in levels:
			for node in level:
				k=int(n2/len(level))
				print(end=' '*(k-1))#beginning
				print(node,end=' '*k)#end
				n1=int(n1/2)
			print('\r')
			print('/'*n2*2,'(h->',h,')')
			h-=1
	def height(self,curnode):
		if curnode:
			return curnode.height
		else:
			return 0
	def LeftRotate(self,z):
		root=z.parent
		y=z.right
		t3=y.left
		y.left=z
		y.parent=root
		z.parent=y
		z.right=t3
		if t3:
			t3.parent=z
		if not y.parent:
			self.root=y
		else:
			if y.parent.left==z:
				y.parent.left=y
			else:
				y.parent.right=y
		z.height=max(self.height(z.left),self.height(z.right))+1
		y.height=max(self.height(y.left),self.height(y.right))+1
	def RightRotate(self,z):
		root=z.parent
		y=z.left
		t3=y.right
		y.right=z
		y.parent=root
		z.parent=y
		z.left=t3
		if t3:
			t3.parent=z
		if not y.parent:
			self.root=y
		else:
			if y.parent.left==z:
				y.parent.left=y
			else:
				y.parent.right=y
		z.height=max(self.height(z.left),self.height(z.right))+1
		y.height=max(self.height(y.left),self.height(y.right))+1			
	def insert(self,data):
		if self.root is None:
			self.root=AVLNode(data)
		else: 
			self._insert(data,self.root)
	def _insert(self,data,curnode):
		if data<curnode.data:
			if curnode.left is None:
				curnode.left=AVLNode(data)
				curnode.left.parent=curnode
				self._inspectInsert(curnode.left)
			else:
				self._insert(data,curnode.left)
		elif curnode.data<data:
			if curnode.right is None:
				curnode.right=AVLNode(data)
				curnode.right.parent=curnode
				self._inspectInsert(curnode.right)
			else:
				self._insert(data,curnode.right)
		else:
			print('duplicate instance of '+str(data)+' found')
		curnode.height=max(self.height(curnode.left),self.height(curnode.right))+1
		#print('tree after inserting ', data)
		#print(self.__repr__())
	def _inspectInsert(self,curnode,path=[]):
		if not curnode.parent:
			return
		path=[curnode]+path
		#for i in range(len(path)):
		#	print(path[i].data, end=' ')
		#print()
		lheight=self.height(curnode.parent.left)
		rheight=self.height(curnode.parent.right)
		if abs(lheight-rheight)>1:
			path=[curnode.parent]+path
			self._balanceAVL(path[0],path[1],path[2])
			return
		newheight=1+curnode.height
		if newheight>curnode.parent.height:
			curnode.parent.height=newheight
		self._inspectInsert(curnode.parent,path)
	def delete(self,data):
		return self._delete(self.find(data))
	def _delete(self,curnode):
		def smallestnode(curnode):
			while(curnode.left):
				curnode=curnode.left
			return curnode
		def childrenNo(curnode):
			count=0
			if curnode.left:
				count+=1
			if curnode.right:
				count+=1
			return count
		if not curnode:
			print('value not present in tree')
			return
		else:
			childcount=childrenNo(curnode)
			parent=curnode.parent
			if childcount==0:
				if not parent:
					self.root=None
				else:
					if curnode==parent.left:
						parent.left=None
					else:
						parent.right=None
					curnode.parent=None
			if childcount==1:
				if curnode.left:
					curnode.data=curnode.left.data
					curnode.left=None
				else:
					curnode.data=curnode.right.data
					curnode.right=None
			if childcount==2:
				nextval=smallestnode(curnode.right)
				curnode.data=nextval.data
				self._delete(nextval)
				return
			if parent:
				parent.height=max(self.height(parent.left),self.height(parent.right))
				self._inspectDelete(parent)
	def _inspectDelete(self,curnode):
		if not curnode:
			return
		lheight=self.height(curnode.left)
		rheight=self.height(curnode.right)
		if abs(lheight-rheight)>1:
			y=self._tallest(curnode)
			x=self._tallest(y)
			self._balanceAVL(curnode,y,x)
		self._inspectDelete(curnode.parent)
	def _tallest(self,curnode):
		l=self.height(curnode.left)
		r=self.height(curnode.right)
		if l>=r:
			return curnode.left
		else:
			return curnode.right
	def _balanceAVL(self,z,y,x):
		#left left
		if y==z.left and x==y.left:
			self.RightRotate(z)
		# left right
		elif y==z.left and x==y.right:
			self.LeftRotate(y)
			self.RightRotate(z)
		#right right
		elif y==z.right and x==y.right:
			self.LeftRotate(z)
		#right left
		elif y==z.right and x==y.left:
			self.RightRotate(y)
			self.LeftRotate(z)		
	def find(self,data):
		if self.root:
			return self._find(self.root,data)
		else:
			return None
	def _find(self,root,data):
		if data==root.data:
			return root
		elif root.data>data and root.left:
			return self._find(root.left,data)
		elif root.data<data and root.right:
			return self._find(root.right,data)
		else:
			return None
	def printTree(self,print_type):
		if print_type=='preorder':
			return self.preorder_traverse(self.root)
		elif print_type=='inorder':
			return self.inorder_traverse(self.root)
		elif print_type=='postorder':
			return self.postorder_traverse(self.root)
		elif print_type=='levelorder':
			return self.levelorder_traverse(self.root)
	def preorder_traverse(self,start,cache=[]):
		if start:
			cache.append(start.data)
			self.preorder_traverse(start.left,cache)
			self.preorder_traverse(start.right,cache)
		return cache
	def inorder_traverse(self,start,cache=[]):
		if start:
			self.inorder_traverse(start.left,cache)
			cache.append(start.data)
			self.inorder_traverse(start.right,cache)
		return cache
	def postorder_traverse(self,start,cache=[]):
		if start:
			self.postorder_traverse(start.left,cache)
			self.postorder_traverse(start.right,cache)
			cache.append(start.data)
		return cache
	def levelorder_traverse(self,start):
		if start is None:
			return
		que=queue.Queue()
		que.put(start)
		level=AVLNode('level')
		null=AVLNode(' ')
		que.put(level)
		cache=[]
		result=[]
		while(que.qsize()>0):
			node=que.get()
			if node==level:
				que.put(level)
				result.append(cache)
				cache=[]
				node=que.get()
			cache.append(node.data)
			if node!=null:
				if node.left:
					que.put(node.left)
				else:
					que.put(null)
				if node.right:
					que.put(node.right)
				else:
					que.put(null)
		return result[:-1]