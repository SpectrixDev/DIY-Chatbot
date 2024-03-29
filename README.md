# 🗣 DIY-Chatbot 
> A lightweight chatbot that knows nothing and has to learn from scratch. Using sqlite and python. Also comes with a Discord intergration and custom Pre-Made Models.

## Introduction

### ❓ What is this? 

This is a collection of parts from a small chatbot that learns from scratch (knowing nothing at the beginning). There's different pre-made integrations that come with this, such as a Discord Intergration and a Cleverbot Intergration (learns from another bot called cleverbot for extra training). 

If you're just interested in training it in a console, there's that too (and it's really small and lightweight). It's written in Python and uses sqlite. 

### 💡 How does it work? 

It used SQL and Python to store a table of word associations for responses to a previous sentence and uses this to match future responses. It's inspired by [Cleverbot](https://www.cleverbot.com/)'s method of learning.

It learns from the previous conversation with the user. It maintains a database of previous replies to the same questions and responds based on queries from the database.

It does not extract the meaning of sentences written by the user. When the user types a message, *it is understood as an answer to previous statement made by the chatbot.* The sentence typed by the user will then be associated with the words present in the previous message. The human message is decomposed in words. The program will try to identify which sentences correspond best to those words, according to the answers that the user gave it. 

Who knows if that made any sense, but maybe the following will paint a better picture:

**Here's an example:** Let's say this bot knows nothing at the beginning, and just says "Hello" once, without knowing what that means. 

```
Bot: Hello
User: Hey, how are you?
```

The bot now knows that if a user tells it, "Hello", it can respond with, "Hey, how are you". But now the bot doesn't know how to respond to, "Hey, how are you?", so it selects something random that it doesn't know in order to learn more. In this case, the only thing it doesn't know is how to respond to the previous question. So this will happen:

```
User: Hey, how are you? 
Bot: Hey, how are you? 
User: I'm fine thanks, how are you? 
```

Eventually (and at a fast rate), it will know a lot more answers, and barely repeats the user. *It doesn't just repeat the same thing that the user says that it doesn't know. Once it's been chatted with enough, it will only ask what the user asked later on.* It might be hard to understand, but once you use it you'll see what I mean.

**Here's one more example:**

```
User: I'm fine thanks, how are you? 
Bot: I'm fine thanks, how are you? 
User: I'm fine. How are you? 
Bot: I'm fine thanks, how are you? 
User: I'm good. 
Bot: I'm fine. How are you? 
User: Doing good. 
Bot: I'm good.
```

As you can see, it's learnt only from user input. 

## ⚙ Setting up

Setup is very easy and fast. However there's extra steps depending on what you want to do. 

### ✅ Basic Setup. 

1. Firstly, *clone the repo or download the zip* (obviously).

2. Next, install the required libaries. You'll mainly need *sqlite3*, which can easily be installed with pip.

```bash
pip install sqlite3
```

3. Go to the Basic Bot folder.

If you want to start from scratch (without the bot knowing anything), simply run the file with no botBrain.sqlite file in the directory.

If you want to start with one of my pretrained models, add it to the Basic Bot folder and name it "botBrain.sqlite". See the README in the models folder or the Basic Bot folder for more info. 


### 👥 Discord Intergration

**The Discord Intergration allows you to let your bot chat to users in your server in a specific channel.**

Fill in the required values in the **config.json** (bot token and channel ID), then simply run **bot.py**.

Not sure how to fill it in? I've provided more detail in [this README](https://github.com/SpectrixOfficial/DIY-Chatbot/blob/master/Discord%20Bot/README.md)

**Here's an example:**

![](https://cdn.discordapp.com/attachments/478201257417244675/516637578167058448/unknown.png)

### 🧠 Pre-Made Models

**I've created my own premade models for everyone**, so if you *don't feel like compeltely training yourself, it can have a small headstart.* You can find them in the **Pre-Made Models** folder. ~~These are essentially a variety of different brains ;)~~ You don't have to use these, and I'll be adding more/training them more. These are created by letting my bot chat to other chatbots, as well as humans. It uses mostly correct grammar and is pretty good.

If you'd like to use them, put them in the same directory as the bot's main file, and name it **botBrain.sqlite**. The bot will still learn from users after starting off with this file.

## 🤝 Contributing

I really appriciate contributions, as I'm not perfect and quite lazy. I know there's many flaws in my program, but we can make it better together. Open up a pull request, or even an issue. I'll check it out! Or, just give the repo a star, I appriciate it! 
