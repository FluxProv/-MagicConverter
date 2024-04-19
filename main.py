import subprocess
import os
import shutil

def convert_to_exe():
    # Запрос пути к папке с файлом .py
    folder_path = input("Введите путь к папке с вашим файлом (.py): ")
    file_name = input("Введите имя вашего файла в формате имя.py: ")

    # Запрос пути к папке с иконкой (если нужно)
    icon_folder_path = input("Введите путь к папке с иконкой (.ico) или введите 'нет': ")
    icon_file_name = None
    if icon_folder_path.lower() != 'нет':
        icon_file_name = input("Введите имя файла иконки (.ico): ")

    # Запрос на конвертацию в один файл
    convert_to_onefile = input("Желаете ли сконвертировать в один файл? (да/нет): ").lower() == 'да'

    # Собираем путь к файлу .py
    py_file_path = os.path.join(folder_path, file_name)

    # Проверяем существует ли файл .py
    if not os.path.exists(py_file_path):
        print(f"Файл {file_name} не найден по указанному пути.")
        return

    # Собираем путь к файлу иконки (если указан)
    icon_path = None
    if icon_folder_path.lower() != 'нет':
        icon_path = os.path.join(icon_folder_path, icon_file_name)
        if not os.path.exists(icon_path):
            print(f"Файл иконки {icon_file_name} не найден по указанному пути.")
            return

    # Подготовка параметров командной строки для pyinstaller
    command = ['pyinstaller']
    if convert_to_onefile:
        command.append('--onefile')
    if icon_path:
        command.extend(['--icon', icon_path])
    command.append(py_file_path)

    # Запуск процесса конвертации
    try:
        subprocess.run(command, check=True)
        print("Конвертация завершена успешно!")
        # Находим путь к папке dist, где находится исполняемый файл
        dist_folder = os.path.join(folder_path, 'dist')
        exe_file = os.listdir(dist_folder)[0]
        exe_file_path = os.path.join(dist_folder, exe_file)
        print(f"Ваш исполняемый файл сохранен по пути: {exe_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации: {e}")

if __name__ == "__main__":
    convert_to_exe()
