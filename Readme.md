# AutoNavX

## Introduction
Autonomous Car Navigation System with Obstacle Avoidance. This repository contains the code for generating simulation data, training a model for car navigation, and testing the autonomous navigation system.


## Project Highlights:
- Developed and simulated an autonomous navigation environment using PyBullet, generating diverse datasets with varied obstacles for training and testing.
- Implemented VGG-16 to process images and control states, achieving 75.15% accuracy and reducing loss by 5%, outperforming baseline CNN results.
- Conducted comparative analysis of neural network architectures for obstacle detection and control prediction, optimizing performance for safer vehicle navigation.

## Data Download
To run inference with VGG16 or train from scratch, please download the weights and `npy` files from [this link](#).

## Data Generation
To generate the data, run the `Car_simulation_Data_generation.py` script. This script will launch a car simulation where you can control the car using the keyboard.

### Controls:
- Press `'s'` to close the simulation when you are done generating the data.

### Running the Data Generation Script:
```bash
python Car_simulation_Data_generation.py
```

This script captures images as input and records the control commands from the keyboard as output.

## Model Training
To train the model using VGG16, run the `Model_training.py` script. This script trains the model on the generated data and saves the trained model.

### Running the Model Training Script:
```bash
python Model_training.py
```

Ensure that the data generated from the previous step is available in the required format.

## Testing the Autonomous Navigation System
To test, run `Car_simulation_Testing.py`. This script will launch a car simulation and use your trained model to control it autonomously.

### Running the Testing Script:
```bash
python Car_simulation_Testing.py
```

Uncomment lines 68–72 in `Car_simulation_Testing.py` to select between using a CNN model or a VGG16 model:
- `# model = tf.keras.models.load_model('car_navigation_model_cnn.h5')`
- `# model = tf.keras.models.load_model('car_navigation_model_vgg16.h5')`

### Video Links for Training and Inference:
- Data Generation: [Link](https://drive.google.com/file/d/15riAcyFzDTyNl0oCPtJWqvBPART6k77T/view?resourcekey)
- AutoNavX Demo: [Link](https://drive.google.com/file/d/1ldTw88nBzJmgnG_aKOEBxu39Tz-b3uie/view?resourcekey)

## Skills:
Deep Learning, Computer Vision, PyBullet, Autonomous Navigation, VGG-16, CNN, Python
 
## Summary:
1. **Data Generation:** Run `Car_simulation_Data_generation.py` to generate data.
2. **Model Training:** Run `Model_training.py` to train with VGG16.
3. **Testing:** Run `Car_simulation_Testing.py` to evaluate autonomous navigation.
