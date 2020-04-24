import os

class Account:
    def __init__(self,aNumb,aName,aType):
        self.aNumb = aNumb
        self.userName = aName
        self.aType = aType
        self.aBalance = 0
    
    def deposit(self,amount):
        self.aBalance += int(amount)
        
    def withdraw(self,amount):
        self.aBalance -= int(amount)
        
    #Getters
    def getBalance(self):
        return self.aBalance
    
    def getAccNumb(self):
        return self.aNumb
    
    def getName(self):
        return self.userName
    
    def getAccType(self):
        return self.aType    
    
    #Setters
    def setBalance(self,newBalance):
        self.aBalance
    
    def setAccNumb(self,newNumb):
        self.aNumb = newBalance
    
    def setAccName(self,newName):
        self.userName = newName
    
    def setAccType(self,newType):
        self.aType = newType  
        
    def dispAccount(self):
        print("=== Account Status ===")
        print("Account Number: ", self.getAccNumb())
        print("Account Holder: ", self.getName())
        print("Account Type: " , self.getAccType())
        print("Account Balance: ", self.getBalance()) 
        
def createAccount(fileName):
    """return an account object and """
    print("+++ NEW ACCOUNT FORM +++" )
    acNumb = int(input("Enter the Account number: "))
    acname = input("Enter the name of the Account Holder: ")
    actype = input("Enter the type of the Account <C/S>: ")
    amount = int(input("Enter Initial Amount: \n   >= 500 for Saving; >= 1000 for current: "))
    print("Your Account was Created Successfully ...")
    acc = Account(acNumb,acname,actype)
    acc.deposit(amount)
    addRecccord(fileName,acNumb,acname,actype,amount)
    return acc

def mainManu():
    """display The main menu of the system and pronpt for a selection"""
    print("\t Welcome to the Bank Account System.\n\n")
    print("01. CREATE A NEW ACCOUNT")
    print("02. DEPOSIT AMOUNT")
    print("03. WITHDRAW AMOUNT")
    print("04. BALANCE REQUEST")
    print("05. LIST OF ALL ACCOUNT HOLDER")
    print("06. DELETE ACCOUNT")
    print("07. MODIFY ACCOUNT INFO")
    print("08. EXIT")
    selection = int(input("Select your option <1-8> : "))
    return selection

def createFile(fileName):
    """Create a file to put the account reccords """
    line1 = "\t\t\t ACCOUNT HOLDER LIST \n"
    line2 = "===========================================================\n"
    line3 = "Account no.\t Name\t\t\t Type\t  Balance\n"
    lines = [line1,line2,line3,line2]

    if os.path.isfile('./'+ fileName) == False:
        #file does not exist, Put the Header
        file = open(fileName,'a')
        for line in lines:
            file.write(line)        
        file.close()
    
def addRecccord(fileName,acNumb,name,acType,acBalance):
    data = " {0:<15} {1:<24} {2:<8} {3:<10} \n" .format(acNumb,name,acType,acBalance)
    file = open(fileName, 'a')
    file.write(data)
    file.close()
    
def findAccount(fileName,acNumb):
    """Return a list of the index and True if the account is in the file, false otherwise"""
    file = open(fileName,'r')
    found = False
    lineIndex = 0
    for line in file: #get each line of the file
        try:
            if int(acNumb) == int(line[0:14]): 
                #get the account number which has a field of 15 (digit and blank spaces)
                found = True
                file.close()
                return [found,lineIndex] 
        except:
            #make sure it ignores the first 4 lines since they are the headers
            pass
        lineIndex += 1 
    file.close()
    return [found,0]

def deleteAccount(fileName,acNumb):
    account = findAccount(fileName,acNumb) # a list of [bool,index of line of the account]
    accIndex = account[1]
    with open(fileName, "r") as f:
        lines = f.readlines()
    with open(fileName, "w") as file:
        for line in lines:
            if line != lines[accIndex]:
                #copy the file and ignore the line containing the accNumb
                file.write(line)    
    file.close()
    f.close()
    
def modifyAcount(fileName,acNumb,name,acType,acBalance):
    deleteAccount(fileName,acNumb)
    addRecccord(fileName,acNumb,name,acType,acBalance)
    
def dispAllAccountHolder(fileName):
    f = open(fileName,'r')
    lines = f.readlines()
    for line in lines:
        print(line.strip('\n'))
    f.close()
    
