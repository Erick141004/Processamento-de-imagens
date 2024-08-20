import PySimpleGUI as sg
from PIL import Image
import pathlib

from PySimpleGUI import popup


def convert_image(input_file_path, output_file_path):
    img = Image.open(input_file_path)
    img.save(output_file_path)
    original_suffix = pathlib.Path(input_file_path).suffix
    new_suffix = pathlib.Path(output_file_path).suffix
    return img

if __name__ == "__main__":
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open', '&Save', '---', 'Properties', 'E&xit'  ]],
                ['&Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
                ['&Help', ['&About...']]]

    # All the stuff inside your window.
    layout = [  [sg.Menu(menu_def)],
                [sg.Image(key="-IMAGE-")] ]

    # Create the Window
    window = sg.Window('Hello Example', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # if user closes window
        if event == sg.WIN_CLOSED:
            break
        elif event == "Open":
            image = sg.popup_get_file("", no_window=True)
            converted_image = convert_image(image)
            window["-IMAGE-"].update(data=converted_image)

        print('Hello', values[0], '!')

    window.close()
