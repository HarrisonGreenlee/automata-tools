import re
import asyncio
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

def convertRegex(inputRegex):
    #TODO
    #inputRegex = sanitize(inputRegex)
    inputRegex = inputRegex.replace("`", "")
    inputRegex = inputRegex.replace("U", "|")
    return re.compile("(\A)("+inputRegex+")(\Z)")

def getRegex():
    userRegex = input("Regular expression: ")
    return convertRegex(userRegex)

async def presentCounterExample(message, counter_example, r1, r2):
    display_counter_example = counter_example
    if counter_example == "":
        display_counter_example = "[EMPTY STRING]"
    
    await message.channel.send("COUNTEREXAMPLE - " + display_counter_example)
    await message.channel.send("R1 EVALUATES TO " + str(bool(r1.match(counter_example))))
    await message.channel.send("R2 EVALUATES TO " + str(bool(r2.match(counter_example))))

async def testBinary(message, r1, r2):
    for i in range(16384):
        testnum = str(int(bin(i)[2:]))
        print(testnum)
        if bool(r1.match(testnum)) != bool(r2.match(testnum)):
            await presentCounterExample(message, testnum, r1, r2)
            return False
    return True

async def testEmpty(message, r1, r2):
    if bool(r1.match("")) != bool(r2.match("")):
        await presentCounterExample(message, "", r1, r2)
        return False
    return True

@client.event
async def on_message(message):
    if ' EQUALS ' in message.content:
        a, b = message.content.split(' EQUALS ')
        
        try:
            r1 = convertRegex(a)
        except:
            await message.channel.send("INVALID SYNTAX IN R1")
            
        try:
            r2 = convertRegex(b)
        except:
            await message.channel.send("INVALID SYNTAX IN R2")

        match = await testEmpty(message, r1, r2)
        if(match):
            match = await testBinary(message, r1, r2)
            
        await message.channel.send("THE TWO REGEX COULD BE EQUAL - " + str(match))

client.run(TOKEN)