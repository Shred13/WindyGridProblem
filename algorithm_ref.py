from random import randint
from random import random
from math import sqrt
from math import log
import numpy as np

def genEnvironment(S,A,Wind,R,C,SR,SC,DR,DC,Stochastic):
	sPrime = 1
	if(Stochastic): sPrime = 3
	T = [[[-1 for _ in range(sPrime)]for _ in range(A)]for i in range(S)]
	Reward = [-1 for _ in range(S)]
	Reward[DR*DC] = 0

	for i in range(R):
		for j in range(C):
			for k in range(A):
				if k == 0: #Up
					T[i*C+j][k][0] =  (i-1)*C+j if i-1 >= 0 else i*C+j
				if k == 1: #Right
					T[i*C+j][k][0] =  i*C+j+1 if j+1 < C else i*C+j
				if k == 2: #Down
					T[i*C+j][k][0] =  (i+1)*C+j if (i+1) < R else i*C+j
				if k == 3: #Left
					T[i*C+j][k][0] =  i*C+j-1 if j-1 >= 0 else i*C+j
				if k == 4: #UpRight
					T[i*C+j][k][0] =  (i-1)*C+j+1 if i-1 >= 0 and j+1 < C else i*C+j
				if k == 5: #RightDown
					T[i*C+j][k][0] =  (i+1)*C+j+1 if (i+1) < R and j+1 < C else i*C+j
				if k == 6: #DownLeft
					T[i*C+j][k][0] =  (i+1)*C+j-1 if (i+1) < R and j-1 >= 0 else i*C+j
				if k == 7: #LeftUp
					T[i*C+j][k][0] =  (i-1)*C+j-1 if i-1 >= 0 and j-1 >= 0 else i*C+j

				T[i*C+j][k][0] = T[i*C+j][k][0]-Wind[j]*C if T[i*C+j][k][0]-Wind[j]*C >= 0 else T[i*C+j][k][0]

				if(Stochastic):
					if(Wind[j]!=0):
						T[i*C+j][k][1] = T[i*C+j][k][0]+C*Wind[j]
						T[i*C+j][k][2] = T[i*C+j][k][0]-C*Wind[j] if T[i*C+j][k][0]-C*Wind[j] >= 0 else T[i*C+j][k][0]
					else:
						T[i*C+j][k][1] = T[i*C+j][k][0]
						T[i*C+j][k][2] = T[i*C+j][k][1]

	return T,Reward

def UCB(Q,qParam,t,A):
	ucb = [(Q[i] + sqrt(2*log(sum(qParam))/qParam[i])) for i in range(A)]
	index = ucb.index(max(ucb))
	qParam[index]+=1
	return index,qParam

def eGreedy(Q,epsilon,t,A): return Q.index(max(Q)) if random()>epsilon*(1/t) else randint(0,A-1)

def SARSA(T,R,Source,Destination,A,S,alpha,gamma,epsilon,Stochastics,Policy,Episodes):
	sPrime = 3 if Stochastics else 1
	qParams = [[1 for _ in range(A)] for _ in range(S)]
	Q = [[0 for _ in range(A)] for _ in range(S)]
	J,K = 0,1
	print("Episodes","Time-Steps","Steps-In-One-Episode")
	print(J,K-1,0)
	for _ in range(Episodes):
		I = 0
		s = Source
		if Policy == 0 : a = eGreedy(Q[s],epsilon,K,A)
		else : a,qParams[s] = UCB(Q[s],qParams[s],K,A)
		while(s!=Destination):
			s1 = T[s][a][randint(0,sPrime-1)]
			r = R[s1]
			if Policy == 0 : a1 = eGreedy(Q[s1],epsilon,K,A)
			else : a1,qParams[s1] = UCB(Q[s1],qParams[s1],K,A)
			Q[s][a] = Q[s][a] + alpha*(r + gamma*Q[s1][a1] - Q[s][a])
			s,a = s1,a1
			J+=1
			I+=1
		K+=1
		print(J,K-1,I)

	return Q

def SARSAlambda(T,R,Source,Destination,A,S,alpha,gamma,epsilon,Stochastics,Policy,lamb,Episodes):
	sPrime = 3 if Stochastics else 1
	qParams = [[1 for _ in range(A)] for _ in range(S)]
	Q = [[0 for _ in range(A)] for _ in range(S)]
	E = [[0 for _ in range(A)] for _ in range(S)]
	J,K = 0,1
	print("Episodes","Time-Steps","Steps-In-One-Episode")
	print(J,K-1,0)
	for _ in range(Episodes):
		I = 0
		s = Source
		if Policy == 0 : a = eGreedy(Q[s],epsilon,K,A)
		else : a,qParams[s] = UCB(Q[s],qParams[s],K,A)
		while(s!=Destination):
			s1 = T[s][a][randint(0,sPrime-1)]
			r = R[s1]
			if Policy == 0 : a1 = eGreedy(Q[s1],epsilon,K,A)
			else : a1,qParams[s1] = UCB(Q[s1],qParams[s1],K,A)
			delta = r + gamma*Q[s1][a1] - Q[s][a]
			E[s][a]+=1
			Q = [[Q[s][a] + alpha*delta*E[s][a] for a in range(A)] for s in range(S)]
			E = [[gamma*lamb*E[s][a] for a in range(A)] for s in range(S)]
			s,a = s1,a1
			J+=1
			I+=1
		K+=1
		print(J,K-1,I)

	return Q



R,C = list(map(int,input().split())) #Grid Dimention
SR,SC,DR,DC = list(map(int,input().split())) #Source and Destination
Wind = list(map(int,input().split())) #Wind
A = int(input()) #Type of moves
Stochastic = True if int(input()) != 0 else False #Stochastic nature of Wind
alpha = float(input())
gamma = float(input())
epsilon = float(input())
Policy = int(input())
lamb = float(input())
Episodes = int(input())
file = int(input())

S = R*C
Source = SR*C+SC
Destination = DR*C+DC

T,Reward = genEnvironment(S,A,Wind,R,C,SR,SC,DR,DC,Stochastic)

if(lamb!=0): Q = SARSAlambda(T,Reward,Source,Destination,A,S,alpha,gamma,epsilon,Stochastic,Policy,lamb,Episodes)
else : Q = SARSA(T,Reward,Source,Destination,A,S,alpha,gamma,epsilon,Stochastic,Policy,Episodes)

def graph(R,C,Q,f):
	mat = open("".join(["Output/M",str(f),".mat"]),"w")
	np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
	for i in range(R):
		mat.write("\t".join(list(map(lambda x:str(x).zfill(5),map(lambda x:round(x,2),[max(j) for j in Q[i*C:i*C+C]])))))
		mat.write("\n")
graph(R,C,Q,file)