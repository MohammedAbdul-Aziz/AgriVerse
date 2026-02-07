
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# --- Configuration ---
MODEL_PATH = 'plant_disease_model.keras'
IMG_HEIGHT = 128
IMG_WIDTH = 128
CLASS_NAMES = ['healthy', 'multiple_diseases', 'rust', 'scab']

# --- Load the model ---
# Check if the model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please run train.py first.")

model = tf.keras.models.load_model(MODEL_PATH)

def predict(image_path: str) -> dict:
    """
    Loads an image, preprocesses it, and returns the model's prediction.
    """
    try:
        # Load and preprocess the image
        img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create a batch
        img_array /= 255.0  # Rescale images

        # Make prediction
        predictions = model.predict(img_array)
        
        # Format the prediction
        # The model returns an array of probabilities.
        # We'll create a dictionary mapping class names to probabilities.
        prediction_scores = predictions[0]
        result = {CLASS_NAMES[i]: float(prediction_scores[i]) for i in range(len(CLASS_NAMES))}
        
        return {"filename": os.path.basename(image_path), "prediction": result}

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # Create a dummy image for testing if no images are available
    if not os.path.exists('plant-pathology-2020-fgvc7/images/Test_0.jpg'):
        print("Creating a dummy image for testing.")
        dummy_image = np.random.rand(IMG_HEIGHT, IMG_WIDTH, 3) * 255
        tf.keras.preprocessing.image.save_img('dummy_test_image.jpg', dummy_image)
        test_image_path = 'dummy_test_image.jpg'
    else:
        test_image_path = 'plant-pathology-2020-fgvc7/images/Test_0.jpg'
    
    # Get a prediction
    prediction = predict(test_image_path)
    print(prediction)

