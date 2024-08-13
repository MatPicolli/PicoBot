# config.py
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    def __init__(self):
        self.default_config = {
            'mudar_direcao': False,
            'seg_mudar_direcao': 60,
            'comer': False,
            'seg_comer': 60,
            'hotkey': False,
            'select_hotkey': '',
            'seg_hotkey': 60,
            'magia': False,
            'seg_magia': 60,
            'magias': []
        }
        self.config = self.default_config.copy()

    def load(self, filename='config.json'):
        try:
            with open(filename, 'r') as f:
                loaded_config = json.load(f)
                # Update default config with loaded values
                self.config.update(loaded_config)
                logging.info(f"Configuração carregada: {self.config}")
        except FileNotFoundError:
            logging.warning(f"Arquivo de configuração '{filename}' não encontrado. Usando configurações padrão.")
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar o arquivo '{filename}'. Usando configurações padrão.")

    def save(self, filename='config.json'):
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=4)
        logging.info(f"Configuração salva: {self.config}")

    def get(self, key):
        value = self.config.get(key)
        logging.debug(f"Obtendo configuração: {key} = {value}")
        return value

    def set(self, key, value):
        self.config[key] = value
        logging.debug(f"Definindo configuração: {key} = {value}")