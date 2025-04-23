from contextlib import nullcontext

import asyncpg
import discord
from discord.ext import commands
from discord.ui import View, Button
TOKEN = 'MTM2Mzk0NDQxOTcwNjkyOTQyNQ.GxTMM3.h05THtkpNeL8s4Idn4O76dJcFTRYFJneSo30qA'

PREFIX = '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

db_pool = None

# Declare db_pool as None initially
@bot.event
async def on_ready():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user="discord_bot_user",
        password="discord_bot_password",
        database="postgres",
        host="127.0.0.1",
        port="5432"
    )
    print(f'Bot connected as {bot.user}')

# Команда help
@bot.command()
async def info(ctx):
    info_text = (
        "🧠 Цей бот допоможе тобі обрати настільну гру!\n"
        "🔍 Доступні функції:\n"
        "• Вибір гри\n"
        "• Отримання правил гри\n"
        "• Посилання на гру\n"
        "Розважайся!"
    )
    await ctx.send(info_text)

# Команда info
@bot.command()
async def help_command(ctx):
    help_text = (
        "**📌 Список доступних команд:**\n"
        "`!info` - Інформація про бота\n"
        "`!help_command` - Список команд\n"
        "`!choose_game` - Обрати гру для гри"
    )
    await ctx.send(help_text)

@bot.command()
async def choose_game(ctx):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM games ORDER BY name")
        if not rows:
            await ctx.send("Немає доступних ігор.")
            return

        view = GameSelectionView(rows)
        await ctx.send("🎲 Обери гру:", view=view)

class GameSelectionView(View):
    def __init__(self, games):
        super().__init__(timeout=None)
        for row in games:
            self.add_item(GameButton(label=row['name'], game_id=row['id']))

class GameButton(Button):
    def __init__(self, label, game_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=str(game_id))
        self.game_id = game_id
        self.rows = []

    async def select_rules(self):
        async with db_pool.acquire() as conn:
            self.rows = await conn.fetch(f"SELECT id, name FROM rules_category WHERE game_id = {self.game_id} AND parent_id IS NULL")
            if not self.rows:
                return
            return RulesMenu(self.rows)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Ви обрали **{self.label}**. Які правила бажаєте дізнатись?",
            view = await self.select_rules(),
            ephemeral=True
        )

class RulesMenu(View):
    def __init__(self, rules):
        super().__init__(timeout=None)
        for row in rules:
            self.add_item(RulesButton(label=row['name'], rule_id=row['id']))


class RulesButton(Button):
    def __init__(self, label, rule_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=str(rule_id))
        self.rule_id = rule_id
        self.rows = []

    async def select_rules(self):
        async with db_pool.acquire() as conn:
            self.rows = await conn.fetch(f"SELECT id, content FROM rules WHERE category_id = {self.rule_id}")
            if self.rows:
                return self.rows[0][1]
            return

    async def select_category(self):
        async with db_pool.acquire() as conn:
            self.rows = await conn.fetch(f"SELECT id, name FROM rules_category WHERE parent_id = {self.rule_id}")
            if not self.rows:
                return
            return RulesMenu(self.rows)

    async def callback(self, interaction: discord.Interaction):
        if await self.select_rules():
            await interaction.response.send_message(
                f"{await self.select_rules()}",
                view=await self.select_category(),
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                view=await self.select_category(),
                ephemeral=True
            )

bot.run(TOKEN)
