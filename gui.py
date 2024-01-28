import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import PhotoImage

import requests
from PIL import ImageTk
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from utils import encode_image

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
ORGAN_CHOICES = ["Kidney", "Chest"]

file_path = ""
selected_organ = ""
image_label = None


def upload_image():
    """
    Upload image from local machine (jpg, jpeg, png)

    """
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
    """ Display uploaded image in the window and
        delete the previous image if it exists

    """
    global image_label
    if image_label:
        image_label.destroy()

    original_image = PILImage.open(file_path)
    resized_image = original_image.resize((400, 400), PILImage.BICUBIC)
    img = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(window, background="#050505", image=img)
    image_label.image = img
    image_label.pack(padx=50, pady=50)
    btn_upload_img.config(state=tk.DISABLED)


def send_analyze_request(file_path, selected_organ):
    """
    Send image to server for analysis

    Parameters
    ----------
    file_path : str
        Path to the image file

    Returns
    -------
    diagnosis : dict
        Dictionary containing the diagnosis and confidence
    """
    encoded_image = encode_image(file_path)

    print(selected_organ)

    url = "http://localhost:8000"

    if selected_organ == "Kidney":
        url += "/kidney"
    elif selected_organ == "Chest":
        url += "/chest"

    payload = {"image": encoded_image}

    response = requests.post(url, json=payload)

    print("Server response:", response.text)

    diagnosis = response.json()

    return diagnosis


def show_diagnosis_window():
    """
    Display diagnosis window with the diagnosis and confidence

    """
    global file_path
    if file_path:
        for widget in window.winfo_children():
            if widget != background_label:
                widget.destroy()

        result = send_analyze_request(file_path, selected_organ)
        diagnosis = result["diagnosis"]
        confidence = result["confidence"]

        diagnosis_label = tk.Label(
            window,
            text=f"Diagnosis: {diagnosis}\nProbability: {confidence*100: .2f}%",
            font=("Calibri", 20),
            background="#F0F0F0",
            height=3,
            width=25,
            bd=2,
            relief="solid"
        )
        diagnosis_label.config(state=tk.DISABLED)
        diagnosis_label.pack(pady=20)

        generate_pdf_button = tk.Button(
            window,
            text="Generate PDF",
            command=lambda: create_diagnosis_pdf(file_path, diagnosis, confidence),
            font=("Calibri", 20),
            bg="black",
            fg="white",
            activeforeground="white",
            activebackground='black',
            bd=5,
            padx=10,
            pady=5,
            compound='bottom'
        )
        generate_pdf_button.pack(pady=10)


def update_selected_organ(event):
    """
    Update the selected organ in the combobox

    Parameters
    ----------
    event : tkinter.Event
        Event that triggered the function

    """
    global selected_organ
    selected_organ = organ_combobox.get()

    analysis_label.config(text=f"{selected_organ} Tomography Analysis")

    btn_upload_img.config(state=tk.ACTIVE)


def create_diagnosis_pdf(image_path, diagnosis, confidence):
    """
    Create a PDF report with the diagnosis and confidence

    Parameters
    ----------
    image_path : str
        Path to the image file
    diagnosis : str
        Diagnosis of the image
    confidence : float
        Confidence of the diagnosis

    Returns
    -------
    pdf_filename : str
        Name of the PDF file

    """
    pdf_filename = f"{selected_organ.lower()}_diagnosis_report.pdf"

    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=15,
        leading=14,
        spaceAfter=10
    )

    content = []

    title = f"<b>{selected_organ} Diagnosis Report</b>"
    content.append(Paragraph(title, styles['Title']))

    content.append(HRFlowable(width="100%", thickness=2, color="black", spaceBefore=5, spaceAfter=5))

    if os.path.exists(image_path):
        img = ReportLabImage(image_path, width=400, height=400)
        content.append(img)

    content.append(HRFlowable(width="100%", thickness=2, color="black", spaceBefore=5, spaceAfter=5))

    diagnosis_text = f"<b>Diagnosis:</b> {diagnosis}"
    probability_text = f"<b>Probability:</b> {confidence}"
    content.append(Paragraph(diagnosis_text, custom_style))
    content.append(Paragraph(probability_text, custom_style))

    doc.build(content)

    print(f"PDF report generated: {pdf_filename}")

    return pdf_filename


# Main window
window = tk.Tk()
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.title("Organ Diagnosis UI")
window.resizable(False, False)

# Set an image as background of window
background_image = PhotoImage(file="bg_gui.png")
background_image = background_image.subsample(
    int(background_image.width() / WINDOW_WIDTH),
    int(background_image.height() / WINDOW_HEIGHT)
)
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# combobox for choosing the organ
selected_organ = tk.StringVar()
selected_organ.set("[Select Organ]")

combobox_style = ttk.Style()
combobox_style.configure('Custom.TCombobox', font=('Calibri', 20))

organ_combobox = ttk.Combobox(
    window,
    values=ORGAN_CHOICES,
    state="readonly",
    font=("Calibri", 15),
    textvariable=selected_organ
)
organ_combobox.pack(pady=10)
organ_combobox.bind("<<ComboboxSelected>>", update_selected_organ)

# button for uploading image
btn_upload_img = tk.Button(
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
btn_upload_img.place(relx=0.5, rely=0.75, anchor="center")

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

# Label displaying chosen organ
analysis_label = tk.Label(
    window,
    font=("Calibri", 20),
    text="[Select Organ] Tomography Analysis",
    compound="center",
    fg="white",
    bg='black',
    bd=0,
    highlightbackground="white",
    highlightthickness=2,
)
analysis_label.pack(padx=20, pady=5)

window.mainloop()