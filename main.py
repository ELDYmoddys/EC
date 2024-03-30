import discord
import asyncio

from discord.ext import tasks, commands
from datetime import datetime
from actions import Actions

PREFIXES = ['!', 'ec!'] # add/change accordingly to your usage
CURRENCY = 'EC' # change to your currency ticker
COOLDOWN = 2 # cooldown between messages (seconds)
DECIMALS = 6 # decimal places for your currency (ie. with 6, the smallest division is 0.000001)
EMB_COLOUR = 0x000000 # colour of embed (hex)

client = commands.Bot(command_prefix = PREFIXES, intents=discord.Intents.all(), help_command=None)

@client.event
async def on_ready():
    print(f"Hello World :D!\nLogged in as {client.user}\nClient ID: {client.user.id}\n""")
    status_change.start()

@tasks.loop()
async def status_change():
    statuses = ["made w/ ❤️ by eld_!", "your status here..!", "hello world :O"] # add/edit status selection to your choosing

    for status in statuses:
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type = discord.ActivityType.watching, name = f"{status}"))
        await asyncio.sleep(20) # time between changes in status (set to 20 seconds)

@client.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def hello(ctx):
    # says hello :D
    await ctx.send(f"Hello, {ctx.author.name}!")

@client.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def create(ctx):

    check = Actions.fetch_balance(ctx.author.id)[0]

    if check == -1:
        Actions.create_user()
        await ctx.send(f"`Success!`\nYour account has been created! Run `{PREFIXES[0]}help` for assistance!")
    else:
        await ctx.send("`Error!`\nYou already have an account!")

@client.command(aliases=['b', 'bal', 'bank', 'wallet'])
@commands.cooldown(1, 2, commands.BucketType.guild)
async def balance(ctx, *uid):
    
    if len(uid) != 0:
        uid = ''.join(uid).strip('<@>')
        try:
            user = await ctx.bot.fetch_user(uid)
        except:
            await ctx.send("`Error!`\nUser does not exist! Please check input.")
        else:
            balance, blocks = Actions.fetch_balance(uid)
            title = f"{user.name}'s Balance"
    else:
        balance, blocks = Actions.fetch_balance(ctx.author.id)
        if balance is not False:
            user = ctx.author
            title = "Your Balance"
        else:
            await ctx.send(f"`Error!`\nYou don't have an account! Create one by running `{PREFIXES[0]}create`!")
    
    if balance is not False:
        embed=discord.Embed(title=title, color=EMB_COLOUR, timestamp=datetime.now())
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="💵 Currency", value="{:{}} {}".format(balance, DECIMALS, CURRENCY), inline=False)
        embed.add_field(name="☑️ Blocks", value=f"{blocks:,} block(s) mined", inline=False)
        embed.set_footer(text="Bot made with ❤️ by eld_!")
        await ctx.send(embed=embed)
    elif balance == -1 and len(uid) != 0:
        await ctx.send(f"`Error!`\nOop! Looks like {user.name} does not have an account.")

@client.command(aliases=['give', 'send'])
@commands.cooldown(1, 2, commands.BucketType.user)
async def pay(ctx, reciever, amount):

    if Actions.fetch_balance(ctx.author.id) != -1:
        reciever = reciever.strip('<@>')
        try:
            reciever = await ctx.bot.fetch_user(reciever)
        except:
            await ctx.send("`Error!`\nInvalid mention or ID.")
        else:
            txn_hash, fail_case = Actions.transaction(ctx.author.id, reciever.id, amount)
    else:
        txn_hash = None
        fail_case = 'no_bal_self'

    if txn_hash is None:
        if fail_case == 'invalid_amt':
            embed=discord.Embed(title="Transaction failed!", description=f"The amount you're sending must be **greater**\n**than zero** or **within the lowest accepted**\n**decimal point** of {DECIMALS} points!", color=EMB_COLOUR)
            embed.set_footer(text=f"Please try again, {ctx.author.name}!")
            await ctx.send(f"<@{ctx.author.id}>", embed=embed)
        elif fail_case == 'no_bal_self':
            embed=discord.Embed(title="Transaction failed!", description=f"You don't have an account! To start, please run `!create`!", color=EMB_COLOUR)
            embed.set_footer(text=f"Please try again, {ctx.author.name}!")
            await ctx.send(f"<@{ctx.author.id}>", embed=embed)
    else:
        embed=discord.Embed(title="Transaction success!", description=f"**{"{:{}} {}".format(amount, DECIMALS, CURRENCY)}** was sent to **{reciever.name}**.", color=EMB_COLOUR)
        embed.add_field(name="Hash:", value=f"`{txn_hash}`", inline=True)
        embed.set_footer(text=f"Currency sent by {ctx.author.name}!")
        await ctx.send(f"<@{ctx.author.id}>", embed=embed)


def build_embed(emb_type, *extra_info):

    pass

client.run('your discord token')
