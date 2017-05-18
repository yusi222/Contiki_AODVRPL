#!/usr/bin/python

import argparse
import re 
sentList =[]
reciveList =[]
result=[]

parser = argparse.ArgumentParser()

parser.add_argument("--infile", "-f", type=str, required=True)
args = parser.parse_args()

print"\n"
#print args.infile

file_ex       =".csv"  
filename      = args.infile
dest_filename = args.infile + file_ex
 
 
No_data_pkt_sent = 0
No_data_pkt_received = 0
No_DIS_pkt =0
No_DAO_pkt =0
No_DIO_pkt =0
Avg_delay  = 0
delay_list =[]
last_rec =0



senter_1 = "ID:10"
reciever_1 = "ID:11"
senter_list_1 = []
reciever_list_1 = []
delay_list_1 =[]

senter_2 = "ID:12"
reciever_2 = "ID:13"
senter_list_2 = []
reciever_list_2 = []
delay_list_2 =[]

senter_3 = "ID:14"
reciever_3 = "ID:15"
senter_list_3 = []
reciever_list_3 = []
delay_list_3 =[]

final_delay_list =[] 

fp = open(filename)
f = fp.readlines()
print "Reading file %s" %filename
for line in f:

    if (re.findall (senter_1,line) and  re.findall("Client_sendingHello.*",line)):     
        No_data_pkt_sent +=1
        sentList = line.split(None, 6)
        subList =[]
        subList.insert(0,sentList[3])
        subList.insert(1,sentList[0])
        senter_list_1.append(subList) 
       
    elif  (re.findall (reciever_1,line) and re.findall("Server_receivedHello.*",line)):  
        No_data_pkt_received +=1
        reciveList = line.split(None, 6) 
        subList =[]
        subList.insert(0,reciveList[3])
        subList.insert(1,reciveList[0])
        reciever_list_1.append(subList)

    elif (re.findall (senter_2,line) and  re.findall("Client_sendingHello.*",line)):     
        No_data_pkt_sent +=1
        sentList = line.split(None, 6)
        subList =[]
        subList.insert(0,sentList[3])
        subList.insert(1,sentList[0])
        senter_list_2.append(subList) 
       
    elif  (re.findall (reciever_2,line) and re.findall("Server_receivedHello.*",line)):  
        No_data_pkt_received +=1
        reciveList = line.split(None, 6) 
        subList =[]
        subList.insert(0,reciveList[3])
        subList.insert(1,reciveList[0])
        reciever_list_2.append(subList)

    elif (re.findall (senter_3,line) and  re.findall("Client_sendingHello.*",line)):     
        No_data_pkt_sent +=1
        sentList = line.split(None, 6)
        subList =[]
        subList.insert(0,sentList[3])
        subList.insert(1,sentList[0])
        senter_list_3.append(subList) 
       
    elif  (re.findall (reciever_3,line) and re.findall("Server_receivedHello.*",line)):  
        No_data_pkt_received +=1
        reciveList = line.split(None, 6) 
        subList =[]
        subList.insert(0,reciveList[3])
        subList.insert(1,reciveList[0])
        reciever_list_3.append(subList)

fp.close()

for send_pkt in senter_list_1:
    for recivepkt in reciever_list_1:
         if send_pkt[0] == recivepkt[0]:
	    delay = int(recivepkt[1]) - int(send_pkt[1])
            delay_list = []
            delay_list.insert(0,send_pkt[0])
            delay_list.insert(1,send_pkt[1])
            delay_list.insert(2,recivepkt[1]) 
            delay_list.insert(3, delay)
	    delay_list_1.append(delay_list)
            final_delay_list.insert(0,delay)


for send_pkt in senter_list_2:
    for recivepkt in reciever_list_2:
         if send_pkt[0] == recivepkt[0]:
	    delay = int(recivepkt[1]) -  int(send_pkt[1])
            delay_list = []
            delay_list.insert(0,send_pkt[0])
            delay_list.insert(1,send_pkt[1])
            delay_list.insert(2,recivepkt[1]) 
            delay_list.insert(3, delay)
	    delay_list_2.append(delay_list)
            final_delay_list.insert(0,delay)


