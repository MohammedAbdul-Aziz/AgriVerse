
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os

# --- Configuration ---
IMAGE_DIR = 'plant-pathology-2020-fgvc7/images'
TRAIN_CSV = 'plant-pathology-2020-fgvc7/train.csv'
IMG_HEIGHT = 128
IMG_WIDTH = 128
BATCH_SIZE = 32
EPOCHS = 5 # In a real scenario, you'd use more epochs

# --- Load and Prepare Data ---
print("Loading and preparing data...")
train_df = pd.read_csv(TRAIN_CSV)
train_df['image_id'] = train_df['image_id'] + '.jpg'

# Identify the label columns
label_cols = ['healthy', 'multiple_diseases', 'rust', 'scab']

# Split data into training and validation sets
train_df, valid_df = train_test_split(train_df, test_size=0.2, random_state=42)

# --- Image Data Generators ---
# This will rescale and augment the images
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
    class_mode='raw' # Use 'raw' for multi-label classification
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


# --- Build the Model ---
print("Building the model...")
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax') # 4 classes
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# --- Train the Model ---
print("Training the model...")
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.n // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.n // BATCH_SIZE
)

# --- Save the Model ---
print("Saving the trained model to plant_disease_model.keras")
model.save('plant_disease_model.keras')

print("Training complete and model saved.")
