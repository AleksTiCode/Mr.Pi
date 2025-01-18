import disnake
from disnake.ext import commands
from disnake import Guild
import sqlite3

def create():
    conn = sqlite3.connect('MrPi.db')
    bd = conn.cursor()
    bd.execute('''CREATE TABLE IF NOT EXISTS servers
               (guild_id INTEGER PRIMARY KEY, role_id TEXT, channel_id TEXT, invite TEXT, log_id TEXT)''')
    conn.commit()
    conn.close()

intents = disnake.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

bot = commands.InteractionBot(intents=intents, activity=disnake.Game(name='Кого забанить)'))

@bot.event
async def on_ready():
    print(f'Bot is online {bot.user}')

@bot.event
async def on_guild_remove(guild: Guild):
    conn = sqlite3.connect('MrPi.db')
    bd = conn.cursor()
    bd.execute('DELETE FROM servers WHERE guild_id = ?', (guild.id,))
    conn.commit()
    conn.close()

@bot.event
async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title='У вас нет прав',
            description='Чтобы использовать этого бота вы должны иметь разрешение администратора либо отдельные разрешения связанные с определённой командой.',
            color=disnake.Color.from_rgb(255,0,0))
        await inter.send(embed=embed, ephemeral=True)


bot.load_extensions("cogs")
create()
bot.run('token')