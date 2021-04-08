import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random
from pprint import pprint

MAX_EPISODE_LEN = 5000
JOINTS=[0,1,4,5]
MAX_TORQUE=100
FORCE_ACTION={
#    0: 0,
#    1: 0,
#    2: 0,
#    3: 0,
}

def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([
      -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0, x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
      -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0, x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0
    ], dtype=np.float64)

class NFEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,show_gui=False,fall_rew=-10,motion_rew=0,const_rew=2,height_rew=0,rand_force=None,mp4_path=None,foot_friction_lat=1,foot_friction_spin=1,pitch_rew=-1,roll_rew=-1,distance_rew=0,max_distance=0,power_rew=-0.2,min_height=0.5,max_pitch=0,max_roll=0,target_height=1.7,rand_force_freq=1000,speed_x_rew=-0.5,speed_y_rew=-0.5,speed_z_rew=0,speed_pitch_rew=0,speed_roll_rew=0,speed_yaw_rew=0,max_steps=5000,debug=False,base_mass=4):
        self.step_counter = 0
        if show_gui:
            mode=p.GUI
        else:
            mode=p.DIRECT
        options=""
        if mp4_path:
            options+="--width=1024 --height=768 --mp4=\""+mp4_path+"\" --mp4fps=240"
        p.connect(mode, options=options)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.observation_space = spaces.Box(np.array([-1]*21), np.array([1]*21))
        self.action_space = spaces.Box(np.array([-1]*4), np.array([1]*4))
        self.prev_pos=None
        self.fall_rew=fall_rew
        self.motion_rew=motion_rew
        self.const_rew=const_rew
        self.height_rew=height_rew
        self.pitch_rew=pitch_rew
        self.roll_rew=roll_rew
        self.distance_rew=distance_rew
        self.power_rew=power_rew
        self.max_distance=max_distance
        self.rand_force=rand_force
        self.foot_friction_lat=foot_friction_lat
        self.foot_friction_spin=foot_friction_spin
        self.min_height=min_height
        self.max_pitch=max_pitch
        self.max_roll=max_roll
        self.target_height=target_height
        self.rand_force_freq=rand_force_freq
        self.speed_x_rew=speed_x_rew
        self.speed_y_rew=speed_y_rew
        self.speed_z_rew=speed_z_rew
        self.speed_pitch_rew=speed_pitch_rew
        self.speed_roll_rew=speed_roll_rew
        self.speed_yaw_rew=speed_yaw_rew
        self.max_steps=max_steps
        self.debug=debug
        self.base_mass=base_mass

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        p.setGravity(0,0,-10)
        self.plane_id = p.loadURDF("plane.urdf")
        #self.wall1_id = p.loadURDF("plane.urdf",[-0.7,0,0],p.getQuaternionFromEuler([0,math.pi/2,0]))
        #self.wall2_id = p.loadURDF("plane.urdf",[0.7,0,0],p.getQuaternionFromEuler([0,-math.pi/2,0]))
        cubeStartPos = [0,0,1.8]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
        #cubeStartOrientation = p.getQuaternionFromEuler([0,0,math.pi/2])
        try:
            self.bot_id = p.loadURDF("/Users/dj/stuff/bot/urdf/bot12.urdf", cubeStartPos, cubeStartOrientation)
        except:
            self.bot_id = p.loadURDF("/content/drive/My Drive/bot/bot12.urdf", cubeStartPos, cubeStartOrientation)

        maxForce = 0
        mode = p.VELOCITY_CONTROL
        for i in range(8):
            p.setJointMotorControl2(self.bot_id, i, controlMode=mode, force=maxForce)

        c = p.createConstraint(self.bot_id, 1, self.bot_id, 2, jointType=p.JOINT_GEAR,jointAxis=[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 5, self.bot_id, 6, jointType=p.JOINT_GEAR,jointAxis=[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        for i in [3,7]:
            p.changeDynamics(self.bot_id, i, lateralFriction=self.foot_friction_lat, spinningFriction=self.foot_friction_spin)

        p.changeDynamics(self.bot_id, -1, mass=self.base_mass)
        if self.debug:
            res=p.getDynamicsInfo(self.bot_id, -1)
            print("base dynamics:",res)
            for i in range(8):
                res=p.getDynamicsInfo(self.bot_id, i)
                print("link #%s dynamics:"%i,res)

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        rot=p.getEulerFromQuaternion(res[1])
        pitch=rot[0]
        roll=rot[1]
        yaw=rot[2]
        rot_around_z = np.array([[np.cos(-yaw),-np.sin(-yaw), 0], [np.sin(-yaw), np.cos(-yaw), 0], [0, 0, 1]])

        obs=[]
        joint_states=[p.getJointState(self.bot_id, JOINTS[i]) for i in range(4)]
        for s in joint_states:
            obs.append(s[0]/math.pi) # pos
        for s in joint_states:
            obs.append(s[1]/math.pi) # vel
        for s in joint_states:
            obs.append(s[3]/MAX_TORQUE) # torque

        res=p.getBaseVelocity(self.bot_id)
        lin_vel=np.dot(rot_around_z,res[0]).tolist()
        ang_vel=np.dot(rot_around_z,res[1]).tolist()

        obs+=[rot[0]/math.pi,rot[1]/math.pi,rot[2]/math.pi] # orient (3)
        obs+=lin_vel # lin vel (3)
        obs+=[ang_vel[0]/math.pi,ang_vel[1]/math.pi,ang_vel[2]/math.pi] # ang vel (3)
        self.observation = obs 

        return np.array(self.observation).astype(np.float32)

    def step(self, action):
        mode = p.POSITION_CONTROL
        for i in range(4):
            a=action[i]
            if i in FORCE_ACTION:
                a=FORCE_ACTION[i]
            pos=a*math.pi
            joint_no=JOINTS[i]
            p.setJointMotorControl2(self.bot_id, joint_no, controlMode=mode, targetPosition=pos, force=MAX_TORQUE)

        p.stepSimulation()

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        #print("pos",pos)
        rot=p.getEulerFromQuaternion(res[1])
        #print("rot",rot)

        pitch=rot[0]
        roll=rot[1]
        yaw=rot[2]

        rot_around_z = np.array([[np.cos(-yaw),-np.sin(-yaw), 0], [np.sin(-yaw), np.cos(-yaw), 0], [0, 0, 1]])

        obs=[]
        joint_states=[p.getJointState(self.bot_id, JOINTS[i]) for i in range(4)]
        power=0
        for s in joint_states:
            obs.append(s[0]/math.pi) # pos
        for s in joint_states:
            obs.append(s[1]/math.pi) # vel
        for s in joint_states:
            v=s[3]/MAX_TORQUE
            obs.append(v) # torque
            power+=v**2
        power/=4.0
        res=p.getBaseVelocity(self.bot_id)
        lin_vel=np.dot(rot_around_z,res[0]).tolist()
        ang_vel=np.dot(rot_around_z,res[1]).tolist()

        obs+=[rot[0]/math.pi,rot[1]/math.pi,rot[2]/math.pi] # orient (3)
        obs+=lin_vel # lin vel (3)
        obs+=[ang_vel[0]/math.pi,ang_vel[1]/math.pi,ang_vel[2]/math.pi] # ang vel (3)
        self.observation = obs 

        height=pos[2]
        if self.debug:
            print("height=%s pitch=%s roll=%s speed_x=%s speed_y=%s speed_pitch=%s speed_roll=%s power=%s"%(height,rot[0],rot[1],lin_vel[0],lin_vel[1],ang_vel[0],ang_vel[1],power))

        done = False
        r_const=self.const_rew
        reward=r_const

        #print("height=%s"%height)
        r_height=abs(self.target_height-height)*self.height_rew
        reward+=r_height

        r_pitch=abs(rot[0])*self.pitch_rew
        reward+=r_pitch
        r_roll=abs(rot[1])*self.roll_rew
        reward+=r_roll

        r_speed_x=abs(lin_vel[0])*self.speed_x_rew
        reward+=r_speed_x
        r_speed_y=abs(lin_vel[1])*self.speed_y_rew
        reward+=r_speed_y
        r_speed_z=abs(lin_vel[2])*self.speed_z_rew
        reward+=r_speed_z

        r_speed_pitch=abs(ang_vel[0])*self.speed_pitch_rew
        reward+=r_speed_pitch
        r_speed_roll=abs(ang_vel[1])*self.speed_roll_rew
        reward+=r_speed_roll
        r_speed_yaw=abs(ang_vel[2])*self.speed_yaw_rew
        reward+=r_speed_yaw
        
        #print("power",power)
        r_power=power*self.power_rew
        reward+=r_power

        if self.debug:
            s="rewards: r_tot=%s"%reward
            if r_const:
                s+=" r_const=%s"%r_const
            if r_height:
                s+=" r_height=%s"%r_height
            if r_pitch:
                s+=" r_pitch=%s"%r_pitch
            if r_roll:
                s+=" r_roll=%s"%r_roll
            if r_speed_x:
                s+=" r_speed_x=%s"%r_speed_x
            if r_speed_y:
                s+=" r_speed_y=%s"%r_speed_y
            if r_speed_z:
                s+=" r_speed_z=%s"%r_speed_z
            if r_speed_pitch:
                s+=" r_speed_pitch=%s"%r_speed_pitch
            if r_speed_roll:
                s+=" r_speed_roll=%s"%r_speed_roll
            if r_speed_yaw:
                s+=" r_speed_yaw=%s"%r_speed_yaw
            if r_power:
                s+=" r_power=%s"%r_power
            print(s)

        #if pos[2]>2:
        #    reward=self.fall_rew
        #    done=True

        if self.min_height and height<self.min_height:
            reward=self.fall_rew
            done=True
        
        if self.max_pitch and abs(rot[0])>=self.max_pitch:
            reward=self.fall_rew
            done=True

        if self.max_roll and abs(rot[1])>=self.max_roll:
            reward=self.fall_rew
            done=True

        if self.max_distance and dist>self.max_distance:
            reward=self.fall_rew
            done=True

        if not done and self.step_counter > self.max_steps:
            reward = 0
            done = True

        info = {}

        self.prev_pos=pos

        if self.rand_force and self.step_counter%self.rand_force_freq==0:
            #print("apply rand force")
            r=random.uniform(-1,1)
            f=np.array(self.rand_force)*r
            p.applyExternalForce(self.bot_id,-1,f,[0,0,0],p.WORLD_FRAME)

        self.step_counter += 1
        return np.array(self.observation).astype(np.float32), reward, done, info

    def render(self):
        pass

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()
