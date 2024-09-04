import PySimpleGUI as sg
from PIL import Image, ExifTags, ImageFilter
from PIL.TiffTags import TAGS
import io
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
# import requests

image_atual = None
image_path = None
max_width = 800
max_height = 600
previous_state = None
start_x = 0
start_y = 0
end_x = 0 
end_y = 0
selecting = False
width_reduction = 0
height_reduction = 0
new_width = 0
new_height = 0

def resize_image(img):
    global max_width
    global max_height
    global width_reduction
    global height_reduction
    global new_width
    global new_height

    try:
        width, height = img.size
        aspect_ratio = width / height

        new_width = max_width
        new_height = int(max_width / aspect_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        new_height = max_height
        new_width = int(max_height * aspect_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        width_reduction = width/new_width
        height_reduction = height/new_height
        
        print(f"WIDHT REAL: {width}")
        print(f"HEIGHT REAL: {height}")
        print(f"WIDHT NOVO: {new_width}")
        print(f"HEIGHT NOVO: {new_height}")

        print(f"WIDTH REDUCTION: {width_reduction}")
        print(f"HEIGHT REDUCTION: {height_reduction}")

        return img
    except Exception as e:
        print(f"ERRO ao rendimencionar a imagem: {str(e)}") 
    
def url_download(url):
    global image_atual
    global previous_state
    # try:
    #     #r = requests.get(url, stream=True)
    #     if r.status_code == 200:
    #         previous_state = image_atual.copy()
    #         image_atual = Image.open(io.BytesIO(r.content))
    #         show_image()
    #     else:
    #         sg.popup("Falha ao baixar a imagem. Verifique a URL e tente novamente.")
    # except Exception as e:
    #     sg.popup(f"Erro ao baixar a imagem: {str(e)}")

def open_image(filename):
    global image_atual
    global image_path

    image_path = filename
    image_atual = Image.open(filename)   
    
    #Converte a image PIL para o formato que o PySimpleGUI
    show_image()

def show_image():
    global image_atual
    try:
        resized_img = resize_image(image_atual)
        #Converte a image PIL para o formato que o PySimpleGUI
        img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memÃ³ria RAM
        resized_img.save(img_bytes, format='PNG')
        window['-IMAGE-'].draw_image(data=img_bytes.getvalue(), location=(0,400))
    except Exception as e:
        sg.popup(f"Erro ao exibir a imagem: {str(e)}")


# def show_image(img):
#     resized_img = resize_image(img)
#     img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memória RAM
#     resized_img.save(img_bytes, format='PNG')
#     window['-IMAGE-'].update(data=img_bytes.getvalue())

def apply_grayScale_filter():
    global image_atual
    global image_path

    try: 
        if image_atual:
            width, height = image_atual.size
            pixels = image_atual.load()
            previous_state = image_atual.copy()

            for w in range(width):
                for h in range(height):
                    r, g, b = image_atual.getpixel((w, h))
                    gray = int(0.3 * r + 0.6 + g + 0.1 * b)
                    pixels[w,h] = (gray, gray, gray)

            show_image(image_atual)
        else: 
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        print(f"ERRO ao aplicar o cinza na imagem: {str(e)}")

def rotate_image(degrees):
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.rotate(degrees, expand=True)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao girar a imagem: {str(e)}")

def apply_sepia_filter():
    global image_atual
    global image_path

    try: 
        if image_atual:
            width, height = image_atual.size
            pixels = image_atual.load()
            previous_state = image_atual.copy()

            for w in range(width):
                for h in range(height):
                    r, g, b = image_atual.getpixel((w, h))
                    gray = int(0.3 * r + 0.6 + g + 0.1 * b)
                    pixels[w,h] = (255 if(gray + 100 > 255) else gray + 100,
                                    255 if(gray + 50 > 255) else gray + 50, 
                                    gray)

            show_image(image_atual)
        else: 
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        print(f"ERRO ao aplicar o sepia na imagem: {str(e)}")

def apply_inversion_filter():
    global image_atual
    global image_path

    try: 
        if image_atual:
            width, height = image_atual.size
            pixels = image_atual.load()
            previous_state = image_atual.copy()

            for w in range(width):
                for h in range(height):
                    r, g, b = image_atual.getpixel((w, h))
                    r = 255 - r
                    g = 255 - g
                    b = 255 - b

                    pixels[w, h] = (r, g, b)

            show_image(image_atual)
        else: 
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        print(f"ERRO ao aplicar o filtro invertido na imagem: {str(e)}")

def apply_four_bits_filter():
    global image_atual
    global previous_state

    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.convert("P", palette="Image.ADAPTIVE", colors=4)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta")
    except Exception as e:
        print(f"ERRO ao aplicar o filtro na imagem: {str(e)}")

def undo():
    global image_atual
    global previous_state


def apply_blur_filter():
    global image_atual
    global previous_state

    radius = sg.popup_get_text("Digite um valor numerio para aplicar o Blur (0 a 20)", default_text="2")
    try:
        radius = int(radius)
        radius = max(0, min(20, radius))
    except ValueError:
        sg.popup("Por favor, insira um valor numérico válido.")
        return

    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.GaussianBlur(radius))
            show_image(image_atual)
        else:
            sg.popup("Nenhuma imagem aberta")
    except Exception as e:
        print(f"ERRO ao aplicar o blur na imagem: {str(e)}")

def apply_contour_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.CONTOUR)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de contorno: {str(e)}")

