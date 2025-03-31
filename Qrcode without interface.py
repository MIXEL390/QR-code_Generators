import qrcode

def generate_qr(data, filename="qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="green", back_color="blue")
    img.save(filename)
    print(f"QR-code saved as {filename}")

if __name__ == "__main__":
    text = input("Write the text or url:       ") # https://github.com/MIXEL390
    generate_qr(text)