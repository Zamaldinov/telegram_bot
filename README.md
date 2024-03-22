Бот предоставляет список чартов из яндекс-музыки.

Чтобы запустить бота, необходимо создать токен через Bot_Father и создать файл .env формата: 

` BOT_TOKEN=<Ваш токен> `

Далее необходимо загрузить все зависимости из файла req.txt
нужно использовать команду pip install -r req.txt

Команды:  
/chart - показывает список чарт песен в выбранном регионе.  
/low - показывает последние 10 треков.  
/high - показывает первые 10 треков.  
/custom - показать треки чарта конкретного жанра.  
/change - смена региона.  
/history показывает историю запрошенных команд (10 запросов)