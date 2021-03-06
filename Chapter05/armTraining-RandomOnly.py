# -*- coding: utf-8 -*-
"""
Created on Sun May 20 21:26:58 2018

@author: Francis
"""
import numpy as np
from math import *
import matplotlib.pyplot as mp


#from keras.optimizers import Adam, SGD,Adadelta,Adagrad
#from keras.utils import to_categorical
#from keras.models import Sequential
#from keras.layers.core import Activation
#from keras.layers.core import Flatten
#from keras.layers.core import Dense
#from keras import backend as K


# functions and classes
# action matrix - all possible combinations of actions of the three motors
ACTIONMAT = np.array([[0,0,-1],[0,0,0],[0,0,1],
       [0,-1,-1],[0,-1,0],[0,-1,1],
       [0,1,-1],[0,1,0],[0,1,1],
       [-1,0,-1],[-1,0,0],[-1,0,1],
       [-1,-1,-1],[-1,-1,0],[-1,-1,1],
       [-1,1,-1],[-1,1,0],[-1,1,1],
       [1,0,-1],[1,0,0],[1,0,1],
       [1,-1,-1],[1,-1,0],[1,-1,1],
       [1,1,-1],[1,1,0],[1,1,1]])

class NeuralNet():
    def __init__(self):
        pass
    
    def build(self, inputs, outputs):
        pass

class RobotArm():
    def __init__(self):
        self.state = [0,0,0]
        
    def setState(self,st):
        self.state = st
        self.position = calHandPosition(st)
        
    def setGoal(self,newGoal):
        self.goal = newGoal
        
    def calcReward(self):
        dx = self.goal[0] - self.position[0]
        dy = self.goal[1] - self.position[1]
        dist2goal = sqrt(dx*dx + dy*dy)
        self.dist2goal = dist2goal
        # we want the reqard to be 100 if the goal is met
        # and porportional to the distance from goal otherwise
        # the arm is 340mm long, so that is as far away as we can get
        #
        reward = (340.0-dist2goal)/340.0 * 100.0
        self.reward = reward
        return reward
        

    def step(self,act,learningRate):
        newState = self.state + (act * learningRate)
        # range check
        for ii in range(3):
            newState[ii]=max(newState[ii],0)
            newState[ii]=min(newState[ii],255.0)
        
        self.setState(newState)
        reward = self.calcReward()
        
        return self.state,reward
# for a given action, return the new state 
        

class Actions():
    def __init__(self):
        pass
    
class Policy():
    def __init__(self):
        pass
    
class State():
    def __init__(self):
        pass
    
    
class genotype():
    def __init__(self):
        pass 

# just a utility to display the joint angle in degrees
def joint2deg(jointPos):
    return jointPos * (180.0 / 255.0)

def calHandPosition(stat):
    m1,m2,m3=stat
    # calculate hand position based on the position of the servo motors
    # m1, m2, m3 = motor command from 0 to 255
    # forward kinematics
    # we first convert each to an angle 
    d1 = 102.5  # length of first joint (sholder to elbow) in mm
    d2 = 97.26  # length of second joint arm (elbow to wrist) in mm
    d3 = 141    # length of thrird joint arm (wrist to hand)
    right = pi/2.0 # right angle, 90 degrees or pi/2 radians
    m1Theta = pi - m1*(pi/255.0)
    m2Theta = pi - m2*(pi/255.0)
    m3Theta = pi - m3*(pi/255.0)
    
    m2Theta = m1Theta-right+m2Theta
    m3Theta = m2Theta-right+m3Theta
    joint1 = np.array([d1*cos(m1Theta),d1*sin(m1Theta)])
    joint2 = np.array([d2*cos(m2Theta),d2*sin(m2Theta)])+joint1
    joint3 = np.array([d3*cos(m3Theta),d3*sin(m3Theta)])+joint2
    return joint3

# begin main program

# starting state
# our arm has states from 0 to 255 which map to degrees from 0 to 180
# here is our beginning state
state = [127,127,127]
oldState = state
learningRate = 2.0
robotArm = RobotArm()
robotArm.setState(state)
goal=[14,251]
robotArm.setGoal(goal)
knt = 0 # counter
reward=0.0  # no reward yet...
d2g=0.0
oldd2g = d2g
curve = []
# let's set the reward value for reaching the goal at 100
while reward < 98:

    index = np.random.randint(0,ACTIONMAT.shape[0])
    action = ACTIONMAT[index]
    state,reward = robotArm.step(action,learningRate)
    d2g = robotArm.dist2goal
    if d2g > oldd2g:
        # if the new reward is worse than the old reward, throw this state away
        #print("old state",oldState,state,d2g,oldd2g)
        state=oldState
        robotArm.setState(state)
        
    knt +=1
    oldd2g=d2g
    oldState=state
    curve.append(reward)
    if knt > 10000: reward = 101
    #print ("NewState ",state, "reward ",reward)
# see how long doing this randomly takes
print ("Count",knt,"NewState ",state, "reward ",max(curve))
mp.plot(curve)
mp.show()




        
        