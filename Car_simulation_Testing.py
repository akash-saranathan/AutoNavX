import pybullet as p
import pybullet_data
import cv2
import numpy as np
import os
import math
import tensorflow as tf
import datetime
import time
import random
keys1 = []


# Function to connect to the physics server
def connect_to_server():
    connection_id = p.connect(p.GUI)
    if connection_id < 0:
        raise ConnectionError("Failed to connect to PyBullet physics server.")
    return connection_id

# Function to preprocess the image
def preprocess_image(img):
    img = cv2.resize(img, (200, 150))  # Resize for consistency
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert from BGRA to BGR
    img = img / 255.0  # Normalize the image
    return img

# Connect to the physics server
try:
    connection_id = connect_to_server()
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
 

    # Load plane and car URDFs
    plane_path = os.path.abspath('simple_plane.urdf')
    print(f"Loading URDF file from: {plane_path}")
    p.loadURDF(plane_path)
    p.setGravity(0, 0, -10)
    camera_pos = [0, 0, 10]  # Adjust the height as needed
    camera_target = [0, 0, 0]

    carpos = [0, 0, 0.1]
    car = p.loadURDF("husky/husky.urdf", carpos[0], carpos[1], carpos[2])

    numJoints = p.getNumJoints(car)
    for joint in range(numJoints):
        print(p.getJointInfo(car, joint))

    targetVel = 1  # rad/s
    maxForce = 100  # Newton
    p.setRealTimeSimulation(1)

  
    num_obstacles = 100

    # Generate obstacle positions
    obstacle_positions = []
    for i in range(num_obstacles):
        x = random.randint(1, 40)  # Random x position between 1 and 100
        y = random.randint(-10, 10)  # Random y position between -50 and 50 to spread them along the y-axis
        obstacle_positions.append((x, y,0.5))
    for pos in obstacle_positions:
        p.loadURDF("cube.urdf", pos, [0, 0, 1.73, 0.7], useFixedBase=False, globalScaling=0.5)




    # Load the trained model
    # model = tf.keras.models.load_model('CNN_car_navigation_model.h5')  #CNN model

    #Uncomment this if you want to use VGG16 model
    model = tf.keras.models.load_model('vgg16_car_navigation_model.h5')  #VGG16 model


    frame_counter = 0
    capture_interval = 5  # Adjust the capture interval as needed
    running = True

    while running:
        keys = p.getKeyboardEvents()

        for k, v in keys.items():
            if k == ord('s') and v & p.KEY_WAS_TRIGGERED:
                running = False

        pos, orn = p.getBasePositionAndOrientation(car)
        pos = list(pos)
        orn = p.getEulerFromQuaternion(orn)

        front_cam = [0.345 * math.cos(orn[2]), 0.345 * math.sin(orn[2]), 0.4]
        camera_pos = [pos[i] + front_cam[i] for i in range(3)]
        camera_target = [pos[0] + math.cos(orn[2]), pos[1] + math.sin(orn[2]), 0.4]

        if frame_counter % capture_interval == 0:
            view_matrix = p.computeViewMatrix(camera_pos, camera_target, [0, 0, 1])
            projection_matrix = p.computeProjectionMatrixFOV(90, 1, 0.01, 100)
            images = p.getCameraImage(640, 480, view_matrix, projection_matrix, renderer=p.ER_BULLET_HARDWARE_OPENGL)
            img = np.array(images[2], dtype=np.uint8)
            img = np.reshape(img, (480, 640, 4))
            img = preprocess_image(img)

            # Predict the direction using the model
            
            prediction = model.predict(np.expand_dims(img, axis=0))
            predicted_index = np.argmax(prediction)
            predicted_key_state = format(predicted_index, '04b')
            predicted_key_state_list = [int(bit) for bit in predicted_key_state]
            predicted_key_state_list += [0] * (4 - len(predicted_key_state_list))
            print(predicted_key_state_list)
            
            # predicted_direction = np.argmax(prediction, axis=1)[0]
            # predicted_direction = np.argmax(predicted_key_state_list)
            binary_string = ''.join(map(str, predicted_key_state_list))  # Convert the list to a string
            predicted_direction = int(binary_string, 2)  # Convert the binary string to decimal
            keys1.append(predicted_direction)
            

            # Initialize key states
            moving_forward = False
            moving_backward = False
            steering_left = False
            steering_right = False

            # Map the predicted direction to key states
            if predicted_direction == 8:
                moving_forward = True
            elif predicted_direction == 4:
                moving_backward = True
            elif predicted_direction == 10:
                print("yes")
                steering_left = True
                moving_forward = True
            elif predicted_direction == 9:
                steering_right = True
                moving_forward = True
            elif predicted_direction == 5:
                steering_right = True
                moving_backward = True
            elif predicted_direction == 6:
                steering_left = True
                moving_backward = True
            

            # Apply forward and backward motion
            if moving_forward:
                for joint in range(2, 6):
                    p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=targetVel, force=maxForce)
            elif moving_backward:
                for joint in range(2, 6):
                    p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=-targetVel, force=maxForce)
            # else:
            #     for joint in range(2, 6):
            #         p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=0, force=maxForce)

            # Apply steering
            if steering_left:
                if moving_forward or moving_backward:
                # print("aama")
                # Reduce speed on left wheels
                    for joint in [2, 4]:  # Assuming these are the left side wheel joints
                        p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=targetVel/2 if moving_forward else -targetVel/2, force=maxForce)
            elif steering_right:
                if moving_forward or moving_backward:
                # Reduce speed on right wheels
                    for joint in [3, 5]:  # Assuming these are the right side wheel joints
                        p.setJointMotorControl2(car, joint, p.VELOCITY_CONTROL, targetVelocity=targetVel/2 if moving_forward else -targetVel/2, force=maxForce)

        frame_counter += 1

        p.stepSimulation()

    p.getContactPoints(car)

finally:
    
    p.disconnect()
