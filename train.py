import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from sklearn.model_selection import train_test_split
import os

# --- Configuration ---
IMAGE_DIR = 'plant-pathology-2020-fgvc7/images'
TRAIN_CSV = 'plant-pathology-2020-fgvc7/train.csv'
IMG_HEIGHT = 224  # Using a larger image size for transfer learning
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 50       # Let's start with 10 epochs for this new model

# --- Load and Prepare Data ---
print("Loading and preparing data...")
train_df = pd.read_csv(TRAIN_CSV)
train_df['image_id'] = train_df['image_id'] + '.jpg'
label_cols = ['healthy', 'multiple_diseases', 'rust', 'scab']
train_df, valid_df = train_test_split(train_df, test_size=0.2, random_state=42)

# --- Image Data Generators with Augmentation ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    train_df,
    directory=IMAGE_DIR,
    x_col='image_id',
    y_col=label_cols,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='raw'
)

validation_generator = validation_datagen.flow_from_dataframe(
    valid_df,
    directory=IMAGE_DIR,
    x_col='image_id',
    y_col=label_cols,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='raw'
)

# --- Build the Model with Transfer Learning ---
print("Building the model using MobileNetV2...")

# 1. Load the base model (pre-trained on ImageNet)
#    - include_top=False means we don't include the final classification layer
#    - weights='imagenet' downloads the pre-trained weights
base_model = MobileNetV2(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
                         include_top=False,
                         weights='imagenet')

# 2. Freeze the base model
#    - We don't want to re-train the expert layers, just use their learned features
base_model.trainable = False

# 3. Create our new model on top
model = Sequential([
    base_model,
    GlobalAveragePooling2D(), # Pools the features from the base model
    Dense(128, activation='relu'),
    Dense(4, activation='softmax') # Our final output layer for 4 classes
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# --- Train the Model ---
print("Training the new model...")
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator
)

# --- Save the Model ---
print("Saving the trained model to plant_disease_model.keras")
model.save('plant_disease_model.keras')

print("Training complete and new, more powerful model saved.")
