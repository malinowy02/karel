import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Obecna pozycja robota')],
            [sg.Text('B'), sg.Text(size=(40,1), key='X')],
            [sg.Text('Y'), sg.Text(size=(40,1), key='Y')],
            [sg.Text('Z'), sg.Text(size=(40,1), key='Z')],
            [sg.Text('Docelowa pozycja')],
            [sg.Text('X'), sg.InputText()],
            [sg.Text('Y'), sg.InputText()],
            [sg.Text('Z'), sg.InputText()],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Quit')] ]

# Create the Window
window = sg.Window('Fanuc TCP', layout)
# Event Loop to process "events" and get the "values" of the inputs


while True:
    event, values = window.read()
    window['X'].update(0)
    window['Y'].update(0)
    window['Z'].update(0)
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
        break
    # print('You entered ', values[0])

window.close()