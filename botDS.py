import discord
from discord.ext import commands
import json
import requests
from discord.utils import get
from discord import Spotify
import os
from discord import Member
import aiohttp
import random
from discord import File
from asyncio import sleep

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

TOKEN = 'ТОКЕН бота пожалуйста введи'
client = commands.Bot(command_prefix = 'ft;')
client.remove_command('help')

players = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('ft;help'))
    print('Школота готова')

@client.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)
    embd = discord.Embed(color = 0x00ffae, description = "Команды бота Школяр", title = 'Немного о мне')
    embd.add_field(name = 'ft;bot', value = "Расскажу все обо мне",inline=True) 
    embd.add_field(name = 'ft;admin', value = "Команды для админов",inline=True) 
    embd.add_field(name = 'ft;all', value = "Все команды бота Школяр",inline=True) 
    embd.set_author(name = 'Школяр', icon_url = 'https://raw.githubusercontent.com/votin306/bot_-/main/jERWaPql4Bg.jpg' )
    embd.set_thumbnail(url="https://media.tenor.com/images/946f1a56cd8b26e455c6f9a280610e3e/tenor.gif")
    await ctx.channel.send(embed = embd)

@client.command()
async def admin(ctx):
    await ctx.channel.purge(limit=1)
    embd = discord.Embed(color = 0x00ffae, description = "Команды для админов", title = 'Все эти команды только для админов и модераторов')
    embd.add_field(name = 'ft;mute (@челик)', value = "Мьютит @челика на сервере(роль @Мут)",inline=True)
    embd.add_field(name = 'ft;unmute (@челик)', value = "Размьютит @челика на сервере(роль @Мут)",inline=True)
    embd.add_field(name = 'ft;ban (@челик)', value = "ЗаБАНю (@челика) ",inline=True)
    embd.add_field(name = 'ft;kick (@челик)', value = "ЗаКЫКню (@челика) ",inline=True)
    await ctx.channel.send(embed = embd)
@client.command()
async def all(ctx):
    await ctx.channel.purge(limit=1)
    embd = discord.Embed(color = 0x00ffae, description = "Все команды бота Школяр", title = 'Все команды для бота')
    embd.add_field(name = 'ft;bot', value = "Расскажу все обо мне",inline=True) 
    embd.add_field(name = 'ft;delete (кол-во)', value = "удалю (кол-во) сообщений в чате",inline=True)
    embd.add_field(name = 'ft;say (слово)', value = "Скажу тебе то что ты написал",inline=True)
    embd.add_field(name = 'ft;embed загол описание', value = "Загол это заголовок описание это описание эмбеда",inline=True)
    embd.add_field(name = 'ft;emoji (эмоджи)', value = "Покажу эмоджи КРУПНЫМ планом",inline=True)
    embd.add_field(name = 'ft;user (@челик)', value = "Покажу информацию о @челик",inline=True)
    embd.add_field(name = 'ft;server', value = "Покажу информацию о сервере",inline=True)
    embd.add_field(name = 'ft;rp', value = "Создам канал рп(права админа)",inline=True)
    embd.add_field(name = 'ft;vote 1 описание', value = "1 = пинг ,описание текст голосования",inline=True)
    embd.add_field(name = 'ft;vote 0 описание', value = "0 = без пинга ,описание текст голосования",inline=True)
    await ctx.channel.send(embed = embd)

@client.command()
async def delete(ctx, arg : int):
    await ctx.channel.purge(limit=arg)
    emb = discord.Embed( title = 'Я прибрал немного :blush:', colour = discord.Color.green())
    emb.add_field(name = 'Было удалено вот столько сообщений', value = arg,)
    await ctx.send(embed=emb)
     
@client.command()
async def say(ctx, *,arg):
    await ctx.channel.send(arg)
    
@client.command(pass_context = True)
async def ban(ctx, user: discord.Member ):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=1)
        emb = discord.Embed( title = 'А я кого-то заБанил', colour = discord.Color.red())
        emb.set_author(name = user.name, icon_url = user.avatar_url ) 
        emb.add_field(name = 'БАН', value = 'Был забанен : {}'.format(user.mention ),)
        await ctx.send(embed=emb)
        await user.ban(reason=None)
    else:
        await ctx.send("**ТЫ ЧТО-ТО ПОПУТАЛ => у тебя недостаточно прав**")


@client.command(pass_context = True)
async def kick(ctx, user: discord.Member ):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=1)
        emb = discord.Embed( title = 'А я кого-то кЫкнул', colour = discord.Color.red())
        emb.set_author(name = user.name, icon_url = user.avatar_url ) 
        emb.add_field(name = 'Кик', value = 'Был изгнан : {}'.format(user.mention ),)
        await ctx.send(embed=emb)
        await user.kick(reason=None)
    else:
        await ctx.send("**ТЫ ЧТО-ТО ПОПУТАЛ => у тебя недостаточно прав**")

@client.command()
async def embed(ctx, titles, *, texts):
    await ctx.channel.purge(limit=1)
    embed=discord.Embed(title= titles, description = texts, color=0x00ffff)
    embed.set_footer(text= ctx.message.author,icon_url = ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )
        await member.add_roles(mute_role)
        emb = discord.Embed( title = 'А я кого-то Заткнул', colour = discord.Color.red())
        emb.set_author(name = member.name, icon_url = member.avatar_url ) 
        emb.add_field(name = 'МЬЮТЬ:nerd: ', value = 'Был замьючен : {}'.format(member.mention ),)
        await ctx.send(embed=emb)
    else:
        await ctx.send("**ТЫ ЧТО-ТО ПОПУТАЛ => у тебя недостаточно прав**")
    
