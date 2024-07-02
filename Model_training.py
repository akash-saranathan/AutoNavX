import os
import cv2
import numpy as np
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import os
import cv2
import numpy as np
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

# Load data log
data_log_path = 'data_log.json'
with open(data_log_path, 'r') as file:
    data_log = json.load(file)

captured_images = []
commands = []
print("here",data_log[0])
for i in range(len(data_log)):

    entry = data_log[i]
    # print(i,entry["image_filename"])
    image_only_path = entry["image_filename"]
    img_path = os.path.join('captured_images', image_only_path)
    if os.path.isfile(img_path):
        # print("yes")
        img = cv2.imread(img_path)
        img = cv2.resize(img, (200, 150))  # Resize for faster training
        img = img / 255.0  # Normalize the image
        captured_images.append(img)
        # Convert key_states to a decimal value
        if isinstance(entry["key_states"], list):  # Check if key_states is a list
            decimal_command = int(''.join(map(str, entry["key_states"])), 2)
        else:  # If it's not a list, convert it directly to decimal
            decimal_command = int(entry['key_states'])
        commands.append(decimal_command)

captured_images = np.array(captured_images)
commands = np.array(commands)
print(captured_images,commands)

# Check if the lengths match
assert len(captured_images) == len(commands), f"Mismatch: {len(captured_images)} images and {len(commands)} commands"

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(captured_images, commands, test_size=0.2, random_state=23)

np.save('X_train.npy', X_train)
np.save('X_val.npy', X_val)
np.save('y_train.npy', y_train)
np.save('y_val.npy', y_val)


# VGG16 model Training

import numpy as np
import pickle
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Activation
from tensorflow.keras.utils import to_categorical

# Load preprocessed data
X_train = np.load('X_train.npy')
X_val = np.load('X_val.npy')
y_train = np.load('y_train.npy')
y_val = np.load('y_val.npy')

# VGG-16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 200, 3))

model = Sequential([
    base_model,
    Flatten(),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    Dense(16),  # Output layer with 16 units
    Activation('softmax')  # Softmax activation function for multi-class classification
])

# Freeze the layers of the VGG16 base model
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, to_categorical(y_train, num_classes=16), epochs=50, batch_size=32, validation_data=(X_val, to_categorical(y_val, num_classes=16)))

# Save the trained model
model.save('vgg16_car_navigation_model.h5')

# Save the training history to a pickle file
with open('history.pkl', 'wb') as file:
    pickle.dump(history.history, file)

# Plot the training history graph
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
