# interface.py
import FreeSimpleGUI as sg
from anti_idle_handler import AntiIdleHandler
from config import Config
import os

class Interface:
    def __init__(self):
        self.config = Config()
        self.anti_idle_handler = None  # Inicialize como None
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
        self.config.load('config.json')
        self.anti_idle_handler = AntiIdleHandler()  # Inicialize aqui

        layout = [
            [sg.Text('Configurações Anti-Idle', font=('Helvetica', 16), justification='center', size=(30, 1))],
            [sg.Frame('Opções', [
                [sg.Checkbox('Mudar direção', key='-MUDARDIRECAO-', font=('Helvetica', 10), default=self.config.get('mudar_direcao'))],
                [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGMUDARDIRECAO-', font=('Helvetica', 10), default_text=self.config.get('seg_mudar_direcao'))],
                [sg.Checkbox('Comer', key='-COMER-', font=('Helvetica', 10), default=self.config.get('comer'))],
                [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGCOMER-', font=('Helvetica', 10), default_text=self.config.get('seg_comer'))],
                [sg.Checkbox('Usar hotkey', key='-USARHOTKEY-', font=('Helvetica', 10), default=self.config.get('hotkey'))],
                [sg.Text('Hotkey:', size=(15,1)), sg.Input(size=(8,1), key='-SELECTHOTKEY-', font=('Helvetica', 10), default_text=self.config.get('select_hotkey'))],
                [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGHOTKEY-', font=('Helvetica', 10), default_text=self.config.get('seg_hotkey'))],
                [sg.Checkbox('Usar magia', key='-USARMAGIA-', font=('Helvetica', 10), default=self.config.get('magia'))],
                [sg.Text('Segundos:', size=(15,1)), sg.Input(size=(8,1), key='-SEGMAGIA-', font=('Helvetica', 10), default_text=self.config.get('seg_magia'))],
            ], font=('Helvetica', 12))],
            [sg.Multiline(key='-MAGIAS-', font=('Helvetica', 10), size=(30, 5), default_text='\n'.join(self.config.get('magias')))],
            [sg.Column([[sg.Button('START', key='-STARTPAUSE-', size=(15, 2), button_color=('white', '#4CAF50'), font=('Helvetica', 12, 'bold'))]], justification='center')]
        ]

        window = sg.Window('Anti-Idle Control', layout, element_justification='center')

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                if self.anti_idle_handler and self.anti_idle_handler.running:
                    self.anti_idle_handler.stop()
                break

            if event == '-STARTPAUSE-':
                if not self.anti_idle_handler.running:
                    self.save_and_apply_config(values)
                    self.anti_idle_handler.start()
                    window['-STARTPAUSE-'].update('PAUSE', button_color=('white', '#F44336'))
                else:
                    self.anti_idle_handler.stop()
                    window['-STARTPAUSE-'].update('START', button_color=('white', '#4CAF50'))

        window.close()

    def save_and_apply_config(self, values):
        try:
            self.config.set('mudar_direcao', values['-MUDARDIRECAO-'])
            self.config.set('seg_mudar_direcao', int(values['-SEGMUDARDIRECAO-']))
            self.config.set('comer', values['-COMER-'])
            self.config.set('seg_comer', int(values['-SEGCOMER-']))
            self.config.set('hotkey', values['-USARHOTKEY-'])
            self.config.set('select_hotkey', values['-SELECTHOTKEY-'])
            self.config.set('seg_hotkey', int(values['-SEGHOTKEY-']))
            self.config.set('magia', values['-USARMAGIA-'])
            self.config.set('seg_magia', int(values['-SEGMAGIA-']))
            self.config.set('magias', [m.strip() for m in values['-MAGIAS-'].split('\n') if m.strip()])
            self.config.save()

            # Apply the new configuration to the AntiIdleHandler
            self.anti_idle_handler.update_config(self.config)
        except ValueError as e:
            sg.popup_error(f"Erro ao salvar configurações: Certifique-se de que todos os valores de segundos sejam números inteiros.")
        except Exception as e:
            sg.popup_error(f"Erro ao salvar configurações: {str(e)}")