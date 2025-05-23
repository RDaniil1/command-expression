from calculate import MainWindow

from PyQt6 import QtCore
from pytest import fixture, raises

from speech_recognition.exceptions import UnknownValueError


@fixture
def app(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)

    return main_window

def test_main_logic(app):
    app.equationEdit.setText('два плюс два разделить четыре')
    app.get_expression_and_result('text')
    assert app.expressionImage.pixmap()
    assert app.resultImage.pixmap()

def test_words(app):
    app.equationEdit.setText('два плюс два')
    assert app.get_words_from_text('text') == ['два', 'плюс', 'два']

    with raises(UnknownValueError) as _:
        app.get_words_from_text('voice')

    assert app.get_words_from_text('other') == ['']

def test_preparation(app):
    TEST_INPUT = ['начало', 'двадцать_два', 'плюс', 'три', 'конец', 'минус', 'тридцать_три'] 
    assert app.prepare_words_for_calculation(TEST_INPUT) == ['начало', 'двадцать два', 'плюс', 'три', 'конец', 'минус', 'тридцать три'] 

def test_number_checking(app):
    CORRECT_INPUT = ['начало', 'двадцать два', 'плюс', 'три', 'конец', 'минус', 'тридцать три'] 
    assert app.check_numbers(CORRECT_INPUT) == ''
    
    INCORRECT_INPUT = ['начало', 'д', 'плюс', 'три', 'конец', 'минус', 'т'] 
    assert app.check_numbers(INCORRECT_INPUT) == "Ошибка при вводе числа. Разряда 'д' не сущетсвует"

def test_nums_indexes(app):
    CORRECT_INPUT = ['начало', 'двадцать два', 'плюс', 'три', 'конец', 'минус', 'тридцать три'] 
    assert app.get_nums_indexes(CORRECT_INPUT) == [1, 3, 6]

def test_replaced_words_with_nums(app):
    CORRECT_INPUT = ['начало', 'двадцать два', 'плюс', 'три', 'конец', 'минус', 'тридцать три'] 
    assert app.get_replaced_words(CORRECT_INPUT) == ['(', '22', '+', '3', ')', '-', '33']

def test_set_expression(app):
    app.set_expression('2 + 2')
    assert app.expressionImage.pixmap()

def test_calculation_image(app):
    app.create_calculation_image(['2'])
    assert app.resultImage.pixmap()

