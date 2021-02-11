import datetime
import schedule

'''i = 1
stop = False


def job():
    global i
    print(f'Hello', name)
    i += 1
    if i == 5:
        stop = True
        return schedule.CancelJob


schedule.every(1).to(3).seconds.do(greet, name='Yandex')

while not stop:
    schedule.run_pending()'''


def cuckoo():
    dt = datetime.datetime.now()
    hour = datetime.datetime.timetuple(dt)[3]
    i = hour % 12 if hour % 12 else 12
    print('Ку' * i)


schedule.every().hour.at(":00").do(cuckoo)

while True:
    schedule.run_pending()