def apply_detail_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.DETAIL)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de detalhe: {str(e)}")

def apply_edge_enhance_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.EDGE_ENHANCE)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de realce de bordas: {str(e)}")

def apply_emboss_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.EMBOSS)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de relevo: {str(e)}")

def apply_find_edges_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.FIND_EDGES)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de detectar bordas: {str(e)}")

def apply_sharpen_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.SHARPEN)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de nitidez: {str(e)}")

def apply_smooth_filter():
    global image_atual
    global previous_state
    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.SMOOTH)
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro de suavizar: {str(e)}")

def apply_minfilter_filter():
    global image_atual
    global previous_state

    size = sg.popup_get_text("Digite a quantidade de filtro (3 a 20):", default_text="3")
    try:
        size = int(size)
        size = max(3, min(20, size))
    except ValueError:
        sg.popup("Por favor, insira um valor numérico válido.")
        return

    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.MinFilter(size=size))
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro mínimo: {str(e)}")

def apply_maxfilter_filter():
    global image_atual
    global previous_state

    size = sg.popup_get_text("Digite a quantidade de filtro (3 a 20):", default_text="3")
    try:
        size = int(size)
        size = max(3, min(20, size))
    except ValueError:
        sg.popup("Por favor, insira um valor numérico válido.")
        return

    try:
        if image_atual:
            previous_state = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.MaxFilter(size=size))
            show_image()
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao aplicar o filtro máximo: {str(e)}")


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
        if(ExifTags.TAGS[tag]):
            valor += f"{ExifTags.TAGS[tag]} - {value}\n"
        else:
            print(f"Essa tag não existe: {tag}")
    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    gps_values = get_gps_information(gps_ifd)

    valor += webbrowser.open(f"\nhttps://www.google.com.br/maps/place/{gps_values[0]},{gps_values[1]}")
    sg.popup(valor)

def calculate_histogram(image):
    if image.mode != 'L':
        image = image.convert('L')
    histogram = image.histogram()
    
    return histogram

def show_histogram(image):
    histogram = calculate_histogram(image)
    
    layout = [
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Fechar')]
    ]
    
    window = sg.Window('Histograma', layout, finalize=True)
    
    fig, ax = plt.subplots()
    ax.hist(range(256), bins=256, weights=histogram)
    
    canvas_elem = window['-CANVAS-']
    canvas = FigureCanvasTkAgg(fig, canvas_elem.Widget)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

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

