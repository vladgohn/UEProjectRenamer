import sys
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import pathlib
import shutil
from PIL import Image, ImageTk

# Функция для определения пути к ресурсам внутри исполняемого файла
def resource_path(relative_path):
    """ Возвращает правильный путь для доступа к ресурсам внутри исполняемого файла """
    try:
        # PyInstaller создает временную папку и там хранит все ресурсы
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Функция для замены строк в файле
def string_replace_in_file(file_path, old_str, new_str):
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            content = content.replace(old_str, new_str)
            file.seek(0)
            file.write(content)
            file.truncate()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while replacing strings in file: {e}")

# Функция для очистки проекта
def clean_project(project_path):
    try:
        dirs_to_clean = [".vs", "Build", "Binaries", "DerivedDataCache", "Intermediate", "Saved", "Platforms"]
        for dir_name in dirs_to_clean:
            dir_path = project_path / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
        messagebox.showinfo("Success", "Project cleaned successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while cleaning the project: {e}")

# Функция для переименования проекта
def rename_project(project_path, new_name):
    try:
        old_name = project_path.name
        new_project_path = project_path.parent / new_name

        # Переименовываем файл .uproject
        uproject_file = project_path / f"{old_name}.uproject"
        if uproject_file.exists():
            with open(uproject_file, 'r+', encoding='utf-8') as file:
                content = json.load(file)
                content['Name'] = new_name
                file.seek(0)
                json.dump(content, file, indent=2)
                file.truncate()
            uproject_file.rename(project_path / f"{new_name}.uproject")
        
        # Переименовываем каталог проекта
        project_path.rename(new_project_path)

        # Переименовываем все вхождения старого имени в новое во всех файлах проекта
        for root, dirs, files in os.walk(new_project_path):
            for filename in files:
                file_path = pathlib.Path(root) / filename
                if file_path.suffix in ['.cpp', '.h', '.txt', '.ini', '.uproject']:
                    string_replace_in_file(file_path, old_name, new_name)

        messagebox.showinfo("Success", f"Project renamed from {old_name} to {new_name}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while renaming the project: {e}")

# Функция, вызываемая при нажатии кнопки "Process"
def process():
    try:
        path = path_entry.get()
        project_path = pathlib.Path(path)
        if not project_path.exists():
            messagebox.showerror("Error", "The specified path does not exist.")
            return

        if rename_var.get():
            new_name = new_name_entry.get()
            if not new_name:
                messagebox.showerror("Error", "Please specify the new project name.")
                return
            rename_project(project_path, new_name)

        if clean_var.get():
            clean_project(project_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the process: {e}")

# Создание и настройка графического интерфейса
root = tk.Tk()
root.title("UE Project Renamer")
root.geometry("400x350")

# Установка иконки приложения
icon_path = resource_path('ui/icon.png')
root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Загрузка баннера
banner_path = resource_path('ui/banner.jpg')
banner_image = Image.open(banner_path)
banner_photo = ImageTk.PhotoImage(banner_image)

# Отображение баннера в графическом интерфейсе
banner_label = tk.Label(root, image=banner_photo)
banner_label.grid(row=0, column=0, columnspan=3, sticky="ew")
path_label = tk.Label(root, text="Path to project")
path_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
path_entry = tk.Entry(root, width=40)
path_entry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")
browse_button = tk.Button(root, text="...", command=lambda: path_entry.insert(0, filedialog.askdirectory()))
browse_button.grid(row=1, column=2, padx=10, pady=(10, 0))
rename_var = tk.BooleanVar()
rename_check = tk.Checkbutton(root, text="Rename project", variable=rename_var)
rename_check.grid(row=2, column=0, padx=10, pady=5, sticky="w")
new_name_entry = tk.Entry(root, width=40)
new_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

clean_var = tk.BooleanVar()
clean_check = tk.Checkbutton(root, text="Clean project", variable=clean_var)
clean_check.grid(row=3, column=0, padx=10, pady=5, sticky="w")

process_button = tk.Button(root, text="Process", command=process)
process_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

#Настройка расширения виджетов по горизонтали
root.grid_columnconfigure(1, weight=1)
root.mainloop()


