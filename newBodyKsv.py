import logging
import os
import shutil

#ключ-номер района с программы заявка, значение-номер района в сетевой папке
regionDict = {'25.':'17_', '06.':'05_', '23.':'07_', '11.':'18_'}
# стандратное имя файла
akt = 'акт прийняття внурішніх і зовнішніх мереж.pdf'

def placeToHome(imd, dD):
	"""
	imd-промежуточная папка, с папками абонентов и файлами внутри ее
	dD-конечная сетевая папка, в которой осуществляется поиск папки района
	"""
	for obj in imd:
		#obj-папка объекта в промежуточной папке
		logging.debug('работаем с {0}'.format(obj))
		#определяем район
		if obj[:3] in regionDict:
			for reg in os.listdir(dD):
				#выбираем район по значению ключа и что это папка
				if os.path.isdir(reg) 
				and reg.startswith(regionDict[obj[:3]]):
					logging.debug('выбрали район: {0}'.format(reg))
					#в папке района просматривем объекты
					for objReg in reg:
						#если объект находим по коду с программы заявка
						if obj[:9] == objReg[:9]:
							#если в этой папке нужный нам скан есть
							if os.path.isfile('{0}\\{1}\\{2}\\{3}'.format(dD, reg, objReg, akt)):
								#сматываем удочки
								logging.info('Файл уже был: {0}\\{1}\\{2}\\{3}'.format(
									dD, reg, objReg, akt))
								break
							#если в этой папке нужного нам скана нет - копируем его
							else:
								shutil.copy('{0}\\{1}\\{2}'.format(imd, obj, akt), 
									'{0}\\{1}\\{2}\\{3}'.format(dD, reg, objReg, akt))
								logging.info('Создали файл: {0}\\{1}\\{2}\\{3}'.format(
									dD, reg, objReg, akt))
								break
					#если объекта нет по коду с программы заявка
					else:
						#копируем весь каталог
						shutil.copytree('{0}\\{1}'.format(imd, obj), 
									'{0}\\{1}'.format(dD, reg))
						logging.info('Скопировали папку с файлом: {0}\\{1}\\{2}\\{3}'.format(
									dD, reg, obj, akt))			
			else:
				#если в сетевой папке такого района нет
				logging.warning('в сетевой папке такого района нет')	
		else:
			#если такого района нет
			logging.warning('ошибка с районом: {0}'.format(obj))
			pass
		