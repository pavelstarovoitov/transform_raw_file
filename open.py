#!/usr/bin/python3

import time
import xlsxwriter
import argparse
import os
import mimetypes
import csv
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
try:
    StrLen = int(config["DEFAULT"]['StrLen'])
except KeyError:
    StrLen = 318


def getfilename(path, format):
    if os.path.isdir(os.path.dirname(path)):
        file = 'result_' + os.path.split(path)[1] + format
        file = os.path.join(os.path.dirname(path), file)
        return file
    else:
        return 1


def bintocsv(path, hexdata):
    file = getfilename(path, '.csv')
    with open(file, mode='w') as outfile:
        data_writer = csv.writer(
            outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in hexdata:
            data_writer.writerow(row)


def bintotext(path, hexdata):
    file = getfilename(path, '.txt')
    with open(file, 'w') as out:
        for row in hexdata:
            str_row = " ".join([s for s in row])
            out.write(str_row + '\n')


def writer(path, hexdata):
    file = getfilename(path, '.xlsx')
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    for row_num, row_data in enumerate(hexdata):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num, col_num, col_data)
    workbook.close()


def gethexdata(path):
    if os.path.exists(path):
        try:
            with open(path, 'r+b') as raw:
                hexdata = raw.read().hex()
        except IsADirectoryError:
            print('it is a directory')
    else:
        print('path', path)
        print('file do not exist')
        return 1
    hexdata_table = []
    for li in range(0, len(hexdata), StrLen):
        hexdata_col = [hexdata[i:i+2] for i in range(li, li+StrLen, 2)]
        hexdata_table.append(hexdata_col)
    return hexdata_table


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', action='store', type=str,
                        required=False,
                        help="path to input data file with binary data")
    parser.add_argument('--dir', action='store', type=str, required=False,
                        help="path to directory with binary data files")
    parser.add_argument('--onefile', action='store', type=bool,
                        required=False,
                        help="if flag true reluts saved in one big file")
    parser.add_argument('--format', action='store', type=str, required=False,
                        help='format for output data file, \
                            choose txt csv of xlsx')
    args = parser.parse_args()
    return args


def main():

    args = args_parser()

    start = time.perf_counter()
    print(f'{0.000:0.4}', 'transformation start')

    if args.file:
        if not os.path.isfile(args.file):
            print('please input path to file')
        path = (os.path.join(os.getcwd(), args.file))
        hexdata_table = gethexdata(path)
        if args.format == 'txt':
            bintotext(path=path, hexdata=hexdata_table)
        if args.format == 'csv':
            bintocsv(path=path, hexdata=hexdata_table)
        if not args.format or args.format == 'xlsx':
            writer(path=path, hexdata=hexdata_table)

    if args.dir:
        if not os.path.isdir(args.dir):
            print('please input path to dir')
        dirpath = os.path.abspath(args.dir)
        files = os.listdir(dirpath)
        if (args.onefile):
            onefile = []
        for file in files:
            mime = mimetypes.guess_type(file)[0]
            file = os.path.join(dirpath, file)
            if mime or os.path.isdir(file):
                continue
            hexdata_table = gethexdata(file)
            if(args.onefile):
                for line in hexdata_table:
                    onefile.append(line)
            if not args.onefile and args.format == 'txt':
                bintotext(path=file, hexdata=hexdata_table)
            if not args.onefile and args.format == 'csv':
                bintocsv(path=file, hexdata=hexdata_table)
            if not args.onefile and (args.format == 'xlsx' or not args.format):
                writer(path=file, hexdata=hexdata_table)

        if args.onefile and args.format == 'txt':
            commonfile = os.path.join(os.path.dirname(file), 'common')
            bintotext(path=commonfile, hexdata=onefile)
        if args.onefile and args.format == 'csv':
            commonfile = os.path.join(os.path.dirname(file), 'common')
            bintocsv(path=commonfile, hexdata=onefile)
        if args.onefile and (args.format == 'xlsx' or not args.format):
            commonfile = os.path.join(os.path.dirname(file), 'common')
            writer(path=commonfile, hexdata=onefile)
    elapsed = time.perf_counter() - start
    print(f'{elapsed:0.4}', 'end')


if __name__ == "__main__":
    main()
