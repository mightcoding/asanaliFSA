from tkinter import *
from tkinter import messagebox
import sqlite3
from mylogo import mylogo
from aldehydes import *

def setup_database():
    conn = sqlite3.connect('asanali_school_aldehyde.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS asanali_users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS school_aldehydes (
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    c.execute('SELECT COUNT(*) FROM school_aldehydes')
    if c.fetchone()[0] == 0:
        aldehydes_info
        c.executemany('INSERT INTO school_aldehydes (name, description) VALUES (?, ?)', aldehydes_info)
        conn.commit()
    conn.close()

def registration_chem(username, password):
    conn = sqlite3.connect('asanali_school_aldehyde.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO asanali_users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('asanali_school_aldehyde.db')
    c = conn.cursor()
    c.execute('SELECT password FROM asanali_users WHERE username = ?', (username,))
    db_password = c.fetchone()
    conn.close()
    return db_password and db_password[0] == password

def get_aldehyde_data():
    conn = sqlite3.connect('asanali_school_aldehyde.db')
    c = conn.cursor()
    c.execute('SELECT name, description FROM school_aldehydes')
    aldehydes = c.fetchall()
    conn.close()
    return aldehydes

def clear_widgets(window):
    for widget in window.winfo_children():
        widget.destroy()

def load_login_interface(window):
    clear_widgets(window)
    logo_image = PhotoImage(file=mylogo) 
    logo_label = Label(window, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=0, column=0, sticky="w")
    
    username_var = StringVar()
    password_var = StringVar()
    Label(window, text="Имя пользователя:").grid(row=1, column=0)
    Entry(window, textvariable=username_var).grid(row=1, column=1)
    Label(window, text="Пароль:").grid(row=2, column=0)
    Entry(window, textvariable=password_var, show='*').grid(row=2, column=1)
    Button(window, text="Войти", command=lambda: login_action(username_var.get(), password_var.get(), window)).grid(row=3, column=0)
    Button(window, text="Регистрация", command=lambda: reg_action(username_var.get(), password_var.get(), window)).grid(row=3, column=1)

def main_menu(username, window):
    clear_widgets(window)
    aldehydes = get_aldehyde_data()
    row = 0
    for aldehyde in aldehydes:
        Button(window, text=aldehyde[0], command=lambda desc=aldehyde[1]: messagebox.showinfo(aldehyde[0], desc)).grid(row=row, column=0, sticky="ew")
        row += 1
    Button(window, text="Вернуться в главное меню", command=lambda: load_login_interface(window)).grid(row=row, column=0)

def login_action(username, password, window):
    if authenticate_user(username, password):
        messagebox.showinfo("Вы смогли войти!", "Вы успешно вошли в свой аккаунт!")
        main_menu(username, window)
    else:
        messagebox.showerror("Ошибка", "Вы ввели еверный логин или пароль.")

def reg_action(username, password, window):
    if registration_chem(username, password):
        messagebox.showinfo("Добро пожаловать в наше приложение!", "Регистрация прошла без проблем!")
        main_menu(username, window)
    else:
        messagebox.showerror("Ошибка", "Такой пользователь уже существует в нашей базе данных.")

def initialize_gui():
    app = Tk()
    app.title('Asanali Aldehyde School App')
    load_login_interface(app)
    app.mainloop()

setup_database()
initialize_gui()
