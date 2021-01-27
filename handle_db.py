import sqlite3, os


def create_DB(category):

    '''This function creates a database for KeepSafe Application'''
    get_DB = sqlite3.connect('keepsafe.db') # Database name

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
    if(not(os.path.exists('keepsafe.db'))):
        create_DB()
    get_DB = sqlite3.connect('keepsafe.db')
    getCurser = get_DB.cursor()
    getCurser.execute(f"INSERT INTO {category} VALUES ('%s','%s')"%(username,passwd))
    
    get_DB.commit()
    get_DB.close()

def modifyElements(category, username, passwd):
    if(not(os.path.exists('keepsafe.db'))):
        raise RuntimeError('No Databases Found!')
    else:
        get_DB = sqlite3.connect('keepsafe.db')
        getCurser = get_DB.cursor()
        getCurser.execute(f'UPDATE {category} SET password={passwd} WHERE username={username}')
        get_DB.commit()
        get_DB.close()

def delElements(category, username, passwd):
    if(not(os.path.exists('keepsafe.db'))):
        raise RuntimeError('No Databases Found!')
    else:
        get_DB = sqlite3.connect('keepsafe.db')
        getCurser = get_DB.cursor()
        getCurser.execute('DELETE FROM {category} WHERE username={username}')
        get_DB.commit()
        get_DB.close()

def getElements(category):
    if(not(os.path.exists('keepsafe.db'))):
        raise RuntimeError('No Databases Found!')
    else:
        get_DB = sqlite3.connect('keepsafe.db')
        getCurser = get_DB.cursor()
        for row in getCurser.execute(f'SELECT * FROM {category}'):
            print(row)
        get_DB.close()
