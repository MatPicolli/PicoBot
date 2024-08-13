# interface.py
import FreeSimpleGUI as sg
from anti_idle_handler import AntiIdleHandler
from config import Config
import os

class Interface:
    def __init__(self):
        #self.config = Config()
        #self.anti_idle_handler = AntiIdleHandler()
        sg.theme('DarkBlue3')
        self.BUTTON_COLOR = ('white', '#1E3F66')
        self.INPUT_COLOR = ('#000000', '#FFFFFF')

    def selecionar_modo(self):
        layout = [
            [sg.Text('Selecione o Modo', font=('Helvetica', 16), justification='center', size=(30, 1))],
            [sg.Button('Anti-Idle', key='-ANTIIDLE-', size=(15, 3), button_color=self.BUTTON_COLOR, font=('Helvetica', 12)),
             sg.Button('Rune Making', key='-RUNEMAKING-', size=(15, 3), button_color=self.BUTTON_COLOR, font=('Helvetica', 12))]
        ]

        window = sg.Window('Anti-Idle Control', layout, element_justification='center')

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-ANTIIDLE-':
                window.close()
                self.anti_idle()
                break
            elif event == '-RUNEMAKING-':
                print('rune making')
                break

        window.close()

    def anti_idle(self):
        self.config = Config()
        self.anti_idle_handler = AntiIdleHandler()

        layout = None

        # se config.json existir e não estiver vazio, carregar as configurações diretamente no layout.
        if os.path.exists('config.json') and os.path.getsize('config.json') > 0:
            self.config.load('config.json')

            layout = [
                [sg.Text('Configurações Anti-Idle', font=('Helvetica', 16), justification='center', size=(30, 1))],
                [sg.Frame('Opções', [
                    [sg.Checkbox('Mudar direção', key='-MUDARDIRECAO-', font=('Helvetica', 10), default=self.config.get('mudar_direcao'))],
                    [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGMUDARDIRECAO-', font=('Helvetica', 10), default_text=self.config.get('seg_mudar_direcao'))],
                    [sg.Checkbox('Comer', key='-COMER-', font=('Helvetica', 10), default=self.config.get('comer'))],
                    [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGCOMER-', font=('Helvetica', 10), default_text=self.config.get('seg_comer'))],
                    [sg.Checkbox('Usar hotkey', key='-USARHOTKEY-', font=('Helvetica', 10), default=self.config.get('usar_hotkey'))],
                    [sg.Text('Hotkey:', size=(15,1)), sg.Input(size=(8,1), key='-SELECTHOTKEY-', font=('Helvetica', 10), default_text=self.config.get('select_hotkey'))],
                    [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGHOTKEY-', font=('Helvetica', 10), default_text=self.config.get('seg_hotkey'))],
                    [sg.Checkbox('Usar magia', key='-USARMAGIA-', font=('Helvetica', 10), default=self.config.get('usar_magia'))],
                    [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGMAGIA-', font=('Helvetica', 10), default_text=self.config.get('seg_magia'))],
                ], font=('Helvetica', 12))],
                    [sg.Multiline(key='-MAGIAS-', font=('Helvetica', 10), size=(30, 5), default_text='\n'.join(self.config.get('magias')))],
                [sg.Column([[sg.Button('START', key='-STARTPAUSE-', size=(15, 2), button_color=('white', '#4CAF50'), font=('Helvetica', 12, 'bold'))]], justification='center')]
            ]

        else:
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

        window = sg.Window('Anti-Idle Control', layout, element_justification='center')

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                if self.anti_idle_handler.running:
                    self.anti_idle_handler.stop()
                break

            if event == '-STARTPAUSE-':
                if not self.anti_idle_handler.running:
                    self.config.load('config.json')
                    self.update_config(values)   
                    self.anti_idle_handler.start()
                    window['-STARTPAUSE-'].update('PAUSE', button_color=('white', '#F44336'))
                else:
                    self.anti_idle_handler.stop()
                    window['-STARTPAUSE-'].update('START', button_color=('white', '#4CAF50'))

        window.close()

    def update_config(self, values):
        try:
            self.config.set('mudar_direcao', values['-MUDARDIRECAO-'])
            self.config.set('seg_mudar_direcao', values['-SEGMUDARDIRECAO-'])
            self.config.set('comer', values['-COMER-'])
            self.config.set('seg_comer', values['-SEGCOMER-'])
            self.config.set('hotkey', values['-USARHOTKEY-'])
            self.config.set('select_hotkey', values['-SELECTHOTHEY-'])
            self.config.set('seg_hotkey', values['-SEGHOTKEY-'])
            self.config.set('magia', values['-USARMAGIA-'])
            self.config.set('seg_magia', values['-SEGMAGIA-'])
            self.config.set('magias', values['-MAGIAS-'].split('\n'))
            self.config.save()
        except Exception as e:
            print(e)