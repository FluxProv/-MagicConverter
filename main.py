import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess
import shutil

class MagicConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MagicConverter")
        self.root.geometry("500x350")
        self.root.configure(bg="#222222")  # Тёмный фон
        self.root.resizable(False, False)  # Запрет изменения размеров окна

        # Создание директории 'out' для сохранения exe-файла
        self.output_dir = os.path.join(os.path.dirname(__file__), "out")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Иконка программы
        self.root.iconbitmap(os.path.join(os.path.dirname(__file__), "images", "icon.ico"))

        # Кастомные иконки для кнопок закрытия и сворачивания
        self.close_icon = Image.open(os.path.join(os.path.dirname(__file__), "images", "close.ico"))
        self.hide_icon = Image.open(os.path.join(os.path.dirname(__file__), "images", "hide.ico"))
        self.close_icon = self.close_icon.resize((20, 20))
        self.hide_icon = self.hide_icon.resize((20, 20))
        self.close_icon = ImageTk.PhotoImage(self.close_icon)
        self.hide_icon = ImageTk.PhotoImage(self.hide_icon)

        # Поле для выбора пути к файлу .py
        self.file_path_label = tk.Label(self.root, text="Выберите файл (.py):", fg="#ffffff", bg="#333333")
        self.file_path_label.pack(pady=(20, 5))

        self.file_path_entry = tk.Entry(self.root, width=40)
        self.file_path_entry.pack(pady=(0, 10), padx=10, ipady=3)  # Установка внутреннего отступа и размера поля ввода

        self.browse_button = tk.Button(self.root, text="Обзор", command=self.browse_file, bg="#77dd77", relief=tk.FLAT)
        self.browse_button.pack(pady=(0, 20))

        # Галочка для выбора иконки
        self.icon_check_var = tk.BooleanVar()
        self.icon_check_var.set(False)
        self.icon_check = tk.Checkbutton(self.root, text="Использовать иконку (.ico):", variable=self.icon_check_var, fg="#ffffff", bg="#333333", selectcolor="#77dd77", command=self.toggle_icon_entry)
        self.icon_check.pack()

        # Поля для выбора пути к иконке
        self.icon_path_label = tk.Label(self.root, text="Путь к иконке (.ico):", fg="#ffffff", bg="#333333")
        self.icon_path_label.pack(pady=(10, 5))
        self.icon_path_entry = tk.Entry(self.root, width=40, state=tk.DISABLED)
        self.icon_path_entry.pack(pady=(0, 10))

        self.icon_browse_button = tk.Button(self.root, text="Обзор", command=self.browse_icon, bg="#77dd77", relief=tk.FLAT, state=tk.DISABLED)
        self.icon_browse_button.pack()

        # Кнопка "Конвертировать в один файл"
        self.onefile_var = tk.BooleanVar()
        self.onefile_var.set(False)
        self.onefile_check = tk.Checkbutton(self.root, text="Конвертировать в один файл", variable=self.onefile_var, fg="#ffffff", bg="#333333", selectcolor="#77dd77")
        self.onefile_check.pack()

        # Кнопка "Конвертировать"
        self.convert_button = tk.Button(self.root, text="Конвертировать", command=self.convert, bg="#77dd77", relief=tk.FLAT)
        self.convert_button.pack(pady=(20, 10))

        # Кнопки закрытия и сворачивания окна
        self.close_button = tk.Button(self.root, image=self.close_icon, command=self.on_close, bg="#333333", relief=tk.FLAT, bd=0)
        self.close_button.place(x=470, y=10)

        self.hide_button = tk.Button(self.root, image=self.hide_icon, command=self.on_hide, bg="#333333", relief=tk.FLAT, bd=0)
        self.hide_button.place(x=440, y=10)

    def toggle_icon_entry(self):
        if self.icon_check_var.get():
            self.icon_path_entry.config(state=tk.NORMAL)
            self.icon_browse_button.config(state=tk.NORMAL)
        else:
            self.icon_path_entry.config(state=tk.DISABLED)
            self.icon_browse_button.config(state=tk.DISABLED)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def browse_icon(self):
        icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if icon_path:
            self.icon_path_entry.delete(0, tk.END)
            self.icon_path_entry.insert(0, icon_path)

    def convert(self):
        input_path = self.file_path_entry.get()

        if not os.path.exists(input_path):
            messagebox.showerror("Ошибка", "Указанный файл или папка не найдены.")
            return

        # Путь для сохранения exe-файла
        output_path = os.path.join(self.output_dir, "output.exe")

        # Команда для конвертации
        command = ['pyinstaller', '--windowed']
        if self.onefile_var.get():
            command.append('--onefile')
        if self.icon_check_var.get():
            icon_path = self.icon_path_entry.get()
            if os.path.exists(icon_path):
                command.extend(['--icon', icon_path])
            else:
                messagebox.showwarning("Предупреждение", "Указанный файл иконки не найден.")

        command.append(input_path)

        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Успех", "Конвертация завершена успешно!Исполняемый файл сохранен в папке dirst.")
            shutil.move(os.path.join(os.path.dirname(input_path), "dist", "output.exe"), output_path)
            messagebox.showinfo("Успех", f"Исполняемый файл сохранен в папке dirst")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Ошибка при конвертации: {e}")

    def on_close(self):
        self.root.destroy()

    def on_hide(self):
        self.root.withdraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MagicConverter(root)
    root.mainloop()
