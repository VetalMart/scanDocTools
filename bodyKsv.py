import os
import shutil
import pickle
import csv
import logging

#logging.basicConfig(filename='programInfo.txt', level=logging.DEBUG, 
 #   format='%(asctime)s - %(levelname)s - %(message)s')


"""
#рабочие адреса папок 
dirWithPickleFile = input("папка (окружения) с файлом pickle> ")
dirWithScanFiles = input("папка с отсканированными файлами> ")
intermidiateDir = input("папка для переименованых папок с файлами> ")
dirDestination = input("корневая папка, с районами> ")
"""
# стандратное имя файла
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

def createIntermidiateDir(imd, dwsf, nCl):
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
    имен папок список nCl (результат nameClean), 

    что бы понять количество файлов, которые нужно разбросать по 
    папкам,-нужно находиться в папке со сканами dwsf-
    """
    counter = 0
    for i in os.listdir(dwsf):
        # адрес папки которая будет создана
        newDir = '{0}\\{1}'.format(imd, nCl[counter].rstrip())
        # создаем папки с нужными именами в промежуточной папке!
        os.mkdir(newDir)
        # тепер в только что созданную папку, нужно переместить файл
        shutil.copy("{0}\\{1}".format(dwsf, i),
                    '{0}\\{1}'.format(newDir, i))
        # теперь перемещенный файл нужно переименовать в стандартную форму
        os.rename('{0}\\{1}'.format(newDir, i),
                  '{0}\\{1}'.format(newDir, akt))
        logging.debug("""в промежуточной папке создали 
            {0}\\{1}""".format(newDir, akt))
        # увеличиваем счетчик на 1 и переходим к следующим парам
        counter += 1

def replaceByRegion(imd, dD):
    """
    проверочно-перемещательная функция.
    1. переместиться в нужное окружение - папку с переименоваными 
    файлами
    2. проходом for сначала прочесать свою папку, потом сетевую
    с районами и найти нужный нам район.
    3. проходом for по папке с районом и если есть нужная - то 
    заходим в нее, если нет - создаем;  
    4. если нашлось и совпали - копируем только файл с исходной
    5. если не нашлось в сетевой папке совпадения - копируем всю папку
    
    lFolders = []
    lFiles = []
    lPass = []
    """
    logging.debug('аргументы функции replaceByRegion промежуточная: {0}\
     сетевая: {1}'.format(imd, dD))
    def checkRegion(iter1, iter2, str1, str2, name, folderD, folderS):
        """
        iter1-имя папки объектa в промежуточной папки
        iter2-имя папки района в сетевой папке
        str1-код района нормальный
        str2-дибильный код района в сетевой папке
        name-глобальная переменная - конечное имя акта
        folderD-конечная сетевая папка, в которой осуществляется поиск 
                папки района
        folderS-промежуточная папка, с папками абонентов и файлами внутри
        ее прототип дальше в коментах, как что и куда
        """
        # проверка региона
        logging.debug('checkRegion: iter1: {0} iter2: {1}'.format(iter1, iter2))
        
        if (iter1.startswith(str(str1))
                and iter2.startswith(str(str2))):
            # переходим в нужную папку района и проходим по ней
            # заходим в нужный нам район сетевой папки
            # проверка полного совпадения имени папки
            if os.path.isdir('{0}\\{1}\\{2}'.format(
                    folderD, iter2, iter1)):
                # если да - проверка совпадения файла
                if os.path.isfile('{0}\\{1}\\{2}\\{3}'.format(
                        folderD, iter2, iter1, name)):
                    # если да - сматываем удочки

                    logging.info('{0}\\{1}\\{2}\\{3} - этот файл уже существовал;'.format(folderD, iter2, iter1, name))
                    #lPass.append('{0}\\{1}\\{2}\\{3}'.format(
                    #    folderD, iter2, iter1, name))
                    pass
                else:
                    # если нет - копируем файл в папку
                    shutil.copy('{0}\\{1}\\{2}'.
                                format(folderS, iter1, name),
                                '{0}\\{1}\\{2}\\{3}'.format(
                                    folderD, iter2, iter1, name))
                    logging.info('папка - {0}\\{1}\\{2} существовала, файл - {3} добавили;'.format(
                        folderD, iter2, iter1, name))
                    #lFiles.append('{0}\\{1}\\{2}\\{3}'.format(
                    #    folderD, iter2, iter1, name))
            else:
                os.chdir('{0}\\{1}'.format(folderD, iter2))
                # если полного совпадения имени папки нет - делаем
                # проверку совпадения частичного имени папки [0:9]
                for k in os.listdir():
                    # проверяем частичные совпадения по коду программы заявка
                    if (k[0:9] == iter1[0:9]):
                        # если да - копируем файл
                        shutil.copy('{0}\\{1}\\{2}'.
                                    format(folderS, iter1, name),
                                    '{0}\\{1}\\{2}\\{3}'.format(
                                        folderD, iter2, k, name))
                        logging.info('папка - {0}\\{1}\\{2} совпала по номеру с программы заявка, файл - {3} добавили;'.format(
                            folderD, iter2, k, name))
                        #lFiles.append('{0}\\{1}\\{2}\\{3}'.format(
                        #    folderD, iter2, k, name))
                        break
                else:
                    # если нет - копируем в корневую папку все дерево
                    shutil.copytree('{0}\\{1}'.format(folderS, iter1), 
                        '{0}'.format(iter1))
                    logging.info('создали каталок с файлом -{0}\\{1}\\{2}\
                        \\{3}'.format(folderD, iter2, iter1, name))
                    #lFolders.append('{0}\\{1}\\{2}\\{3}'.format(
                    #    folderD, iter2, iter1, name))

    # проходим по папке с переименоваными папками
    for i in os.listdir(imd):
        """
        проходим по корневой сетевой папке с районами
        dD = dirDestination и если находим подходящий район
        заходим в эту папку, и делаем проверку на наличе подходящей 
        папки объекта. Если есть - то копируем в нее только файл, 
        если нет - то копируем всю папку с файлом 
        i-папка объекта в промежуточной папке
        j-папка района в сетевой папке
        """
        for j in os.listdir(dD):
            if not j.endswith(' - Ярлык.lnk'):
                checkRegion(i, j, '25.', '17_', akt, dD, imd)
                checkRegion(i, j, '06.', '05_', akt, dD, imd)
                checkRegion(i, j, '23.', '07_', akt, dD, imd)
                checkRegion(i, j, '11.', '18_', akt, dD, imd)

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
                                logging.info('''Создали файл: 
                                    {0}\\{1}\\{2}\\{3}'''.format(
                                    dD, reg, objReg, akt))
                                break
                    #если объекта нет по коду с программы заявка
                    else:
                        #копируем весь каталог
                        shutil.copytree('{0}\\{1}'.format(imd, obj), 
                                    '{0}\\{1}\\{2}'.format(dD, reg, obj))
                        logging.info('''Скопировали папку с файлом: 
                            {0}\\{1}\\{2}\\{3}'''.format(
                                    dD, reg, obj, akt))           
        else:
            #если такого района нет
            logging.warning('ошибка с районом: {0}'.format(obj))
            pass