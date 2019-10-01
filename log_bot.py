from tkinter import *
from tkinter.ttk import *
import discord
from discord.ext.commands import Bot
import asyncio
import time
import csv
import datetime
import numpy as np
CLIENT_ID = "ID"
CLIENT_TOKEN = "TOKEN"
Client = Bot('!')
DEFAULT_CHANNEL_ID= "DEFAULT CHANNEL ID"
DEFAULT_CHANNEL = discord.Object(id=DEFAULT_CHANNEL_ID)
listen = True
canWrite = True
error = False
debug = True
errors = []
msg = '''
/// SquarerFive | Server Surveillance  ///
/// PRIVATE USE ONLY!! ///
'''
department = "Security"
usage = "CURRENT RUNNING AS: **DISCORD BOT USER**"

print(msg) 
def validate():
    global canWrite
    try:
        a = open("bool.txt", 'r+')
    except:
        a = open("bool.txt", 'w+')
    b = a.readline()
    print(b)
    if b == '':
        Mdata = [["Username","Time", "Message"]]
        with open('log.csv','a+',newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in Mdata:
                writer.writerows(Mdata)
            csv_file.close()
        a.write('False')
        print('File does not have content')
        a.close()
    else:
        a.close()
validate()
async def write(message, user, msg, main):
    global errors
    data = []
    b = str(user)
    c = str(msg)
    data.append(b)
    data.append(str(datetime.datetime.now()).replace(":", "").replace(".",""))
    data.append(c)
    file = open('log.txt', 'a+')
    file.write(message+'\n') 
    try:
        with open('log.csv', "a+", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
    except:
        if (debug==True):
            await Client.send_message(main.channel, 'IO ERROR: Access Denied when trying to access the CSV file.')
            await Client.send_message(main.channel, 'Some information: ' + str(datetime.datetime.now()))
        errors.append(1)
    data.clear()
async def send_message(message,channel):
    try:
        a=Client.get_channel(channel)
        await Client.send_message(channel,message)
    except:
        errors.append(1)
@Client.command()
async def send_propaganda(*,message: str):
    await Client.say(message)
@Client.command()
async def process(*,iterations: int):
    if iterations <= 0:
        await Client.say("Iterations are less or equal to zero. I do not wan't to waste processing power.")
    else:
        for i in range(iterations):
            percent = i / iterations * 100
            b = "Processing data. {}%.".format(str(percent))
            await Client.say(b)
@Client.command()
async def debug(idx):
    global debug
    t=False
    try:
        if (int(idx)==0):
            debug = False
            
        if (int(idx)==1):
            debug = True
        await Client.say("Debug = {}".format(idx))
    except Exception as e:
        print("Error when setting debug mode")
        print(e)
@Client.command()
async def status():
    global listen
    listen = True
    await Client.say("Online and Running")
@Client.event
async def on_ready():
    print('Logged in as '+Client.user.name+' (ID:'+Client.user.id+') | '+str(len(Client.servers))+' servers')
    servers=str(len(Client.servers))
    await Client.change_presence(game=discord.Game(name='Monitoring Server, connected to: {}.'.format(servers + ' server(s).')))
   # a=Client.get_channel(DEFAULT_CHANNEL_ID)
   # await Client.send_message(a, "hello")

@Client.event
async def on_message(message):
    text = "recieved: "+(str(message.content))+" from "+str(message.author)
    formattedText = 'USER= '+(str(message.author)) + " MESSAGE: "+str(message.content)
    #print("recieved: "+(str(message.content))+" from "+str(message.author))
    await Client.process_commands(message)
    print("Recieved message")
    if message.content.startswith("!advancedserverstatus"):
        x = message.server.members
        cd = []
        cd.clear()
        await Client.send_message(message.channel, 'Enumerating through members.')
        for idx, items in enumerate(x):
            print(items)
            cd.append(idx)
        await Client.send_message(message.channel, str(cd))
        await Client.send_message(message.channel, "Iterated through: "+str(len(cd)) + " members.")
        if len(errors) > 0:
            await Client.send_message(message.channel, str(len(errors)) + " error(s) detected.")
        else:
            await Client.send_message(message.channel, "No errors are present.")
        await Client.send_message(message.channel, "Logged in as: {}".format(CLIENT_ID) +"\nCurrent Mode: Debug"+"\nOther Information:"+"\nDepartment: {}".format(department) + "\nState: {}".format(usage) +"\nUsage Stats: Complies to GDPR Privacy Policy")

    if not message.author.bot:
        #await Client.send_message(message.channel, 'I SHOULD ONLY SEND THIS ONCE!')
        if listen == True:
            await write(formattedText, message.author, message.content, message)
        else:
           # await Client.send_message(message.channel, 'Boolean gate is closed')
           print('')
Client.run(CLIENT_TOKEN)


