import csv
from datetime import date,datetime
from statistics import mean
users_file = open("Клиенты имеющие заказ на 1 поток.csv", mode="r", encoding='utf-8')
users_reader = csv.DictReader(users_file,delimiter = ';' )

orders_file = open("Заказы на 1 поток.csv", mode="r", encoding='utf-8')
orders_reader = csv.DictReader(orders_file,delimiter = ';' )

add_orders_file = open("Заказы на доп проверку.csv", mode="r", encoding='utf-8')
add_orders_reader = csv.DictReader(add_orders_file,delimiter = ';' )

message_file = open("message.csv", mode="r", encoding='utf-8')
message_reader = csv.DictReader(message_file,delimiter = ';' )


anow_orders_file = open("Другие заказы.csv", mode="r", encoding='utf-8')
anow_orders_reader = csv.DictReader(anow_orders_file,delimiter = ';' )

pays_file = open("Платежы.csv", mode="r", encoding='utf-8')
pays_reader = csv.DictReader(pays_file,delimiter = ';' )

accpref_file = open("Lg150853.csv", mode="r", encoding='utf-8')
accpref_reader = csv.DictReader(accpref_file,delimiter = ';' )

accpref_file_2 = open("Lg180463.csv", mode="r", encoding='utf-8')
accpref_reader_2 = csv.DictReader(accpref_file_2,delimiter = ';' )


w_file = open("res4.csv", mode="w", encoding='utf-8')
file_writer = csv.writer(w_file, delimiter = ";",lineterminator="\r")
file_writer.writerow(['OrderId','ClientID','LVM','PayingType(0 - мес, 1 - год)', 'PackedgeLevel(0 - минимум, 1- стандарт, 2 - премиум)','NymberOfSub', 'DaysBeforPaing', 'NumOfCallToSup',
                    #    'AnseringTime',
                         'NumOfAddServ',
                        #    'FrequensyOfOccur', 
                           'AcademicPerf','Status'])

min_time = lambda y, z:  y if abs(y)<abs(z) else z
i = 0
for order in orders_reader:
    i+=1
    OrderId = order["ID"]
    ClientID = order["ID клиента"]
 
    LVM = [int(user["LTV"].split('.')[0]) for user in users_reader if user["ID"] == ClientID][0] 
    users_file.seek(0)
    PayingType = 0 if 'помесячно' in order["Список позиций"] else 1
    PackedgeLevel = 0 if 'Минимум' in order["Список позиций"] else 1 if 'Стандарт' in order["Список позиций"] else 2
    NymberOfSub = 1 + len([x["Список позиций"] for x in anow_orders_reader if x["ID клиента"]==ClientID])
    anow_orders_file.seek(0)
    if PayingType == 1:
        DaysBeforPaing = [datetime.strptime(pay["Data"].split(' ')[0], '%d.%m.%Y') for pay in pays_reader if pay["Order"] == OrderId] 
        DaysBeforPaing = (list(map(lambda x: (
                              min_time(
                              int((datetime(x.year,x.month,5) - x).total_seconds())//(60*60*24)
                              ,int((datetime(x.year if x.month + 1 < 13 else x.year + 1 ,x.month + 1 if x.month + 1 < 13 else 1 ,5)  - x).total_seconds())//(60*60*24))
                              )
                              ,DaysBeforPaing))[1:])
        if len(DaysBeforPaing) != 0:
            DaysBeforPaing = mean(DaysBeforPaing)
        else:
            DaysBeforPaing = 0
    else:
        DaysBeforPaing = 0
    pays_file.seek(0)
    
    numofcallArr = [x['NumberOfMessage'] for x in message_reader if x['Name'] == order['Имя клиента'] ]
    NumOfCallToSup = 0 if len(numofcallArr) == 0 else numofcallArr[0] if len(numofcallArr) == 1 else sum(list(map(int,numofcallArr)))
    message_file.seek(0)
    # AnseringTime = 10 #not ready 
    NumOfAddServ = 0
    for x in add_orders_reader:
        if x["ID клиента"] == ClientID:
            NumOfAddServ += 1
    add_orders_file.seek(0)
    # FrequensyOfOccur = 0#not ready
    AcademicPerfArr = [x['Прогресс сколько из скольки'] for x in accpref_reader if ''.join(i for i in x['ССылка'] if i.isdigit()) == ClientID]
    if len(AcademicPerfArr) == 0 or AcademicPerfArr[0] == '':
        AcademicPerfArr = [x['Прогресс сколько из скольки'] for x in accpref_reader_2 if ''.join(i for i in x['ССылка'] if i.isdigit()) == ClientID]
        accpref_file_2.seek(0) 
    AcademicPerf = 0 if len(AcademicPerfArr) == 0 else (AcademicPerfArr[0].split('/')[0]) if len(AcademicPerfArr) == 1 else AcademicPerfArr  
    accpref_file.seek(0) 
    Status = 1 if order['Статус'] == 'Отказ' else 0
    file_writer.writerow([OrderId, ClientID,LVM,PayingType, PackedgeLevel,NymberOfSub, DaysBeforPaing, NumOfCallToSup,
                        #    AnseringTime,
                             NumOfAddServ,
                            #    FrequensyOfOccur,
                                 AcademicPerf, Status])

