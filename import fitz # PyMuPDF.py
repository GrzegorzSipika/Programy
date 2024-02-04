from PIL import Image

def is_green(pixel, tolerance=50):
    # Sprawdź, czy kolor piksela jest w zakresie kolorów zielonych
    return pixel[1] > pixel[0] + tolerance and pixel[1] > pixel[2] + tolerance

def crop_green_frame(image_path, output_path, tolerance=50):
    # Wczytaj obraz
    img = Image.open(image_path)

    # Pobierz rozmiar obrazu
    width, height = img.size

    # Inicjalizuj krawędzie obszaru zielonej ramki
    left, top, right, bottom = width, height, 0, 0

    # Przeszukaj obraz w poszukiwaniu obszaru zielonej ramki
    for x in range(width):
        for y in range(height):
            # Pobierz kolor piksela
            pixel = img.getpixel((x, y))
            
            # Sprawdź, czy kolor piksela wskazuje na zieloną ramkę z tolerancją
            if is_green(pixel, tolerance):
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    # Sprawdź, czy znaleziono obszar zielonej ramki
    if left < right and top < bottom:
        # Wyciąć obszar zielonej ramki
        cropped_img = img.crop((left, top, right, bottom))

        # Zapisz wycięty obraz do nowego pliku
        cropped_img.save(output_path)
    else:
        print("Nie znaleziono obszaru zielonej ramki.")

if __name__ == "__main__":
    input_image_path = "D:/Magisterka/Wyniki ankiet/b.jpg"
    output_image_path = "D:/Magisterka/Wyniki ankiet/2.jpg"

    crop_green_frame(input_image_path, output_image_path)
