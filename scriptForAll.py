"""Logic of using function."""
import logging
import os

from bodyKsv import create_intermidiate_dir, get_info_from_txt_file
from bodyKsv import place_to_home

# add base dir
BASE_DIR = os.path.dirname(__file__)
# scan folder
SCAN_DIR = os.path.join(BASE_DIR, 'scan')
# imd folder
IMD_DIR = os.path.join(BASE_DIR, 'imd')
# name of txt file
TXT_FILE = os.path.join(BASE_DIR, 'scan.txt')

if os.path.exists(r'\\skv-fs02\kv\Проект'):
    REMOTE_DIR = r'\\skv-fs02\kv\Проект'
elif os.path.exists(os.path.join(BASE_DIR, 'rem')):
    REMOTE_DIR = os.path.join(BASE_DIR, 'rem')
else:
    os.mkdir(os.path.join(BASE_DIR, 'rem', '17_ксв'))
    REMOTE_DIR = os.path.join(BASE_DIR, 'rem')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logFile.txt', filemode='w'
)

logging.info('программа начала \n\n')
logging.debug('current directory:{0}'.format(BASE_DIR))

if os.path.isfile(TXT_FILE) and os.path.isdir(SCAN_DIR):
    #  создаем промежуточную папку
    if os.path.isdir(IMD_DIR):
        logging.debug('промежуточная папка существовала {0}\\imd'.format(
            BASE_DIR))
        pass
    else:
        os.mkdir('imd')
        logging.info('создали промежуточную папку {0}\\imd'.format(BASE_DIR))

    #  получили список номеров и имен
    logging.debug('get_info_from_txt_file started')
    listWithInfo = get_info_from_txt_file(TXT_FILE)
    logging.info('данные с текстового файла прочлись отлично\n')

    #  создаем промежуточную папку с данными
    logging.debug('create_intermidiate_dir started')
    create_intermidiate_dir(IMD_DIR, SCAN_DIR, listWithInfo)
    logging.info('наполнение промежуточной папки закончили\n')

    #  раскладываем по полкам в удаленной папке
    logging.debug('place_to_home started')
    place_to_home(IMD_DIR, REMOTE_DIR)
    logging.info('наполнение сетевой папки закончили\n')

    logging.info('программа отработала. Пока!!!')
else:
    print("""
        У вас не создана папка со сканкопиями с именем scan, либо
        не создат текстовый файл scan.txt со списком, посмотрите еще раз, и
        потом запускайте программу""")
