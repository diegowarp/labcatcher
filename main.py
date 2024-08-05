import rawpy
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyperclip
from colorspacious import cspace_convert

def convert_rgb_to_bgr(image):
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image_bgr

def load_image(file_path):
    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'nef':
        with rawpy.imread(file_path) as raw:
            image_rgb = raw.postprocess()
    else:
        image_rgb = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    return image_rgb

def adjust_intensity(lab_color, adjustment_factor):
    l, a, b = lab_color
    l = min(l * adjustment_factor, 100)  # ensure l is within the range [0, 100]
    return (l, a, b)



roi = []
circle_center = None
circle_radius = 0
final_circle_center = None
original_image = None
image_with_roi = None

def select_roi(event, x, y, flags, param):
    global circle_center, circle_radius, final_circle_center, original_image, image_with_roi
    if event == cv2.EVENT_LBUTTONDOWN:
        circle_center = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and circle_center is not None:
        circle_radius = int(np.sqrt((x - circle_center[0]) ** 2 + (y - circle_center[1]) ** 2))
        image_with_roi = original_image.copy()
        cv2.circle(image_with_roi, circle_center, circle_radius, (0, 255, 0), 2)
        cv2.imshow("Image", image_with_roi)
    elif event == cv2.EVENT_LBUTTONUP:
        final_circle_center = circle_center
        circle_center = None
        image_with_roi = original_image.copy()
        cv2.circle(image_with_roi, final_circle_center, circle_radius, (0, 255, 0), 2)
        cv2.imshow("Image", image_with_roi)

def resize_image(image, max_width=800, max_height=800):
    height, width = image.shape[:2]
    proportion = min(max_width / width, max_height / height)
    new_width = int(width * proportion)
    new_height = int(height * proportion)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def calculate_rgb_color(image, center, radius):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    roi_rgb = cv2.bitwise_and(image, image, mask=mask)

    valid_pixels = np.where(mask == 255)
    average_rgb_color = np.mean(roi_rgb[valid_pixels], axis=0)

    return average_rgb_color

def calculate_lab_color(image, center, radius):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    average_rgb_color = calculate_rgb_color(image_rgb, center, radius)
    average_rgb_color = average_rgb_color / 255  # Normalizar para o intervalo 0-1
    average_lab_color = cspace_convert(average_rgb_color, "sRGB1", "CIELab")

    return average_lab_color

def lab_to_rgb(lab_color):
    lab_color_scaled = np.array([[[(lab_color[0] * 2.55, lab_color[1] + 128, lab_color[2] + 128)]]], dtype=np.float32)
    rgb_color = cv2.cvtColor(lab_color_scaled, cv2.COLOR_LAB2BGR)
    rgb_color = tuple(map(int, rgb_color[0, 0]))
    return rgb_color

def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.NEF;*.JPG;*.JPEG;*.PNG;*.BMP;*.TIFF;*.SVG")])
    return file_path

def display_result(lab_color):
    result_window = tk.Toplevel()
    result_window.title("Result")
    result_window.geometry("720x150")
    result_window.configure(bg='#D1E8E2')

    lab_color_rounded = tuple(round(component, 2) for component in lab_color)
    lab_color_str = '\t'.join(f'{num:.2f}' for num in lab_color)
    tk.Label(result_window, text=f"LAB color of the selected region:\n {lab_color_rounded}", font=("Helvetica", 12), bg='#D1E8E2').pack(pady=10)

    def copy_result():
        pyperclip.copy(str(lab_color_str))

    tk.Button(result_window, text="Copy", command=copy_result, width=15, height=2,
              font=("Helvetica", 12),
              bg='#B4CFEC', relief='flat').pack(pady=5)

def display_about():
    about_window = tk.Toplevel()
    about_window.title("About")
    about_window.geometry("320x150")
    about_window.configure(bg='#D1E8E2')

    tk.Label(about_window, text="LABCatcher Version 0.9\n\nDeveloped by: Diego Bomfim \nGitHub: diegowarp", font=("Helvetica", 12), bg='#D1E8E2').pack(pady=30)

def display_instructions():
    instructions_window = tk.Toplevel()
    instructions_window.title("Instructions")
    instructions_window.geometry("660x440")
    instructions_window.configure(bg='#D1E8E2')

    instructions = (
        "Welcome to LABCatcher! Your facilitator in collecting LAB colors.\n\n\n"
        "1. Click on 'Choose Image' to select an image.\n\n"
        "2. Use the mouse to draw a circle in the area of interest.\n\n"
        "3. Press the 'ENTER' key to calculate the LAB color of the selected area.\n\n"
        "4. If you have drawn a wrong region, press the 'c' key to redo.\n\n"
        "5. If you have chosen the wrong image, press the 'esc' key to choose another.\n\n"
        "6. The result will be displayed in a new window.\n\n"
        "7. Use the 'Copy' button to copy the LAB result to the clipboard."
    )

    tk.Label(instructions_window, text="How to use LABCatcher?", font=("Helvetica", 16), bg='#D1E8E2').pack(pady=5)

    tk.Label(instructions_window, text=instructions, font=("Helvetica", 12), bg='#D1E8E2').pack(pady=30)
    tk.Button(instructions_window, text="Back", command=instructions_window.destroy, width=15, height=2, font=("Helvetica", 12),
              bg='#B4CFEC', relief='flat').pack(pady=5)

def start_program():
    global final_circle_center, circle_radius, original_image, image_with_roi  # Adicione image_with_roi ao global
    image_path = choose_image()

    if image_path:
        image = load_image(image_path)
        image = resize_image(image)
        image = convert_rgb_to_bgr(image)
        original_image = image.copy()
        image_with_roi = original_image.copy()  # Crie a cópia para image_with_roi aqui
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", select_roi, image)

        while True:
            cv2.imshow("Image", image_with_roi)  # Agora image_with_roi já tem um valor atribuído
            key = cv2.waitKey(1) & 0xFF
            if key == 13 or key == 10:  # Verifica se a tecla 'Enter' foi pressionada
                break
            elif key == ord("c"):
                image_with_roi = original_image.copy()
                final_circle_center = None
                circle_radius = 0
                cv2.imshow("Image", image_with_roi)  # Atualiza a janela com a imagem original sem a ROI
            elif key == 27:  # ESC key
                cv2.destroyAllWindows()
                start_program()  # Restart the program
                return

        cv2.destroyAllWindows()

        if final_circle_center is not None and circle_radius > 0:
            lab_color = calculate_lab_color(image, final_circle_center, circle_radius)
            lab_color = adjust_intensity(lab_color, 1.11)
            display_result(lab_color)
        else:
            messagebox.showerror("Error", "No region was selected.")
    else:
        return


if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("LABCatcher")
    main_window.geometry("760x340")
    main_window.configure(bg='#D1E8E2')

    tk.Label(main_window, text="LABCatcher", font=("Helvetica", 42), bg='#D1E8E2').pack(pady=30)
    tk.Button(main_window, text="Choose Image", command=start_program, width=30, height=2,
              font=("Helvetica", 12), bg='#B4CFEC', relief='flat').pack(pady=5)
    tk.Button(main_window, text="Instructions", command=display_instructions, width=30, height=2,
              font=("Helvetica", 12), bg='#B4CFEC', relief='flat').pack(pady=5)
    tk.Button(main_window, text="About", command=display_about, width=30, height=2, font=("Helvetica", 12),
              bg='#B4CFEC', relief='flat').pack(pady=5)

    main_window.mainloop()