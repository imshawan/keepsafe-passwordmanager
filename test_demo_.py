''' This script was developed to check whether if all the functions of the "handle_db.py" are working properly
    This Script has the basic functionality to add, modify, delete and view database
    
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''


import os
import handle_db as db

inp = ""
while inp != 'exit':
    os.system('cls')
    print('1. Create new table')
    print('2. Enter values into a table')
    print('3. Modify elements')
    print('4. View Contents of a specific table')
    print('5. View Tables')
    print('6. Delete elements \n')
    
    inp = input("Input Selection: ")
    if inp.isalpha():
        inp = inp.lower()
    if inp =='1':
        tablename = input("Table Name: ")
        db.create_DB(tablename)
    elif inp == '2':
        tablename = input("Table Name: ")
        usrname = input("Username: ")
        passwd = input("Password: ")
        try:
            db.addElements(tablename, usrname, passwd)
            print('Values Stored!')
            input()
        except RuntimeError as err:
            op = input(err + ", Do you want to create one? Y/N").lower()
            if op == 'y':
                db.create_DB(tablename)
                db.addElements(tablename, usrname, passwd)

    elif inp == '3':
        tablename = input("Table Name: ")
        os.system('cls')
        print('1. Modify Username')
        print('2. Password \n')
        ans = int(input('ENTER: '))
        if ans == 1:
            currUsr = input('Enter current username: ')
            usrname = input('Enter new Username: ')
            db.modifyElements(tablename, 'username', currUsr, usrname)
        elif ans == 2:
            currpass = input('Enter current Password: ')
            passwd = input('Enter new Password: ')
            db.modifyElements(tablename, 'password', currpass, passwd)
        
    elif inp == '4':
        tablename = input("Table Name: ")
        try:
            fields = db.getElements(tablename)
            print(fields)
            input()
        except RuntimeError as err:
            print(err)
            input()

    elif inp =='5':
        tables  = db.getTables()
        for table in tables:
            print(table)
            input()
    elif inp == '6':
        tablename = input("Table Name: ")
        usrname = input("Username: ")
        p = db.delElements(tablename, usrname)
        print(p)
    else:
        pass
        
