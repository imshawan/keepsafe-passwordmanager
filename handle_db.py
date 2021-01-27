import sqlite3, os


def create_DB():
    '''This function creates a database for KeepSafe Application'''
    getConnect = sqlite3.connect('keepsafe.db') # Database name
    getCurser = getConnect.cursor()
	# Create table
    getCurser.execute('''CREATE TABLE KeepSafe(category text, username text, password text)''')
    getConnect.commit()
    getConnect.close()

def addElements(category, username, passwd):
    if(not(path.exists("keepsafe.db"))):
        create_DB()
    pass

def modifyElements(category, username, passwd):
    pass

def delElements(category, username, passwd):
    pass
