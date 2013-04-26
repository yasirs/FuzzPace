import os
import subprocess as sub
import copy

class Fasta:
	"""Stores one fasta record """
	def __init__(self,l1,l2):
		if l1[0]!='>':
			raise IOError('Line %s does not begin with >' %l1)
		if l2[0]=='>':
			raise IOError('Line %s should be sequence, has >' %l2)
		self.name=l1
		self.seq=l2
	def __str__(self):
		return self.name + self.seq


class FastaFile:
	"""A fasta file"""
	def __init__(self,fname):
		self.name = fname
		self.recs = []
		f = open(fname,'r')
		nameline = True
		for line in f:
			if nameline:
				l1 = line
			else:
				l2 = line
			if (not nameline):
				rec = Fasta(l1,l2)
				del l1, l2
				self.recs.append(rec)
			nameline = not nameline
		if (not nameline):
			if l1.rstrip()!='':
				raise IOError('Dangling line %s in file %s' %(l1,fname))
		f.close()
	def write(self,ofilename):
		f = open(ofilename,'w')
		for rec in self.recs:
			f.write(str(rec))
		f.close()
	def __str__():
		return "FastaFile of %i records, read from %s" %(len(self.rec),self.name)

data = FastaFile('data/data.pace')
working = copy.deepcopy(data)

done = False
i=0
while not done:
	del working.recs[i]
	working.write('input.pace')
	p = sub.Popen(['mpirun','-np','4','PaCE','input.pace',str(len(working.recs))],stdout=sub.PIPE,stderr=sub.PIPE)
	p.wait
	a,b=p.communicate()
	if b:
		# there was an error. Hence, the working copy is now smaller error example
		os.system('cp input.pace best/')
		if ((len(working.recs) % 10) ==0):
			# write every 10th one, just to be sure
			os.system('cp input.pace best/n%i.pace' %len(working.recs))
		print "Error with %i inputs!" %(len(working.recs))
	else:
		# no error
		os.system('rm Cont* estClust* NonC*')
		working = FastaFile('best/input.pace')
		if i<len(working.recs)-1:
			i=i+1
			print "No error with %ith deletion, trying next one" %i
		else:
			done=True
			print "Tried all deletions!"
	#that's it, go back and remove i from the working set
	
