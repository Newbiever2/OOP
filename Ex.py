class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id=citizen_id
        self.__name=name
        self.__accountlist=[]
        
    def add_account(self,account):
        if not isinstance(account,Account):
            return None
        self.__accountlist.append(account)
        
    
    @property
    def accountlist(self):
        return self.__accountlist
    @property 
    def name(self):
        return self.__name
    @property 
    def citizen_id(self):
        return self.__citizen_id
    
    
    
    
    
class Account:
    def __init__(self, account_number: str, owner: User,money):
        self.__account_number=account_number
        self.__owner=owner
        self.__money=money
        self.__card=None
        self.__limit=40000
        self.__transaction=[]

    def setdepositmoney(self,gmoney):
        if self.__money<0:
            return "not enoght of money"
        self.__money=(self.__money+gmoney)
    def setwithdrawmoney(self,gmoney):
        if self.__limit<gmoney:
            return "Expected result: Exceeds daily withdrawal limit of 40,000 baht"
        if gmoney>self.__money:
            return "not enoght of money"
        self.__money=(self.__money-gmoney)
    def transaction(self,process,money,ATMnumber):
        self.__transaction.append(f"{process}={ATMnumber.machine_id},{money},{self.__money}")
    def create_card(self,card_number: str, account, pin: str):
        if not isinstance(account,Account):
            return "Error"
        create_card=ATMCard(card_number,account,pin)
        self.__card=create_card
    @property
    def limit(self):
        return self.__limit
    @property
    def showtransaction(self):
        return self.__transaction
    @property
    def money(self):
        return self.__money
    @property
    def account_number(self):
        return self.__account_number
    @property
    def owner(self):
        return self.__owner
    @property
    def card(self):
        return self.__card
    
    
    
    
    
class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number=card_number
        self.__account=account
        self.__pin=pin


    @property
    def card_number(self):
        return self.__card_number
    @property
    def account(self):
        return self.__account
    @property
    def pin(self):
        return self.__pin

class ATMMachine:
    def __init__(self, machine_id: str, initial_amount: float):
        self.__machine_id=machine_id
        self.__initial_amount=initial_amount
        
    def setInitial_amount(self,money):
        if self.__initial_amount<0:
            return "Expected result: ATM has insufficient funds"
        self.__initial_amount=money
        
    def insertCard(self,ATM,atmcard,pin):
        if not isinstance(ATM,ATMMachine):
            return None
        for user in bank.userlist:
            for account in user.accountlist:
                if account.card.card_number==atmcard and account.card.pin == pin:
                    return f"{account.card.card_number} , {account.account_number} , Success"
                else: 
                    return "Invalid pin"
        return None
    def deposit_money(self,atm,account: Account,deposit_money):
        atm.setInitial_amount(self.initial_amount+deposit_money)
        if atm.initial_amount<0:
            return "Expected result: ATM has insufficient funds"
        if deposit_money<0:
            return "error"
        if not isinstance(atm,ATMMachine):
            return "error"
        acc_money=account.money
        account.setdepositmoney(deposit_money)
        account.transaction('D',deposit_money,atm)
        
        return "success"
    def withdraw_money(self,atm,account: Account,withdarw_money):
        atm.setInitial_amount(self.initial_amount-withdarw_money)
        if atm.initial_amount<0:
            return "Expected result: ATM has insufficient funds"
        if withdarw_money>account.money:
            return "Error"
        if withdarw_money<0:
            return "error"
        if not isinstance(atm,ATMMachine):
            return "error"
        acc_money=account.money
        if account.limit<0:
            return "Expected result: Exceeds daily withdrawal limit of 40,000 baht"
        account.transaction('W',withdarw_money,atm)
        return account.setwithdrawmoney(withdarw_money)
        
        
    def tranfer(self,atm,account1,account2,money):
        if money>account1.money:
            return "Error"
        if money<0:
            return "Error"
        if not isinstance(atm,ATMMachine):
            return "Error"
        acc_money=account1.money
        account1.setwithdrawmoney(money)
        account1.transaction('TW',money,atm)
        acc_money1=account2.money
        account2.setdepositmoney(money)
        account2.transaction('TD',money,atm)
        return "success"
    @property
    def machine_id(self):
        return self.__machine_id
    @property
    def initial_amount(self):
        return self.__initial_amount
    
        
        
class Bank:
    def __init__(self):
        self.__userlist=[]
        self.__ATMlist=[]
    
    def create_user(self,id,name):
        user=User(id,name)
        self.__userlist.append(user)
    def create_user_account(self,owner:User,account_number,ATM_number,money):
        acc=Account(account_number,owner,money)
        owner.add_account(acc)
        acc.create_card(ATM_number,acc,'1234')


    def create_ATM(self,machine_id: str, initial_amount):
        ATM=ATMMachine(machine_id,initial_amount)
        self.__ATMlist.append(ATM)
        
    def searchATM(self,ATMid):
        for ATM in self.__ATMlist:
            if ATM.machine_id == ATMid:
                return ATM
        
        
    @property
    def userlist(self):
        return self.__userlist
    @property
    def ATMlist(self):
        return self.ATMlist
    
    
    
    
    
    
