import discord
import asyncio
import os
import twitchcheck
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# setting up the bot and prefix.
prefix = "!"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")


# startup
@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)

    # change status
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("being lukas' buddy"))


async def twitchchecker():
    streamping = False
    await bot.wait_until_ready()
    channel = int(os.getenv("CHANNEL"))
    channel = bot.get_channel(channel)  # Insert channel ID here
    while not bot.is_closed():
        jsondata = twitchcheck.checkuser("lukeitslukas")
        if jsondata == "empty":
            streamping = False
        if jsondata != "empty":
            if not streamping:
                embed = discord.Embed(title="https://www.twitch.tv/lukeitslukas", url="https://www.twitch.tv"
                                                                                      "/lukeitslukas",
                                      color=0xff0080)
                embed.set_author(name="lukeitslukas is now streaming")
                embed.set_thumbnail(url="https://static-cdn.jtvnw.net/jtv_user_pictures/d4b76918-2335-4793-89f8"
                                        "-798fc40c2ab6-profile_image-70x70.png")
                embed.add_field(name="Whats Happening?", value=jsondata['stream']['channel']['status'], inline=True)
                embed.add_field(name="Playing", value=jsondata['stream']['game'], inline=True)
                embed.set_footer(text="say hi c:")
                embed.set_image(url=jsondata['stream']['preview']['large'])
                msg = "@everyone, lukeitslukas is live"
                await channel.send(msg, embed=embed)
                streamping = True
        await asyncio.sleep(60)


@bot.command()
async def ping(ctx):
    await ctx.send("shut")


# let him out
if __name__ == "__main__":
    bot.loop.create_task(twitchchecker())
    token = os.getenv("BOTTOKEN")
    bot.run(token)
