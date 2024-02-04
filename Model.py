import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

def load_data(data_path):
    images = []
    labels = []

    for folder_name in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder_name)
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):
                img_path = os.path.join(folder_path, filename)
                image = cv2.imread(img_path)
                image = cv2.resize(image, (64, 64))  # Dostosuj rozmiar obrazów
                images.append(image)
                labels.append(int(folder_name))  # Zakładam, że nazwy folderów są identyfikatorami predyspozycji naukowych

    return np.array(images), np.array(labels)

def load_new_data(new_data_path):
    new_images = []
    for filename in os.listdir(new_data_path):
        if filename.endswith(".jpg"):
            img_path = os.path.join(new_data_path, filename)
            image = cv2.imread(img_path)
            image = cv2.resize(image, (64, 64))
            new_images.append(image)
    return np.array(new_images)

def build_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))  # Wartość wyjściowa - zakres od 0 do 1

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(model, train_images, train_labels):
    model.fit(train_images, train_labels, epochs=10)

def main():
    # Ścieżki do danych treningowych i nowych danych testowych
    train_data_path = "D:/Magisterka/Wyniki ankiet/b"
    new_data_path = "D:/Magisterka/Nowe dane testowe"

    # Wczytaj dane treningowe
    train_images, train_labels = load_data(train_data_path)

    # Wczytaj nowe dane testowe
    new_images = load_new_data(new_data_path)

    # Zbuduj model
    model = build_model()

    # Trenuj model
    train_model(model, train_images, train_labels)

    # Predykcja na nowych danych testowych
    predictions = model.predict(new_images)
    print("Predykcje dla nowych danych:", predictions)

if __name__ == "__main__":
    main()
