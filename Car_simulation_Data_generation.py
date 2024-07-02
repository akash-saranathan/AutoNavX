import pybullet as p
import pybullet_data
import cv2
import numpy as np
import os
import math
import datetime
import time
import random


count = 0

def generate_random_obstacle_positions(num_obstacles, min_distance, max_distance, radius):
    positions = []
    for _ in range(num_obstacles):
        distance = random.uniform(min_distance, max_distance)
        angle = random.uniform(-math.pi / 4, math.pi / 4)  # Spread obstacles within a 90-degree arc in front of the car
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        positions.append([x, y, 0.5])
    return positions

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# p.loadURDF("plane.urdf")
plane_path = os.path.abspath('simple_plane.urdf')
print(f"Loading URDF file from: {plane_path}")
p.loadURDF(plane_path)

p.setGravity(0, 0, -10)

carpos = [0, 0, 0.1]
car = p.loadURDF("husky/husky.urdf", carpos[0], carpos[1], carpos[2])

numJoints = p.getNumJoints(car)
for joint in range(numJoints):
    print(p.getJointInfo(car, joint))

targetVel = 1  # rad/s
maxForce = 100  # Newton
p.setRealTimeSimulation(1)




num_obstacles = 50

# Generate obstacle positions
obstacle_positions = []
for i in range(num_obstacles):
    x = random.randint(1, 60)  # Random x position between 1 and 100
    y = random.randint(-10, 10)  # Random y position between -50 and 50 to spread them along the y-axis
    obstacle_positions.append((x, y,0.5))
for pos in obstacle_positions:
    p.loadURDF("cube.urdf", pos, [0, 0, 1.73, 0.7], useFixedBase=False, globalScaling=0.5)



frame_counter = 0
capture_interval = 120
running = True
captured_images = []
data_log = []
filepaths = []

while running:
    
    keys = p.getKeyboardEvents()
    key_states = [0, 0, 0, 0]

    moving_forward = False
    moving_backward = False
    steering_left = False
    steering_right = False

    pos, orn = p.getBasePositionAndOrientation(car)
    pos = list(pos)
    orn = p.getEulerFromQuaternion(orn)

    front_cam = [0.345 * math.cos(orn[2]), 0.345 * math.sin(orn[2]), 0.4]
    camera_pos = [pos[i] + front_cam[i] for i in range(3)]
    camera_target = [pos[0] + math.cos(orn[2]), pos[1] + math.sin(orn[2]), 0.4]

    for k, v in keys.items():
        if k == p.B3G_UP_ARROW:
            if v & p.KEY_IS_DOWN:
                moving_forward = True
                key_states[0] = int(v & p.KEY_IS_DOWN)
            elif v & p.KEY_WAS_RELEASED:
                moving_forward = False

        if k == p.B3G_DOWN_ARROW:
            if v & p.KEY_IS_DOWN:
                moving_backward = True
                key_states[1] = int(v & p.KEY_IS_DOWN)
            elif v & p.KEY_WAS_RELEASED:
                moving_backward = False

        if k == p.B3G_LEFT_ARROW:
            if v & p.KEY_IS_DOWN:
                steering_left = True
                key_states[2] = int(v & p.KEY_IS_DOWN)
            elif v & p.KEY_WAS_RELEASED:
                steering_left = False

        if k == p.B3G_RIGHT_ARROW:
            if v & p.KEY_IS_DOWN:
                steering_right = True
                key_states[3] = int(v & p.KEY_IS_DOWN)
            elif v & p.KEY_WAS_RELEASED:
                steering_right = False

        if k == ord('s') and v & p.KEY_WAS_TRIGGERED:
            running = False

    # Apply forward and backward motion
    if moving_forward:
        for joint in range(2, 6):
            p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=targetVel, force=maxForce)
    elif moving_backward:
        for joint in range(2, 6):
            p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=-targetVel, force=maxForce)
    else:
        for joint in range(2, 6):
            p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=0, force=maxForce)

    # Apply steering
    if steering_left:
        if moving_forward or moving_backward:
            # Reduce speed on left wheels
            for joint in [2, 4]:  # Assuming these are the left side wheel joints
                p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=targetVel/2 if moving_forward else -targetVel/2, force=maxForce)
    elif steering_right:
        if moving_forward or moving_backward:
            # Reduce speed on right wheels
            for joint in [3, 5]:  # Assuming these are the right side wheel joints
                p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=targetVel/2 if moving_forward else -targetVel/2, force=maxForce)

    if frame_counter % capture_interval == 0:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
        view_matrix = p.computeViewMatrix(camera_pos, camera_target, [0, 0, 1])
        projection_matrix = p.computeProjectionMatrixFOV(90, 1, 0.01, 100)
        images = p.getCameraImage(640, 480, view_matrix, projection_matrix, renderer=p.ER_BULLET_HARDWARE_OPENGL)
        img = np.array(images[2], dtype=np.uint8)
        img = np.reshape(img, (480, 640, 4))
        captured_images.append(img)
        count+=1

        filename = str(count) + '.png'
        filepath = os.path.join('captured_images', filename)
        filepaths.append(filepath)

        data_log.append({
            "timestamp": timestamp,
            "image_filename": filename,
            "key_states": key_states
        })

    frame_counter += 1

    p.stepSimulation()

p.getContactPoints(car)
p.disconnect()

from itertools import zip_longest
# print(data_log[100]["key_states"])
for image_cap, image_path in zip_longest(captured_images, filepaths):
    cv2.imwrite(image_path, image_cap)


import json

# Assuming `data_log` is a list of dictionaries with image paths and key states


# Save data log to a JSON file
data_log_path = 'data_log.json'
with open(data_log_path, 'w') as file:
    json.dump(data_log, file)

