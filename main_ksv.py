import sys
from bodyKsv import *

"""
удаленный комп - то куда нужно забрасывать \\skv-fs02\kv\Проект\

"""

while True:
    print("""
	Что нужно сделать? (Введие цифру)

	1. Ввести иформацию в файл;
	2. Показать информацию с файла;
	4. Разбросать сканкопии в промежуточную, а потом в именованые папки;
	5. Закинуть сканкопии или папки в сетевую папку;
	6. Вийти;
	""")
    a = input('> ')
    if int(a) == 6:
        sys.exit()
    elif int(a) == 1:
        dirWithPickleFile = input(
            "введи папку (окружения) с файлом pickle\n> ")
        os.chdir(dirWithPickleFile)
        listInfo = packInPickle()
        n = input("назовите файл pickle\n> ")
        createFilePickle(listInfo, n)
    elif int(a) == 2:
        dirWithPickleFile = input(
            "введи папку (окружения) с файлом pickle\n> ")
        os.chdir(dirWithPickleFile)
        print("Выберите нужный файл")
        c = 1
        for i in os.listdir():
            if i.endswith('pickle'):
                print('{0}. {1}'.format(c, i))
                c += 1

        n = input("> ")
        listInfo = getInformationFromPickleFile('{0}.pickle'.format(n))
        for i in listInfo:
            print(i)
    elif int(a) == 4:
        intermidiateDir = input(
            "Введите адрес промежуточной папки с файлами\n> ")
        dirWithScanFiles = input(
            "Введите адрес папки с отсканированными переименоваными файлами\n> ")
        dirWithPickleFile = input(
            "введи папку (окружения) с файлом pickle\n> ")
        os.chdir(dirWithPickleFile)
        print("Выберите нужный файл")
        c = 1
        for i in os.listdir():
            if i.endswith('pickle'):
                print('{0}. {1}'.format(c, i))
                c += 1

        n = input("> ")
        listInfo = getInformationFromPickleFile('{0}.pickle'.format(n))
        listClean = nameClean(listInfo)
        createIntermidiateDir(intermidiateDir, dirWithScanFiles,
                              listClean)
    elif int(a) == 5:
        intermidiateDir = input(
            "Введите адрес промежуточной папки с файлами\n> ")
        dirDestination = input("Введие адрес сетевой папки\n> ")
        replaceByRegion(intermidiateDir, dirDestination)
    else:
        print("Ввел не то. Давай еще раз")
