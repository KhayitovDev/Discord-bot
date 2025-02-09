from datetime import datetime
import discord
from discord.ext import commands
from app.utils import insert_language_preference
from app.models import LanguagePreference, WikipediaChanges
from core.config import settings

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(settings.CHANNEL_ID)
    await channel.send(f"Hello, this is our Wiki bot")
    
@bot.command()
async def setLang(ctx, language: str):

    await insert_language_preference(user_id=ctx.author.id, language=language) 
    await ctx.send(f"You have set your language to: {language}")
    return

@bot.command()
async def changeLang(ctx, language: str):
    user_id = ctx.author.id 
    language_preference = await LanguagePreference.find_one(LanguagePreference.user_id == user_id)
    if language_preference:
        language_preference.language = language
        await language_preference.save()
        
        await ctx.send(f"You successfully changed your preferred language to: {language}")
        return
    else:
        await ctx.send(f"You have not set any language preference yet.")
        return
    
@bot.command()
async def recent(ctx):
    user_id = ctx.author.id 
    language_preference = await LanguagePreference.find_one(LanguagePreference.user_id == user_id)
    
    if language_preference:
        language = language_preference.language
        documents = await WikipediaChanges.find(WikipediaChanges.language == language).to_list()

        if documents:
            for doc in documents:
                title = doc.title
                title_url = doc.title_url
                comment = doc.comment
                timestamp = doc.timestamp
                user = doc.user
                
                message = (
                    f"**Recent Change:**\n"
                    f"**Title:** {title}\n"
                    f"**Comment:** {comment}\n"
                    f"**User:** {user}\n"
                    f"**Timestamp:** {timestamp}\n"
                    f"**Language:** {language.capitalize()}\n"
                    f"**Url:** {title_url}\n"
                    "--------------------------------------"
                )
                
                await ctx.send(message)
        else:
            await ctx.send("No recent changes found for your preferred language.")
    else:
        await ctx.send("You haven't set a language preference yet.")
        
    return

@bot.command(name="stats")
async def stats(ctx, date: str = None, language: str = "en"):
    """
    Example: !stats 2025-02-09 en
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        await ctx.send("Invalid date format. Please use yyyy-mm-dd.")
        return
    try:
        changes_count = await WikipediaChanges.find(
            {"date": {"$gte": datetime.combine(date_obj, datetime.min.time()), "$lt": datetime.combine(date_obj, datetime.max.time())}, "language": language}
        ).count()

        if changes_count > 0:
            await ctx.send(f"On {date}, there were {changes_count} changes for the '{language}' language.")
        else:
            await ctx.send(f"No changes found for {date} in '{language}' language.")
    except Exception as e:
        await ctx.send(f"An error occurred while fetching stats: {e}")
