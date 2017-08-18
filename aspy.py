
'''上下文管理器的原理
'''
class PyContextManager:
	def __enter__(self):
		self.openFile = open(self.filename,self.mode)
		print("enter")
		return self.openFile
	def __exit__(self,*unused):
		print("exit")
		self.openFile.close()

	def __init__(self,filename,mode):
		self.filename = filename
		self.mode = mode


with PyContextManager("1.txt",'w') as f:
	f.write("1")
	print("do something")