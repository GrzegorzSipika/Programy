import os

from PIL import Image

def is_green(pixel, tolerance=50):
    return pixel[1] > pixel[0] + tolerance and pixel[1] > pixel[2] + tolerance

def overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def crop_green_frames(image_path, output_dir, max_frames=4, min_frame_size=(50, 50), tolerance=50):
    img = Image.open(image_path)
    width, height = img.size

    frame_count = 0  # Licznik ramki
    saved_frames = []  # Lista zapisanych obszarów

    # Sprawdź, czy katalog wyjściowy istnieje, jeśli nie, utwórz go
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))

            if is_green(pixel, tolerance):
                left, top, right, bottom = x, y, x, y

                # Poszukiwanie granic ramki
                while right < width and is_green(img.getpixel((right, y)), tolerance):
                    right += 1

                while bottom < height and is_green(img.getpixel((x, bottom)), tolerance):
                    bottom += 1

                # Sprawdź, czy ramka ma odpowiednie wymiary
                if right - left > min_frame_size[0] and bottom - top > min_frame_size[1]:
                    # Sprawdź, czy obszar nie nachodzi na już zapisane obszary
                    overlap_flag = False
                    for frame in saved_frames:
                        if overlap(left, top, right - left, bottom - top, *frame):
                            overlap_flag = True
                            break

                    if not overlap_flag:
                        # Wycięcie i zapis ramki
                        frame_count += 1
                        cropped_img = img.crop((left, top, right, bottom))
                        output_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
                        cropped_img.save(output_path)

                        # Zapisanie współrzędnych zapisanego obszaru
                        saved_frames.append((left, top, right - left, bottom - top))

                # Sprawdź, czy osiągnięto maksymalną liczbę ramek
                if frame_count == max_frames:
                    break

        # Przerwij zewnętrzną pętlę, jeśli osiągnięto maksymalną liczbę ramek
        if frame_count == max_frames:
            break

    if frame_count == 0:
        print("Nie znaleziono obszarów zielonych ramek.")
    else:
        print(f"Znaleziono i zapisano {frame_count} obszarów zielonych ramek.")

if __name__ == "__main__":
    input_image_path = "D:/Magisterka/Wyniki ankiet/a.jpg"
    output_directory = "D:/Magisterka/Wyniki ankiet/frames"

    crop_green_frames(input_image_path, output_directory, max_frames=4, min_frame_size=(50, 50))
