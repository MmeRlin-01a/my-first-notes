from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QListWidget, QGroupBox, QHBoxLayout, QPushButton, QInputDialog, QMessageBox
import json

last_item = None
while True:
    try:
        with open('notes.json', 'r', encoding='utf-8') as file:
            all_notes = json.load(file)
        break
    except:
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump({}, file)

def update_notes_list():
    notes_list_box.clear()
    notes_list_box.addItems(all_notes.keys())

def on_item_clicked():
    global last_item
    save()
    current_item = notes_list_box.currentItem()
    if current_item:
        name = current_item.text()
        note.setPlainText(all_notes[name]['текст'])
        tags = all_notes[name].get('таги', [])
        tags_list_box.clear()
        tags_list_box.addItems(tags)
        last_item = current_item

def save():
    global last_item
    if last_item:
        name = last_item.text()
        all_notes[name]['текст'] = note.toPlainText()

def add_note():
    name, ok = QInputDialog.getText(main_win, "Новая заметка", "Введите название заметки:")
    if ok and name:
        if name in all_notes:
            QMessageBox.warning(main_win, "Ошибка", "Заметка с таким именем уже существует.")
            return
        all_notes[name] = {
            'текст': '',
            'таги': []
        }
        update_notes_list()
        items = notes_list_box.findItems(name, Qt.MatchExactly)
        if items:
            notes_list_box.setCurrentItem(items[0])
        note.clear()

def add_tag():
    current_item = notes_list_box.currentItem()
    if current_item:
        tag_name, ok = QInputDialog.getText(main_win, "Добавить тег", "Введите название тега:")
        if ok and tag_name:
            name = current_item.text()
            tags = all_notes[name].setdefault('таги', [])
            if tag_name not in tags:
                tags.append(tag_name)
                update_info()
            else:
                QMessageBox.information(main_win, "Информация", "Такой тег уже есть.")

def delete_tag():
    current_item = notes_list_box.currentItem()
    if current_item:
        name = current_item.text()
        tag_item = tags_list_box.currentItem()
        if tag_item:
            tag_name = tag_item.text()
            tags = all_notes[name].get('таги', [])
            if tag_name in tags:
                tags.remove(tag_name)
                update_info()

def update_info():
    current_item = notes_list_box.currentItem()
    if not current_item:
        return
    name = current_item.text()
    tags = all_notes[name].get('таги', [])
    tags_list_box.clear()
    tags_list_box.addItems(tags)

