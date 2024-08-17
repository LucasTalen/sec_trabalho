from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import qrcode
import os


def generate_qr_code_with_transparent_background(cpf, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=25,
        border=1,
    )
    qr.add_data(cpf)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img_data = img.getdata()
    new_image_data = []
    for item in img_data:
        if item[:3] == (255, 255, 255):
            new_image_data.append((255, 255, 255, 0))
        else:
            new_image_data.append(item)
    img.putdata(new_image_data)
    img.save(filename, format="PNG")

def create_badge_front(background_path, image_path, name, matricula, cargo, cpf):
    background = Image.open(background_path)
    photo = Image.open(image_path).resize((550, 550))
    draw = ImageDraw.Draw(background)
    background.paste(photo, (475, 640))
    font = ImageFont.truetype("arial.ttf", 65)
    draw.text((150, 1300), f"Nome: {name}", fill="gray", font=font)
    draw.text((150, 1450), f"Matrícula: {matricula}", fill="gray", font=font)
    draw.text((150, 1600), f"CPF: {cpf}", fill="gray", font=font)
    draw.text((150, 1750), f"Cargo: {cargo}", fill="gray", font=font)
    return background

def create_badge_back(background_path, image_path):
    background = Image.open(background_path).convert("RGBA")
    photo = Image.open(image_path).resize((800, 800)).convert("RGBA")
    

    draw = ImageDraw.Draw(background)
    background.paste(photo, (320, 950), photo)
    


    return background

def generate_pdf(badges, output_pdf, front_background_path, back_background_path):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4
    x = 50
    y = height - 450

    
    # Criar QR Code
    qr_code_path = f"qr_code.png"
    print(badges['cpf'])
    generate_qr_code_with_transparent_background(badges['cpf'], qr_code_path)
    
    # Criar frente do crachá
    front_badge_path = f"badge_front_{badges['matricula']}.png"
    front_badge_image = create_badge_front(front_background_path, badges['image_path'], badges['name'], badges['matricula'], badges['cargo'], badges['cpf'])
    front_badge_image.save(front_badge_path)
    
    # Criar verso do crachá
    back_badge_path = f"badge_back_{badges['matricula']}.png"
    back_badge_image = create_badge_back(back_background_path, badges['qrcode'])
    back_badge_image.save(back_badge_path)
    
    # Adicionar frente e verso ao PDF
    c.drawImage(front_badge_path, x, y, width=300, height=400)
    y -= 450
    if y < 50:
        c.showPage()
        y = height - 450
    
    c.drawImage(back_badge_path, x, y, width=300, height=400)
    y -= 450
    if y < 50:
        c.showPage()
        y = height - 450

    c.save()
    
    os.remove(back_badge_path)
    os.remove(front_badge_path)
    os.remove(qr_code_path)
    




# badges_info = [
#     {"image_path": "foto1.jpg", "qrcode":"qr_code.png", "name": "Yan Vaz", "matricula": "087654", "cargo":"Operador de Empilhadeira", "cpf":"000.000.000-00"},
# ]

front_background_path = "./site_sec/utils/cracha/1.png"
back_background_path = "./site_sec/utils/cracha/2.png"

