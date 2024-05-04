from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog ,QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QListWidget
import json #Json файлы
import os   #библиотека os

app = QApplication([])
notes_win = QWidget()

notes_win.setWindowTitle('Умные заметки')

#0
field_text = QTextEdit()

notes_GB = QGroupBox('Список заметок')
tags_GB = QGroupBox('Список тегов')

V = QVBoxLayout()
main_H = QHBoxLayout()

V.addWidget(notes_GB)
V.addWidget(tags_GB)

main_H.addWidget(field_text)
main_H.addLayout(V)

notes_win.setLayout(main_H)

#1
list_notes = QListWidget()

create_note_button = QPushButton('Создать заметку')
delete_note_button = QPushButton('Удалить заметку')
save_note_button = QPushButton('Сохранить заметки')

notes_GB_V = QVBoxLayout()
notes_GB_H = QHBoxLayout()

notes_GB_H.addWidget(create_note_button)
notes_GB_H.addWidget(delete_note_button)

notes_GB_V.addWidget(list_notes)
notes_GB_V.addLayout(notes_GB_H)
notes_GB_V.addWidget(save_note_button)

notes_GB.setLayout(notes_GB_V)

#2
list_tags = QListWidget()
field_tag = QLineEdit()

create_tag_button = QPushButton('Создать тег')
delete_tag_button = QPushButton('Удалить тег')
search_tag_button = QPushButton('Искать по тегу')

tag_GB_V = QVBoxLayout()
tag_GB_H = QHBoxLayout()

tag_GB_H.addWidget(create_tag_button)
tag_GB_H.addWidget(delete_tag_button)

tag_GB_V.addWidget(list_tags)
tag_GB_V.addWidget(field_tag)
tag_GB_V.addLayout(tag_GB_H)
tag_GB_V.addWidget(search_tag_button)

tags_GB.setLayout(tag_GB_V)

def show_note():   #показать заметку
    note_name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[note_name]['text'])
    list_tags.clear()
    list_tags.addItems(notes[note_name]['tags'])

def add_notes():   #добавить заметку
    note_name,result = QInputDialog.getText(notes_win,'Добавление заметки.', 'Добавить заментку:')
    if result and note_name != '':
        notes[note_name]={
            'text':'',
            'tags':[]
        }
        list_notes.addItem(note_name)

def add_tag():     #добавить тег
    tag_name = field_tag.text()
    if len(list_notes.selectedItems()) > 0:
        note_name = list_notes.selectedItems()[0].text()
        notes[note_name]['tags'].append(tag_name)
        list_tags.addItem(tag_name)


def del_note():     #удалить заметку 
    if len(list_notes.selectedItems()) > 0:
        note_name = list_notes.selectedItems()[0].text()#если есть выбранная заметка
        del notes[note_name]
        list_notes.clear()
        field_text.clear()
        list_tags.clear()
        list_notes.addItems(notes)

def del_tag():     #удалить тег
    if len(list_notes.selectedItems())+len(list_tags.selectedItems()) > 0:
        tag_name = list_tags.selectedItems()[0].text()
        note_name = list_notes.selectedItems()[0].text()
        notes[note_name]['tags'].remove(tag_name)
        list_tags.clear()
        list_tags.addItems(notes[note_name]['tags'])

def save_note():    #сохранить заметку
    with open('notes_data.json', 'w') as file:
        json.dump(notes, file)

def change_note(): 
    if len(list_notes.selectedItems()) > 0:
        note_name = list_notes.selectedItems()[0].text()
        if note_name in notes:
            notes[note_name]['text']=field_text.toPlainText()


def search_tag():   #икать по тегу

        if search_tag_button.text() == 'Искать по тегу' and field_tag.text()  != '':
            tag_name = field_tag.text() 
            notes_filter = {}
            for note_name in notes:
                if tag_name in notes[note_name]['tags']:
                    notes_filter [note_name]  =  notes[note_name]
            list_tags.clear()
            field_tag.clear()
            list_notes.clear()
            list_notes.addItems(notes_filter)
            search_tag_button.setText('Сбросить поиск')

        else:
            list_tags.clear()
            field_text.clear()
            list_notes.clear()
            list_notes.addItems(notes)
            search_tag_button.setText('Искать по тегу')
            
field_text.cursorPositionChanged.connect(change_note)
list_notes.itemClicked.connect(show_note)           
    
delete_note_button.clicked.connect(del_note)    #удалить заметку
create_note_button.clicked.connect(add_notes)   #добавить заметку
save_note_button.clicked.connect(save_note)     #сохранить заметку

delete_tag_button.clicked.connect(del_tag)      #удалить тег
create_tag_button.clicked.connect(add_tag)      #добавить тег
search_tag_button.clicked.connect(search_tag)   #искать по тегу

field_tag.setPlaceholderText('Введите тег...')  #setPlaceholderText

#словарь заметок:
if os.path.isfile('notes_data.json'):   #файл есть - считать
    with open('notes_data.json', 'r') as file: 
        notes = json.load(file)
else:     #файла нет, создаем
    notes = {


        'О планетах':
            {
                'text':'Что если вод на марсе это признак жизни?',
                'tags':['Марс','гипотезы']
            },



        "О чёрных дырах":
            {
                "text":"Сингулярность на горизонте событий отсутствует",
                "tags":["черные дыры","факты"]
            },


        "Название заметки":
            {
                "text":'ТУТ ТЕКСТ ЗАМЕТКИ',
                "tags":['ТУТ','СПИСОК',"ТЕГОВ"]
            }


    }
    

#запись в файл:
    with open('notes_data.json', 'w') as file:
        json.dump(notes, file)

#отображение окна приложения: 
list_notes.addItems(notes)

notes_win.show()
app.exec_()






















































































































































































