import sys

from PIL import Image, ImageDraw, ImageFont

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from contextlib import redirect_stdout
from pathlib import Path 

from sympy import preview
from ru_word2number import w2n

import speech_recognition as sr
import pyaudio


command_dispatcher = {
    'разделить' : '/',
    'умножить' : '*', 
    'плюс' : '+',
    'минус' : '-',
    'степень' : '**',
    'начало' : '(',
    'конец' : ')'
}

symbol_dispatcher = {
     '/' : 'разделить',
     '*' : 'умножить', 
     '+' : 'плюс',
     '-' : 'минус',
     '**' : 'степень',
     '(' : 'начало',
     ')' : 'конец',
     '_' : ' '
}

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.setWindowTitle('Расчёт выражения')
        loadUi(self.UI_PATH, self)
        
        self.okButton.clicked.connect(lambda: self.get_expression_and_result('text'))
        self.voiceButton.clicked.connect(lambda: self.get_expression_and_result('voice'))        

        self.calculation_path = str(Path(__file__).parent / "calc.png")
        self.expression_path = str(Path(__file__).parent / "expression.png")
        
    def show_error_window(self, message: str):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Ошибка')
        msg_box.setText(message)
        msg_box.exec()

    def create_calculation_image(self, words: list[str]):
        try:
            preview(eval(''.join(words)), viewer='file', \
                    filename=self.calculation_path, dvioptions=["-D 650"])
            self.set_expression(' '.join(words))

            img = QPixmap(self.calculation_path)
            self.resultImage.setPixmap(img)
        except:
            self.show_error_window('Ошибка ввода данных')  
    
    def get_words_from_text(self, mode: str):
        if mode == 'text':
            return self.equationEdit.text().split() 
        elif mode == 'voice':
            return self.get_text_from_voice().split()
        else:
            return ['']

    def get_text_from_voice(self):
        recognizer = sr.Recognizer()

        with redirect_stdout(None):        
            text= ''
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source, duration=2)

                text = recognizer.recognize_google(audio_data, language='ru-RU')

        return text
        
    def prepare_words_for_calculation(self, words: list[str]):
        words = [word.replace('_', ' ') for word in words]
        prepared_words = []
        for word in words:
            if word in symbol_dispatcher.keys():
                word = word.replace(word, symbol_dispatcher[word])
            prepared_words += [word]

        return prepared_words

    def get_expression_and_result(self, mode: str):
        words = self.get_words_from_text(mode)
        words = self.prepare_words_for_calculation(words)
        
        failure_status = self.check_numbers(words)
        if failure_status:
            self.show_error_window(failure_status)
            return 

        words = self.get_replaced_words(words)
        self.create_calculation_image(words)

    def set_expression(self, expression: str):
        self.create_expression_image(expression)
        
        try:
            img = QPixmap(self.expression_path)
            self.expressionImage.setPixmap(img)
        except:
            self.show_error_window('Неверный ввод данных')
        
    def create_expression_image(self, expression: str):
        img = Image.new('RGB', (800, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((25, 25), expression, (0, 0, 0))
        img.save(self.expression_path)

    def get_replaced_words(self, equation: list[str]) -> list[str]:
        for i in range(len(equation)):
            try:
                equation[i] = str(w2n.word_to_num(equation[i]))
            except IndexError:
                num_rank = equation[i].split(' ')
                equation[i] = str(sum([w2n.word_to_num(rank) for rank in num_rank]))
            except ValueError:
                pass
    
        for i in range(len(equation)):
            value_exists_in_dict = command_dispatcher.get(equation[i]) != None
            if value_exists_in_dict:
                equation[i] = command_dispatcher.get(equation[i])
        
        return equation

    def get_nums_indexes(self, equation: list[str]) -> list[int]:
        num_indexes = []
        for i in range(len(equation)):
            not_exists_in_dict = command_dispatcher.get(equation[i]) == None
            if not_exists_in_dict:
                num_indexes += [i]
        
        return num_indexes[:]
    
    def check_numbers(self, equation: list[str]):
        num_indexes = self.get_nums_indexes(equation)        
        equation = [equation[i] for i in num_indexes]
            
        equation = sum([number.split() for number in equation], [])
        
        try:
            for rank in equation:
                rank = w2n.word_to_num(rank)
        except ValueError:
            return f"Ошибка при вводе числа. Разряда '{rank}' не сущетсвует"
        
        return ''
        
    UI_PATH = Path(__file__).parent / "window.ui"
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()