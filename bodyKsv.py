"""Function for sorting script."""
import logging
import os
import shutil

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

        # новая папка в промежуточной папке
        new_imd_dir = os.path.join(imd, giftf[counter].rstrip())
        # файл скана в папке сканов
        scan_file = os.path.join(dwsf, i)
        # перемещенный скан
        replaced_file = os.path.join(new_imd_dir, i)
        # переименованый скан
        renamed_file = os.path.join(new_imd_dir, akt)

        if not os.path.isdir(new_imd_dir):
            #  создаем папки с нужными именами в промежуточной папке!
            os.mkdir(new_imd_dir)
            #  тепер в только что созданную папку, нужно переместить файл
            shutil.copy(scan_file, replaced_file)
            #  теперь перемещенный файл нужно переименовать в стандартную форму
            os.rename(replaced_file, renamed_file)
            logging.debug("""в промежуточной папке создали {0}""".format(
                renamed_file))
            #  увеличиваем счетчик на 1 и переходим к следующим парам
            counter += 1
        else:
            logging.info('в промежуточной папке, \
                папка уже есть {0}'.format(new_imd_dir))
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

                # папка района
                reg_dir = os.path.join(dd, reg)

                # выбираем район по значению ключа и что это папка
                if os.path.isdir(reg_dir) and reg.startswith(
                        regionDict[obj[:3]]):
                    logging.debug('выбрали район: {0}'.format(reg))
                    # в папке района просматривем объекты
                    for objReg in os.listdir(reg_dir):

                        # имя файла в папке сетевай/район/абонент
                        end_file_name = os.path.join(dd, reg, objReg, akt)
                        # файл по адресу промежуточная/абонент/файл
                        source_file = os.path.join(imd, obj, akt)
                        # папка промежуточная/абонент
                        obj_dir = os.path.join(imd, obj)
                        # перемещенная папка абонента сетевая/район/абонент
                        replaced_obj_dir = os.path.join(dd, reg, obj)
                        # если объект находим по коду с программы заявка

                        if obj[:9] == objReg[:9]:
                            # если в этой папке нужный нам скан есть
                            if os.path.isfile(end_file_name):
                                # сматываем удочки
                                logging.info('Файл уже был:{0}'.format(
                                    end_file_name))
                                break
                            # если в папке нужного нам скана нет-копируем его
                            else:
                                shutil.copy(source_file, end_file_name)
                                logging.info('Создали файл:{0}'.format(
                                    end_file_name))
                                break

                    # если объекта нет по коду с программы заявка
                    else:
                        # копируем весь каталог
                        shutil.copytree(obj_dir, replaced_obj_dir)
                        logging.info('Скопировали папку \
                            с файлом:{0}'.format(os.path.join(
                            replaced_obj_dir, akt)))
        else:
            # если такого района нет
            logging.warning('ошибка с районом: {0}'.format(obj))
            pass
