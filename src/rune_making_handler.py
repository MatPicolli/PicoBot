import pyautogui
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RuneMakingHandler:
    def __init__(self):
        self.running = False
        self.wait_time = 0.5
        
        # Verificar se o OpenCV está disponível
        try:
            import cv2
            self.use_opencv = True
            self.confidence = 0.5
        except ImportError:
            self.use_opencv = False
            logging.warning("OpenCV não está instalado. A detecção de imagens pode ser menos precisa.")

    def locate_image(self, image_name):
        try:
            if self.use_opencv:
                location = pyautogui.locateOnScreen(image_name, confidence=self.confidence)
            else:
                location = pyautogui.locateOnScreen(image_name)
            
            if location:
                return pyautogui.center(location)
            else:
                logging.warning(f"Imagem {image_name} não encontrada na tela.")
                return None
        except Exception as e:
            logging.error(f"Erro ao localizar imagem {image_name}: {str(e)}")
            return None

    def drag_and_drop(self, start_image, end_image):
        start_pos = self.locate_image(start_image)
        end_pos = self.locate_image(end_image)
        
        if start_pos and end_pos:
            pyautogui.moveTo(start_pos)
            pyautogui.mouseDown()
            pyautogui.moveTo(end_pos, duration=0.5)
            pyautogui.mouseUp()
            time.sleep(self.wait_time)
        else:
            logging.error(f"Não foi possível realizar o drag and drop de {start_image} para {end_image}")

    def type_spell(self, spell):
        pyautogui.press('enter')
        pyautogui.typewrite(spell)
        pyautogui.press('enter')
        time.sleep(self.wait_time)

    def make_rune(self):
        rune_pos = self.locate_image('imgs/1.png')
        if not rune_pos:
            logging.error("Runa inicial não encontrada. Abortando operação.")
            return False

        self.drag_and_drop('imgs/1.png', 'imgs/2.png')
        self.type_spell("adura vita")
        time.sleep(2)  # Ajuste este tempo conforme necessário

        blue_rune_pos = self.locate_image('imgs/3.png')
        if not blue_rune_pos:
            logging.error("Runa azul não encontrada após o feitiço. Algo deu errado.")
            return False

        self.drag_and_drop('imgs/3.png', rune_pos)
        logging.info("Runa criada com sucesso!")
        return True

    def run(self):
        self.running = True
        while self.running:
            if self.make_rune():
                logging.info("Aguardando para criar a próxima runa...")
                time.sleep(5)
            else:
                logging.error("Falha ao criar runa. Tentando novamente em 5 segundos...")
                time.sleep(5)

    def stop(self):
        self.running = False