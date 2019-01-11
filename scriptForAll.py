import os
import sys
import logging

from bodyKsv import *

"""
удаленный комп - то куда нужно забрасывать \\skv-fs02\kv\Проект\

"""
#remoteFolder = '\\skv-fs02\kv\Проект\'
remoteFolder = 'rem'
txtFile = 'scan.txt'
#scanFolder = '{0}\\{1}'.format(os.getcwd(), 'scan')
scanFolder = 'scan'
#создаем промежуточную папку
#imdFolder = os.mkdir('imd')
imdFolder = 'imd'

#получили список номеров и имен
listWithInfo = getInfoFromTxtFile(txtFile)
#создали нужный нам список чистых имен
#создаем промежуточную папку с данными
createIntermidiateDir(imdFolder, scanFolder, listWithInfo)
#раскладываем по полкам в удаленной папке
replaceByRegion(imdFolder, remoteFolder)
