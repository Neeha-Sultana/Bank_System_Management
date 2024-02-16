from clrprint import *
import mysql.connector
import csv
print("<^> <^> <^> <^> <^> <^> <^> <^>BANK MANAGEMENT SYSTEM<^> <^> <^> <^> <^> <^> <^> <^>")
while True:
    ps=input("ENTER PASSWORD:")
    a=open("password.txt",'r')
    s=a.read()
    if ps==s:
        print("Valid Password")
        break
    else:
        print("Invalid Password")
    a.close()
#1. SIGN UP
def signup():
    while(True):
        print("~~~~~~~~~~~~~~~~~~~SIGN UP~~~~~~~~~~~~~~~~~~~~~~~~~")
        a = input("USERNAME(more than 3 characters): ")
        if len(a) >= 4:
            pass
        else:
            print("Username doesn't meet minimum length requirements ")
            s = input("Enter Space to go to previous menu and 0 to retry: ")
            if s == " ":
                break
            elif s == "0":
                continue
            else:
                print("Invalid Input")
                a = input("Press Enter to Exit: ")
        f = open(a + ".txt", "w+")
        p = input("PASSWORD: ")
        f.write(p)
        f.close()
        print("--------------SIGNED UP SUCCESSFULLY---------------")
        wa = input("Press any key to go to Main Menu: ")
        break
