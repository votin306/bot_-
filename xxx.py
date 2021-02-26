import discord
from discord.ext import commands
import json
import requests
from discord.utils import get
from discord import Spotify
import os

help_text = "фыва"
TOKEN = 'токен'
client = commands.Bot(command_prefix = '#')
like = "811644070635241492"

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('#школяр'))
    print('Школота готова')

@client.command()
async def школяр(ctx):
    await ctx.channel.purge(limit=1)
    embd = discord.Embed(color = 0x00ffae, description = help_text, title = 'Немного о мне')
    embd.set_author(name = 'Школяр', icon_url = 'https://raw.githubusercontent.com/votin306/bot_-/main/jERWaPql4Bg.jpg' ) 
    embd.set_thumbnail(url="https://raw.githubusercontent.com/votin306/bot_-/main/jERWaPql4Bg.jpg")
    await ctx.channel.send(embed = embd)

@client.command()
async def удали(ctx, arg : int):
    await ctx.channel.purge(limit=arg)
    emb = discord.Embed( title = 'Я прибрал немного :blush:', colour = discord.Color.green())
    emb.add_field(name = 'Было удалено вот столько сообщений', value = arg,)
    await ctx.send(embed=emb)
     
@client.command()
async def скажи(ctx, *,arg):
    await ctx.channel.send(arg)
    
@client.command(pass_context = True)
async def БАН(ctx, user: discord.Member ):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed( title = 'А я кого-то заБанил', colour = discord.Color.red())
    emb.set_author(name = user.name, icon_url = user.avatar_url ) 
    emb.add_field(name = 'БАН', value = 'Был забанен : {}'.format(user.mention ),)
    await ctx.send(embed=emb)
    await user.ban(reason=None)


@client.command(pass_context = True)
async def пых(ctx, user: discord.Member ):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed( title = 'А я кого-то кЫкнул', colour = discord.Color.red())
    emb.set_author(name = user.name, icon_url = user.avatar_url ) 
    emb.add_field(name = 'Кик', value = 'Был изгнан : {}'.format(user.mention ),)
    await ctx.send(embed=emb)
    await user.kick(reason=None)
    

@client.command()
async def эмбед(ctx, titles, *, texts):
    await ctx.channel.purge(limit=1)
    embed=discord.Embed(title= titles, description = texts, color=0x00ffff)
    embed.set_footer(text= ctx.message.author,icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def заткнись(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )
    await member.add_roles(mute_role)
    emb = discord.Embed( title = 'А я кого-то Заткнул', colour = discord.Color.red())
    emb.set_author(name = member.name, icon_url = member.avatar_url ) 
    emb.add_field(name = 'МЬЮТЬ:nerd: ', value = 'Был замьючен : {}'.format(member.mention ),)
    await ctx.send(embed=emb)
    
@client.command(pass_context=True)
async def говори(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )
    await member.remove_roles(mute_role)
    emb = discord.Embed( title = 'А я разрешил кому-то разговаривать', colour = discord.Color.red())
    emb.set_author(name = member.name, icon_url = member.avatar_url ) 
    emb.add_field(name = 'НЕМЬЮТЬ :nerd: ', value = 'Был разамьючен : {}'.format(member.mention ),)
    await ctx.send(embed=emb)


@client.command(pass_context=True)
async def эмоджи(ctx, emoji: discord.Emoji):
    emb = discord.Embed( title = "Емодзи(жы) :arrow_right: ==> {}".format(emoji.name), colour = discord.Color.green())
    emb.set_image(url=emoji.url)
    await ctx.send(embed=emb)

@client.command(pass_context=True)
async def инфо(ctx, member: discord.Member = None ):
    if member == None:
        if ctx.message.author.bot == True :
            bot_test = "ТЫ БОТЯРА"
        if ctx.message.author.bot == False :
            bot_test = "ТЫ ЧЕЛОВЕК"
        emb = discord.Embed( title = "Инфа о пользователе => {}".format(ctx.message.author.name),description = "**Как его зовут: {}** \nВысокая роль на серваке: {}\n**Зарегался в: {}\n**ID челика: {}\n**Цвет в HEX: {}**\nБотяра: {}\n**Аватарка: Тыкни на эту картинку :arrow_upper_right:**".format(ctx.message.author,ctx.message.author.top_role.mention,ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p По UTC"),ctx.message.author.id,ctx.message.author.colour,bot_test), colour = discord.Color.green())  
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=emb)
    else:
        if member.bot == True :
            bot_test = "ТЫ БОТЯРА"
        if member.bot == False :
            bot_test = "ТЫ ЧЕЛОВЕК"
        emb = discord.Embed( title = "Инфа о пользователе => {}".format(member.name),description = "**Как его зовут: {}** \nВысокая роль на серваке: {}\n**Зарегался в: {}\n**ID челика: {}\n**Цвет в HEX: {}**\nБотяра: {}\n**Аватарка: Тыкни на эту картинку :arrow_upper_right:**".format(member.name,member.top_role.mention,member.created_at.strftime("%a, %#d %B %Y, %I:%M %p По UTC"),member.id,member.colour,bot_test), colour = discord.Color.green())  
        emb.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=emb)

@client.command(pass_context=True)
async def сервер(ctx):
    guild = ctx.message.guild
    emb = discord.Embed( title = "**Информация о сервере => {}**".format(guild.name),description = "**Информация о сервере => {}**", colour = discord.Color.green())
    emb.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=emb)

@client.command(pass_context=True)
async def кук(ctx):
    for attachment in ctx.message.attachments:
        print(attachment.url)

client.run(TOKEN)
