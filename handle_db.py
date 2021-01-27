''' This module includes all the database managements required for KeepSafe - Password Manager
    Designed and developed by Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''

import sqlite3, os

DATABASE = 'keepsafe.db' # Database name

def create_DB(category): # Category is the name of the tables

    '''This function creates a database for KeepSafe Application'''
    get_DB = sqlite3.connect(DATABASE) 

    #IF empty table, then just create the database file and return
    if category == "":
        return
    else:
        getCurser = get_DB.cursor()
            # Create table
        getCurser.execute(f'CREATE TABLE {category}(username text, password text)')
        get_DB.commit()
        get_DB.close()

def addElements(category, username, passwd):
    '''Adds elements to database, pass arguements: category, username and password'''
    if(not(os.path.exists(DATABASE))):
        create_DB("")   # Creates a blank database without any tables
    get_DB = sqlite3.connect(DATABASE)
    getCurser = get_DB.cursor()
    try:
        getCurser.execute(f"INSERT INTO {category} VALUES ('%s','%s')"%(username,passwd))
        get_DB.commit()
        get_DB.close()
        return "success"
    except sqlite3.OperationalError as err:
        raise RuntimeError(err)
        

def modifyElements(category, username, passwd):
    '''Edit/Modifys elements from database, pass arguements: category, username and password'''
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')   # Handles FileNotFoundError
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        try:
            getCurser.execute(f'UPDATE {category} SET password={passwd} WHERE username={username}')
            get_DB.commit()
            get_DB.close()
            return "success"
        except sqlite3.OperationalError as err:
            raise RuntimeError(err)

def delElements(category, username, passwd):
    '''Deletes elements from database, pass arguements: category, username and password'''
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')   # Handles FileNotFoundError
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        try:
            getCurser.execute('DELETE FROM {category} WHERE username={username}')
            get_DB.commit()
            get_DB.close()
            return "success"
        except sqlite3.OperationalError as err:
            raise RuntimeError(err)

def getElements(category):
    '''Returns elements from database, pass arguements: category'''
    fields = []
    if(not(os.path.exists(DATABASE))):
        raise RuntimeError('No Databases Found!')   # Handles FileNotFoundError
    else:
        get_DB = sqlite3.connect(DATABASE)
        getCurser = get_DB.cursor()
        try:
            for row in getCurser.execute(f'SELECT * FROM {category}'):
                fields.append(row)
            get_DB.close()
            return fields
        except sqlite3.OperationalError as err:
            raise RuntimeError(err)
