!!! An Python Script for the Abuseipdb.com API [UNOFFICIAL] !!!

!!! Скрипт Python для API Abuseipdb.com [НЕОФИЦИАЛЬНЫЙ] !!!

Python программа для удобной проверки IP-адресов на сайт abuseipdb.com через API, в новой версии:
1. Добавлена локализация для английского и китайского языка.
2. Добавлена функция задержки отправки запросов на проверку IP адресов, побудил добавить это, cloudflare.
3. Мелкие изменения графического интерфейса и работы кода в целом.

![abuseipdb com_API_GUI_v 3 0 1](https://github.com/user-attachments/assets/f95f35ff-4072-4500-9435-9ca5e7999cb3)


Сборка программы в исполняемый файл для запуска в операционной системе Microsoft Windows без необходимости устанавливать Python (но для компиляции всё же python потребуется но один раз), для этого в командной строке windows перейдем в директорию с скаченным файлом [abuseipdb.com_API_GUI_v.3.0.1.py и f1-ks.ico] и выполни команду:

  >python -m PyInstaller --onefile --windowed --icon=f1-ks.ico abuseipdb.com_API_GUI_v.3.0.1.py

далее рядом с файлом [abuseipdb.com_API_GUI_v.3.0.1.py] появится ещё один файл [abuseipdb.com_API_GUI_v.3.0.1.spec] откроем этот файл любым текстовым редактором, поправим в нём одну строку:

a = Analysis(
...
    datas=[('f1-ks.ico','.')], # Вот тут добавляем ('f1-ks.ico','.')
... )

и сохраним изменения.
далее запускаем ещё раз сборку программы, но уже с файла [abuseipdb.com_API_GUI_v.3.0.1.spec]:

  >python -m PyInstaller abuseipdb.com_API_GUI_v.3.0.1.spec

после сборки рядом с файлами py и spec появится папка dist, в этой папке будет исполняемы файл готовый к работе.

PS
Возможно, потребуется установка пакетов (если они ранее у вас не устанавливались):
  >pip install requests

  >pip install os

  >pip install PyInstaller

!!! Можно просто скачать готовый исполняемый файл для запуска на MS Windows из папки dist !!!
