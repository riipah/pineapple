from PluginManager import PluginManager
import discord

print("Starting Pineapple")
print("Starting Discord Client")
# Creates a discord client, which we will use to connect and interact with the server.
# All methods with @client.event annotations are event handlers for this client.
client = discord.Client()

print("Loading plugins")
# Loads and initializes the plugin manager for the bot
pm = PluginManager("plugins/", client)
pm.load_plugins()
pm.register_events()
print("Plugins loaded and registered")


@client.event
async def on_ready():
    """
    Event handler, fires when the bot has connected and is logged in
    """
    print('Logged in as ' + client.user.name + " (" + client.user.id + ")")

    # Change nickname to nickname in configuration
    for instance in client.servers:
        await client.change_nickname(instance.me, pm.botPreferences.nickName)


@client.event
async def on_message(message):
    """
    Event handler, fires when a message is received in the server.
    :param message: discord.Message object containing the received message
    """
    try:
        if message.content.startswith(pm.botPreferences.commandPrefix):
            # Send the received message off to the Plugin Manager to handle the command
            words = message.content.partition(' ')
            await pm.handle_command(message, words[0][len(pm.botPreferences.commandPrefix):], words[1:])
    except Exception as e:
        await client.send_message(message.channel, "Error: " + str(e))


@client.event
async def on_typing(channel, user, when):
    """
    Event handler, fires when a user is typing in a channel
    :param channel: discord.Channel object containing channel information
    :param user: discord.Member object containing the user information
    :param when: datetime timestamp
    """
    try:
        await pm.handle_typing(channel, user, when)
    except Exception as e:
        await client.send_message(channel, "Error: " + str(e))


@client.event
async def on_message_delete(message):
    """
    Event handler, fires when a message is deleted
    :param message: discord.Message object containing the deleted message
    """
    try:
        if message.author.name != "PluginBot":
            await pm.handle_message_delete(message)
    except Exception as e:
        await client.send_message(message.channel, "Error: " + str(e))


# Run the client and login with the bot token (yes, this needs to be down here)
client.run(pm.botPreferences.token)