def crop_selected_area():
    global start_x, start_y
    global end_x, end_y
    global width_reduction
    global height_reduction
    global image_atual
    global new_width

    print(start_x)
    print(start_y)
    print(end_x)
    print(end_y)    

    x1 = start_x * new_width
    print(x1)

    x1_real_image = int(start_x * width_reduction)
    x2_real_image = int(end_x * width_reduction)
    y1_real_image = int(start_y * height_reduction)
    y2_real_image = int(end_y * height_reduction)

    print(f"X1: {x1_real_image} - X2: {x2_real_image} --- Y1: {y1_real_image} - Y2: {y2_real_image}")       

    if x1_real_image > x2_real_image:
        x1_real_image, x2_real_image = x2_real_image, x1_real_image

    if y1_real_image > y2_real_image:
        y1_real_image, y2_real_image = y2_real_image, y1_real_image

    image_atual = image_atual.crop((x1_real_image, y1_real_image, x2_real_image, y2_real_image))     
    show_image()

layout = [
    [sg.Menu([
            ['Arquivo', ['Abrir', 'Abrir URL', 'Salvar', 'Fechar']],
            ['Editar', ['Desfazer']],
            ['Imagem', [
                'Girar', ['Girar 90 graus à direita', 'Girar 90 graus à esquerda'], 
                'Filtro', ['Preto e Branco', 'Sépia', 'Negativo', '4 bits', 
                           'Blur', 'Contorno', 'Detalhe', 'Realce de bordas',
                           'Relevo', 'Detectar bordas', 'Nitidez', 'Suavizar',
                           'Filtro mínimo', 'Filtro máximo']
            ]],
            ['EXIF', ['Mostrar dados da imagem', 'Mostrar dados de GPS']], 
            ['Sobre a image', ['Informacoes']], 
            ['Sobre', ['Desenvolvedor']]
        ])],
    [sg.Graph(key='-IMAGE-', canvas_size=(800, 600), change_submits=True, drag_submits=True, graph_bottom_left=(0,0), graph_top_right=(400, 400))],
]

window = sg.Window('Photo Shoping', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Abrir URL':
        url = sg.popup_get_text("Digite a url")
        if url:
            url_download(url)
    elif event == 'Desfazer':
        undo()
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Informacoes':
        info_image()
    elif event == 'Mostrar dados da imagem':
        info_image_property()
    elif event == 'Mostrar dados de GPS':
        print("Dados de GPS")
        # gps_data()
    elif event == 'Girar 90 graus à direita':
        rotate_image(-90)
    elif event == 'Girar 90 graus à esquerda':
        rotate_image(90)
    elif event == 'Preto e Branco':
        apply_grayScale_filter()
    elif event == 'Sépia':
        apply_sepia_filter()
    elif event == 'Negativo':
        apply_inversion_filter()
    elif event == '4 bits':
        apply_four_bits_filter()
    elif event == 'Blur':
        apply_blur_filter()
    elif event == 'Contorno':
        apply_contour_filter()
    elif event == 'Detalhe':
        apply_detail_filter()
    elif event == 'Realce de bordas':
        apply_edge_enhance_filter()
    elif event == 'Relevo':
        apply_emboss_filter()
    elif event == 'Detectar bordas':
        apply_find_edges_filter()
    elif event == 'Nitidez':
        apply_sharpen_filter()
    elif event == 'Suavizar':
        apply_smooth_filter()
    elif event == 'Filtro mínimo':
        apply_minfilter_filter()
    elif event == 'Filtro máximo':
        apply_maxfilter_filter()
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por Erick - BCC 6º Semestre')
    elif event.startswith('-IMAGE-'):
        if '-IMAGE-' in values and values['-IMAGE-'] is not None:
            if event.endswith('-IMAGE-+UP'):
                selecting = False
                end_x, end_y = values['-IMAGE-']
                end_y = 400 - end_y
                crop_selected_area()
            elif not selecting:
                selecting = True
                start_x, start_y = values['-IMAGE-']
                start_y = 400 - start_y

window.close()