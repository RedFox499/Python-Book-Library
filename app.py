import tkinter
import os
from tkinter import filedialog
import xml.etree.ElementTree as ET
from pathlib import Path
import ebooklib
from ebooklib import epub
import zipfile
import re
from tkinter import ttk
import subprocess
import sqlite3
from tkinter.messagebox import showinfo
import sys


#b83e8d
root = tkinter.Tk()
root.title("Библиотека книг")
root.configure(bg='#1e1e1e')
root.geometry("1280x720")

connection = sqlite3.connect('dbbooks.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
author TEXT NOT NULL,
date TEXT NOT NULL,
genre TEXT NOT NULL,
series TEXT NOT NULL,
description TEXT NOT NULL,
imagepath text NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pathes (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
path TEXT NOT NULL
)
''')
global currentid

def search_books():
    conn = sqlite3.connect("dbbooks.db")
    cursor = conn.cursor()
    query = entrySearch.get()
    pattern = f"%{query}%"
    cursor.execute("""
        SELECT ID, name, author, date, genre, series, description
        FROM books
        WHERE name LIKE ? OR author LIKE ?
    """, (pattern, pattern))
    for item in tree.get_children():
        tree.delete(item)
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)
    conn.close()

def inspect_book():
    conn = sqlite3.connect("dbbooks.db")
    cursor = conn.cursor()
    id1 = currentid
    cursor.execute("""
            SELECT path
            FROM pathes
            WHERE name = ?
        """, (id1,))
    path = cursor.fetchone()
    if sys.platform.startswith('darwin'):  # macOS
        subprocess.call(('open', path[0]))
    elif os.name == 'nt':  # Windows
        os.startfile(path[0])
    elif os.name == 'posix':  # Linux
        subprocess.call(('xdg-open', path[0]))


def on_select(event):
    selectedItem = tree.selection()
    item = tree.item(selectedItem)
    values = item["values"]
    if values:
        global currentid
        textbox.config(state="normal")
        textbox.delete('1.0', tkinter.END)
        textbox.insert(tkinter.END, values[6])
        textbox.config(state="disabled")
        label22.config(text=values[2])
        label55.config(text=values[4])
        label11.config(text=values[1])
        label44.config(text=values[3])
        label66.config(text=values[5])
        if values[7] == 'none' or values[7] == 'Unknwn':
            imaggge.config(file='images.png')
        else:
            imaggge.config(file=values[7])
        currentid = values[0]

def edit():
    def set_entry_text(entryy, text):
        entryy.delete(0, tkinter.END)
        entryy.insert(0, text)
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    def savethat():
        name = TitleEntry.get()
        author = authorEntry.get()
        date = dateEntry.get()
        genre = genreEntry.get()
        series = seriesEntry.get()
        desc = textboxShhs.get("1.0", tkinter.END)
        conn = sqlite3.connect("dbbooks.db")
        cursor = conn.cursor()
        pathimg = imggEntry.get()
        cursor.execute("""
            UPDATE books
            SET name = ?, author = ?, date = ?, genre = ?, series = ?, description = ?, imagepath = ?
            WHERE id = ?
        """, (name, author, date, genre, series, desc, pathimg, currentid))
        conn.commit()
        conn.close()
        Update()
        showInfo("Редактирование", "Сохранено!")
        second.destroy()
    def openimg():
        imagepath = filedialog.askopenfilename(title="Выбрать избражение",
                                          filetypes=((".jpeg", ".jpeg"), (".png", ".png")))
        if not imagepath:
            return
        image.config(file=imagepath)
        imggEntry.delete(0, tkinter.END)
        imggEntry.insert(tkinter.END, imagepath)

    second = tkinter.Toplevel(root)
    second.title("Редактирование")
    second.geometry("700x500")
    second.configure(bg='#1e1e1e')

    labelTitle = tkinter.Label(second, text="Название книги", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    TitleEntry = tkinter.Entry(second, font="Calibri 12 bold")

    labelauthor = tkinter.Label(second, text="Автор", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    authorEntry = tkinter.Entry(second, font="Calibri 12 bold")

    labeldate = tkinter.Label(second, text="Год", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    dateEntry = tkinter.Entry(second, font="Calibri 12 bold")

    labelgenre = tkinter.Label(second, text="Жанр", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    genreEntry = tkinter.Entry(second, font="Calibri 12 bold")

    labelseries = tkinter.Label(second, text="Серия", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    seriesEntry = tkinter.Entry(second, font="Calibri 12 bold")

    labeldesc = tkinter.Label(second, text="Описание", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    textboxShhs = tkinter.Text(second, bg='#1a1919', width=45, height=10, fg="white")

    labelImgg = tkinter.Label(second, text="Изображение", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    imggEntry = tkinter.Entry(second, font="Calibri 12 bold")



    labelImgg.place(x=20, y=310)
    imggEntry.place(x=20, y=340)

    image = tkinter.PhotoImage(file="", width=180, height=240)
    image_label = tkinter.Label(second, image=image)
    image_label.place(x=340, y=230)

    set_entry_text(TitleEntry, label11.cget("text"))
    set_entry_text(authorEntry,label22.cget("text"))
    set_entry_text(dateEntry, label44.cget("text"))
    set_entry_text(genreEntry, label55.cget("text"))
    set_entry_text(seriesEntry, label66.cget("text"))
    textfromtextbox = textbox.get(1.0, tkinter.END)
    textboxShhs.insert(tkinter.END, textfromtextbox)

    buttonOpenimg = tkinter.Button(second, text="Открыть изображение", font="Calibri 12 bold",
                                bg='#b83e8d',
                                fg='white',
                                border=0,
                                width=20, command=openimg)

    buttonSave = tkinter.Button(second, text="Сохранить", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=savethat)

    buttonOpenimg.place(x=20, y=380)
    buttonSave.place(x=20,y=420)
    labelTitle.place(x=20, y=20)
    TitleEntry.place(x=20, y=50)
    labelauthor.place(x=20, y=80)
    authorEntry.place(x=20, y=110)
    labeldate.place(x=20, y=140)
    dateEntry.place(x=20, y=170)
    labelgenre.place(x=20, y=200)
    genreEntry.place(x=20, y=220)
    labelseries.place(x=20, y=250)
    seriesEntry.place(x=20, y=280)
    labeldesc.place(x=400, y=20)
    textboxShhs.place(x=250,y=50)

def removeUser():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    item = tree.item(tree.selection())
    id = item["values"][0]
    cursor.execute('DELETE FROM books WHERE ID = ?', (id,))
    cursor.execute('DELETE FROM pathes WHERE name = ?', (id,))
    connection.commit()
    Update()
    connection.close()

def Update():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM books ORDER BY ID;")
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)

def showInfo(title, msg):
    showinfo(title=title, message=msg)

def openBook():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    global path
    path = filedialog.askopenfilename(title="Выбрать книгу", filetypes=((".Epub", ".epub"), (".FB2", ".fb2"), (".pdf", ".pdf"), (".txt", ".txt")))
    if not path:
        return
    global filee
    global extension1
    filee = Path(path)
    project_dir = os.getcwd()
    books_dir = os.path.join(project_dir, "books")
    os.makedirs(books_dir, exist_ok=True)
    extension1 = filee.suffix
    if extension1 == '.fb2':
        tree = ET.parse(path)
        ns = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
        root = tree.getroot()
        firstname = root.findtext(".//fb2:author/fb2:first-name", namespaces=ns)
        middlename = root.findtext(".//fb2:author/fb2:middle-name", namespaces=ns)
        lastname =  root.findtext(".//fb2:author/fb2:last-name", namespaces=ns)
        if middlename:
            fullname = lastname + " " + firstname + " " + middlename
        else:
            fullname = lastname + " " + firstname
        genre = root.findtext(".//fb2:title-info/fb2:genre", namespaces=ns)
        booktitle = root.findtext(".//fb2:title-info/fb2:book-title", namespaces=ns)
        annotation = root.findtext(".//fb2:annotation/fb2:p", namespaces=ns)
        date = root.findtext(".//fb2:title-info/fb2:date", namespaces=ns)
        if not date:
            date = "None"
        name = ""
        numm = ""
        for seq in root.findall(".//fb2:sequence", namespaces=ns):
            name = seq.attrib.get("name")
        for seq in root.findall(".//fb2:title-info/fb2:sequence", namespaces=ns):
            numm = seq.attrib.get("number")
        if not numm:
            numm = " "
        name2 = name + " " + numm
        imgpath = "none"
        cursor.execute('INSERT INTO books (name, author, date, genre, series, description, imagepath) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (booktitle, fullname, date, genre, name2, annotation, imgpath))
        book_id = cursor.lastrowid
        #new_filename = f"{fullname}_{booktitle}_{date}_{book_id}.fb2"
        #new_path = os.path.join(books_dir, new_filename)
        #shutil.copy2(path, new_path)
        cursor.execute('INSERT INTO pathes (name, path) VALUES (?, ?)',
                       (book_id, path))
        connection.commit()
        connection.close()
        Update()

    elif extension1 == '.epub':
        textbox.config(state="normal")
        textbox.delete('1.0', tkinter.END)
        book = epub.read_epub(path)
        metadata = {
            'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else None,
            'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else None,
            'date': book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else None,
            'description': book.get_metadata('DC', 'description')[0][0] if book.get_metadata('DC', 'description') else None,
            'genre': book.get_metadata('DC', 'subject')[0][0] if book.get_metadata('DC', 'subject') else None
        }
        author = metadata['author']
        indexx = 0
        firstname = ""
        secondname = ""
        for letter in range(len(author)):
            if author[letter] == " ":
                indexx = letter
                break
            else:
                firstname += author[letter]
        for letter in range(indexx, len(author)):
            secondname += author[letter]
        full = secondname + " " + firstname

        def clean_year(raw_date):
            if not raw_date:
                return None
            match = re.search(r'\d{4}', raw_date)
            return match.group(0)
        fullname = full
        booktitle = metadata['title']
        text = metadata['description']
        genre = metadata['genre']
        if not text:
            text = "None"
        if not genre:
            genre = "None"
        date=clean_year(metadata['date'])
        def get_calibre_series_metadata(path):
            series_name = None
            series_index = None
            try:
                with zipfile.ZipFile(path, 'r') as zf:
                    opf_path = None
                    for name in zf.namelist():
                        if name.endswith('.opf') and 'content' in name.lower():
                            opf_path = name
                            break
                    if opf_path:
                        with zf.open(opf_path) as opf_file:
                            tree = ET.parse(opf_file)
                            root = tree.getroot()
                            ns = {'opf': 'http://www.idpf.org/2007/opf'}
                            for meta in root.findall('.//opf:metadata/opf:meta', ns):
                                if meta.get('name') == 'calibre:series':
                                    series_name = meta.get('content')
                                elif meta.get('name') == 'calibre:series_index':
                                    series_index = meta.get('content')

                                if series_name and series_index:
                                    break

            except zipfile.BadZipFile:
                print(f"Error: '{path}' is not a valid EPUB file.")
            except FileNotFoundError:
                print(f"Error: '{path}' not found.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            if series_name == None:
                series_name = "None"
            if series_index == None:
                series_index = " "
            return series_name, series_index

        series, index = get_calibre_series_metadata(path)
        series = series + " " + index
        imgpath = "none"
        cursor.execute('INSERT INTO books (name, author, date, genre, series, description, imagepath) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (booktitle, fullname, date, genre, series, text, imgpath))
        book_id = cursor.lastrowid
        print("book_id =", book_id)
        #new_filename = f"{fullname}_{booktitle}_{date}_{book_id}.epub"
        #new_path = os.path.join(books_dir, new_filename)
        #shutil.copy2(path, new_path)
        cursor.execute('INSERT INTO pathes (name, path) VALUES (?, ?)',
                       (book_id, path))
        connection.commit()
        connection.close()
        Update()
    else:
        name, _ = os.path.splitext(os.path.basename(path))
        name = name.replace("__", "_").lower()

        year_match = re.search(r'(\d{4})', name)
        year = year_match.group(1) if year_match else None

        series_match = re.search(r'\d{4}_(\d{1,2})(?:_|__|$)', name)
        series = series_match.group(1) if series_match else None

        base = name.split(year)[0] if year else name
        parts = base.strip("_").split("_")

        author = parts[0].capitalize() if parts else None
        title = " ".join(parts[1:]).strip() if len(parts) > 1 else None
        #new_filename = f"{author}_{title}_{year}{extension1}"
        #new_path = os.path.join(books_dir, new_filename)
        genre = "Unknwn"
        text = "Unknwn"
        #shutil.copy2(path, new_path)
        imgpath = "none"
        cursor.execute('INSERT INTO books (name, author, date, genre, series, description, imagepath) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (title, author, year, genre, series, text, imgpath))
        cursor.execute('INSERT INTO pathes (name, path) VALUES (?, ?)',
                       (title, path))
        connection.commit()
        connection.close()
        Update()

def resetS():
    Update()
    entrySearch.delete(0, tkinter.END)


def process_fb2(path):
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    project_dir = os.getcwd()
    books_dir = os.path.join(project_dir, "books")
    tree = ET.parse(path)
    ns = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
    root = tree.getroot()
    firstname = root.findtext(".//fb2:author/fb2:first-name", namespaces=ns)
    middlename = root.findtext(".//fb2:author/fb2:middle-name", namespaces=ns)
    lastname = root.findtext(".//fb2:author/fb2:last-name", namespaces=ns)
    if middlename:
        fullname = lastname + " " + firstname + " " + middlename
    else:
        fullname = lastname + " " + firstname
    genre = root.findtext(".//fb2:title-info/fb2:genre", namespaces=ns)
    booktitle = root.findtext(".//fb2:title-info/fb2:book-title", namespaces=ns)
    annotation = root.findtext(".//fb2:annotation/fb2:p", namespaces=ns)
    date = root.findtext(".//fb2:title-info/fb2:date", namespaces=ns)
    if not date:
        date = "None"
    name = ""
    numm = ""
    for seq in root.findall(".//fb2:sequence", namespaces=ns):
        name = seq.attrib.get("name")
    for seq in root.findall(".//fb2:title-info/fb2:sequence", namespaces=ns):
        numm = seq.attrib.get("number")
    if not numm:
        numm = " "
    name2 = name + " " + numm
    imgpath = "none"
    cursor.execute('INSERT INTO books (name, author, date, genre, series, description, imagepath) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (booktitle, fullname, date, genre, name2, annotation, imgpath))
    book_id = cursor.lastrowid
    #new_filename = f"{fullname}_{booktitle}_{date}_{book_id}.fb2"
    #new_path = os.path.join(books_dir, new_filename)
    #shutil.copy2(path, new_path)
    cursor.execute('INSERT INTO pathes (name, path) VALUES (?, ?)',
                   (book_id, path))
    connection.commit()
    connection.close()
    Update()

def process_epub(path):
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    project_dir = os.getcwd()
    books_dir = os.path.join(project_dir, "books")
    book = epub.read_epub(path)
    metadata = {
        'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else None,
        'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else None,
        'date': book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else None,
        'description': book.get_metadata('DC', 'description')[0][0] if book.get_metadata('DC', 'description') else None,
        'genre': book.get_metadata('DC', 'subject')[0][0] if book.get_metadata('DC', 'subject') else None
    }
    author = metadata['author']
    indexx = 0
    firstname = ""
    secondname = ""
    for letter in range(len(author)):
        if author[letter] == " ":
            indexx = letter
            break
        else:
            firstname += author[letter]
    for letter in range(indexx, len(author)):
        secondname += author[letter]
    full = secondname + " " + firstname

    def clean_year(raw_date):
        if not raw_date:
            return None
        match = re.search(r'\d{4}', raw_date)
        return match.group(0)

    fullname = full
    booktitle = metadata['title']
    text = metadata['description']
    genre = metadata['genre']
    if not text:
        text = "None"
    if not genre:
        genre = "None"
    date = clean_year(metadata['date'])

    def get_calibre_series_metadata(path):
        series_name = None
        series_index = None
        try:
            with zipfile.ZipFile(path, 'r') as zf:
                opf_path = None
                for name in zf.namelist():
                    if name.endswith('.opf') and 'content' in name.lower():
                        opf_path = name
                        break
                if opf_path:
                    with zf.open(opf_path) as opf_file:
                        tree = ET.parse(opf_file)
                        root = tree.getroot()
                        ns = {'opf': 'http://www.idpf.org/2007/opf'}
                        for meta in root.findall('.//opf:metadata/opf:meta', ns):
                            if meta.get('name') == 'calibre:series':
                                series_name = meta.get('content')
                            elif meta.get('name') == 'calibre:series_index':
                                series_index = meta.get('content')

                            if series_name and series_index:
                                break

        except zipfile.BadZipFile:
            print(f"Error: '{path}' is not a valid EPUB file.")
        except FileNotFoundError:
            print(f"Error: '{path}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        if series_name == None:
            series_name = "None"
        if series_index == None:
            series_index = " "
        return series_name, series_index

    series, index = get_calibre_series_metadata(path)
    series = series + " " + index
    imgpath = "none"
    cursor.execute('INSERT INTO books (name, author, date, genre, series, description, imagepath) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (booktitle, fullname, date, genre, series, text, imgpath))
    book_id = cursor.lastrowid
    #new_filename = f"{fullname}_{booktitle}_{date}_{book_id}.epub"
    #new_path = os.path.join(books_dir, new_filename)
    #shutil.copy2(path, new_path)
    cursor.execute('INSERT INTO pathes (name, path) VALUES (?, ?)',
                   (book_id, path))
    connection.commit()
    connection.close()
    Update()

def process_else(path):
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    project_dir = os.getcwd()
    books_dir = os.path.join(project_dir, "books")
    name, _ = os.path.splitext(os.path.basename(path))
    name = name.replace("__", "_").lower()

    year_match = re.search(r'(\d{4})', name)
    year = year_match.group(1) if year_match else None

    series_match = re.search(r'\d{4}_(\d{1,2})(?:_|__|$)', name)
    series = series_match.group(1) if series_match else None

    base = name.split(year)[0] if year else name
    parts = base.strip("_").split("_")

    author = parts[0].capitalize() if parts else None
    title = " ".join(parts[1:]).strip() if len(parts) > 1 else None

    genre = "Unknwn"
    text = "Unknwn"
    imgpath = "Unknwn"
    cursor.execute('INSERT INTO books (name, author, date, genre, series, description, imagepath) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (title, author, year, genre, series, text, imgpath))
    book_id = cursor.lastrowid
    #new_filename = f"{author}_{title}_{year}_{book_id}.{ext}"
    #new_path = os.path.join(books_dir, new_filename)
    #shutil.copy2(path, new_path)
    cursor.execute('INSERT INTO pathes (name, path) VALUES (?, ?)',
                   (book_id, path))
    connection.commit()
    connection.close()
    Update()

def scandirectory():
    folder = filedialog.askdirectory(title="Выберите папку с книгами")

    if not folder:
        return
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            global ext
            ext = filename.lower().split('.')[-1]
            if ext == "fb2":
                process_fb2(filepath)
            elif ext == "epub":
                process_epub(filepath)
            else:
                process_else(filepath)




def sortbyname():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("""
               SELECT *
               FROM books
               ORDER BY name COLLATE NOCASE;
           """, )
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)
    connection.close()

def sortbyauthor():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("""
               SELECT *
               FROM books
               ORDER BY author COLLATE NOCASE;
           """, )
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)
    connection.close()

def sortbydate():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("""
               SELECT *
               FROM books
               ORDER BY date;
           """, )
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)
    connection.close()

def sortbygenre():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("""
               SELECT *
               FROM books
               ORDER BY genre COLLATE NOCASE;
           """, )
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)
    connection.close()

def sortbyseries():
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("""
               SELECT *
               FROM books
               ORDER BY series;
           """, )
    records = cursor.fetchall()
    for record in records:
        tree.insert("", tkinter.END, values=record)
    connection.close()

def changeseries():
    third = tkinter.Toplevel(root)
    third.title("Редактирование")
    third.geometry("400x130")
    third.configure(bg='#1e1e1e')
    selectedItems = tree.selection()
    connection = sqlite3.connect('dbbooks.db')
    cursor = connection.cursor()
    def savetha():
        new_series_value = newValue_entry.get()
        for item in selectedItems:
            book_id = tree.item(item, 'values')[0]
            cursor.execute("UPDATE books SET series = ? where ID = ?", (new_series_value, book_id))
        connection.commit()
        connection.close()
        Update()
        third.destroy()
    newValue_entry = tkinter.Entry(third, font="Calibri 12 bold")
    entryLabel = tkinter.Label(third, text="Серия", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
    buttonSaave = tkinter.Button(third, text="Сохранить", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=savetha)
    newValue_entry.place(x=10,y=50, width=360)
    entryLabel.place(x=10,y=20)
    buttonSaave.place(x=280,y=80)

buttonSerries = tkinter.Button(root, text="Серии", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=changeseries)

buttonSerries.place(x=650,y=620)
columns = ("ID", "name", "author", "date", "genre", "series", "description")

tree = ttk.Treeview(root, columns=columns, show="headings")

buttonName = tkinter.Button(root, text="Название", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=sortbyname)
buttonAuthors = tkinter.Button(root, text="Авторы", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=sortbyauthor)
buttonDate = tkinter.Button(root, text="Дата публикации", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=18, command=sortbydate)
buttonGenre = tkinter.Button(root, text="Жанр", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=sortbygenre)
buttonSeries = tkinter.Button(root, text="Серия", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=sortbyseries)
buttonReset = tkinter.Button(root, text="Сбросить", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=10, command=resetS)
buttonAdd = tkinter.Button(root, text="Добавить книгу", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=15, command=openBook)
buttonEdit = tkinter.Button(root, text="Редактировать", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=15, command=edit)
buttonRemove = tkinter.Button(root, text="Удалить книгу", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=15, command=removeUser)

buttonInspect = tkinter.Button(root, text="Открыть книгу", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=15, command=inspect_book)

buttonSearch = tkinter.Button(root, text="Найти", font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=15, command=search_books)
entrySearch = tkinter.Entry(root, font="Calibri 12 bold", width=35)

scanDirectory = tkinter.Button(root, text="Скан",font="Calibri 12 bold",
                            bg='#b83e8d',
                            fg='white',
                            border=0,
                            width=9, command=scandirectory)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tkinter.CENTER)
tree.column("ID", width=8,anchor=tkinter.W)

scanDirectory.place(x=1160, y=30)
entrySearch.place(x=650, y=580)
buttonSearch.place(x=940, y=577)
buttonInspect.place(x=650, y=530)
buttonEdit.place(x=880,y=30)
buttonName.place(x=30, y=30)
buttonAuthors.place(x=140, y=30)
buttonDate.place(x=250, y=30)
buttonGenre.place(x=420, y=30)
buttonSeries.place(x=530, y=30)
buttonReset.place(x=640, y=30)
buttonAdd.place(x=740, y=30)
buttonRemove.place(x=1020, y=30)

imaggge = tkinter.PhotoImage(file="")
imagggeLabel = tkinter.Label(root, image=imaggge, width=240, height=320)
imagggeLabel.place(x=380, y=370)
textbox = tkinter.Text(root, bg='#1a1919', width=40, height=20, fg="white", state="disabled")
textbox.place(x=30,y=370)
tree.place(x=30, y=80, height=270)

label1 = tkinter.Label(root, text="Название книги: ", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
label11 = tkinter.Label(root, text="", font="Calibri 12 bold", bg='#1e1e1e', fg='white')

label2 = tkinter.Label(root, text="Имя автора: ", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
label22 = tkinter.Label(root, text="", font="Calibri 12 bold", bg='#1e1e1e', fg='white')

label5 = tkinter.Label(root, text="Жанр: ", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
label55 = tkinter.Label(root, text="", font="Calibri 12 bold", bg='#1e1e1e', fg='white')

label4 = tkinter.Label(root, text="Год издания: ", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
label44 = tkinter.Label(root, text="", font="Calibri 12 bold", bg='#1e1e1e', fg='white')

label6 = tkinter.Label(root, text="Серия: ", font="Calibri 12 bold", bg='#1e1e1e', fg='white')
label66 = tkinter.Label(root, text="", font="Calibri 12 bold", bg='#1e1e1e', fg='white')

label1.place(x=650, y=370)
label11.place(x=770, y=370)

label2.place(x=650, y=400)
label22.place(x=740, y=400)

label6.place(x=650, y=430)
label66.place(x=700, y=430)

label5.place(x=650, y=460)
label55.place(x=700, y=460)

label4.place(x=650, y=490)
label44.place(x=750, y=490)

Update()
connection.commit()
connection.close()
tree.bind("<<TreeviewSelect>>", on_select)
root.mainloop()