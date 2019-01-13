import os
import shutil
import logging

#стандратное имя файла
akt = 'акт прийняття внурішніх і зовнішніх мереж.pdf'
#ключ-номер района с программы заявка, значение-номер района в сетевой папке
regionDict = {'25.':'17_', '06.':'05_', '23.':'07_', '11.':'18_'}

def getInfoFromTxtFile(source):
    """
    функция которая импортирует данные с txt файла
    возвращает список с данными c чистыми имиенами
    """
    with open(source, 'r') as txtfile:
        data = [' '.join(i.rstrip('\n').split(' ')[1:]) for i in txtfile]
        return data

def createIntermidiateDir(imd, dwsf, gIFTF):
    """
    функция которая должна:
    1. создать папки
    2. забросить туда файлы
    3. переименовать их в нужную форму
    imd - папка для хранения уже переименованых папок с файлами
    (переменная intermidiateDir)
    dwsf - папка со сканироваными файлами 
    так же нужен счетчик counter для прохождения по списку: 
    самих файлов dwcf переменная dirWithScanFiles, 
    имен папок список gIFTF (результат getInfoFromTxtFile), 

    что бы понять количество файлов, которые нужно разбросать по 
    папкам,-нужно находиться в папке со сканами dwsf-
    """
    counter = 0
    for i in os.listdir(dwsf):
        # адрес папки которая будет создана
        newDir = '{0}\\{1}'.format(imd, gIFTF[counter].rstrip())
        # создаем папки с нужными именами в промежуточной папке!
        os.mkdir(newDir)
        # тепер в только что созданную папку, нужно переместить файл
        shutil.copy("{0}\\{1}".format(dwsf, i),
                    '{0}\\{1}'.format(newDir, i))
        # теперь перемещенный файл нужно переименовать в стандартную форму
        os.rename('{0}\\{1}'.format(newDir, i),
                  '{0}\\{1}'.format(newDir, akt))
        logging.debug("""в промежуточной папке создали \
            \r\t{0}\n\t\t\\{1}""".format(newDir, akt))
        # увеличиваем счетчик на 1 и переходим к следующим парам
        counter += 1

def placeToHome(imd, dD):
    """
    imd-промежуточная папка, с папками абонентов и файлами внутри ее
    dD-конечная сетевая папка, в которой осуществляется поиск папки района
    """
    for obj in os.listdir(imd):
        #obj-папка объекта в промежуточной папке
        logging.debug('работаем с {0}'.format(obj))
        #определяем район
        if obj[:3] in regionDict:
            for reg in os.listdir(dD):
                #выбираем район по значению ключа и что это папка
                if os.path.isdir('{0}\\{1}'.format(dD,reg)) \
                and reg.startswith(regionDict[obj[:3]]):
                    logging.debug('выбрали район: {0}'.format(reg))
                    #в папке района просматривем объекты
                    listDir = os.listdir('{0}\\{1}'.format(dD,reg))
                    for objReg in os.listdir('{0}\\{1}'.format(dD,reg)):
                        #если объект находим по коду с программы заявка
                        if obj[:9] == objReg[:9]:
                            #если в этой папке нужный нам скан есть
                            if os.path.isfile('{0}\\{1}\\{2}\\{3}'.format(
                                dD, reg, objReg, akt)):
                                #сматываем удочки
                                logging.info('''Файл уже был: 
                                    {0}\\{1}\\{2}\\{3}'''.format(
                                        dD, reg, objReg, akt))
                                break
                            #если в папке нужного нам скана нет-копируем его
                            else:
                                shutil.copy('{0}\\{1}\\{2}'.format(
                                    imd, obj, akt), 
                                    '{0}\\{1}\\{2}\\{3}'.format(
                                        dD, reg, objReg, akt))
                                logging.info('Создали файл: \
                                    {0}\\{1}\\{2}\\{3}'.format(
                                    dD, reg, objReg, akt))
                                break
                    #если объекта нет по коду с программы заявка
                    else:
                        #копируем весь каталог
                        shutil.copytree('{0}\\{1}'.format(imd, obj), 
                                    '{0}\\{1}\\{2}'.format(dD, reg, obj))
                        logging.info('Скопировали папку с файлом: \
                            {0}\\{1}\\{2}\\{3}'.format(
                                    dD, reg, obj, akt))           
        else:
            #если такого района нет
            logging.warning('ошибка с районом: {0}'.format(obj))
            pass
