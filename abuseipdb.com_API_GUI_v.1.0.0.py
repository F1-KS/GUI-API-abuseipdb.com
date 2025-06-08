import os
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
from pathlib import Path


class IpAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Analyzer abuseipdb.com - версия 1.0.0")
        self.root.geometry("600x780")

        # Получаем путь к текущему исполнимому файлу EXE
        exe_path = os.path.dirname(os.path.abspath(__file__))

        # Путь к иконке, встроенной в EXE
        icon_path = os.path.join(exe_path, 'f1-ks.ico')
                # Устанавливаем иконку
        root.wm_iconbitmap(icon_path)

        self.api_key = tk.StringVar()
        self.ip_addresses = []
        self.result_filepath = Path(__file__).parent / "ip_analysis_results.txt"

        # Загрузка API ключа при старте программы
        self.load_api_key()

        # Создание элементов интерфейса
        self.create_widgets()

    def load_api_key(self):
        "Загружаем API ключ из файла, если он существует."
        if Path("api_key.txt").exists():
            with open("api_key.txt", "r", encoding="utf-8") as file:
                self.api_key.set(file.read().strip())

    def create_widgets(self):
        # Поле для ввода API ключа
        self.api_key_label = tk.Label(self.root, text="Введите API ключ abuseipdb.com:")
        self.api_key_label.pack(pady=5)

        self.api_key_entry = tk.Entry(self.root, textvariable=self.api_key, width=50)
        self.api_key_entry.pack(pady=5, padx=30, fill=tk.X)

        self.save_api_key_button = tk.Button(self.root, text="Сохранить API ключ", command=self.save_api_key)
        self.save_api_key_button.pack(pady=5)

        # Поле для загрузки IP адресов
        self.ip_input_label = tk.Label(self.root, text="Введите или загрузите список IP-адресов:")
        self.ip_input_label.pack(pady=5)

        self.ip_input_text = tk.Text(self.root, height=10, width=50)
        self.ip_input_text.pack(pady=5, padx=30, fill=tk.X)

        self.load_ip_button = tk.Button(self.root, text="Загрузить из файла", command=self.load_ip_from_file)
        self.load_ip_button.pack(pady=5)

        # Поле для отображения хода выполнения
        self.progress_label = tk.Label(self.root, text="Ход выполнения:")
        self.progress_label.pack(pady=5)

        self.progress_text = tk.Text(self.root, height=5, width=50)
        self.progress_text.pack(pady=5, padx=30, fill=tk.X)

        # Поле для вывода результатов и кнопка для сохранения результата
        self.result_label = tk.Label(self.root, text="Результаты:")
        self.result_label.pack(pady=5)

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack(pady=5, padx=30, fill=tk.X)

        self.save_result_button = tk.Button(self.root, text="Сохранить результат", command=self.save_result)
        self.save_result_button.pack(pady=5)

        # Кнопка для выполнения анализа
        self.analyze_button = tk.Button(self.root, text="Запустить проверку", command=self.analyze_ips, height=2, width=20, bg="green", fg="white", font=("Arial", 14, "bold"))
        self.analyze_button.pack(pady=5)

    def save_api_key(self):
        api_key = self.api_key.get().strip()
        if api_key:
            with open("api_key.txt", "w", encoding="utf-8") as file:
                file.write(api_key)
            messagebox.showinfo("Сохранено", "API ключ успешно сохранен!")
        else:
            messagebox.showwarning("Ошибка", "API ключ не может быть пустым.")

    def load_ip_from_file(self):
        file_path = filedialog.askopenfilename(title="Выберите файл с IP-адресами", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                ip_addresses = file.readlines()
                self.ip_addresses = [ip.strip() for ip in ip_addresses]
                self.ip_input_text.delete(1.0, tk.END)
                self.ip_input_text.insert(tk.END, "\n".join(self.ip_addresses))

    def analyze_ips(self):
        api_key = self.api_key.get().strip()
        if not api_key:
            messagebox.showwarning("Ошибка", "Введите API ключ!")
            return

        self.progress_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.progress_text.insert(tk.END, "Запуск анализа...\n")

        # Получаем список IP адресов
        ip_addresses = self.ip_input_text.get(1.0, tk.END).strip().split("\n")
        if not ip_addresses:
            messagebox.showwarning("Ошибка", "Список IP-адресов пуст!")
            return

        url = 'https://api.abuseipdb.com/api/v2/check'
        headers = {
            'Accept': 'application/json',
            'Key': api_key
        }

        with open(self.result_filepath, "w", encoding="utf-8") as result_file:
            for ip in ip_addresses:
                ip = ip.strip()
                if not ip:
                    continue

                querystring = {'ipAddress': ip, 'maxAgeInDays': '90'}
                response = requests.get(url, headers=headers, params=querystring)

                if response.status_code == 200:
                    decoded_response = response.json()
                    ip_address = decoded_response.get('data', {}).get('ipAddress', '')
                    total_reports = decoded_response.get('data', {}).get('totalReports', 0)
                    country_code = decoded_response.get('data', {}).get('countryCode', '')

                    if total_reports == 0:
                        result = f"Чистый {ip_address} {country_code} = 0 записей\n"
                    elif 1 <= total_reports <= 4:
                        result = f"Немного грязный {ip_address} {country_code} = до 4-х записей\n"
                    elif 5 <= total_reports <= 10:
                        result = f"Грязный {ip_address} {country_code} = до 10-и записей\n"
                    else:
                        result = f"Очень грязный {ip_address} {country_code} = больше 10 записей\n"

                    self.result_text.insert(tk.END, result)
                    result_file.write(result)
                    self.progress_text.insert(tk.END, f"Обработан IP: {ip}\n")
                else:
                    error_message = f"Ошибка при запросе для IP {ip}. Статус: {response.status_code}\n"
                    self.result_text.insert(tk.END, error_message)
                    result_file.write(error_message)
                    self.progress_text.insert(tk.END, f"Ошибка при запросе для IP: {ip}\n")

        self.progress_text.insert(tk.END, "Анализ завершен.")

    def save_result(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.result_text.get(1.0, tk.END))
            messagebox.showinfo("Сохранено", "Результат успешно сохранен!")

if __name__ == "__main__":
    root = tk.Tk()
    app = IpAnalyzerApp(root)
    root.mainloop()
