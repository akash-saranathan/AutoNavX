# AutoNavX: Autonomous Car Navigation System with obstacle avoidance

This repository contains the code for generating simulation data, training a model for car navigation, and testing the autonomous navigation system.

To run inference with VGG16 or train from scratch, please download the weights and npy files from this [link](https://drive.google.com/drive/folders/1ZUXp2J0J8eAhoMmieh4N57tYUP5LLrJd?usp=sharing).

## Data Generation

To generate the data, run the Car_simulation_Data_generation.py script. This script will launch a car simulation where you can control the car using the keyboard.

Controls:
Press 's' to close the simulation when you are done generating the data.

## Running the Data Generation Script:

Run the following command in your terminal or command prompt:
```python
python Car_simulation_Data_generation.py
```

This script captures images as input and records the control commands from the keyboard as output.

## Model Training

To train the model using VGG16, run the Model_training.py script. This script will train the model on the generated data and save the trained model.

## Running the Model Training Script:

Run the following command in your terminal or command prompt:
```python
python Model_training.py
```

Ensure that the data generated from the previous step is available in the required format.

## Testing the Autonomous Navigation

To test the autonomous navigation system, run the Car_simulation_Testing.py script. This script will launch the car simulation and use the trained model to control the car autonomously.

## Running the Testing Script:

Run the following command in your terminal or command prompt:
```python
python Car_simulation_Testing.py
```

Uncomment the relevant lines (68-72) in the script to choose between using a CNN model or a VGG16 model. Press 's' to close the simulation when you are done testing.

In Car_simulation_Testing.py, uncomment the following lines to choose the model:
```python
# model = tf.keras.models.load_model('car_navigation_model_cnn.h5')
# or
# model = tf.keras.models.load_model('car_navigation_model_vgg16.h5')
```
## Video Links for Training and Inference
- Data Generation: [Link](https://drive.google.com/file/d/15riAcyFzDTyNl0oCPtJWqvBPART6k77T/view?resourcekey) 
- AutoNavX Demo: [Link](https://drive.google.com/file/d/1ldTw88nBzJmgnG_aKOEBxu39Tz-b3uie/view?resourcekey)

## Summary
1. Data Generation: Run Car_simulation_Data_generation.py to generate data.
2. Model Training: Run Model_training.py to train the model using VGG16.
3. Testing: Run Car_simulation_Testing.py to test the autonomous navigation system.

# AutoNavX
