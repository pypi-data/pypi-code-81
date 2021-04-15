import discord, random
from discord.ext import commands

prefixs = []
maxed = "False"
client = commands.Bot(command_prefix = prefixs)
tokens = ""

######################################

Player1 = {
    "UserID": "", "Healt": 20, "Name": "", "Turn": "False"
}

Player2 = {
    "UserID": "", "Healt": 20, "Name": "", "Turn": "False"
}

######################################
def Start(token, prefix):
    prefixs.append(prefix)
    tokens = token

    ################

    @client.event
    async def on_ready():
        print("Bot Is Online")

    @client.command()
    async def battle(ctx, member : discord.Member):
        if Player1["UserID"] == "":

            if ctx.author.id == member.id:
                embed = discord.Embed(
                    title = "Error Deciline Battle",
                    description = "You Can't Battle With Your Self",
                    color = discord.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                Player1["UserID"] = ctx.author.id
                Player2["UserID"] = member.id

                Player1["Name"] = ctx.author.name
                Player2["Name"] = member.name

                embed2 = discord.Embed(
                    title = "Battle Generated!",
                    descirption = "Battle Generated. Wait People to accept The Battle.",
                    color = discord.Color.green()
                )
                await ctx.send(embed=embed2)
        else:
            embed3 = discord.Embed(
                title = "Error Deciline Battle",
                description = "Battle Only Can Generated 1, Please Wait People To Finish The Battle",
                color = discord.Color.red()
            )
            await ctx.send(embed=embed3)

    @client.command()
    async def accept(ctx):
        if ctx.author.id == Player2["UserID"]:
            embed = discord.Embed(
                title = " < Select Skill Below >",
                description = "Attack - Attack Oppent [ Damage 4 - 7 ]\nHeal - Heal Yourself [ Healt Incrased 3 - 9 ]",
                color = discord.Color.green()
            )
            await ctx.send(embed=embed)

    @client.command()
    async def Attack():
        if Player1["Healt"] < 1 or Player2["Healt"] < 1:
            await ctx.send("You Win!")
            Player1["UserID"] = ""
            Player1["Turn"] = "False"
            Player1["Healt"] = 20
            Player1["Name"] = ""

            Player2["UserID"] = ""
            Player2["Turn"] = "False"
            Player2["Healt"] = 20
            Player2["Name"] = ""
        else:
            pass

        if ctx.author.id == Player1["UserID"]:
            if Player1["Turn"] == "True":

                Attacked = random.randint(4, 7)

                Player1["Turn"] = "False"
                Player2["Turn"] = "True"
                Player2["Healt"] -= Attacked

                embed = disocrd.Embed(
                    title = "Attack {}".format((Player2["Name"])),
                    descirption = "{} Player Decresed ( 20 / {} )".format((Player2["Name"], Attacked)),
                    color = discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Waiting For Oppent Attack ( You Already Attacking Before )")

        if ctx.author.id == Player2["UserID"]:
            if Player2["Turn"] == "True":

                Attackeds = random.randint(4, 7)

                PLayer2["Turn"] = "False"
                Player1["Turn"] = "True"
                Player1["Healt"] -= Attackeds

                embeds = disocrd.Embed(
                    title = "Attack {}".format((Player1["Name"])),
                    descirption = "{} Player Decresed ( 20 / {} )".format((Player1["Name"], Attackeds)),
                    color = discord.Color.blue()
                )
                await ctx.send(embed=embeds)
            else:
                await ctx.send("Waiting For Oppent Attack ( You Already Attacking Before )")

    @client.command()
    async def howgay(ctx, member : discord.Member):
        r = random.randrange(100)
        embed = discord.Embed(
            title = "Gay Generator",
            description = f"{member} Has {r}% Gay!",
            color = discord.Color.red()
        )

        await ctx.send(embed=embed)

    @client.command()
    async def Heal(ctx):
        if ctx.author.id == Player1["UserID"]:
            if Player1["Turn"] == "True":
                Heal = random.randint(4, 7)

                Player1["Turn"] = "False"
                Player2["Turn"] = "True"
                Player1["Healt"] += Heal
                embed = discord.Embed(
                    title = "Heal Potion",
                    description = "You Used Healt Potion And Incrased {} ( 20 / {} )".format((Heal, Player1["Healt"])),
                    color = discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Waiting For Oppent Attack ( You Already Attacking Before )")

        if ctx.author.id == Player2["UserID"]:
            if Player2["Turn"] == "True":
                Heals = random.randint(4, 7)

                Player2["Turn"] = "False"
                Player1["Turn"] = "True"
                Player2["Healt"] += Heals
                embeds = discord.Embed(
                    title = "Heal Potion",
                    description = "You Used Healt Potion And Incrased {} ( 20 / {} )".format((Heals, Player2["Healt"])),
                    color = discord.Color.blue()
                )
                await ctx.send(embed=embeds)
            else:
                await ctx.send("Waiting For Oppent Attack ( You Already Attacking Before )")

def add_command(names, response):
    if maxed == "False":
        @client.command(name=names)
        async def responsseeeeeee(ctx):
            await ctx.send(response)
    else:
        maxed = "True"
        print('Max Command Reached')

client.run(tokens)