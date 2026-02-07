
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os


MODEL_PATH = 'plant_disease_model.keras'
IMG_HEIGHT = 128
IMG_WIDTH = 128
CLASS_NAMES = ['healthy', 'multiple_diseases', 'rust', 'scab']


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please run train.py first.")

model = tf.keras.models.load_model(MODEL_PATH)

def analyze_nutrient_status(image_tensor):
  
    image_tensor = tf.cast(image_tensor, tf.float32)
    b, g, r = tf.unstack(image_tensor, axis=-1)
    
    vegetation_index = (2 * g) - r - b + 510
    mean_index = tf.reduce_mean(vegetation_index)
    mean_value = mean_index.numpy()
    
    
    if mean_value > 560:
        return "Optimal"
    elif 540 <= mean_value <= 560:
        return "Slight Deficiency Detected"
    else:
        return "Significant Deficiency Detected"

def predict(image_path: str) -> dict:
    """
    Loads an image, preprocesses it, and returns the model's prediction for
    both disease and nutrient status.
    """
    try:
        # --- Disease Prediction ---
        # Load and preprocess the image for the deep learning model
        img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array_normalized = image.img_to_array(img)
        
        # --- Nutrient Analysis ---
        # Use the non-normalized image array for vegetation index calculation
        nutrient_status = analyze_nutrient_status(img_array_normalized)

        # Continue with normalization for the disease prediction model
        img_array_normalized = np.expand_dims(img_array_normalized, axis=0)  # Create a batch
        img_array_normalized /= 255.0  # Rescale images

        # Make disease prediction
        predictions = model.predict(img_array_normalized)
        
        # Format the disease prediction
        prediction_scores = predictions[0]
        result = {CLASS_NAMES[i]: float(prediction_scores[i]) for i in range(len(CLASS_NAMES))}
        
        return {
            "filename": os.path.basename(image_path),
            "prediction": result,
            "nutrient_status": nutrient_status
        }

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

