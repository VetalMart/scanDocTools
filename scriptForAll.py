"""Docstring in public module."""
import logging
import os

from bodyKsv import create_intermidiate_dir, get_info_from_txt_file
from bodyKsv import place_to_home

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logFile.txt', filemode='w'
)

logging.info('программа начала \n\n')
logging.debug('current directory:{0}'.format(os.getcwd()))
"""
удаленный комп - то куда нужно забрасывать \\skv-fs02\kv\Проект\

"""
remoteFolder = r'\\skv-fs02\kv\Проект'
#  remoteFolder = 'c:\\users\\vitalii.martynenko\\scanDocTools\\rem'
txtFile = 'scan.txt'
cwd = os.getcwd()

if os.path.isfile('{0}\\{1}'.format(cwd, txtFile)) \
   and os.path.isdir('{0}\\scan'.format(cwd)):
    scanFolder = '{0}\\{1}'.format(cwd, 'scan')
    # scanFolder = 'c:\\users\\vitalii.martynenko\\scanDocTools\\scan'
    #  создаем промежуточную папку
    if os.path.isdir('{0}\\imd'.format(cwd)):
        logging.debug('промежуточная папка существовала {0}\\imd'.format(cwd))
        pass
    else:
        imdFolder = '{0}\\{1}'.format(cwd, os.mkdir('imd'))
        logging.info('создали промежуточную папку {0}\\imd'.format(cwd))
        # imdFolder = 'c:\\users\\vitalii.martynenko\\scanDocTools\\imd'

    #  получили список номеров и имен
    logging.debug('get_info_from_txt_file started')
    listWithInfo = get_info_from_txt_file(txtFile)
    logging.info('данные с текстового файла прочлись отлично\n')

    #  создаем промежуточную папку с данными
    logging.debug('create_intermidiate_dir started')
    create_intermidiate_dir('{0}\\imd'.format(cwd),
                            '{0}\\scan'.format(cwd), listWithInfo)
    logging.info('наполнение промежуточной папки закончили\n')

    #  раскладываем по полкам в удаленной папке
    logging.debug('place_to_home started')
    place_to_home('{0}\\imd'.format(cwd), remoteFolder)
    logging.info('наполнение сетевой папки закончили\n')

    logging.info('программа отработала. Пока!!!')
else:
    print("""
        У вас не создана папка со сканкопиями с именем scan, либо
        не создат текстовый файл scan.txt со списком, посмотрите еще раз, и
        потом запускайте программу""")
