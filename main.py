from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image
from gtts import gTTS
from pytesseract import image_to_string
import os
import playsound

class ImageToSoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sound Converter")
        self.root.geometry("600x400")

        self.label = Label(root, text="Select an image to convert:")
        self.label.pack(pady=10)

        self.browse_button = Button(root, text="Browse Image", command=self.load_image)
        self.browse_button.pack(pady=5)

        self.text_display = ScrolledText(root, width=70, height=10)
        self.text_display.pack(pady=10)

        self.convert_button = Button(root, text="Convert to Sound", command=self.convert_to_sound)
        self.convert_button.pack(pady=5)

        self.play_button = Button(root, text="Play Sound", command=self.play_sound)
        self.play_button.pack(pady=5)
        
        self.image_path = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if self.image_path:
            self.extract_text()

    def extract_text(self):
        try:
            loaded_image = Image.open(self.image_path)
            decoded_text = image_to_string(loaded_image)
            cleaned_text = " ".join(decoded_text.split("\n"))
            self.text_display.delete(1.0, "end")
            self.text_display.insert("insert", cleaned_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")

    def convert_to_sound(self):
        try:
            text = self.text_display.get(1.0, "end").strip()
            if not text:
                messagebox.showwarning("Warning", "No text to convert")
                return

            sound = gTTS(text, lang="en")
            sound.save("sound.mp3")
            messagebox.showinfo("Success", "Sound saved successfully as 'sound.mp3'")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating sound: {str(e)}")

    def play_sound(self):
        if os.path.exists("sound.mp3"):
            playsound.playsound("sound.mp3")
        else:
            messagebox.showwarning("Warning", "No sound file found. Please convert an image first.")


if __name__ == "__main__":
    root = Tk()
    app = ImageToSoundApp(root)
    root.mainloop()
