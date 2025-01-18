import disnake
from disnake.ext import commands
from app import bot
import sqlite3

class Unban(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
    
    @commands.slash_command(name='unban', description='Разбан пользователя')
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, inter: disnake.ApplicationCommandInteraction, member: str):
            try:    
                conn = sqlite3.connect('MrPi.db')
                bd = conn.cursor()
                bd.execute('SELECT log_id FROM servers WHERE guild_id = ?', (inter.guild.id,))
                bd_par = bd.fetchone()
                log_channel = bd_par[0]
                conn.close()        
            
                channel = bot.get_channel(int(log_channel))
                try:
                    user = await bot.fetch_user(int(member))
                    await inter.guild.unban(user)
                
                    embed_unban  = disnake.Embed(
                        title='Произошёл разбан на сервере!!!',
                        description=f'Участник {user.mention} был разбанен\nНадеемся, он исправился)',
                        color=disnake.Color.from_rgb(0,77,255))
                    await inter.send(content=f'_Успешно\nУчастник {user.mention} разбанен_', ephemeral=True)
                    await channel.send(embed=embed_unban)
                except disnake.NotFound:
                    embed = disnake.Embed(
                        title='Пользователь не забанен либо указано неправильное id пользователя',
                        color=disnake.Color.from_rgb(255,0,0))
                    await inter.send(embed=embed, ephemeral=True)
            except Exception:
                embed_TE = disnake.Embed(
                    title='Не удалось(',
                    description='Для того, чтобы использовать бота администратор сервера должен его настроить.\nЕсли же бот настроен, то значит в его настройке есть ошибка.\nЕсли же бот настроен правильно, то это может быть связано с тем, что бот не имеет доступа к каналу логов, либо роль бота ниже роли участника, которого надо разбанить\nТакже проверьте разоешения бота: с версии 1.1.2 для бота требуется разрешение "администратор"\nСообщите администратору об этом!',
                    color=disnake.Color.from_rgb(255,0,0))
                await inter.send(embed=embed_TE, ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(Unban(bot))