def delete_note():
    current_item = notes_list_box.currentItem()
    if current_item:
        name = current_item.text()
        reply = QMessageBox.question(main_win, "Удалить заметку", f"Вы действительно хотите удалить заметку '{name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del all_notes[name]
            update_notes_list()
            note.clear()
            tags_list_box.clear()

def search_notes_by_tag():
    tag, ok = QInputDialog.getText(main_win, "Поиск по тегу", "Введите тег:")
    if ok and tag:
        matching_notes = []
        for note_name, note_data in all_notes.items():
            tags = note_data.get('таги', [])
            if tag in tags:
                matching_notes.append(note_name)
        if matching_notes:
            QMessageBox.information(main_win, "Результаты поиска", 
                                    "Заметки, содержащие тег '{}':\n{}".format(
                                        tag, "\n".join(matching_notes)))
        else:
            QMessageBox.information(main_win, "Результаты поиска", 
                                    "Заметки с тегом '{}' не найдены.".format(tag))

app = QApplication([])

app.setStyleSheet("""
    QWidget {
        font-family: 'Arial Rounded MT Bold', Helvetica, sans-serif;
        font-size: 14px;
        background-color: #FFF8F0; /* Тёплый бежевый фон */
        color: #4B3F2F; /* Тёмный шоколадный текст */
    }
    QPushButton {
        background-color: #FFA07A; /* Тёплый персиковый */
        border: none;
        border-radius: 10px; /* Закругление углов */
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #FF7F50;
    }
    QGroupBox {
        border: 2px solid #D2691E; /* Тёплый оттенок */
        border-radius: 10px; /* Закругление углов */
        margin-top: 10px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px;
    }
    QListWidget {
        background-color: #FFE4B5; /* Тёплый светлый оттенок */
        border: 2px solid #CD853F;
        border-radius: 10px;
        padding: 5px;
    }
    QTextEdit {
        background-color: #FFF0E0;
        border: 2px solid #D2B48C;
        border-radius: 10px;
        padding: 8px;
    }
""")

app.setStyleSheet("""
    QWidget {
        font-family: 'Arial Rounded MT Bold', Helvetica, sans-serif;
        font-size: 20px; /* Увеличенный размер шрифта */
        background-color: #FFF8F0;
        color: #4B3F2F;
    }
    QPushButton {
        background-color: #FFA07A;
        border: none;
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 20px; /* Параметр для кнопок */
    }
    QGroupBox {
        border: 2px solid #D2691E;
        border-radius: 10px;
        margin-top: 10px;
        padding: 10px;
        font-weight: bold;
        font-size: 14px; /* Заголовки групп */
    }
    QListWidget {
        background-color: #FFE4B5;
        border: 2px solid #CD853F;
        border-radius: 10px;
        padding: 5px;
        font-size: 20px; /* Размер текста внутри списков */
    }
    QTextEdit {
        background-color: #FFF0E0;
        border: 2px solid #D2B48C;
        border-radius: 10px;
        padding: 8px;
        font-size: 20px; /* Размер текста в редакторе */
    }
""")

main_win = QWidget()
main_win.setWindowTitle("Заметки от Мирона")
main_win.move(900, 70)
main_win.resize(900, 700)

# Основная компоновка
base_layout = QVBoxLayout()
line_1 = QHBoxLayout()

# Поле заметки
note = QTextEdit()
note.setPlaceholderText('Введите заметку здесь...')
btn_add_note = QPushButton('добавить заметку')
btn_delete_note = QPushButton('удалить заметку')
btn_add_note.clicked.connect(add_note)
btn_delete_note.clicked.connect(delete_note)

note_box = QGroupBox('Заметка')
note_layout = QVBoxLayout()
note_layout.addWidget(note)
note_layout.addWidget(btn_add_note)
note_layout.addWidget(btn_delete_note)
note_box.setLayout(note_layout)

# Левая часть - список заметок и поиск
line_2 = QVBoxLayout()
notes_box = QGroupBox('заметки')
notes_list_box = QListWidget()

# Загружать все заметки
update_notes_list()
notes_list_box.currentItemChanged.connect(on_item_clicked)

btn_search_tag = QPushButton('Поиск по тегу')
btn_search_tag.clicked.connect(search_notes_by_tag)

notes_box_layout = QVBoxLayout()
notes_box_layout.addWidget(notes_list_box)
notes_box_layout.addWidget(btn_search_tag)
notes_box.setLayout(notes_box_layout)

# Справа - теги
tags_box = QGroupBox('Теги')
tags_list_box = QListWidget()
add_tag_btn = QPushButton('добавить тег')
delete_tag_btn = QPushButton('удалить тег')

add_tag_btn.clicked.connect(add_tag)
delete_tag_btn.clicked.connect(delete_tag)

tags_box_layout = QVBoxLayout()
tags_box_layout.addWidget(tags_list_box)
tags_box_layout.addWidget(add_tag_btn)
tags_box_layout.addWidget(delete_tag_btn)
tags_box.setLayout(tags_box_layout)

# Собираем в горизонтальный лэйаут
line_2.addWidget(notes_box)
line_2.addWidget(tags_box)

line_1.addWidget(note_box)
line_1.addLayout(line_2)
base_layout.addLayout(line_1)

main_win.setLayout(base_layout)
main_win.show()

app.exec_()

# Сохранение при закрытии
with open('notes.json', 'w', encoding='utf-8') as file:
    json.dump(all_notes, file)