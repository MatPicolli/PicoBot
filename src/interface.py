import FreeSimpleGUI as sg

# Definindo o tema e as cores
sg.theme('DarkBlue3')
BUTTON_COLOR = ('white', '#1E3F66')
INPUT_COLOR = ('#000000', '#FFFFFF')

def selecionar_modo():
    layout = [
        [sg.Text('Selecione o Modo', font=('Helvetica', 16), justification='center', size=(30, 1))],
        [sg.Button('Anti-Idle', key='-ANTIIDLE-', size=(15, 3), button_color=BUTTON_COLOR, font=('Helvetica', 12)),
         sg.Button('Rune Making', key='-RUNEMAKING-', size=(15, 3), button_color=BUTTON_COLOR, font=('Helvetica', 12))]
    ]

    janela = sg.Window('Anti-Idle Control', layout, element_justification='center')

    while True:
        evento, valores = janela.read()

        if evento == sg.WINDOW_CLOSED:
            break
        elif evento == '-ANTIIDLE-':
            janela.close()
            anti_idle()
            break
        elif evento == '-RUNEMAKING-':
            print('rune making')
            break

    janela.close()

def anti_idle():
    import anti_idle_handler

    layout = [
        [sg.Text('Configurações Anti-Idle', font=('Helvetica', 16), justification='center', size=(30, 1))],
        [sg.Frame('Opções', [
            [sg.Checkbox('Mudar direção', key='-MUDARDIRECAO-', font=('Helvetica', 10))],
            [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGMUDARDIRECAO-', font=('Helvetica', 10))],
            [sg.Checkbox('Comer', key='-COMER-', font=('Helvetica', 10))],
            [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGCOMER-', font=('Helvetica', 10))],
            [sg.Checkbox('Usar hotkey', key='-USARHOTKEY-', font=('Helvetica', 10))],
            [sg.Text('Hotkey:', size=(15,1)), sg.Input(size=(8,1), key='-SELECTHOTHEY-', font=('Helvetica', 10))],
            [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGHOTKEY-', font=('Helvetica', 10))],
            [sg.Checkbox('Usar magia', key='-USARMAGIA-', font=('Helvetica', 10))],
            [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGMAGIA-', font=('Helvetica', 10))],
        ], font=('Helvetica', 12))],
        [sg.Frame('Lista de Magias', [
            [sg.Multiline(key='-MAGIAS-', size=(30,6), font=('Helvetica', 10))]
        ], font=('Helvetica', 12))],
        [sg.Column([[sg.Button('START', key='-STARTPAUSE-', size=(15, 2), button_color=('white', '#4CAF50'), font=('Helvetica', 12, 'bold'))]], justification='center')]
    ]

    janela = sg.Window('Anti-Idle Control', layout, element_justification='center')

    anti_idle_running = False
    while True:
        evento, valores = janela.read()

        if evento == sg.WINDOW_CLOSED:
            break

        if evento == '-STARTPAUSE-':
            anti_idle_running = not anti_idle_running
            janela['-STARTPAUSE-'].update('PAUSE' if anti_idle_running else 'START', 
                                          button_color=('white', '#F44336' if anti_idle_running else '#4CAF50'))
            print('anti-idle running:', anti_idle_running)

        if anti_idle_running:
            # passa por parametro todos os valores
            anti_idle_handler.start(valores['-MUDARDIRECAO-','-SEGMUDARDIRECAO-','-COMER-',
                                            '-SEGCOMER-','-USARHOTKEY-','-SELECTHOTHEY-',
                                            '-SEGHOTKEY-','-USARMAGIA-','-SEGMAGIA-','-MAGIAS-'])

    janela.close()

if __name__ == "__main__":
    selecionar_modo()