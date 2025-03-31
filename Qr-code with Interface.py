import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk

class QRGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Main window
        self.title("QR_CODE GENERATOR")
        self.geometry("600x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.logo_image = None
        self.qr_image = None

        self.selected_color = "black"

        self.create_widgets()

    def create_widgets(self):
        # Add info
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=20, padx=20, fill="x")
        
        self.label = ctk.CTkLabel(self.input_frame, text="Add a text or URL:")
        self.label.pack(anchor="w", padx=10, pady=5)
        
        self.entry = ctk.CTkEntry(self.input_frame, width=400)
        self.entry.pack(pady=5, padx=10, fill="x")
        
        # Settings
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=10, padx=20, fill="x")
        
        self.color_label = ctk.CTkLabel(self.settings_frame, text="Qr-code color:")
        self.color_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.color_picker = ctk.CTkButton(
            self.settings_frame, 
            text="Choose", 
            width=80, 
            command=self.choose_color
        )
        self.color_picker.grid(row=0, column=1, padx=5, pady=5)
        
        self.logo_btn = ctk.CTkButton(
            self.settings_frame, 
            text="Add logo?", 
            command=self.add_logo
        )
        self.logo_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Check
        self.preview_label = ctk.CTkLabel(self, text="QuikCheck:")
        self.preview_label.pack(pady=10)
        
        self.preview_canvas = tk.Canvas(self, width=200, height=200, bg="white")
        self.preview_canvas.pack()
        
        # Gen button
        self.generate_btn = ctk.CTkButton(
            self, 
            text="Generate QR-code", 
            command=self.generate_qr
        )
        self.generate_btn.pack(pady=20)

    def choose_color(self):
        color = ctk.CTkInputDialog(
            text="Enter color (hex or name):", 
            title="Color Selection"
        ).get_input()
        if color:
            self.selected_color = color
            self.color_picker.configure(fg_color=color)

    def add_logo(self):
        logo_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if logo_path:
            self.logo_image = Image.open(logo_path)
            messagebox.showinfo("Logo", "Logo succesfully added!")

    def generate_qr(self):
        data = self.entry.get()
        if not data:
            messagebox.showerror("Error", "Please enter text or URL!")
            return

        try:
            qr = qrcode.QRCode(
                version=4,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=4
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Use stored color
            img = qr.make_image(
                fill_color=self.selected_color, 
                back_color="white"
            ).convert('RGB')
            
            
            self.show_preview(img)
            self.save_qr()
            
        except Exception as e:
            messagebox.showerror("Error", f"Generation failed: {str(e)}")

        try:
            self.qr_image = img
            self.show_preview(img)
            self.save_qr()
        except:
            self.qr_image = None

    def show_preview(self, img):
        preview_img = img.resize((200, 200))
        self.tk_image = ImageTk.PhotoImage(preview_img)
        self.preview_canvas.create_image(
            100, 100, anchor=tk.CENTER, image=self.tk_image
        )

    def save_qr(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        if file_path:
            self.qr_image.save(file_path)
            messagebox.showinfo("Congrats", f"QR-code saved as:\n{file_path}")

if __name__ == "__main__":
    app = QRGeneratorApp()
    app.mainloop()
