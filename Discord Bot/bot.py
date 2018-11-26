import discord, asyncio; from discord.ext import commands

import re, json, sqlite3
from collections import Counter
from string import punctuation
from math import sqrt

connection = sqlite3.connect('botBrain.sqlite')
cursor = connection.cursor()

with open("config.json") as f:
    config = json.load(f)

create_table_request_list = [
    'CREATE TABLE words(word TEXT UNIQUE)',
    'CREATE TABLE sentences(sentence TEXT UNIQUE, used INT NOT NULL DEFAULT 0)',
    'CREATE TABLE associations (word_id INT NOT NULL, sentence_id INT NOT NULL, weight REAL NOT NULL)',
]
for create_table_request in create_table_request_list:
    try:
        cursor.execute(create_table_request)
    except:
        pass

def get_id(entityName, text):
    """Retrieve an entity's unique ID from the database, given its associated text.
    If the row is not already present, it is inserted.
    The entity can either be a sentence or a word."""
    tableName = entityName + 's'
    columnName = entityName
    cursor.execute('SELECT rowid FROM ' + tableName + ' WHERE ' + columnName + ' = ?', (text,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute('INSERT INTO ' + tableName + ' (' + columnName + ') VALUES (?)', (text,))
        return cursor.lastrowid

def get_words(text):
    """Retrieve the words present in a given string of text.
    The return value is a list of tuples where the first member is a lowercase word,
    and the second member the number of time it is present in the text."""
    wordsRegexpString = '(?:\w+|[' + re.escape(punctuation) + ']+)'
    wordsRegexp = re.compile(wordsRegexpString)
    wordsList = wordsRegexp.findall(text.lower())
    return Counter(wordsList).items()

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name="your messages and learning...", type=3))
    print("=========\nConnected\n=========\n")
    

async def __local_check(ctx):
        return await ctx.channel.id == await bot.get_channel(config['chatbotChannelID'])

async def chatbot():
    await bot.wait_until_ready()
    B = "Hello World."
    channel = bot.get_channel(config['chatbotChannelID'])
    def message_check(msg):
            return msg.channel == channel and msg.author.bot == False
    while not bot.is_closed():
        if B == '':
            pass
        try:
            await channel.send(B)
        except Exception:
            pass
        H = await bot.wait_for('message', check=message_check)
        print("Recieved user input")
        ctx = await bot.get_context(H)
        H = await commands.clean_content().convert(ctx, H.content)
        words = get_words(B)
        words_length = sum([n * len(word) for word, n in words])
        sentence_id = get_id('sentence', H)
        for word, n in words:
            word_id = get_id('word', word)
            weight = sqrt(n / float(words_length))
            cursor.execute('INSERT INTO associations VALUES (?, ?, ?)', (word_id, sentence_id, weight))
        connection.commit()
        cursor.execute('CREATE TEMPORARY TABLE results(sentence_id INT, sentence TEXT, weight REAL)')
        words = get_words(H)
        words_length = sum([n * len(word) for word, n in words])
        for word, n in words:
            weight = sqrt(n / float(words_length))
            cursor.execute('INSERT INTO results SELECT associations.sentence_id, sentences.sentence, ?*associations.weight/(4+sentences.used) FROM words INNER JOIN associations ON associations.word_id=words.rowid INNER JOIN sentences ON sentences.rowid=associations.sentence_id WHERE words.word=?', (weight, word,))
        cursor.execute('SELECT sentence_id, sentence, SUM(weight) AS sum_weight FROM results GROUP BY sentence_id ORDER BY sum_weight DESC LIMIT 1')
        row = cursor.fetchone()
        cursor.execute('DROP TABLE results')
        if row is None:
            cursor.execute('SELECT rowid, sentence FROM sentences WHERE used = (SELECT MIN(used) FROM sentences) ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
        B = row[1]
        cursor.execute('UPDATE sentences SET used=used+1 WHERE rowid=?', (row[0],))

bot.loop.create_task(chatbot())
bot.run(config['discordBotToken'])
