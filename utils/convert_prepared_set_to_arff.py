#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Скриптец конвертит данные разделенные пробелом в арфф файл
# Дело в том, что данные, разделенные пробелами, используются
# в матлабовском дата майнинге, 
# а арфф файлы умеет обрабатывать weka
# Разделенные пробелом данные поступают со стандартного входа
# арфф файл пишется в стандартный вывод

import sys
from optparse import OptionParser


# Метод печатает заголовок, заодно считает, сколько элементов в этом заголовке есть
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
    # Разбор входных параметров
    parser = OptionParser()
    parser.add_option ("-n", "--names", dest="names_filename",
                       help="file with column names")
    parser.add_option ("-l", "--is_learn", action="store_true", dest="is_learn", default=False,
                       help="input data is learn set and first column is spam probability")

    (options, args) = parser.parse_args()

    names_filename = options.names_filename
    assert isinstance (names_filename, str)

    is_learn = options.is_learn

    # Сначала пишем заголовок 
    features_count = printHeader (names_filename)

    # Потом пишем значения полей через запятую
    for lines in sys.stdin:
        fields = lines.strip ().split (" ")
        # Для обучающей выборки надо перенести вероятности из начала в конец строки,
        # Для полной - поставить вместо вероятности знак вопроса
        if (is_learn):
            fields.append (fields.pop (0))
        else:
            fields.append ("?")

        assert (len (fields) == features_count)
        print ",".join (fields)