@client.command(pass_context=True)
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )
        await member.remove_roles(mute_role)
        emb = discord.Embed( title = 'А я разрешил кому-то разговаривать', colour = discord.Color.red())
        emb.set_author(name = member.name, icon_url = member.avatar_url ) 
        emb.add_field(name = 'НЕМЬЮТЬ :nerd: ', value = 'Был разамьючен : {}'.format(member.mention ),)
        await ctx.send(embed=emb)
    else:
        await ctx.send("**ТЫ ЧТО-ТО ПОПУТАЛ => у тебя недостаточно прав**")

@client.command(pass_context=True)
async def emoji(ctx, emoji: discord.Emoji):
    emb = discord.Embed( title = "Емодзи(жы) :arrow_right: ==> {}".format(emoji.name), colour = discord.Color.green())
    emb.set_image(url=emoji.url)
    print(emoji.id)
    await ctx.send(embed=emb)

@client.command(pass_context=True)
async def user(ctx, member: discord.Member = None ):
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
async def server(ctx):
    guild = ctx.message.guild
    emb = discord.Embed( title = "**Информация о сервере => {}**".format(guild.name),description = "**ID сервака: {}\n**Кол-во участников(всех): {}\n**Значек сервера: Нажми сюда :arrow_upper_right:\n**Уровень модерации: {}\n**Регион: {}**\nАФК канал: {}\n**Таймаут в АФК: {} минут**\nВладелец сервера: {}".format(guild.id,guild.member_count,guild.verification_level,guild.region,guild.afk_channel,guild.afk_timeout,guild.owner_id), colour = discord.Color.green())
    emb.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=emb)

@client.command(pass_context=True)
async def rp(ctx):
    if ctx.message.author.guild_permissions.manage_channels:
        guild = ctx.message.guild
        categor = await guild.create_category_channel(name = "В гостях у {}".format(ctx.message.author.name), overwrites=None, reason=None, position=None)
        await guild.create_text_channel("Дом", overwrites=None, category=categor, reason=None)
        await guild.create_text_channel("Жизнь", overwrites=None, category=categor, reason=None)
        await guild.create_text_channel("Праздники", overwrites=None, category=categor, reason=None)
        await guild.create_text_channel("Полиция", overwrites=None, category=categor, reason=None)
        await guild.create_text_channel("Школа", overwrites=None, category=categor, reason=None)
        await guild.create_voice_channel("Комната: {}".format(ctx.message.author.name), overwrites=None, category=categor, reason=None)
        emb = discord.Embed( title = "**Был создан рп в честь {}**".format(ctx.message.author.name),description = "Ты его можешь обнаружить внизу всех списков", colour = discord.Color.green())
        emb.set_thumbnail(url="https://www.meme-arsenal.com/memes/b79a94f9a1014e10a5ced1463d9de98f.jpg")
        await ctx.send(embed=emb)
    else:
        await ctx.send("**ТЫ ЧТО-ТО ПОПУТАЛ => у тебя недостаточно прав**")

@client.command(pass_context=True)
async def bot(ctx):
    emb = discord.Embed( title = "**Немного обо мне**",description = "Эй приветики меня зовут Школяр\n**Мой разработчик - 😼FtXivan YT😼#0049**\nХелп команда - ft;help\n**Префикс ft;**", colour = discord.Color.green())
    emb.add_field(name = 'Разработан на', value = "Discord.py\nPython 3.9",inline=False)
    emb.add_field(name = 'МОЙ Инвайт', value = "[Сюды](https://discord.com/api/oauth2/authorize?client_id=788968021355528212&permissions=8&scope=bot)",inline=True)
    emb.add_field(name = 'DiscordApp', value = "[Сюды](https://discord.com)",inline=True)
    emb.add_field(name = 'Сервер разраба', value = "[Сюды](https://discord.gg/2STFYbKYGC)",inline=True)
    emb.set_footer(text= ctx.message.author.name,icon_url = ctx.author.avatar_url)
    await ctx.send(embed=emb)

@client.command(pass_context=True)
async def vote(ctx,sts ,*, texts):
    if ctx.message.author.guild_permissions.administrator:
        if sts == "1":
            await ctx.send(ctx.message.guild.default_role)
        if sts == "0":
            await ctx.send("||Да да нету пинга||")
        emb = discord.Embed( title = "**:yum: Голосование :zany_face: **",description = texts, colour = discord.Color.green())
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await msg.add_reaction("🧐")
    else:
        await ctx.send("**ТЫ ЧТО-ТО ПОПУТАЛ => у тебя недостаточно прав**")

@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="Я тут подвез МеМаСыКи", description="only english language", colour = discord.Color.green())
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(pass_context=True)
async def nsfw(ctx):
    if ctx.channel.is_nsfw():
        embed = discord.Embed(title="SEX", description="оу дап", colour = discord.Color.blue())  
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
    else:
       embed = discord.Embed(title=":smirk: Кхм Кхм :smirk: ", description="Мне кажется ты не туда эту команду ввел\n**Веведи её в nsfw канал а потом делай дела**\nХехе",colour = discord.Color.blue())  
       await ctx.send(embed=embed)

@client.command(pass_context=True)
async def comment(ctx, member: discord.Member,*, reason):
    guild = ctx.message.guild
    await member.send("Эй дружище, ты получил замечание на сервере {}\nПо поводу: {}".format(guild.name, reason))

client.run(TOKEN)
