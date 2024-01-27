import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import PhotoImage

import requests
from PIL import ImageTk
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet
import os
from utils import encode_image

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
ORGAN_CHOICES = ["LIVER", "HEAD"]

file_path = ""
selected_organ = ""


def upload_image():
    global file_path
    file_path = filedialog.askopenfilename(
        title=f"Select {selected_organ} Image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
    )

    if file_path:
        print(f"Selected {selected_organ} Image:", file_path)
        display_uploaded_image()
        btn_analyze_img.config(state=tk.ACTIVE)


def display_uploaded_image():
    original_image = PILImage.open(file_path)
    resized_image = original_image.resize((400, 400), PILImage.BICUBIC)
    img = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(window, background="#050505", image=img)
    image_label.image = img
    image_label.pack(padx=50, pady=50)


def send_analyze_request(file_path):
    encoded_image = encode_image(file_path)

    url = "http://localhost:8000/upload_image"

    payload = {"image": encoded_image}

    response = requests.post(url, json=payload)

    print("Server response:", response.text)  # Add this line to print the server response

    diagnosis = response.json()

    return diagnosis


def show_diagnosis_window():
    if file_path:
        result = send_analyze_request(file_path)
        diagnosis = result["diagnosis"]
        confidence = result["confidence"]

        diagnosis_window = tk.Toplevel()
        diagnosis_window.title("Diagnosis")
        diagnosis_window.geometry("400x400")
        diagnosis_window.resizable(False, False)
        diagnosis_window.config(background="#BBBBBB")

        diagnosis_label = tk.Label(
            diagnosis_window,
            text=f"Diagnosis: {diagnosis}",
            font=("Calibri", 16),
            background="#BBBBBB"
        )
        diagnosis_label.pack(pady=20)

        probability_label = tk.Label(
            diagnosis_window,
            text=f"Probability: {confidence:.2f}",
            font=("Calibri", 16),
            background="#BBBBBB"
        )
        probability_label.pack(pady=20)

        create_diagnosis_pdf(file_path, diagnosis, confidence)


def update_selected_organ(event):
    global selected_organ
    selected_organ = organ_combobox.get()

    organ_combobox.pack_forget()
    upload_image_button.config(state=tk.ACTIVE)

    analysis_label = tk.Label(
        window,
        font=("Calibri", 20),
        text=f"{selected_organ} Tomography Analysis",
        compound="center",
        fg="white",
        bg='black',
        bd=0,
        highlightbackground="white",
        highlightthickness=2,
    )
    analysis_label.pack(padx=20, pady=5)


def create_diagnosis_pdf(image_path, diagnosis, probability):
    pdf_filename = "diagnosis_report.pdf"

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    styles = getSampleStyleSheet()

    content = []

    if os.path.exists(image_path):
        img = ReportLabImage(image_path, width=400, height=400)
        content.append(img)

    diagnosis_text = f"Diagnosis: {diagnosis}"
    probability_text = f"Probability: {probability:.2f}"

    content.append(Paragraph(diagnosis_text, styles["Normal"]))
    content.append(Paragraph(probability_text, styles["Normal"]))

    doc.build(content)

    print(f"PDF report generated: {pdf_filename}")

    return pdf_filename


window = tk.Tk()
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.title("Project title")
window.resizable(False, False)

# set an image as background of window
background_image = PhotoImage(file="bg_gui.png")
background_image = background_image.subsample(
    int(background_image.width() / WINDOW_WIDTH),
    int(background_image.height() / WINDOW_HEIGHT)
)
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# combobox for choosing the organ
organ_combobox = ttk.Combobox(
    window,
    values=ORGAN_CHOICES,
    state="readonly",
    font=("Calibri", 15)
)
organ_combobox.set("Choose Organ")
organ_combobox.pack(pady=10)
organ_combobox.bind("<<ComboboxSelected>>", update_selected_organ)

# button for uploading image
upload_image_button = tk.Button(
    window,
    text="UPLOAD IMAGE",
    command=upload_image,
    font=("Calibri", 20),
    fg="white",
    bg='black',
    activeforeground="white",
    activebackground='black',
    state=tk.DISABLED,
    compound='bottom',
    bd=5,
)
upload_image_button.place(relx=0.5, rely=0.75, anchor="center")

# button for analyzing image
btn_analyze_img = tk.Button(
    window,
    text="ANALYZE IMAGE",
    font=("Calibri", 20),
    fg="white",
    bg="black",
    activeforeground="white",
    activebackground='black',
    state=tk.DISABLED,
    compound='bottom',
    bd=5,
    command=show_diagnosis_window
)
btn_analyze_img.place(relx=0.5, rely=0.9, anchor="center")

window.mainloop()
