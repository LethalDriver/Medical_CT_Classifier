import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import PhotoImage
from PIL import ImageTk, Image
import base64

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
ORGAN_CHOICES = ["Liver", "MAYBE OTHERS"]

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
    original_image = Image.open(file_path)
    resized_image = original_image.resize((400, 400), Image.BICUBIC)
    img = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(window, background="#050505", image=img)
    image_label.image = img
    image_label.pack(padx=50, pady=50)


def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image:
        encoded_image = base64.b64encode(image.read())
    return encoded_image.decode('utf-8')


def send_analyze_request(file_path):
    try:
        encoded_image = encode_image_to_base64(file_path)
        print("Encoded Image:", encoded_image)
        # SIMULATE SENDING HTTP REQUEST

        # SIMULATE RECEIVING THE RESPONSE
        http_response = "Successfully received HTTP response"

        if "Successfully received HTTP response" in http_response:
            show_diagnosis_window()
    except Exception as e:
        print(f"Error sending analyze request: {e}")


def get_analyze_result():
    # GET THE PROBABILITY RESULTS FROM HTTPS
    return 0.85  # placeholder


def show_diagnosis_window():
    if file_path:
        probability_result = get_analyze_result()

        diagnosis_window = tk.Toplevel()
        diagnosis_window.title("Diagnosis")
        diagnosis_window.geometry("400x400")
        diagnosis_window.resizable(False, False)
        diagnosis_window.config(background="#BBBBBB")

        diagnosis_label = tk.Label(
            diagnosis_window,
            text=f"Diagnosis: Temporary text",
            font=("Calibri", 16),
            background="#BBBBBB"
        )
        diagnosis_label.pack(pady=20)

        probability_label = tk.Label(
            diagnosis_window,
            text=f"Probability: {probability_result:.2f}",
            font=("Calibri", 16),
            background="#BBBBBB"
        )
        probability_label.pack(pady=20)


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
    command=lambda: send_analyze_request(file_path)
)
btn_analyze_img.place(relx=0.5, rely=0.9, anchor="center")

window.mainloop()
