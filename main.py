import PySimpleGUI as sg
from PIL import Image
from PIL import ExifTags
from PIL.TiffTags import TAGS
import io
import webbrowser
import os

image_atual = None
image_path = None

def resize_image(img):
    img = img.resize((800, 600), Image.Resampling.LANCZOS) 
    return img

def open_image(filename):
    global image_atual
    global image_path
    image_path = filename
    image_atual = Image.open(filename)    
    
    resized_img = resize_image(image_atual)
    #Converte a image PIL para o formato que o PySimpleGUI
    img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memória RAM
    resized_img.save(img_bytes, format='PNG')
    window['-IMAGE-'].update(data=img_bytes.getvalue())

def save_image(filename):
    global image_atual
    if image_atual:
        with open(filename, 'wb') as file:
            image_atual.save(file)

def info_image():
    global image_atual
    global image_path
    if image_atual:
        largura, altura = image_atual.size
        formato = image_atual.format
        tamanho_bytes = os.path.getsize(image_path)
        tamanho_mb = tamanho_bytes / (1024 * 1024)
        sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")

def info_image_property():
    global image_atual
    global image_path
    
    #layout_popup = [[sg.Button()]]

    exif = image_atual.getexif()
    valor = ""

    for tag, value in exif.items():
        valor += f"{ExifTags.TAGS[tag]} - {value}\n"

    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    gps_values = get_gps_information(gps_ifd)

    valor += webbrowser.open(f"\nhttps://www.google.com.br/maps/place/{gps_values[0]},{gps_values[1]}")
    sg.popup(valor)

def get_gps_information(valor):
    directionLat = valor[1]
    coordinatesLat = valor[2]
    directionLong = valor[3]
    coordinatesLong  = valor[4]

    sumLat = float(coordinatesLat[0]) + (float(coordinatesLat[1])/60) + (float(coordinatesLat[2])/3600) 
    sumLong = float(coordinatesLong[0]) + (float(coordinatesLong[1])/60) + (float(coordinatesLong[2])/3600) 

    if directionLat == "N":
        sumLat *= 1
    elif directionLat == "S":
        sumLat *= -1

    if directionLong == "W":
        sumLong *= -1
    elif directionLong == "E":
        sumLong *= 1   

    return [sumLat, sumLong]
                

layout = [
    [sg.Menu([
            ['Arquivo', ['Abrir', 'Salvar', 'Fechar']],
            ['Sobre a image', ['Informacoes', '---','Informacoes Especiais']], 
            ['Sobre', ['Desenvolvedor']]
        ])],
    [sg.Image(key='-IMAGE-', size=(800, 600))],
]

window = sg.Window('Aplicativo de image', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Informacoes':
        info_image()
    elif event == 'Informacoes Especiais':
        info_image_property()
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por [Seu Nome] - BCC 6º Semestre')


window. Close()