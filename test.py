import discord
from discord.ext import commands
import json
import requests
from discord.utils import get

help_text = 'Салям-малейкум\nЯ школьник учусь обслуживать сервера\n\n~~СПИСОК МОИХ КОМАНД~~\n\n #удали5 - Удалить 5 сообщений \n #удали10 - Удалить 10 сообщений  \n #удали50 - Удалить 50 сообщений \n #удали100 - Удалить 100 сообщений \n\n~~СПИСОК ЭМБЕДОВ~~\n\n #сообщение слово - Вместо слово можно предложение вставить(сообщение)\n#важно слово - Вместо слово можно предложение вставить(Важное сообщение)\n\n~~МОДЕРАЦИЯ~~\n\n#БАН @пользователь - забанить пользователя\n#пых @пользователь - ВЫКИНУТЬ НАФИГ @пользователя \n\n~~ПРИКОЛЬЧИКИ~~\n\n#скажи слово - скажет предложение от бота(может пинговать)'
TOKEN = 'префикс'
client = commands.Bot(command_prefix = '#')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Школота готова'))
    print('Школота готова')

@client.command()
async def школяр(ctx):
    embd = discord.Embed(color = 0x00ffae, description = help_text, title = 'Немного о мне')
    await ctx.channel.send(embed = embd)

@client.command()
async def удали5(ctx):
    await ctx.channel.purge(limit=6)
    embd = discord.Embed(color = 0x00ffae, description = 'Было удалено 5 сообщений\nПо моему как-то мало', title = 'Удалено')
    await ctx.channel.send(embed = embd)

@client.command()
async def удали10(ctx):
    await ctx.channel.purge(limit=11)
    embd = discord.Embed(color = 0x00ffae, description = 'Было удалено 10 сообщений\nУдалил самое главное', title = 'Удалено')
    await ctx.channel.send(embed = embd)

@client.command()
async def удали50(ctx):
    await ctx.channel.purge(limit=51)
    embd = discord.Embed(color = 0x00ffae, description = 'Было удалено 50 сообщений\nПочистил так-то норм', title = 'Удалено')
    await ctx.channel.send(embed = embd)

@client.command()
async def удали100(ctx):
    await ctx.channel.purge(limit=101)
    embd = discord.Embed(color = 0x00ffae, description = 'Было удалено 100 сообщений\nНе переборщил ты или как', title = 'Удалено')
    await ctx.channel.send(embed = embd)
     
@client.command()
async def скажи(ctx, *,arg):
    await ctx.channel.send(arg)
    
@client.command(pass_context = True)
async def БАН(ctx, user: discord.Member ):
    await ctx.channel.send('⬇━ОН УЛЕТАЕТ ИЗ СЕРВАКа В БАН')
    await ctx.channel.send(user)
    await user.ban(reason=None)

@client.command(pass_context = True)
async def пых(ctx, user: discord.Member ):
    await ctx.channel.send('⬇━ОН УЛЕТАЕТ ИЗ СЕРВАКа в КЫК')
    await ctx.channel.send(user)
    await user.kick(reason=None)
    

@client.command()
async def важно(ctx, *, texts):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    embed=discord.Embed(title='⬇━━━━ВАЖНО━━━━⬇', description = texts, color=0x00ffff)
    embed.set_footer(text=author)
    await ctx.send(embed=embed)

@client.command()
async def новость(ctx, *, texts):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    embed=discord.Embed(title='НОВОСТЬ', description = texts, color=0x00bfff)
    embed.set_footer(text=author)
    await ctx.send(embed=embed)

@client.command()
async def правило(ctx, *, texts):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    embed=discord.Embed(title='⬇━━━━ПРАВИЛА━━━━⬇', description = texts, color=0x8b00ff)
    embed.set_footer(text=author)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def заткнись(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )
    await member.add_roles(mute_role)
    await ctx.channel.send('⬇━ОН Заткнулся')
    await ctx.channel.send(member)
    
@client.command(pass_context=True)
async def говори(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Мут' )
    await member.remove_roles(mute_role)
    await ctx.channel.send('⬇━ОН Умеет разговаривать')
    await ctx.channel.send(member)

@client.command(pass_context=True)
async def music(ctx, channel):
    url = ctx.message.content
    url = url.strip('https://www.youtube.com/watch?v=naIKplXzxTY')

    vc = await client.connect(channel)

client.run(TOKEN)
