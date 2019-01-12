import os
import sys
import logging

from bodyKsv import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
"""filename='programInfo.txt', filemode='w',"""

logging.info('scriptForAll started')
"""
удаленный комп - то куда нужно забрасывать \\skv-fs02\kv\Проект\

"""
#remoteFolder = '\\skv-fs02\kv\Проект\'
remoteFolder = 'c:\\users\\vitalii.martynenko\\scanDocTools\\rem'
txtFile = 'scan.txt'
#scanFolder = '{0}\\{1}'.format(os.getcwd(), 'scan')
scanFolder = 'c:\\users\\vitalii.martynenko\\scanDocTools\\scan'
#создаем промежуточную папку
#imdFolder = os.mkdir('imd')
imdFolder = 'c:\\users\\vitalii.martynenko\\scanDocTools\\imd'

#получили список номеров и имен
logging.info('getInfoFromTxtFile started')
listWithInfo = getInfoFromTxtFile(txtFile)
logging.info('getInfoFromTxtFile finished')

#создаем промежуточную папку с данными
logging.info('createIntermidiateDir started')
createIntermidiateDir(imdFolder, scanFolder, listWithInfo)
logging.info('createIntermidiateDir finished')

#раскладываем по полкам в удаленной папке
logging.info('replaceByRegion started')
replaceByRegion(imdFolder, remoteFolder)
logging.info('replaceByRegion finished')
