!!! An Python Script for the Abuseipdb.com API [UNOFFICIAL] !!!
!!! Скрипт Python для API Abuseipdb.com [НЕОФИЦИАЛЬНЫЙ] !!!

Python программа для удобной проверки IP-адресов на сайт abuseipdb.com через API.

<img width="312" alt="image" src="https://github.com/user-attachments/assets/fbb609b2-e147-442b-8be9-669162c503eb" />

Сборка программы в исполняемый файл для запуска в операционной системе Microsoft Windows без необходимости устанавливать Python, для этого в командной строке windows перейдем в директорию с скаченным файлом [abuseipdb.com_API_GUI_v.1.0.0.py и f1-ks.ico] и выполни команду:

  >python -m PyInstaller --onefile --windowed --icon=f1-ks.ico abuseipdb.com_API_GUI_v.1.0.0.py

далее рядом с файлом [abuseipdb.com_API_GUI_v.1.0.0.py] появится ещё один файл [abuseipdb.com_API_GUI_v.1.0.0.spec] откроем этот файл любым текстовым редактором, поправим в нём одну строку:

a = Analysis(
...
    datas=[('f1-ks.ico','.')], # Вот тут добавляем ('f1-ks.ico','.')
... )

и сохраним изменения.
далее запускаем ещё раз сборку программы, но уже с файла [abuseipdb.com_API_GUI_v.1.0.0.spec]:

  >python -m PyInstaller abuseipdb.com_API_GUI_v.1.0.0.spec

после сборки рядом с файлами py и spec появится папка dist, в этой папке будет исполняемы файл готовый к работе.

PS
Возможно, потребуется установка пакетов (если они ранее у вас не устанавливались):
  >pip install requests

  >pip install os

  >pip install PyInstaller

!!! Можно просто скачать готовый исполняемый файл для запуска на MS Windows из папки dist !!!
