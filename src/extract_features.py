import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model
from PIL import Image

PROCESSED_DIR = "data/processed"
FEATURES_FILE = "data/features.npy"
IMG_SIZE = (224, 224)

# Charger MobileNetV2 pré-entraîné, sans la couche de classification
base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

def load_and_preprocess(img_path):
    img = Image.open(img_path).convert("RGB").resize(IMG_SIZE)
    x = np.array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)  # normalisation spécifique MobileNet
    return x

def extract_features():
    feature_list = []
    filenames = []

    for file in os.listdir(PROCESSED_DIR):
        if file.lower().endswith((".jpg", ".png")):
            path = os.path.join(PROCESSED_DIR, file)
            try:
                x = load_and_preprocess(path)
                features = model.predict(x, verbose=0)  # shape (1, 1280)
                feature_list.append(features.flatten())
                filenames.append(file)
            except Exception as e:
                print(f"❌ Erreur avec {file}: {e}")

    features_array = np.array(feature_list)
    np.save(FEATURES_FILE, features_array)
    print(f"✅ Features extraites pour {len(filenames)} images et sauvegardées dans {FEATURES_FILE}")

    return features_array, filenames

if __name__ == "__main__":
    features, names = extract_features()
