#Tests the viability of the quality vectors as a recommendation engine

import random
import numpy as np

epochs=1000
entropy=32

tags=["anime","letsplay","funny","prank","review","edu","reaction"]

print "Max distance:",len(tags)*(entropy/2)**2

#Used for both users and videos for laziness
class User:
	def __init__(self):
		self.likes={
			tags[i]:np.random.normal(0,0.2) for i in random.sample(
				xrange(len(tags)),
				np.random.randint(2,len(tags)-1)
			)
		}
		self.prefs=np.random.randint(0,256,len(tags))

def dist(a,b):
	d=np.abs(a-b)
	#Adjust the raw distance so it's modular
	d=((d>entropy/2)+1)*entropy/2-d
	#Dot product compresses the dimensionality
	return np.dot(d,d)

def calc_vote(user,vid):
	vote=0.0
	for like,by in user.likes.iteritems():
		if like in vid.likes:
			vote+=by
	vote/=len(user.likes)
	
	return vote

def format_likes(x):
	for key,val in x.iteritems():
		print key+(":%d"%val),

users=[User() for j in xrange(100)]
videos=[User() for j in xrange(2000)]

def test_accuracy():
	merr=0
	mean=0
	
	for user in users:
		sugg=np.repeat(np.inf,11)
		sv=np.repeat(None,11)
		
		for vid in videos:
			err=abs(2*dist(user.prefs,vid.prefs)/float(entropy*len(tags))-calc_vote(user,vid))
			
			if err>merr:
				merr=err
			
			mean+=err
	
	return merr,mean/(len(users)*len(videos))

print "Initial error:",test_accuracy()

for epoch in xrange(epochs):
	for user in random.sample(users,10):
		for vid in random.sample(videos,20):
			#Vote is gaussian oriented around the sum of the weighted average
			# of the user's likes
			vote=np.random.normal(calc_vote(user,vid),0.1)
			
			vp=vid.prefs
			up=user.prefs
			
			d=(np.abs(vp-up)>entropy/2)*2-1
			order=(vp>up)-(up>vp)
			
			vid.prefs=(vp+order*d)%entropy
			user.prefs=(up-order*d)%entropy

print "Error after {} epochs:".format(epochs),test_accuracy()
