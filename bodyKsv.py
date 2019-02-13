"""Function for sorting script."""
import logging
import os
import shutil

# add base dir
BASE_DIR = os.path.dirname(__file__)

# стандратное имя файла
akt = 'акт прийняття внурішніх і зовнішніх мереж.pdf'
# ключ-номер района с программы заявка, значение-номер района в сетевой папке
regionDict = {'02.': '01_', '19.': '02_', '05.': '03_', '04.': '04_',
              '06.': '05_', '15.': '06_', '23.': '07_',
              '12.': '13_', '03.': '14_', '14.': '15_', '18.': '16_',
              '25.': '17_', '11.': '18_', '16.': '19_', '09.': '20_',
              '01.': '21_', '24.': '22_', '21.': '23_', '20.': '24_',
              '08.': '25_', '22.': '26_'}


def get_info_from_txt_file(source):
    """
    функция которая импортирует данные с txt файла.

    возвращает список с данными c чистыми имиенами

    """
    with open(source, 'r') as txtfile:
        data = [''' '''.join(i.rstrip('\n').split(' ')[1:]) for i in txtfile]
        return data


def create_intermidiate_dir(imd, dwsf, giftf):
    """
    функция которая должна.

    1. создать папки
    2. забросить туда файлы
    3. переименовать их в нужную форму
    imd - папка для хранения уже переименованых папок с файлами
    (переменная intermidiateDir)
    dwsf - папка со сканироваными файлами
    так же нужен счетчик counter для прохождения по списку:
    самих файлов dwcf переменная dirWithScanFiles,
    имен папок список giftf (результат get_info_from_txt_file),

    что бы понять количество файлов, которые нужно разбросать по
    папкам,-нужно находиться в папке со сканами dwsf-
    """
    counter = 0
    for i in os.listdir(dwsf):
        if not os.path.isdir('''{0}\\{1}'''.format(imd,
                                                   giftf[counter].rstrip())):
            #  адрес папки которая будет создана
            new_dir = '''{0}\\{1}'''.format(imd, giftf[counter].rstrip())
            #  создаем папки с нужными именами в промежуточной папке!
            os.mkdir(new_dir)
            #  тепер в только что созданную папку, нужно переместить файл
            shutil.copy("""{0}\\{1}""".format(dwsf, i),
                        '''{0}\\{1}'''.format(new_dir, i))
            #  теперь перемещенный файл нужно переименовать в стандартную форму
            os.rename('''{0}\\{1}'''.format(new_dir, i),
                      '''{0}\\{1}'''.format(new_dir, akt))
            logging.debug("""в промежуточной папке создали {0}\\{1}""".format(
                new_dir, akt))
            #  увеличиваем счетчик на 1 и переходим к следующим парам
            counter += 1
        else:
            logging.info('в промежуточной папке, \
                папка уже есть {0}\\{1}'.format(imd, giftf[counter].rstrip()))
            counter += 1


def place_to_home(imd, dd):
    """
    Раскладывает по местам файлы и папки.

    imd-промежуточная папка, с папками абонентов и файлами внутри ее
    dd-конечная сетевая папка, в которой осуществляется поиск папки района
    """
    for obj in os.listdir(imd):
        # obj-папка объекта в промежуточной папке
        logging.debug('работаем с {0}'.format(obj))
        # определяем район
        if obj[:3] in regionDict:
            for reg in os.listdir(dd):
                # выбираем район по значению ключа и что это папка
                if os.path.isdir('{0}\\{1}'.format(dd, reg)) \
                        and reg.startswith(regionDict[obj[:3]]):
                    logging.debug('выбрали район: {0}'.format(reg))
                    # в папке района просматривем объекты
                    for objReg in os.listdir('{0}\\{1}'.format(dd, reg)):
                        # если объект находим по коду с программы заявка
                        if obj[:9] == objReg[:9]:
                            # если в этой папке нужный нам скан есть
                            if os.path.isfile('{0}\\{1}\\{2}\\{3}'.format(
                                    dd, reg, objReg, akt)):
                                # сматываем удочки
                                logging.info('Файл уже \
                                    был:{0}\\{1}\\{2}\\{3}'.format(
                                    dd, reg, objReg, akt))
                                break
                            # если в папке нужного нам скана нет-копируем его
                            else:
                                shutil.copy('{0}\\{1}\\{2}'.format(
                                    imd, obj, akt),
                                    '{0}\\{1}\\{2}\\{3}'.format(
                                    dd, reg, objReg, akt))
                                logging.info('Создали \
                                    файл:{0}\\{1}\\{2}\\{3}'.format(
                                    dd, reg, objReg, akt))
                                break
                    # если объекта нет по коду с программы заявка
                    else:
                        # копируем весь каталог
                        shutil.copytree('{0}\\{1}'.format(imd, obj),
                                        '{0}\\{1}\\{2}'.format(dd, reg, obj))
                        logging.info('Скопировали папку \
                            с файлом:{0}\\{1}\\{2}\\{3}'.format(
                            dd, reg, obj, akt))
        else:
            # если такого района нет
            logging.warning('ошибка с районом: {0}'.format(obj))
            pass
