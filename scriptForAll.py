import os
import sys
import logging

from bodyKsv import *

"""
удаленный комп - то куда нужно забрасывать \\skv-fs02\kv\Проект\

"""
#remoteFolder = '\\skv-fs02\kv\Проект\'
remoteFolder = 'rem'
csvFile = 'scan.csv'
#scanFolder = '{0}\\{1}'.format(os.getcwd(), 'scan')
scanFolder = 'scan'
#создаем промежуточную папку
#imdFolder = os.mkdir('imd')
imdFolder = 'imd'

#получили список номеров и имен
listWithInfo = getInfoFromCsvFile(csvFile)
#создали нужный нам список чистых имен
nClCSV = nameCleanCSV(listWithInfo)
#создаем промежуточную папку с данными
createIntermidiateDir(imdFolder, scanFolder, nClCSV)
#раскладываем по полкам в удаленной папке
replaceByRegion(imdFolder, remoteFolder)
