import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import json
from pathlib import Path
import time
import threading


class IpAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.minsize(536, 400)  # Минимальный размер окна (уменьшен, т.к. кнопки теперь в фиксированной панели)

        # Получаем путь к текущему исполнимому файлу EXE
        exe_path = os.path.dirname(os.path.abspath(__file__))

        # Путь к иконке, встроенной в EXE
        icon_path = os.path.join(exe_path, 'f1-ks.ico')
                # Устанавливаем иконку
        root.wm_iconbitmap(icon_path)

        self.api_key = tk.StringVar()
        self.delay = tk.DoubleVar(value=1.0)  # Задержка по умолчанию 1 секунда
        self.ip_addresses = []
        self.result_filepath = Path(__file__).parent / "ip_analysis_results.txt"
        self.is_analyzing = False  # Флаг для отслеживания процесса анализа
        self.canvas = None  # Ссылка на canvas для обновления прокрутки
        
        # Локализация
        self.translations = self._init_translations()
        self.current_language = self.load_language()  # Загружаем сохраненный язык или русский по умолчанию
        
        # Загрузка геометрии окна
        self.load_window_geometry()
        
        # Загрузка API ключа при старте программы
        self.load_api_key()

        # Создание элементов интерфейса
        self.create_widgets()
        
        # Обновляем заголовок окна
        self.update_window_title()
        
        # Привязываем обработчик закрытия окна для сохранения геометрии
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Привязываем обработчик изменения размера/позиции окна для сохранения геометрии
        self.geometry_save_timer = None
        self.root.bind("<Configure>", self.on_window_configure)
        
        # Устанавливаем прокрутку вверх (начало) после создания виджетов
        self.root.after(200, self.scroll_to_top)
    
    def _init_translations(self):
        """Инициализация словарей переводов"""
        return {
            "ru": {
                "window_title": "IP Analyzer abuseipdb.com - версия 3.0.0",
                "api_key_label": "Введите API ключ abuseipdb.com:",
                "save_api_key": "Сохранить API ключ",
                "delay_label": "Задержка между запросами (секунды), привет от Cloudflare:",
                "ip_input_label": "Введите или загрузите список IP-адресов:",
                "load_from_file": "Загрузить из файла",
                "progress_label": "Ход выполнения:",
                "results_label": "Результаты:",
                "save_result": "Сохранить результат",
                "start_check": "Запустить проверку",
                "checking": "Проверка выполняется...",
                "api_key_saved": "API ключ успешно сохранен!",
                "api_key_empty": "API ключ не может быть пустым.",
                "api_key_required": "Введите API ключ!",
                "ip_list_empty": "Список IP-адресов пуст!",
                "analysis_running": "Анализ уже выполняется!",
                "select_file": "Выберите файл с IP-адресами",
                "result_saved": "Результат успешно сохранен!",
                "error": "Ошибка",
                "saved": "Сохранено",
                "start_analysis": "Запуск анализа...",
                "analysis_complete": "Анализ завершен.",
                "processed_ip": "Обработан IP:",
                "error_request": "Ошибка при запросе для IP",
                "status": "Статус:",
                "clean": "Чистый",
                "slightly_dirty": "Немного грязный",
                "dirty": "Грязный",
                "very_dirty": "Очень грязный",
                "records": "записей",
                "up_to": "до",
                "more_than": "больше"
            },
            "en": {
                "window_title": "IP Analyzer abuseipdb.com - version 3.0.0",
                "api_key_label": "Enter abuseipdb.com API key:",
                "save_api_key": "Save API key",
                "delay_label": "Delay between requests (seconds), greetings from Cloudflare:",
                "ip_input_label": "Enter or load IP address list:",
                "load_from_file": "Load from file",
                "progress_label": "Progress:",
                "results_label": "Results:",
                "save_result": "Save result",
                "start_check": "Start check",
                "checking": "Checking in progress...",
                "api_key_saved": "API key saved successfully!",
                "api_key_empty": "API key cannot be empty.",
                "api_key_required": "Enter API key!",
                "ip_list_empty": "IP address list is empty!",
                "analysis_running": "Analysis is already running!",
                "select_file": "Select file with IP addresses",
                "result_saved": "Result saved successfully!",
                "error": "Error",
                "saved": "Saved",
                "start_analysis": "Starting analysis...",
                "analysis_complete": "Analysis complete.",
                "processed_ip": "Processed IP:",
                "error_request": "Error requesting IP",
                "status": "Status:",
                "clean": "Clean",
                "slightly_dirty": "Slightly dirty",
                "dirty": "Dirty",
                "very_dirty": "Very dirty",
                "records": "records",
                "up_to": "up to",
                "more_than": "more than"
            },
            "zh": {
                "window_title": "IP 分析器 abuseipdb.com - 版本 3.0.0",
                "api_key_label": "输入 abuseipdb.com API 密钥:",
                "save_api_key": "保存 API 密钥",
                "delay_label": "请求之间的延迟（以秒为单位），来自 Cloudflare 的问候 :",
                "ip_input_label": "输入或加载 IP 地址列表:",
                "load_from_file": "从文件加载",
                "progress_label": "进度:",
                "results_label": "结果:",
                "save_result": "保存结果",
                "start_check": "开始检查",
                "checking": "正在检查...",
                "api_key_saved": "API 密钥保存成功！",
                "api_key_empty": "API 密钥不能为空。",
                "api_key_required": "请输入 API 密钥！",
                "ip_list_empty": "IP 地址列表为空！",
                "analysis_running": "分析已在运行！",
                "select_file": "选择包含 IP 地址的文件",
                "result_saved": "结果保存成功！",
                "error": "错误",
                "saved": "已保存",
                "start_analysis": "开始分析...",
                "analysis_complete": "分析完成。",
                "processed_ip": "已处理 IP:",
                "error_request": "请求 IP 时出错",
                "status": "状态:",
                "clean": "干净",
                "slightly_dirty": "略脏",
                "dirty": "脏",
                "very_dirty": "非常脏",
                "records": "条记录",
                "up_to": "最多",
                "more_than": "超过"
            }
        }
    
    def t(self, key):
        """Получить перевод по ключу для текущего языка"""
        return self.translations.get(self.current_language, self.translations["ru"]).get(key, key)
    
    def update_window_title(self):
        """Обновить заголовок окна"""
        self.root.title(self.t("window_title"))
    
    def load_language(self):
        """Загрузить сохраненный язык из файла"""
        lang_file = Path("language.txt")
        if lang_file.exists():
            try:
                with open(lang_file, "r", encoding="utf-8") as file:
                    lang = file.read().strip()
                    if lang in ["ru", "en", "zh"]:
                        return lang
            except:
                pass
        return "ru"  # По умолчанию русский
    
    def save_language(self):
        """Сохранить выбранный язык в файл"""
        try:
            with open("language.txt", "w", encoding="utf-8") as file:
                file.write(self.current_language)
        except:
            pass
    
    def load_window_geometry(self):
        """Загрузить сохраненную геометрию окна"""
        geometry_file = Path("window_geometry.txt")
        if geometry_file.exists():
            try:
                with open(geometry_file, "r", encoding="utf-8") as file:
                    geometry = file.read().strip()
                    if geometry:
                        self.root.geometry(geometry)
                        return
            except:
                pass
        # Геометрия по умолчанию, если файл не существует или произошла ошибка
        # self.root.geometry("536x757")
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Устанавливаем размеры окна по умолчанию
        window_width = 536
        window_height = 757
        # Рассчитываем позицию окна, чтобы оно было по центру экрана
        position_left = (screen_width - window_width) // 2
        position_top = (screen_height - window_height) // 2
        # Устанавливаем размеры и позицию окна
        self.root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    def save_window_geometry(self):
        """Сохранить текущую геометрию окна"""
        try:
            geometry = self.root.geometry()
            with open("window_geometry.txt", "w", encoding="utf-8") as file:
                file.write(geometry)
        except:
            pass
    
    def on_window_configure(self, event=None):
        """Обработчик изменения размера/позиции окна"""
        # Сохраняем геометрию только если это изменение самого окна, а не дочерних виджетов
        if event and event.widget == self.root:
            # Отменяем предыдущий таймер, если он есть
            if self.geometry_save_timer:
                self.root.after_cancel(self.geometry_save_timer)
            # Устанавливаем новый таймер для сохранения через 500мс после последнего изменения
            self.geometry_save_timer = self.root.after(500, self.save_window_geometry)
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        self.save_window_geometry()
        self.root.destroy()
    
    def scroll_to_top(self):
        """Прокрутить canvas вверх (начало), чтобы отображалась верхняя часть интерфейса с выбором языка"""
        if self.canvas:
            try:
                # Обновляем canvas, чтобы убедиться, что все виджеты отрисованы
                self.canvas.update_idletasks()
                # Прокручиваем в начало (верх)
                self.canvas.yview_moveto(0.0)
            except:
                pass
    
    def change_language(self, event=None):
        """Переключение языка интерфейса"""
        lang_map = {"Русский": "ru", "English": "en", "中文": "zh"}
        selected = self.language_var.get()
        self.current_language = lang_map.get(selected, "ru")
        
        # Сохраняем выбранный язык
        self.save_language()
        
        # Обновляем заголовок окна
        self.update_window_title()
        
        # Обновляем все элементы интерфейса
        if hasattr(self, 'api_key_label'):
            self.api_key_label.config(text=self.t("api_key_label"))
        if hasattr(self, 'save_api_key_button'):
            self.save_api_key_button.config(text=self.t("save_api_key"))
        if hasattr(self, 'delay_label'):
            self.delay_label.config(text=self.t("delay_label"))
        if hasattr(self, 'ip_input_label'):
            self.ip_input_label.config(text=self.t("ip_input_label"))
        if hasattr(self, 'load_ip_button'):
            self.load_ip_button.config(text=self.t("load_from_file"))
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=self.t("progress_label"))
        if hasattr(self, 'result_label'):
            self.result_label.config(text=self.t("results_label"))
        if hasattr(self, 'save_result_button'):
            self.save_result_button.config(text=self.t("save_result"))
        if hasattr(self, 'analyze_button'):
            if not self.is_analyzing:
                self.analyze_button.config(text=self.t("start_check"))
            else:
                self.analyze_button.config(text=self.t("checking"))

    def load_api_key(self):
        "Загружаем API ключ из файла, если он существует."
        if Path("api_key.txt").exists():
            with open("api_key.txt", "r", encoding="utf-8") as file:
                self.api_key.set(file.read().strip())

    def create_widgets(self):
        # Верхняя панель с выбором языка (правый верхний угол)
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Определяем начальное значение выпадающего списка на основе загруженного языка
        lang_display_map = {"ru": "Русский", "en": "English", "zh": "中文"}
        initial_lang = lang_display_map.get(self.current_language, "Русский")
        
        # Выпадающий список (упаковываем первым, чтобы был справа)
        self.language_var = tk.StringVar(value=initial_lang)
        language_combo = ttk.Combobox(top_frame, textvariable=self.language_var, 
                                      values=["Русский", "English", "中文"], 
                                      state="readonly", width=12)
        language_combo.pack(side=tk.RIGHT, padx=5)
        language_combo.bind("<<ComboboxSelected>>", self.change_language)
       
        # Описание языка (упаковываем последним, чтобы было слева)
        language_label = tk.Label(top_frame, text="Язык / Language / 语言 :")
        language_label.pack(side=tk.RIGHT, padx=5)
        
        # Фиксированная нижняя панель для кнопок (создаем первой, чтобы она была внизу)
        bottom_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.save_result_button = tk.Button(bottom_frame, text=self.t("save_result"), command=self.save_result)
        self.save_result_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка для выполнения анализа
        self.analyze_button = tk.Button(bottom_frame, text=self.t("start_check"), command=self.analyze_ips, height=2, bg="green", fg="white", font=("Arial", 14, "bold"))
        self.analyze_button.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Создаем контейнер для прокручиваемого контента
        self.canvas = tk.Canvas(self.root, bd=0, relief='flat', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas)
        
        canvas_window = self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_scroll_region(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas_width = event.width
            self.canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.canvas.bind("<Configure>", configure_canvas_width)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Упаковываем canvas и scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Поле для ввода API ключа
        self.api_key_label = tk.Label(scrollable_frame, text=self.t("api_key_label"))
        self.api_key_label.pack(pady=5, anchor=tk.W)

        self.api_key_entry = tk.Entry(scrollable_frame, textvariable=self.api_key)
        self.api_key_entry.pack(pady=5, fill=tk.X)

        self.save_api_key_button = tk.Button(scrollable_frame, text=self.t("save_api_key"), command=self.save_api_key)
        self.save_api_key_button.pack(pady=5)

        # Поле для установки задержки между запросами
        delay_frame = tk.Frame(scrollable_frame)
        delay_frame.pack(pady=5, fill=tk.X)
        self.delay_label = tk.Label(delay_frame, text=self.t("delay_label"))
        self.delay_label.pack(side=tk.LEFT, padx=5)
        self.delay_entry = tk.Spinbox(delay_frame, from_=0.0, to=60.0, increment=0.1, textvariable=self.delay, width=10)
        self.delay_entry.pack(side=tk.LEFT, padx=5)

        # Поле для загрузки IP адресов
        self.ip_input_label = tk.Label(scrollable_frame, text=self.t("ip_input_label"))
        self.ip_input_label.pack(pady=5, anchor=tk.W)

        # Фрейм для IP адресов с прокруткой
        ip_frame = tk.Frame(scrollable_frame)
        ip_frame.pack(pady=5, fill=tk.X)
        self.ip_input_text = tk.Text(ip_frame, height=8, wrap=tk.WORD)
        ip_scrollbar = tk.Scrollbar(ip_frame, orient=tk.VERTICAL, command=self.ip_input_text.yview)
        self.ip_input_text.configure(yscrollcommand=ip_scrollbar.set)
        self.ip_input_text.grid(row=0, column=0, sticky="ew")
        ip_scrollbar.grid(row=0, column=1, sticky="ns")
        ip_frame.grid_columnconfigure(0, weight=1, minsize=0)
        ip_frame.grid_rowconfigure(0, weight=0)

        self.load_ip_button = tk.Button(scrollable_frame, text=self.t("load_from_file"), command=self.load_ip_from_file)
        self.load_ip_button.pack(pady=5)

        # Поле для отображения хода выполнения
        self.progress_label = tk.Label(scrollable_frame, text=self.t("progress_label"))
        self.progress_label.pack(pady=5, anchor=tk.W)

        # Фрейм для прогресса с прокруткой
        progress_frame = tk.Frame(scrollable_frame)
        progress_frame.pack(pady=5, fill=tk.X)
        self.progress_text = tk.Text(progress_frame, height=4, wrap=tk.WORD)
        progress_scrollbar = tk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.progress_text.yview)
        self.progress_text.configure(yscrollcommand=progress_scrollbar.set)
        self.progress_text.grid(row=0, column=0, sticky="ew")
        progress_scrollbar.grid(row=0, column=1, sticky="ns")
        progress_frame.grid_columnconfigure(0, weight=1, minsize=0)
        progress_frame.grid_rowconfigure(0, weight=0)

        # Поле для вывода результатов
        self.result_label = tk.Label(scrollable_frame, text=self.t("results_label"))
        self.result_label.pack(pady=5, anchor=tk.W)

        # Фрейм для результатов с прокруткой
        result_frame = tk.Frame(scrollable_frame)
        result_frame.pack(pady=5, fill=tk.X)
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD)
        result_scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky="ew")
        result_scrollbar.grid(row=0, column=1, sticky="ns")
        result_frame.grid_columnconfigure(0, weight=1, minsize=0)
        result_frame.grid_rowconfigure(0, weight=0)

    def save_api_key(self):
        api_key = self.api_key.get().strip()
        if api_key:
            with open("api_key.txt", "w", encoding="utf-8") as file:
                file.write(api_key)
            messagebox.showinfo(self.t("saved"), self.t("api_key_saved"))
        else:
            messagebox.showwarning(self.t("error"), self.t("api_key_empty"))

    def load_ip_from_file(self):
        file_path = filedialog.askopenfilename(title=self.t("select_file"), filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                ip_addresses = file.readlines()
                self.ip_addresses = [ip.strip() for ip in ip_addresses]
                self.ip_input_text.delete(1.0, tk.END)
                self.ip_input_text.insert(tk.END, "\n".join(self.ip_addresses))

    def analyze_ips(self):
        if self.is_analyzing:
            messagebox.showwarning(self.t("error"), self.t("analysis_running"))
            return

        api_key = self.api_key.get().strip()
        if not api_key:
            messagebox.showwarning(self.t("error"), self.t("api_key_required"))
            return

        # Получаем список IP адресов
        ip_addresses = self.ip_input_text.get(1.0, tk.END).strip().split("\n")
        ip_addresses = [ip.strip() for ip in ip_addresses if ip.strip()]
        if not ip_addresses:
            messagebox.showwarning(self.t("error"), self.t("ip_list_empty"))
            return

        # Запускаем анализ в отдельном потоке
        self.is_analyzing = True
        self.analyze_button.config(state=tk.DISABLED, text=self.t("checking"))
        self.progress_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.update_progress(self.t("start_analysis") + "\n")
        
        thread = threading.Thread(target=self._analyze_ips_thread, args=(api_key, ip_addresses), daemon=True)
        thread.start()

    def _analyze_ips_thread(self, api_key, ip_addresses):
        """Выполняет анализ IP в отдельном потоке"""
        url = 'https://api.abuseipdb.com/api/v2/check'
        headers = {
            'Accept': 'application/json',
            'Key': api_key
        }
        delay = self.delay.get()

        total_ips = len(ip_addresses)
        processed = 0

        with open(self.result_filepath, "w", encoding="utf-8") as result_file:
            for ip in ip_addresses:
                if not self.is_analyzing:  # Проверка на остановку
                    break

                querystring = {'ipAddress': ip, 'maxAgeInDays': '90'}
                try:
                    response = requests.get(url, headers=headers, params=querystring)

                    if response.status_code == 200:
                        decoded_response = response.json()
                        ip_address = decoded_response.get('data', {}).get('ipAddress', '')
                        total_reports = decoded_response.get('data', {}).get('totalReports', 0)
                        country_code = decoded_response.get('data', {}).get('countryCode', '')

                        if total_reports == 0:
                            result = f"{self.t('clean')} {ip_address} {country_code} = 0 {self.t('records')}\n"
                        elif 1 <= total_reports <= 4:
                            result = f"{self.t('slightly_dirty')} {ip_address} {country_code} = {self.t('up_to')} 4 {self.t('records')}\n"
                        elif 5 <= total_reports <= 10:
                            result = f"{self.t('dirty')} {ip_address} {country_code} = {self.t('up_to')} 10 {self.t('records')}\n"
                        else:
                            result = f"{self.t('very_dirty')} {ip_address} {country_code} = {self.t('more_than')} 10 {self.t('records')}\n"

                        self.update_result(result)
                        result_file.write(result)
                        processed += 1
                        self.update_progress(f"{self.t('processed_ip')} {ip} ({processed}/{total_ips})\n")
                    else:
                        error_message = f"{self.t('error_request')} {ip}. {self.t('status')} {response.status_code}\n"
                        self.update_result(error_message)
                        result_file.write(error_message)
                        self.update_progress(f"{self.t('error_request')} {ip}\n")
                except Exception as e:
                    error_message = f"{self.t('error_request')} {ip}: {str(e)}\n"
                    self.update_result(error_message)
                    result_file.write(error_message)
                    self.update_progress(f"{self.t('error_request')} {ip}\n")

                # Задержка между запросами
                if delay > 0 and ip != ip_addresses[-1]:  # Не задерживаемся после последнего IP
                    time.sleep(delay)

        self.update_progress(self.t("analysis_complete") + "\n")
        self.is_analyzing = False
        self.root.after(0, self._analysis_complete)

    def update_progress(self, text):
        """Обновляет поле прогресса в главном потоке"""
        self.root.after(0, lambda: self.progress_text.insert(tk.END, text))
        self.root.after(0, lambda: self.progress_text.see(tk.END))

    def update_result(self, text):
        """Обновляет поле результатов в главном потоке"""
        self.root.after(0, lambda: self.result_text.insert(tk.END, text))
        self.root.after(0, lambda: self.result_text.see(tk.END))

    def _analysis_complete(self):
        """Вызывается после завершения анализа"""
        self.analyze_button.config(state=tk.NORMAL, text=self.t("start_check"))

    def save_result(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.result_text.get(1.0, tk.END))
            messagebox.showinfo(self.t("saved"), self.t("result_saved"))

if __name__ == "__main__":
    root = tk.Tk()
    app = IpAnalyzerApp(root)
    root.mainloop()
