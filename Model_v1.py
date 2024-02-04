import os
import keras
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


main_folder = 'D:/Magisterka/Wyniki ankiet/Skany'


model = ResNet50(weights='imagenet')

label_images_dict = {}

for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    

    if os.path.isdir(subfolder_path) and "wyniki_ankiety" in subfolder:

        label_file_path = os.path.join(subfolder_path, f"wyniki_ankiety_{subfolder}.txt")
        
        if os.path.exists(label_file_path):
            with open(label_file_path, 'r') as label_file:
                label = label_file.read().strip()
        else:
            print(f"Warning: Label file not found for {subfolder}")
            continue

        image_files = [file for file in os.listdir(subfolder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for img_file in image_files:
            img_path = os.path.join(subfolder_path, img_file)

            img = keras.utils.load_img(img_path, target_size=(224, 224))
            print("Wymiary obrazu:", img.size)

            x = keras.utils.img_to_array(img)

            print("Dane przed preprocess_input:")
            print(x)

            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            print("Dane po preprocess_input:")
            print(x)

            predictions = model.predict(x)
 
            decoded_predictions = decode_predictions(predictions, top=3)[0]

            print(f"Predictions for {img_file} in folder {subfolder} with label {label}:")
            for i, (imagenet_id, prediction_label, score) in enumerate(decoded_predictions):
                print(f"{i + 1}: {prediction_label} ({score:.2f})")

                if label not in label_images_dict:
                    label_images_dict[label] = []
                label_images_dict[label].append(img_file)
            print("\n")

for label, images in label_images_dict.items():
    print(f"{label}: {images}")
