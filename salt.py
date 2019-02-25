import os

def splitName(s):
    """функция для деланья из полных имен-фамилий с инициалами"""
    l = s.split('\n')
    l.remove('')
    lN = []
    for i in l:
        j = i.split(' ')
        if len(j) == 2:
            lN.append('{0}{1}'.format(j[1], j[0]))
        else:
            lN.append('{0}.{1}.{2}'.format(j[1][0], j[2][0], j[0]))
    return lN

"""
Код для фильтрации текста из бухгалтеркого файла, который сбрасивает
Левикина.
"""
def obj_with_vrez(s) -> dict:
    """Виделяет с текста объекты в которых выполнена врезка.

        И стандартные и не стандартные.
        s - сырой текст с екселя;
    """
    raw_list = s.split('03217')  # делим на объекты по коду, для всех один 
    # делим список на три части: номер, адрес, остальная инфа
    temp_list = [i.split('\n', maxsplit=2) for i in raw_list]
    vrez_dict = {}      # словарь с объектами где есть врезка 
    # отбираем объекты где есть врезка
    for i in temp_list:
        for j in i:
            # 60500ID - код врезки
            # 60600ID - код тех.надзора
            # с врезкой, без тех.надзора
            if ('60500ID' in j 
                and '60600ID' not in j):
                # ключ - номер, значение - адрес; 
                # обрезаем пробелы
                vrez_dict.setdefault(i[0].strip(), i[1].strip())

    return vrez_dict

def st_obj(d, standart=0) -> dict:
    """Отбирает объекты внешнего присоединения.

    d - словарь со всеми присоединениями; 
    standart - флаг: если 1 - стандартное; 
                     если 0 - нестандартное(по умолчанию);
    """
    if standart==1:
        check_type = '250133'   # код стандартного присоединения
    elif standart==0:
        check_type = '250233'   # код нестандартного присоединения
    
    temp_dict = {}              # промежуточный словарь
    
    for k, v in d.items():
        if check_type in k:
            temp_dict.setdefault(k, v)

    return temp_dict

def whats_in_folder(d, needs=0) -> dict:
    """Возвращает необходимое. 

    Функция шерстит папку Кравченко, какие там акты по нестандартним есть,
    и в зависимости от этого, может потребоваться следующая инфа:
    1. Какие акты есть;
    2. Каких актов нет;

    Во избежании лишнего гемора с переходами по файловой системе, 
    мы подразумеваем что уже находимся в папке с екселевскими файлами, 
    по нестандартному присоединению, которые делала Кравченко;

    d - словарь с объектами с нестандартным присоединением;
    needs - флаг: 0 - поиск в папке, каких актов нет;
                  1 - поиск в папке, какие акты есть;  
    """
    # удаляем расширения, подразумеваем что они еще .xls
    # и создаем сразу список
    set_folder_files = {i.rstrip('.xls') for i in os.listdir()}
    temp_dict = {}
    diff = set(d).difference(set_folder_files)
    inter = set(d).intersection(set_folder_files)
    if needs==0:
        for i in diff:
            temp_dict.setdefault(i, d[i])            
    elif needs==1:
        for i in inter:
            temp_dict.setdefault(i, d[i])             

    return temp_dict

def dict_to_txt(d)->None:
    """Печатает в текстовый файл словарь
    
    - печатает с кодировкой cp1251 для windows;
    - нужно будет ввести имя файла.
    - в файле информация идет так: "Ключ" {табуляция} "значение" - для 
        удобства вставки в ексель;

    d - словарь который нужно завернуть в файл"""
    name = input("Enter file name(no extention)> ")
    with open('{0}.txt'.format(name), 'w', encoding='cp1251') as f:
        for k, v in d.items():
            f.write('{0}\t{1}\n'.format(k, v))
