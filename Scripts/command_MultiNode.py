#!/usr/bin/python

import argparse
import re 
sentList =[]
reciveList =[]
result=[]

parser = argparse.ArgumentParser()

parser.add_argument("--infile", "-f", type=str, required=True)
args = parser.parse_args()


file_ex       =".csv"  
filename      = args.infile
dest_filename = args.infile + file_ex
 
print "log file :  %s "%filename

PACKET_SIZE_BYTE = 40 
BIT_PER_BYTE     =8 
MILLSECOND_TO_SECOND= 0.001


No_data_pkt_sent = 0
No_data_pkt_received = 0
pkt_sent_list = []
pkt_received_list = []
No_DIS_pkt =0
No_DAO_pkt =0
No_DIO_pkt =0
Avg_delay  = 0
delay_list =[]
last_rec =0

senter_1 = "ID:10"
reciever_1 = "ID:8"

senter_list_1 = []
reciever_list_1 = []
delay_list_1 =[]
throughput_list =[]
final_delay_list =[] 
Avg_throughput = 0
print"-----------------------------------------"
print"Extracting Data from File :%s "%filename
print"-----------------------------------------"
fp = open(filename)
f = fp.readlines() 
for line in f:

    if (re.findall (senter_1,line) and  re.findall("Client_sendingHello.*",line)):     
        sentList = line.split(None, 6)
        subList =[]
        subList.insert(0,sentList[3])
        subList.insert(1,sentList[0])
        if sentList[3] not in pkt_sent_list:
	     pkt_sent_list.insert(0,sentList[3])  
             No_data_pkt_sent +=1
             senter_list_1.append(subList) 
    elif  (re.findall (reciever_1,line) and re.findall("Server_receivedHello.*",line)):  
        reciveList = line.split(None, 6) 
        subList =[]
        subList.insert(0,reciveList[3])
        subList.insert(1,reciveList[0])
        if reciveList[3] not in pkt_received_list :
      		pkt_received_list.insert(0,reciveList[3]) 
        	No_data_pkt_received +=1
                reciever_list_1.append(subList)

    if (re.findall("RPL: Sending a DIS.*",line)  ):     
        No_DIS_pkt +=1
     
    if (re.findall("Incoming DIO from.*",line)  ):     
        No_DIO_pkt +=1

    if (re.findall("Recived Dio.*",line)  ):     
        No_DIO_pkt +=1

    if((re.findall("Sending a DAO.*",line))): # or (re.findall("Sending a No-Path DAO.*",line))):     
	No_DAO_pkt +=1 
fp.close()
#print reciever_list_1


for send_pkt in senter_list_1:
    for recivepkt in reciever_list_1:
         if send_pkt[0] == recivepkt[0]:
	    delay = int(recivepkt[1]) - int(send_pkt[1])
            throughput = float((PACKET_SIZE_BYTE * BIT_PER_BYTE))/  float(delay* MILLSECOND_TO_SECOND)
            delay_list = []
            delay_list.insert(0,send_pkt[0])
            delay_list.insert(1,send_pkt[1])
            delay_list.insert(2,recivepkt[1]) 
            delay_list.insert(3, delay)
            delay_list.insert(4,throughput )
	    delay_list_1.append(delay_list)
            throughput_list.insert(0,throughput)
            final_delay_list.insert(0,delay)

last_sent = sentList[3]
PDR = float (len(pkt_received_list)) / float(len(pkt_sent_list))
Avg_delay = sum(final_delay_list) /float(len(final_delay_list))
Avg_throughput = sum(throughput_list) /float(len(throughput_list))
Control_packet = No_DIS_pkt + No_DIO_pkt + No_DIO_pkt + No_DAO_pkt

print"-----------------------------------------"
print "simulation Summary:--- "
print"-----------------------------------------"
print "No_data_pkt_sent: %d "%len(pkt_sent_list)
print "No_data_pkt_received :%d "%len(pkt_received_list)
print "No of Pkt Droped %d "% ( No_data_pkt_sent- No_data_pkt_received)
print "No of Control Packets %d "%Control_packet
print "PDR :%f"%PDR 
print "AVg_Delay : %f milliseconds"%Avg_delay
print "Avg_throughput : %d  bits per second"%Avg_throughput

print"-----------------------------------------"
print"       Writing Data into %s" %dest_filename
print"-----------------------------------------"


thefile = open(dest_filename, 'w')
thefile.write("\n") 

thefile.write("\nSUMMERY:--------\n")
thefile.write("\n")
thefile.write("No_data_pkt_Sent,")
thefile.write("%s," % No_data_pkt_sent )
thefile.write("\n")
thefile.write("No_data_pkt_Received,")
thefile.write("%s," % No_data_pkt_received)


thefile.write("\n")
thefile.write("PDR,")
thefile.write("%s," % PDR)

thefile.write("\n")
thefile.write("Avg_delay,")
thefile.write("%s milliseconds " % Avg_delay)
thefile.write("\n")

thefile.write("Avg_throughput,")
thefile.write("%s bitssecond " % Avg_throughput)
thefile.write("\n")

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


thefile.write("\n ----,-----------------------,--------\n") 
thefile.write("\n DETAILS:------\n") 
thefile.write("\n -----,----------------------,------\n") 
thefile.write("Source,")
thefile.write("Destination,")
thefile.write("Packet_No,")
thefile.write("Sent_Time,")
thefile.write("Received_time,")
thefile.write("Delay(milliseconds) ,\n")
thefile.write("Throughput (bits_per_second)\n")
thefile.write(senter_1)
thefile.write(",")
thefile.write(reciever_1)
thefile.write(",")

for item in  delay_list_1:
    for conte in item:
      thefile.write("%s," % conte)
    thefile.write("\n")
    thefile.write(",,")


thefile.close()
print"-----------------------------------------"
print"           END"
print"-----------------------------------------"
