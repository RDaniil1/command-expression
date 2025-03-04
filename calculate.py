#latex is also needed
 
import sys

from PIL import Image, ImageDraw, ImageFont

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.uic.load_ui import loadUi
from PyQt6.QtGui import QPixmap

from pathlib import Path 

from sympy import preview
from ru_word2number import w2n


symbol_dispatcher = {
    'разделить' : '/',
    'умножить' : '*', 
    'плюс' : '+',
    'минус' : '-',
    'степень' : '**',
    'начало' : '(',
    'конец' : ')'
}

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.setWindowTitle('Расчёт выражения')
        loadUi(self.UI_PATH, self)
        
        self.okButton.clicked.connect(self.get_expression_and_result)

        self.calculation_path = str(Path(__file__).parent / "calc.png")
        self.expression_path = str(Path(__file__).parent / "expression.png")
        
    def show_error_window(self, message: str):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Error')
        msg_box.setText(message)
        msg_box.exec()

    def create_calculation_image(self, words: list[str]):
        try:
            preview(eval(''.join(words)), viewer='file', filename=self.calculation_path, dvioptions=["-D 650"])
            self.set_expression(' '.join(words))

            img = QPixmap(self.calculation_path)
            self.resultImage.setPixmap(img)
        except:
            self.show_error_window('Ошибка ввода данных')

    def get_expression_and_result(self):
        words = self.equationEdit.text().split()
        words = [word.replace('_', ' ') for word in words]
        
        result = self.check_numbers(words)
        if result != 'Correct':
            self.show_error_window(result)
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
        font = ImageFont.truetype("arial.ttf", size=35)
        draw.text((25, 25), expression, (0, 0, 0), font=font)
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
            value_exists_in_dict = symbol_dispatcher.get(equation[i]) != None
            if value_exists_in_dict:
                equation[i] = symbol_dispatcher.get(equation[i])
        
        return equation

    def get_nums_indexes(self, equation: list[str]) -> list[str]:
        num_indexes = []
        for i in range(len(equation)):
            not_exists_in_dict = symbol_dispatcher.get(equation[i]) == None
            if not_exists_in_dict:
                num_indexes += [i]
        
        return num_indexes[:]
    
    def check_numbers(self, equation: list[str]):
        num_indexes = self.get_nums_indexes(equation)        
        equation = [equation[i] for i in range(len(equation)) if i in num_indexes]
            
        equation = sum([number.split() for number in equation], [])
        
        try:
            for rank in equation:
                rank = w2n.word_to_num(rank)
        except ValueError:
            return f"Ошибка при вводе числа. Разряда '{rank}' не сущетсвует"
        
        return 'Correct'
        
    UI_PATH = Path(__file__).parent / "window.ui"
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
