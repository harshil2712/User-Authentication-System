#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import os
# os.getcwd()


# In[2]:


# os.mkdir('hello')


# In[3]:


## PyQt
## tkinter


# ## User Authentication System

# #### feature list
# - SignUp
#     - username (will be unique)
#     - email (will be unique)
#     - password
#     - personal details
#         - name
#         - phone number
#         - dob
#     - Password Recovery
#         - backupcodes (autogenerated - 5)
#         - Security Question - 2 
#         - otp from phone number (twilio)
# - SignIn
#     - forgot password
#         - password recovery
#     - username
#     - password
#     - change password
#     - profile
#     
# - Database

# In[1]:


def initializeDatabase():
    db = pd.read_csv('database.csv')
    return db

# initializeDatabase()


# In[2]:


# df.loc[len(df)] = [123, 'harshil', 'harshil@gmail.com','Qwerty@123','Harshil Bansal','9354328855','27/12/1996','ASDF123','Angel Priya','Cat']
# df.to_csv('database.csv', index = False)


# In[3]:


def checkPasswordStrength(passw):
    return passw


# In[4]:


def getPersonalDetails():
    # name, phone, dob
    name = input('Enter name: ').title()
    while True:
        phone = input('Enter Phone number: +91')
        if len(phone) != 10:
            print('Invalid')
        else:
            break
    dob = input('Enter Data of Birth in DD/MM/YYYY format: ')
    return name, phone, dob


# In[5]:


def genBackUpCode():
    # 'ASDF123'
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digit = '0123456789'
    import random as r
    s = ''
    for i in range(4):
        s += r.choice(alpha)
    for i in range(3):
        s += r.choice(digit)
    return s

# genBackUpCode()


# In[6]:


def getSecurityAnswers():
    while True:
        ans1 = input('Your favourite city: ').lower()
        ans2 = input('Your favourite animal: ').lower()
        con = input('Do you want to lock these answers? y/n: ')
        if con.lower() == 'y':
            return ans1, ans2
        else:
            print('Enter again...')
            
# getSecurityAnswers()


# In[7]:


def getUserID():
    db = initializeDatabase()
    return len(db) + 1
    
#     if len(db) == 0: return 1
#     else:
#         last = db['userId'].loc[len(db)-1]
#         return last + 1
    
# getUserID()


# In[8]:


def updateDatabase(db):
    db.to_csv('database.csv', index = False)
    print('Update Successful')
    return


# In[21]:


def getSystemDateTime():
    from datetime import datetime
    current_datetime = datetime.now()
    return current_datetime.strftime("%d-%m-%Y %H:%M:%S")

# getSystemDateTime()


# In[ ]:


def checkEmailFormat(email):
    something@something.com


# In[9]:


def forgotPassword(username):
    choose = input('''
    Enter 1 to recover password using Security Question
    Enter 2 to recover password using backup Codes
    : ''')
    db = initializeDatabase()
    if choose == '1':
        storedans1 = db.SecAns1.loc[db[db.username == username].index].tolist()[0]
        storedans2 = db.SecAns2.loc[db[db.username == username].index].tolist()[0]
        for i in range(3):
            ans1 = input('Your favourite city: ').lower()
            ans2 = input('Your favourite animal: ').lower()
            if ans1 == storedans1 and ans2 == storedans2:
                passw = input('Enter a strong password: ')
                passw = checkPasswordStrength(passw)
                db.password.loc[db[db.username == username].index] = passw
                updateDatabase(db)
                return True
            else:
                print('Wrong answers... please try again...')
        return False
    elif choose == '2':
        storedcode = db.backup_code.loc[db[db.username == username].index].tolist()[0]
        for i in range(3):
            code = input('Enter your Backup Code: ')
            if code == storedcode:
                passw = input('Enter a strong password: ')
                passw = checkPasswordStrength(passw)
                db.password.loc[db[db.username == username].index] = passw
                updateDatabase(db)
                return True
            else:
                print('Wrong answers... please try again...')
        return False
    else:
        return False
    
            

# forgotPassword('harshil')


# In[16]:


def signUp():
    print('Welcome to KRMU Sign Up Portal')
    status = 1
    while status == 1:
        userName = input('Enter a new username: ').lower()
        if userName == '0':
            return 'Failed'
        db = initializeDatabase()
        print(db)
        if userName not in db.username.tolist():
            email = input('Enter email address: ').lower()
            checkEmailFormat(email)
            if email not in db.email.tolist():
                status = 0
                passw = input('Enter a strong password: ')
                passw = checkPasswordStrength(passw)
                name, phone, dob = getPersonalDetails()
                code = genBackUpCode()
                print(f'Bhai, your backup code is {code}')
                ans1, ans2 = getSecurityAnswers()
                userid = getUserID()
                dateTime = getSystemDateTime()
                db.loc[len(db)] = [userid, userName, email, passw, name, phone, dob, code, ans1, ans2, dateTime]
                updateDatabase(db)
                return 'Successful'
            else:
                print('Email already exists. please try again... or Press 0 to Exit')
        else:
            print('Username already in use. Please try another... or Press 0 to Exit')
            
# signUp()


# In[11]:


def signIn():
    print('Welcome to KRMU Sign In Portal')
    while True:
        username = input('Enter your username: ')
        if username == '0':
            return 'Failed'
        db = initializeDatabase()
        print(db)
        if username in db.username.tolist():
            for i in range(3):
                passw = input('Enter your password: ')
                storedpassw = db.password.loc[db[db.username == username].index].tolist()[0]
                if passw == storedpassw:
                    return 'Successful'
                    # profile()
                    return
                else:
                    print(f'Incorrect password. {2-i} chances left. Please try again...')
            print('SignIn Failed')
            fp = input('''
            Enter 1 to Forgot password: 
            Enter any key to Exit
            : ''')
            if fp == '1':
                if not(forgotPassword(username)):
                    return 'Failed'
            else:
                return 'Failed'
        else:
            print('username not registered.. Please try again... or Press 0 to Exit')
                
# signIn()


# In[13]:


def homepage():
    global pd
    import pandas as pd
    while True:
        mode = input('''
        Enter 1 for SignUp
        Enter 2 for SignIn
        Enter 0 to Exit
        : ''')
        if   mode == '1': print('SignUp', signUp())
        elif mode == '2': print('SignIn', signIn())
        elif mode == '0':
            print('Thank you...')
            break
        else:
            print('Invalid Input... Please try again...')
            
homepage()


# In[36]:


# df.drop(index=df.index, inplace = True)
# df.to_csv('database.csv', index = False)


# In[20]:


db


# In[ ]:


print('Hello')


# ### VCS: Version Control System

# In[ ]:




