# anti_idle_handler.py
import time
import keyboard
import random
from config import Config
import threading
import logging
import os


# Se o sistema for windows, usar o comando 'cls' para limpar a tela
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AntiIdleHandler:
    def __init__(self):
        self.config = Config()
        self.running = False
        self.thread = None
        self.action_timers = {
            'mudar_direcao': 0,
            'comer': 0,
            'hotkey': 0,
            'magia': 0
        }
        self.default_seconds = 15  # Valor padrão de 15 segundos

    def update_config(self, new_config):
        self.config = new_config
        self.action_timers = {action: 0 for action in self.action_timers}

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
            logging.info("AntiIdleHandler iniciado")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        logging.info("AntiIdleHandler parado")

    def _run(self):
        while self.running:
            self._check_and_perform_actions()
            if keyboard.is_pressed('insert'):
                self.running = False
            time.sleep(1)

    def _check_and_perform_actions(self):
        for action in self.action_timers:
            if self.config.get(action):
                self.action_timers[action] += 1
                max_seconds = self._get_action_seconds(action)
                logging.debug(f"Ação: {action}, Timer: {self.action_timers[action]}, Max: {max_seconds}")
                if self.action_timers[action] >= max_seconds:
                    self._perform_action(action)
                    self._reset_timer(action)

    def _get_action_seconds(self, action):
        try:
            # pega os segundos configurados na config.json
            seconds = self.config.get(f'seg_{action}')
            return int(seconds) if seconds is not None else self.default_seconds
        except ValueError:
            logging.warning(f"Valor inválido para seg_{action}. Usando valor padrão de {self.default_seconds} segundos.")
            return self.default_seconds

    def _perform_action(self, action):
        logging.info(f"Executando ação: {action}")
        if action == 'mudar_direcao':
            self.mudar_direcao()
        elif action == 'comer':
            self.comer()
        elif action == 'hotkey':
            self.usar_hotkey()
        elif action == 'magia':
            self.usar_magia()

    def _reset_timer(self, action):
        max_seconds = self._get_action_seconds(action)
        self.action_timers[action] = random.randint(1, max_seconds)
        logging.debug(f"Timer resetado para {action}: {self.action_timers[action]}")

    def mudar_direcao(self):
        direcao = ['ctrl+right', 'ctrl+left', 'ctrl+up', 'ctrl+down']
        escolhida = random.choice(direcao)
        logging.info(f"Mudando direção: {escolhida}")
        keyboard.press_and_release(escolhida)

    def comer(self):
        logging.info("Executando ação de comer")
        # Implementar lógica para comer
        # Por exemplo:
        # keyboard.press_and_release('f')

    def usar_hotkey(self):
        hotkey = self.config.get('select_hotkey')
        if hotkey:
            logging.info(f"Usando hotkey: {hotkey}")
            keyboard.press_and_release(hotkey)
        else:
            logging.warning("Nenhuma hotkey configurada")

    def usar_magia(self):
        magias = self.config.get('magias')
        if magias:
            magia_escolhida = random.choice(magias)
            logging.info(f"Usando magia: {magia_escolhida}")
            keyboard.press_and_release('enter')
            keyboard.write(magia_escolhida)
        else:
            logging.warning("Nenhuma magia configurada")