for send_pkt in senter_list_3:
    for recivepkt in reciever_list_3:
         if send_pkt[0] == recivepkt[0]:
	    delay = int(recivepkt[1]) -  int(send_pkt[1])
            delay_list = []
            delay_list.insert(0,send_pkt[0])
            delay_list.insert(1,send_pkt[1])
            delay_list.insert(2,recivepkt[1]) 
            delay_list.insert(3, delay)
	    delay_list_3.append(delay_list)
            final_delay_list.insert(0,delay)


print "DelayList"
print delay_list_1

print "finaldelay"
print final_delay_list

print "No_data_pkt_sent"
print No_data_pkt_sent

print "No_data_pkt_received"
print No_data_pkt_received

print "last rec"
print last_rec 

print "sentList"
print sentList

last_sent = sentList[3]
Through_put = float(No_data_pkt_received) / float( No_data_pkt_sent)
print "Through_put "
print Through_put 

print "AVg_Delay"

Avg_delay = sum(final_delay_list) /float(len(final_delay_list))
print Avg_delay

print"___"
fs = open(filename)
f = fs.readlines() 
for line in f: 
    if (re.findall("RPL: Sending a DIS.*",line)  ):     
        No_DIS_pkt +=1
     
    if (re.findall("Incoming DIO from.*",line)  ):     
        No_DIO_pkt +=1

    if (re.findall("-DIO with.*",line)  ):     
        No_DIO_pkt +=1

    if((re.findall("Sending a DAO.*",line))): # or (re.findall("Sending a No-Path DAO.*",line))):     
        No_DAO_pkt +=1
       # print "*******"
       # print sentList 
                  
fs.close() 

Control_packet = No_DIS_pkt + No_DIO_pkt + No_DIO_pkt + No_DAO_pkt

thefile = open(dest_filename, 'w')
thefile.write("\n") 


thefile.write("\n")
thefile.write("No_data_pkt_Sent,")
thefile.write("%s," % No_data_pkt_sent )
thefile.write("\n")
thefile.write("No_data_pkt_Received,")
thefile.write("%s," % No_data_pkt_received)


thefile.write("\n")
thefile.write("Through_put,")
thefile.write("%s," % Through_put)


thefile.write("\n")
thefile.write("No_DIS_pkt,")
thefile.write("%s," % No_DIS_pkt)
thefile.write("\n")

thefile.write("No_DAO_pkt,")
thefile.write("%s," % No_DAO_pkt)
thefile.write("\n")

thefile.write("No_DIO_pkt,")
thefile.write("%s," % No_DIO_pkt)
thefile.write("\n")

thefile.write("No_control_pkt,")
thefile.write("%s," % Control_packet)
thefile.write("\n")


thefile.write("Avg_delay,")
thefile.write("%s," % Avg_delay)
thefile.write("\n")


thefile.write("\n-----Details------\n") 
thefile.write("Source,")
thefile.write("Destination,")
thefile.write("Packet_No,")
thefile.write("Sent_Time,")
thefile.write("Received_time,")
thefile.write("Delay,\n")

thefile.write(senter_1)
thefile.write(",")
thefile.write(reciever_1)
thefile.write(",")

for item in  delay_list_1:
    for conte in item:
      thefile.write("%s," % conte)
    thefile.write("\n")
    thefile.write(",,")


thefile.write("\n")
thefile.write(senter_2)
thefile.write(",")
thefile.write(reciever_2)
thefile.write(",")

for item in  delay_list_2:
    for conte in item:
      thefile.write("%s," % conte)
    thefile.write("\n")
    thefile.write(",,")


thefile.write("\n")
thefile.write(senter_3)
thefile.write(",")
thefile.write(reciever_3)
thefile.write(",")

for item in  delay_list_3:
    for conte in item:
      thefile.write("%s," % conte)
    thefile.write("\n")
    thefile.write(",,")


thefile.close()
