#!/usr/bin/env python 2.7

import datetime
import pypostgre as ppg


GROWTH = 'TAXA DE CRESCIMENTO'
PREDICTION = 'PREVISAO PROXIMO MES'
EXHAUSTION = 'PREVISAO DE ESGOTAMENTO'

#==============================================================================

### DEFINING PROGRAMMING CONSTANTS

SHOW_DEBUG = True
SSE_ALPHA = 0.5
DBNAME = 'capacidade'
TYPE_FILENAME = 'types.dat'

#==============================================================================

### EXCEPTION CLASSES

class WrongNameException(Exception):
    pass

#==============================================================================

### FUNCTION DEFINITIONS

    # STANDARDIZE_NAME 
    # STANDARDIZE_COLUMN
    # STANDARDIZE_TABLE
    # STANDARDIZE_DATABASE

#==============================================================================
### STADARDIZE_NAME


def get_path(filename):
    
    s = filename.split('/')
    final = ''

    for i in range(0,len(s)-1):
        final += s[i] + '/'

    return final

def standardize_name(state, num, tb_type, yy=None, mm=None):

    if type(state) is not str or (state != 'B' and state != 'F'):
        raise WrongNameException('Invalid State Name {}. Must be B (Brute) or F (Filtered)'.format(state))

    if type(tb_type) is not str:
        raise WrongNameException('Invalid Table Type Name {}.'.format(tb_type))

    if type(num) is not int:
        raise WrongNameException('Invalid Table Number {}.'.format(tb_type))

    now = datetime.datetime.now()

    if yy is None:
        yy = now.year
    if mm is None:
        mm = now.month
    if yy > 99:
        yy = yy % 100

    if yy < 0 or mm <= 0 or mm > 12:
        raise WrongNameException('Invalid Date {}/{}.'.format(mm, yy))

    sy = str(yy).rjust(2,'0')
    sm = str(mm).rjust(2,'0')
    sn = str(num)

    name = sy + '-' + sm + '-' + tb_type + '-' + sn

    if SHOW_DEBUG is True:
        print 'NAME IS {}'.format(name)

    return name


#==============================================================================
### STADARDIZE_COLUMN

def standardize_column(table, pattern, standart):

    if not pattern.isupper() or not standart.isupper():
        raise WrongNameException('Invalid pattern {} or standart {}. Must be uppercase'.format(pattern, standart))

    columns = ppg.get_columns(DBNAME, table)

    flag = False
    for col in columns:

        if col.upper().rfind(pattern) is -1:
            continue

        if SHOW_DEBUG is True:
            print 'PATTERN {} FIND ON {}'.format(pattern, col)

        ppg.rename_column(DBNAME, table, col, standart)
        flag = True
        break

    if not flag:
        raise WrongNameException('Pattern {} not found on table {}.'.format(pattern, table))


#==============================================================================
### STADARDIZE_TABLE

def standardize_table(table):

    try:
        standardize_column(table, 'NOME', NAME)
    except WrongNameException as w:
        print w
        print 'STANDARDIZATION FAILED ON {} ON {}'.format(NOME, table)

    
    try:
        standardize_column(table, 'OCUPAD', OCCUPIED)
    except WrongNameException as w:
        print w
        print 'STANDARDIZATION FAILED ON {} ON {}'.format(OCCUPIED, table)

    
    try:
        standardize_column(table, 'DISPONIVEL', AVAILABLE)
    except WrongNameException as w:
        print w
        print 'STANDARDIZATION FAILED ON {} ON {}'.format(AVAILABLE, table)

    
    try:
        standardize_column(table, 'TOTAL', TOTAL)
    except WrongNameException as w:
        print w
        print 'STANDARDIZATION FAILED ON {} ON {}'.format(TOTAL, table)


#==============================================================================
### STADARDIZE

def standardize():

    if SHOW_DEBUG is True:
        print 'STARTING STANDARDIZATION OF TABLES'

    tables = ppg.get_tables_names(DBNAME)

    for tb in tables:
        standardize_table(tb)

    if SHOW_DEBUG is True:
        print 'STANDARDIZATION COMPLETE'