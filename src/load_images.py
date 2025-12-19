import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
IMG_SIZE = (224, 224)

# Crée le dossier processed s'il n'existe pas
os.makedirs(PROCESSED_DIR, exist_ok=True)

def load_and_process_images():
    images = []
    filenames = []

    for file in os.listdir(RAW_DIR):
        if file.lower().endswith((".jpg", ".png")):
            raw_path = os.path.join(RAW_DIR, file)
            try:
                img = Image.open(raw_path).convert("RGB")
                img_resized = img.resize(IMG_SIZE)
                img_array = np.array(img_resized) / 255.0
                images.append(img_array)
                filenames.append(file)

                # Sauvegarde dans processed
                processed_path = os.path.join(PROCESSED_DIR, file.lower())
                img_resized.save(processed_path)

            except Exception as e:
                print(f"❌ Erreur avec {file}: {e}")

    images = np.array(images)
    print(f"✅ {len(images)} images traitées et sauvegardées dans {PROCESSED_DIR}")
    return images, filenames

def show_sample_images(images, filenames, n=5):
    plt.figure(figsize=(15,3))
    for i in range(min(n, len(images))):
        plt.subplot(1, n, i+1)
        plt.imshow(images[i])
        plt.title(filenames[i])
        plt.axis("off")
    plt.show()

if __name__ == "__main__":
    imgs, names = load_and_process_images()
    show_sample_images(imgs, names, n=5)