def getAllData(fileName):
    """Get all the info into a dictionary 
    return a dictionary; {acNumb:[name,type,balance]}
    """
    data = {}
    f = open(fileName,'r')
    lines = f.readlines()
    for line in lines:
        try:
            if line[1].isdigit(): #first character after the empty space
                lineLst = line.split()
                acNumb = int(lineLst[0])
                name = lineLst[1]
                acType = lineLst[2]
                acBalnace = int(lineLst[3])
                data[acNumb] = [name,acType,acBalnace]
                
        except:
            pass #just the header data that has an empty space
    f.close()
    return data

def main():
    exit = False
    fileName = "bankAccountRecord.txt"
    createFile(fileName)
    #addRecccord(fileName,289,'kader','c',3000)
    #addRecccord(fileName,100,'kader','s',500)
    #deleteAccount(fileName,100)

    while exit == False:
        os.system('cls') #clear the screen// will only work when on shell
        selection = mainManu()
        #SHOULD UPDATE data IN V2, TO MAKE IT FASTER
        data = getAllData(fileName) # all the data in a dictionary
        if selection == 1: #create an account
            userAccount = createAccount(fileName)
            userAccount.dispAccount()   
            
        elif selection == 2: #deposit account
            print( "+++ TRANSACTION FORM +++" )
            acNumb = input("Enter Account Number: ")
            if findAccount(fileName,acNumb)[0] == True: #account exist
                acData = data[int(acNumb)] # a list of name, type and balance
                name = acData[0]
                typ = acData[1]
                bal = acData[2]
                userAccount = Account(acNumb,name,typ)
                userAccount.deposit(bal) #the initial balance
                userAccount.dispAccount()
                amount = int(input("Enter the amount to deposit: "))
                userAccount.deposit(amount) #new amount to add
                modifyAcount(fileName,acNumb,name,typ,userAccount.getBalance())
                print("Record updated" )
              
            else:
                print("Account does no exit, please check the number or create new account")
                
        elif selection == 3: #withdraw money
            print("+++ TRANSACTION FORM +++" )
            acNumb = input("Enter Account Number: ")
            if findAccount(fileName,acNumb)[0] == True: #account exist
                acData = data[int(acNumb)] # a list of name, type and balance
                name = acData[0]
                typ = acData[1]
                bal = acData[2]
                userAccount = Account(acNumb,name,typ)
                userAccount.deposit(bal) #the initial balance
                userAccount.dispAccount()
                amount = int(input("Enter the amount to withdraw: "))
                userAccount.withdraw(amount) #new amount to add
                modifyAcount(fileName,acNumb,name,typ,userAccount.getBalance())
                print("Record updated" )
              
            else:
                print("Account does no exit, please check the number or create new account")
            
        elif selection == 4: #Balance request
            print("+++ BALANCE INFORMATION +++" )
            acNumb = input("Enter Account Number: ")
            if findAccount(fileName,acNumb)[0] == True: #account exist
                acData = data[int(acNumb)] # a list of name, type and balance
                name = acData[0]
                typ = acData[1]
                bal = acData[2]
                userAccount = Account(acNumb,name,typ)
                userAccount.deposit(bal) #the initial balance
                userAccount.dispAccount()
                              
            else:
                print("Account does no exit, please check the number or create new account")
            
        elif selection == 5: #display all account holders
            dispAllAccountHolder(fileName)
            
        elif selection == 6: #delete account
            print("+++ BALANCE INFORMATION +++" )
            acNumb = input("Enter Account Number: ")
            if findAccount(fileName,acNumb)[0] == True: #account exist
                confirm = input("Are you sure you want to delete the account? Y/N ")
                if confirm.lower() == 'y':
                    deleteAccount(fileName,acNumb)
                    print("Account Deleted" )
                else:
                    print("Account NOT Deleted") 
            else:
                print("Account does no exit, please check the number or create new account")
             
        elif selection == 7: #Modify account
            print("+++ ACCOUNT MODIFICATION +++" )
            acNumb = int(input("Enter the Account number: "))
            if findAccount(fileName,acNumb)[0] == True: #account exist
                acname = input("Enter the New name of the Account Holder: ")
                actype = input("Enter the New type of the Account <C/S>: ")
                balance = int(input("Enter New Balance: "))
                modifyAcount(fileName,acNumb,acname,actype,balance)
                print("Record Updated Successfully ...") 
            else:
                print("Account does no exit, please check the number or create new account")
             
        elif selection == 8: #exit the program
            print("You are exiting the Bank Account System \n Good Bye!!!")
            exit = True
                           
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