# กำหนดรูปแบบของ user ดังนี้ {รหัสประชาชน : [ชื่อ, หมายเลขบัญชี, จำนวนเงิน, หมายเลข ATM ]}
user ={'1-1101-12345-12-0':['Harry Potter','1234567890','12345',20000],
       '1-1101-12345-13-0':['Hermione Jean Granger','0987654321','12346',1000]}

atm ={'1001':1000000,'1002':200000}
bank=Bank()

# TODO 1 : จากข้อมูลใน user ให้สร้าง instance โดยมีข้อมูล
# TODO :   key:value โดย key เป็นรหัสบัตรประชาชน และ value เป็นข้อมูลของคนนั้น ประกอบด้วย
# TODO :   [ชื่อ, หมายเลขบัญชี, หมายเลขบัตร ATM, จำนวนเงินในบัญชี]
# TODO :   return เป็น instance ของธนาคาร
# TODO :   และสร้าง instance ของเครื่อง ATM จำนวน 2 เครื่อง

bank.create_user('1-1101-12345-12-0','Harry Potter')
bank.create_user('1-1101-12345-13-0','Hermione Jean Granger')
bank.create_user_account(bank.userlist[0],'1234567890','12345',500000)
bank.create_user_account(bank.userlist[1],'0987654321','12346',1000)

atm1=ATMMachine('1001',atm['1001'])
atm2=ATMMachine('1002',atm['1002'])
bank.create_ATM('1001',atm['1001'])
bank.create_ATM('1002',atm['1002'])
# TODO 2 : เขียน method ที่ทำหน้าที่สอดบัตรเข้าเครื่อง ATM มี parameter 2 ตัว ได้แก่ 1) instance ของธนาคาร
# TODO     2) atm_card เป็นหมายเลขของ atm_card
# TODO     return ถ้าบัตรถูกต้องจะได้ instance ของ account คืนมา ถ้าไม่ถูกต้องได้เป็น None
# TODO     ควรเป็น method ของเครื่อง ATM


# TODO 3 : เขียน method ที่ทำหน้าที่ฝากเงิน โดยรับ parameter 3 ตัว คือ 1) instance ของเครื่อง atm
# TODO     2) instance ของ account 3) จำนวนเงิน
# TODO     การทำงาน ให้เพิ่มจำนวนเงินในบัญชี และ สร้าง transaction ลงในบัญชี
# TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
# TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0


#TODO 4 : เขียน method ที่ทำหน้าที่ถอนเงิน โดยรับ parameter 3 ตัว คือ 1) instance ของเครื่อง atm
# TODO     2) instance ของ account 3) จำนวนเงิน
# TODO     การทำงาน ให้ลดจำนวนเงินในบัญชี และ สร้าง transaction ลงในบัญชี
# TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
# TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0 และ ไม่ถอนมากกว่าเงินที่มี


#TODO 5 : เขียน method ที่ทำหน้าที่โอนเงิน โดยรับ parameter 4 ตัว คือ 1) instance ของเครื่อง atm
# TODO     2) instance ของ account ตนเอง 3) instance ของ account ที่โอนไป 4) จำนวนเงิน
# TODO     การทำงาน ให้ลดจำนวนเงินในบัญชีตนเอง และ เพิ่มเงินในบัญชีคนที่โอนไป และ สร้าง transaction ลงในบัญชี
# TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
# TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0 และ ไม่ถอนมากกว่าเงินที่มี


# Test case #1 : ทดสอบ การ insert บัตร โดยค้นหาเครื่อง atm เครื่องที่ 1 และบัตร atm ของ harry
# และเรียกใช้ function หรือ method จากเครื่อง ATM
# ผลที่คาดหวัง : พิมพ์ หมายเลข account ของ harry อย่างถูกต้อง และ พิมพ์หมายเลขบัตร ATM อย่างถูกต้อง
# Ans : 12345, 1234567890, Success

findATM1=bank.searchATM('1001')
print(bank.searchATM('1001').insertCard(findATM1,'12345','1234'))

# Test case #2 : ทดสอบฝากเงินเข้าในบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 1000 บาท
# ให้เรียกใช้ method ที่ทำการฝากเงิน
# ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Hermione ก่อนฝาก หลังฝาก และ แสดง transaction
# Hermione account before test : 1000
# Hermione account after test : 2000
print("Hermione account before test :")
print(bank.userlist[1].accountlist[0].money)
bank.searchATM('1002').deposit_money(atm2,bank.userlist[1].accountlist[0],1000)