#2. LOGIN AND BANK DETAILS
def login_and_bank():
    while(True):
            print("~~~~~~~~~~~~~~~~~~~~LOGIN~~~~~~~~~~~~~~~~~~~~~~~~")
            try:
                u = input("USERNAME: ")
                a = open(u + ".txt", "r")
                s = a.read()
                p = input("PASSWORD: ")
                a.close()
            except:
                print("INVALID USERNAME")
                s = int(input("Enter 9 to go to previous menu and 0 to retry: "))
                if s == 9:
                    break
                elif s == 0:
                    continue
                else:
                    print("INVALID INPUT")
                    a = input("Press Enter to Exit: ")
             #IF PASSWORD ENTERED IS CORRECT       
            if p == s:
                print()
                print("---------LOGGED IN SUCCESSFULLY---------------")
                clrprint("=======================================================================================================================",clr="r")
                clrprint("~~~~~~~~~~~~~~~~~~~~~CHOOSE AN OPTION(number)~~~~~~~~~~~~~~~~~~~~~~~~",clr="p")
                clrprint("1. BANK TRANSACTION",clr="r")
                clrprint("2. CHANGE PASSWORD",clr="y")
                clrprint("3. MAIN MENU",clr="g")
                clrprint("4. LOG OUT AND EXIT",clr="default")
                a = int(input("ENTER YOUR CHOICE: "))


                #1.  BANK TRANSACTION
                if a==1:
                    # SOURCE CODE FOR BANKING TRANSACTIONS
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print("************************************BANK TRANSACTION**************************************")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    #creating database
                    cnx=mysql.connector.connect(host="localhost",user="root",passwd="")
                    cursor=cnx.cursor()
                    cursor.execute("create database if not exists bank")
                    cursor.execute("use bank")
                    #creating required tables 
                    cursor.execute("create table if not exists bank_master(acno char(4) primary key,name varchar(30),city char(20),mobileno char(11),balance int(6))")
                    cursor.execute("create table if not exists banktrans(acno char (4),amount int(6),dot date,ttype char(1),foreign key (acno) references bank_master(acno))")
                    cnx.commit()
                    while(True):
                        clrprint("1. CREATE ACCOUNT",clr="p")
                        clrprint("2. DEPOSIT MONEY",clr="b")
                        clrprint("3. WITHDRAW MONEY",clr="y")
                        clrprint("4. DISPLAY ACCOUNT DETAILS",clr="r")
                        clrprint("5. CSV FILING",clr="g")
                        clrprint("6. DELETE ACCOUNT",clr="default")
                        ch=int(input("ENTER YOUR CHOICE: "))
                        # A. PROCEDURE FOR CREATING A NEW ACCOUNT OF THE APPLICANT
                        if(ch==1):
                            print("************CREATE ACCOUNT**************")
                            print("All information prompted are mandatory to be filled")
                            acno=str(input("ENTER ACCOUNT NUMBER:"))
                            name=input("ENTER  CUSTOMER NAME(limit 35 characters): ")
                            city=str(input("ENTER CITY NAME: "))
                            mn=str(input("ENTER MOBILE NO.: "))
                            balance=0
                            cursor.execute("insert into bank_master values('"+acno+"','"+name+"','"+city+"','"+str(mn)+"','"+str(balance)+"')")
                            cnx.commit()
                            print("------Account is successfully created!!!------")
        
                        # B. PROCEDURE FOR UPDATING DETAILS AFTER THE DEPOSITION OF MONEY BY THE APPLICANT
                        elif(ch==2):
                            print("************DEPOSIT MONEY********************")
                            acno=str(input("ENTER ACCOUNT NUMBER:"))
                            dp=int(input("ENTER AMOUNT TO BE DEPOSITED: "))
                            dot=str(input("ENTER DATE OF TRANSACTION(YYYY-MM-DD):"))
                            ttype="d"
                            cursor.execute("insert into banktrans values('"+acno+"','"+str(dp)+"','"+dot+"','"+ttype+"')")
                            cursor.execute("update bank_master set balance=balance+'"+str(dp)+"' where acno='"+acno+"'")
                            cnx.commit()
                            print("------Amount has been deposited successully!!!-------")

                        # C. PROCEDURE FOR UPDATING THE DETAILS OF ACCOUNT AFTER THE WITHDRAWAL OF MONEY BY THE APPLICANT
                        elif(ch==3):
                            print("************WITHDRAW MONEY**************")
                            acno=str(input("ENTER ACCOUNT NUMBER: "))
                            wd=int(input("ENTER AMOUNT TO BE WITHDRAWN: "))
                            dot=str(input("ENTER DATE OF TRANSACTION(YYYY-MM-DD): "))
                            ttype="w"
                            cursor.execute("insert into banktrans values('"+acno+"','"+str(wd)+"','"+dot+"','"+ttype+"')")
                            cursor.execute("update bank_master set balance=balance-'"+str(wd)+"' where acno='"+acno+"'")
                            cnx.commit()
                            print("------Amount has been withdrawn successfully!!!-------")

                        # D. PROCEDURE FOR DISPLAYING THE ACCOUNT OF THE ACCOUNT HOLDER AFTER HE/SHE ENTERS HIS/HER ACCOUNT NUMBER
                        elif(ch==4):
                            print("************DISPLAY ACCOUNT**************")
                            acno=str(input("ENTER ACCOUNT NUMBER:"))
                            cursor.execute("select * from bank_master where acno='"+acno+"'")
                            print("Account Details")
                            for i in cursor:
                                print(i)
                        #E. CSV FILING
                        elif(ch==5):
                            print("*****************CSV FILING******************")
                            def csvwrite_module(dbname,tablename):
                                cursor.execute("select * from {};".format(tablename))
                                tabledata = cursor.fetchall()
                                with open(dbname+".csv", 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerows(tabledata)
                                print("Data written in ",dbname+".csv"," file successfully.")
                                print("Data Printing of ",dbname+".csv"," file now: \n")
                                file = open(dbname+".csv", 'r')
                                for i in file:
                                    print(i)
                                print("Data of", tablename, "table from database",dbname, "is converted to csv file name",dbname+".csv","and printed sucessfully: \n")

                            dbname = "bank"
                            tablename = input("Please enter Table name(bank_master or banktrans): ")
                            csvwrite_module(dbname,tablename)



                        elif (ch==6):
                            print("****************DELETE ACCOUNT*********************")
                            acno=str(input("ENTER THE ACCOUNT NUMBER WHICH HAS TO BE DELETED: "))
                            s=input("Are you sure you want to delete the account(Y/N): ")
                            if s=="y" or s=="Y":
                                cursor.execute("delete from bank_master where acno='"+acno+"'")
                                print("---------Account deleted successfully-----------")
                            else:
                                z=input("Press Enter to go back to Main Menu: ")
                                
                        
                        #F. LOGOUT
                        else:
                            print("************GO BACK**************")
                            y=input("press any key to Go Back: ")
                            continue
                #2. CHANGE PASSWORD
                elif a == 2:
                    print("~~~~~~~~~~~~~~CHANGE PASSWORD~~~~~~~~~~~~~~~~~~~")
                    print("Please fill the details correctly, any wrong input will lead to closing of this application.")
                    u = input("ENTER USERNAME: ")
                    a = open(u + ".txt", "r")
                    s = a.read()
                    a.close()
                    p = input("ENTER CURRENT PASSWORD: ")
                    if p == s:
                        np = input("ENTER NEW PASSWORD: ")
                        a = open(u + ".txt", "w+")
                        a.write(np)
                        a.close()
                        print("-----------------PASSWORD CHANGED SUCCESSFULLY---------------")
                        t = input("Press enter to return to Main Menu")
                        print()
                        break
                    else:
                        print("You have entered wrong password. Press Enter to exit")
                        exit()

                # 3. MAIN MENU
                elif a == 3:
                        s = input("Press Enter to go to Main Menu")
                        print()
                        break

                # 4. LOG OUT AND EXIT
                elif a == 4:
                    print("--------------LOGGED OUT SUCCESSFULLY------------------")
                    print("Press enter to exit.")
                    a = input()
                    exit()

                # FOR INVALID INPUT
                else:
                    s = input("Enter SPACE to go to previous Menu and 0 to retry")
                    if s == " ":
                        break
                    elif s == "0":
                        continue
                    else:
                        print("Invalid Input")
                        a = input("Press Enter to Exit...")
                        exit()

            # IF PASSWORD ENTERED IS WRONG 
            else:
                    a = input("You have entered wrong password. press enter to retry")
                    continue
#EXIT
def exitfunc():
     while(True):
            s = input("Do you really want to quit program.(Y/N): ")
            if s=="Y" or s=="y":
                quit()
            elif s=="n" or s=="N":
                break
            else:
                print("Invalid Input.")
                continue
while(True):
    clrprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",clr="y")
    clrprint("                             WELCOME TO CORPORATION BANK!!!",clr="r")
    clrprint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",clr="y")
    clrprint("                              ***** MAIN MENU *****",clr="m")
    clrprint("PLEASE CHOOSE AN OPTION(only digit)",clr="r")
    clrprint("1. SIGN UP",clr="g")
    clrprint("2. LOGIN",clr="m")
    clrprint("3. EXIT",clr="y")
    opt = int(input("ENTER YOUR CHOICE: "))
    if opt==1:
        signup()
    elif opt==2:
        login_and_bank()
    elif opt==3:
        exitfunc()
