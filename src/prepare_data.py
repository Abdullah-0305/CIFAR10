import os
from PIL import Image
import pillow_heif

RAW_DIR = "data/raw"
VIDEO_EXTENSIONS = (".mp4", ".mov")


def convert_heic_to_jpg(heic_path):
    heif_file = pillow_heif.read_heif(heic_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data
    )

    jpg_path = os.path.splitext(heic_path)[0] + ".jpg"
    image.save(jpg_path, "JPEG", quality=95)
    os.remove(heic_path)

    print(f"✔ Converti : {os.path.basename(jpg_path)}")


def normalize_jpg_extension(file_path):
    base, ext = os.path.splitext(file_path)
    if ext == ".JPG":
        new_path = base + ".jpg"
        os.rename(file_path, new_path)
        print(f"🔁 Renommé : {os.path.basename(new_path)}")


def clean_raw_folder():
    for filename in os.listdir(RAW_DIR):
        file_path = os.path.join(RAW_DIR, filename)

        if not os.path.isfile(file_path):
            continue

        # Supprimer les vidéos
        if filename.lower().endswith(VIDEO_EXTENSIONS):
            os.remove(file_path)
            print(f"🗑 Supprimé (vidéo) : {filename}")

        # Convertir HEIC → JPG
        elif filename.lower().endswith(".heic"):
            convert_heic_to_jpg(file_path)

        # Normaliser .JPG → .jpg
        elif filename.endswith(".JPG"):
            normalize_jpg_extension(file_path)

    print("\n✅ Nettoyage terminé")


if __name__ == "__main__":
    clean_raw_folder()