print("Hermione account after test :")
print(bank.userlist[1].accountlist[0].money)
# Test case #3 : ทดสอบฝากเงินเข้าในบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน -1 บาท
# ผลที่คาดหวัง : แสดง Error
print(bank.searchATM('1002').deposit_money(atm2,bank.userlist[1].accountlist[0],-1))

# Test case #4 : ทดสอบการถอนเงินจากบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 500 บาท
# ให้เรียกใช้ method ที่ทำการถอนเงิน
# ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Hermione ก่อนถอน หลังถอน และ แสดง transaction
# Hermione account before test : 2000
# Hermione account after test : 1500
print("Hermione account before test :")
print("limit",bank.userlist[1].accountlist[0].limit)
print(bank.userlist[1].accountlist[0].money)
bank.searchATM('1002').withdraw_money(atm2,bank.userlist[1].accountlist[0],500)

print("Hermione account after test :")
print(bank.userlist[1].accountlist[0].money)
print("limit",bank.userlist[1].accountlist[0].limit)
# Test case #5 : ทดสอบถอนเงินจากบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 2000 บาท
# ผลที่คาดหวัง : แสดง Error
print(bank.searchATM('1002').withdraw_money(atm2,bank.userlist[1].accountlist[0],2000))

# Test case #6 : ทดสอบการโอนเงินจากบัญชีของ Harry ไปยัง Hermione จำนวน 10000 บาท ในเครื่อง atm เครื่องที่ 2
# ให้เรียกใช้ method ที่ทำการโอนเงิน
# ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Harry ก่อนถอน หลังถอน และ แสดงจำนวนเงินในบัญชีของ Hermione ก่อนถอน หลังถอน แสดง transaction
# Harry account before test : 20000
# Harry account after test : 10000
# Hermione account before test : 1500
# Hermione account after test : 11500
print("Harry account before test :")
print(bank.userlist[0].accountlist[0].money)

print("Hermione account before test :")
print(bank.userlist[1].accountlist[0].money)

bank.searchATM('1002').tranfer(atm2,bank.userlist[0].accountlist[0],bank.userlist[1].accountlist[0],10000)
print("Harry account after test :")
print(bank.userlist[0].accountlist[0].money)
print("Hermione account after test :")
print(bank.userlist[1].accountlist[0].money)

# Test case #7 : แสดง transaction ของ Hermione ทั้งหมด 
# ผลที่คาดหวัง
# Hermione transaction : D-ATM:1002-1000-2000
# Hermione transaction : W-ATM:1002-500-1500
# Hermione transaction : TD-ATM:1002-10000-11500
print(bank.userlist[1].accountlist[0].showtransaction[0])
print(bank.userlist[1].accountlist[0].showtransaction[1])
print(bank.userlist[1].accountlist[0].showtransaction[2])
# Test case #8 : ทดสอบการใส่ PIN ไม่ถูกต้อง 
# ให้เรียกใช้ method ที่ทำการ insert card และตรวจสอบ PIN
# atm_machine = bank.get_atm('1001')
# test_result = atm_machine.insert_card('12345', '9999')  # ใส่ PIN ผิด
# ผลที่คาดหวัง
# Invalid PIN
print(bank.searchATM('1001').insertCard(findATM1,'12345','9999'))

# Test case #9 : ทดสอบการถอนเงินเกินวงเงินต่อวัน (40,000 บาท)
# atm_machine = bank.get_atm('1001')
# account = atm_machine.insert_card('12345', '1234')  # PIN ถูกต้อง
# harry_balance_before = account.get_balance()
# print(f"Harry account before test: {harry_balance_before}")
# print("Attempting to withdraw 45,000 baht...")
# result = atm_machine.withdraw(account, 45000)
# print(f"Expected result: Exceeds daily withdrawal limit of 40,000 baht")
# print(f"Actual result: {result}")
# print(f"Harry account after test: {account.get_balance()}")
# print("-------------------------")

account= bank.searchATM('1001').insertCard(bank.searchATM('1001'),'12345','1234')
print(account)
print(bank.searchATM('1002').withdraw_money(atm2,bank.userlist[0].accountlist[0],45000))
# Test case #10 : ทดสอบการถอนเงินเมื่อเงินในตู้ ATM ไม่พอ
# atm_machine = bank.get_atm('1002')  # สมมติว่าตู้ที่ 2 มีเงินเหลือ 200,000 บาท
# account = atm_machine.insert_card('12345', '1234')

# print("Test case #10 : Test withdrawal when ATM has insufficient funds")
# print(f"ATM machine balance before: {atm_machine.get_balance()}")
# print("Attempting to withdraw 250,000 baht...")
# result = atm_machine.withdraw(account, 250000)
# print(f"Expected result: ATM has insufficient funds")
# print(f"Actual result: {result}")
# print(f"ATM machine balance after: {atm_machine.get_balance()}")
# print("-------------------------")
print(bank.searchATM('1002').withdraw_money(atm2,bank.userlist[0].accountlist[0],250000))