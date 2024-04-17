# hhDailyApiChecker_v1
Engl
This is still almost a draft and there is a lot of code that will need to be refactored. The script will be finalized in the next releases.
There will also be new functionality.
Daily output of number of new vacancies for PYTHON developers without experience and with experience 1-3 years.

I wanted to get a summary of the number of new vacancies without visiting the site hh.ru


For legacy versions, use:
asyncio.get_event_loop().run_until_complete(SendToTg(FinalMess)) (line 116)
asyncio.get_event_loop().run_until_complete(RunAio()) (line 163)
for new ones, comment out or delete the two methods above and uncomment:
# asyncio.run(SendToTg(FinalMess)) (line 117)
# asyncio.run(RunAio()) (line 162)

You can empty the STOREvacs.db database and run the script with the 'SETup' argument (example: python 3 run.py SETup)
and then this Database will be filled from scratch. Or you can use the STOREvacs.db database that you have already started: it will
be even better this way.

This script should be run daily by cron with the "daily" argument. Example of a line in the cron configuration file
59 23 * * * python3 /your/script/path/run.py daily
Thus, around midnight you will receive a daily summary with a Telegram message.

-----
# hhDailyApiChecker_v1
Russ
Это пока еще почти черновик и тут много кода, который нужно будет рефакторить. Скрипт будет доработан в следуюзих релизах.
Также  появится новый функционал.
Ежедневный вывод количества новых вакансий для разработчиков на PYTHON без опыта работы и с опытом работы 1-3 года.

Цель скрипт раз в сутки информировать пользователя о количестве новых вакансий на сайте hh.ru 

Для устаревших версий используйте:
asyncio.get_event_loop().run_until_complete(SendToTg(FinalMess)) (строка 116)
asyncio.get_event_loop().run_until_complete(RunAio()) (строка 163)
для новых закомментируйте или удалите два метода выше и раскоментируйте 
# asyncio.run(SendToTg(FinalMess)) (строка 117)
# asyncio.run(RunAio()) (строка 162)

Вы можете опустащить Базу данных STOREvacs.db  и запустить скрипт с аргументом 'SETup' (пример: python3 run.py SETup)
и тогда эта База данных заполнится с нуля. Или же вы можете использовать уже начатую Базу данных STOREvacs.db: так будет 
даже лучше. 

Данный скрипт должен запусктаться ежедневно по cron с аргументом daily. Пример строки в конфигурационном файле cron:
59 23 * * * python3 /your/script/path/run.py daily
Таким образом около полуночи вы будете получать ежедневную сводку с отправкой в Телеграм.




