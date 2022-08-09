#-----------------------------------------------------------------Imports------------------------------------------------------------------------------------
import asyncio
from unicodedata import name
import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands.errors import MissingPermissions
from discord.ext.commands import has_permissions
from discord.ui import Button
from datetime import timedelta
import os
from dotenv import load_dotenv

#-----------------------------------------------------------------Variables------------------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
servers = [766008315367915600]
client = discord.Bot()
messages = discord.Message
#------------------------------------------------------------------Moderation----------------------------------------------------------------------------------

@client.slash_command(guild_ids=servers, name='ban', description="bans a member from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Option(discord.Member, description="Which member do you want to ban?", required=True),
              reason: Option(str, description='Why?', required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("BRUH! You can't ban yourself!")
        if reason == None:
            reason == f'None provided by {ctx.author}.'
        await member.ban(reason=reason)
        await ctx.respond(f'<@{ctx.author.id}>, <@{member.id}> has been banned from the server. ✈️')


@client.slash_command(name='lock', description='Lock a channel', guild_ids=servers)
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.respond('Channel has been locked')


@client.slash_command(name='unlock', description='Unlock a channel', guild_ids=servers)
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=True)
    await ctx.respond('Channel has been unlocked')

@client.slash_command(guild_ids=servers, name="kick", description="Kicks a member from the server.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, description="Who do you want to kick?", required=True),
               reason: Option(str, description="Why?", required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("BRUH! You can't kick yourself!")
    elif member.guild_permissions.administrator:
        await ctx.respond("Stop trying to kick an admin :rolling_eyes:")
    else:
        if reason == None:
            reason = f'None provided by {ctx.author}.'
            await member.kick(reason=reason)
            await ctx.respond(f'<@{ctx.author.id}>, <@{member.id}> has been kicked from the server. ✈️')


@client.slash_command(guild_ids=servers, name='clear', description="clears a channel's messages")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear(ctx, messages : Option(int, description='How many messages do you want to clear?', required=True)):
    await ctx.defer()
    z = await ctx.channel.purge(limit=messages)
    await ctx.respond(f'I have cleared {len(z)}')


@client.slash_command(guild_ids = servers, name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do this, this person is a moderator!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error

@client.slash_command(guild_ids = servers, name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error
#--------------------------------------------------------------Fun Commands------------------------------------------------------------------------------------

@client.slash_command(guild_ids=servers, name="rollrick", description="dunno what to put here")
async def rollrick(ctx):
    await ctx.respond("Bruh! Have you been sitting under a rock? Its called rickroll! Use /rickroll")


@client.slash_command(guild_ids=servers, name="ping", description="Check if the bot is as fast as you lol")
async def ping(ctx):
    await ctx.respond(f"Pong! 🏓 \n\nLatency {client.latency * 1000} .ms")

@client.slash_command(guild_ids=servers, name="pingpong", description='this is sure gonna confuse me ;-;')
async def pingpong(ctx):
    await ctx.respond("BRHUHHHHHHHHHH!!!! WHY? I'm confused now!!")


@client.slash_command(guild_ids=servers, name="bye", description="Say bye!")
async def bye(ctx):
    await ctx.respond("Bye, Cya <:fluffy_puffy:987391645152579614> !")


@client.slash_command(guild_ids=servers, name="about_dev", description="About the developer!")
async def about_dev(ctx):
    await ctx.respond(
        "The developer of me is <@944874986328449104> ! He is very cool and He learnt python long ago.... Thats why he made me!!! HE IS THE BEST")


@client.slash_command(guild_ids=servers, name="rickroll", description="Rickroll a member of the server!")
async def rickroll(ctx, member: Option(discord.Member, description='Who do you want to rickroll?', required=True)):
    await ctx.respond(
        f'{ctx.author.mention} just rickrolled {member.mention}! https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713')


@client.slash_command(guild_ids=servers, name="slap", description="Slap your enemy >:D")
async def slap(ctx, member: Option(discord.Member, description="Who do you want to slap? >:)", required=True)):
    await ctx.respond(
        f'AHHHHHHH {ctx.author.mention} just slapped {member.mention} ! https://tenor.com/view/will-smith-chris-rock-jada-pinkett-smith-oscars2022-smack-gif-25234614')



@client.slash_command(guild_ids=servers, name='sleep', description='Tell the bot to sleep')
async def sleep(ctx):
    await ctx.respond(
        "Ok..... I will sleep ;-;. BUT DON'T WAKE ME UP!!!!"
    )

@client.slash_command(guild_ids=servers, name='wakeup', description='Wake me up.. except, I DONT WANT TO WAKE UP!!')
async def wakeup(ctx):
    await ctx.respond(
        "DONT WAKE ME UP!!!! I JUST SLEPT! ;-; I guess I'll just wake up then.."
    )

@client.slash_command(guild_ids=servers, name='help', description=' All the commands in this bot')
async def help(ctx):
    embed = discord.Embed(title='Help', description='All the commands of this bot', color=discord.Color.teal())
    embed.add_field(name='Moderation Commands', value='ban, kick, lock, unlock, mute, unmute')
    embed.add_field(name='Fun Commands', value='sleep, wakeup, bruh, pong, ping2, slap, rickroll, bye, rollrick')
    embed.add_field(name='Info', value='about_dev, ping')
    embed.set_footer(text=f'Issued by {ctx.author}', icon_url=ctx.author.avatar.url)
    embed.set_image(url='https://cdn.vox-cdn.com/thumbor/DMXD2zLif49j6IP2i3Avda2Cyl0=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/22312759/rickroll_4k.jpg')
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    await ctx.respond(embed=embed)


@client.slash_command(guild_ids=servers, name="pong", description="DONT MAKE TYPOS")
async def pong(ctx):
    await ctx.respond(":0. Bruh!! Dont try to confuse me!! I'm smart! Use /ping or !ping instead")


@client.slash_command(guild_ids=servers, name='ping2',description='DONT DO THIS!!!')
async def ping2(ctx):
    await ctx.respond("/ping")


@client.slash_command(guild_ids=servers, name='bruh', description='umm.. Idk why you would use this command lol')
async def bruh(ctx):
    await ctx.respond('Ummmmmmmmmmmmmmmmmmmmmmmmmmmmmmm..BREHHHH')



# ---------------------------------------------------------------Events----------------------------------------------------------------------------------------

@client.event
async def on_ready():
    print(
        f'Bot has logged in as {client.user}')


load_dotenv()
token = os.getenv("BOT_TOKEN")
client.run(f'{token}')
