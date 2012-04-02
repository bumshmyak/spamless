#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser


def printHeader (names_filename):
    print "@relation web_graph_extended_links_features"
    print ""
    features_count = 0
    for line in open (names_filename, "r"):
        fields = line.strip ().lstrip ('#').split (',')
        # TODO: С названием меры класса тоже можно будет подумать
        fields.append ("relevance")
        features_count = len (fields [2:])
        for field in fields [2:]:
            print "@attribute " + field +  " numeric"
    
    print ""
    print "@data"

    return features_count



if __name__ == "__main__":

    # Надо сконвертировать данные в арфф файл
    # Сначала мы разбираем параметры
    # Пусть csv формат поступает со стандартного входа
    # В качестве флага передается, является ли первый столбец оценками спам/неспам
    # Еще в качестве параметра передаются названия столбцов из файла с фичами
    # 
    parser = OptionParser()
    parser.add_option ("-n", "--names", dest="names_filename",
                       help="file with column names")
    parser.add_option ("-l", "--is_learn", action="store_true", dest="is_learn", default=False,
                       help="input data is learn set and first column is spam probability")

    (options, args) = parser.parse_args()

    names_filename = options.names_filename
    assert isinstance (names_filename, str)

    is_learn = options.is_learn

    # Сначала пишем заголовок (название арфа тоже можно передавать как параметр)
    # Потом атрибуты и в конце данные
    features_count = printHeader (names_filename)

    for lines in sys.stdin:
        # Сплиттим все значения
        fields = lines.strip ().split (" ")
        if (is_learn):
            fields.append (fields.pop (0))
        else:
            fields.append ("?")

        assert (len (fields) == features_count)

        print ",".join (fields)

    # Если выборка обучающая вытаскиваем название из начала и вставляем его в конец
    # Если контрольная - пишем в конец "?"
    # Выводим в стандартный вывод, разделив поля запятыми
