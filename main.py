import discord
import os
import snscrape.modules.twitter as sntwitter
import pandas as pd
from replit import db

my_secret = os.environ['TOKEN']
client = discord.Client()


maxTweets = 20

users = ['Logic301', 'DrLupo', 'CriticalRole']

tweets_list1 = []

def get_tweets():
  for x in users:
    for i,tweet in enumerate(sntwitter.TwitterUserScraper(username=x).get_items()):
      if i > maxTweets:
        break
      tweets_list1.append([ tweet.date, tweet.url])

      tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'URL'])

    tweets_df1 = tweets_df1.sort_values(by=['Datetime'], ascending=True)
    tweets_df1['Datetime'] = tweets_df1['Datetime'].dt.strftime("%Y-%m-%d %H:%M:%S")
  return tweets_df1

def add_users(user):
  if "users" in db.keys():
    users = db["users"]
    users.append(user)
    db["users"] = users
  else:
    db["users"] = [user]
    

def delete_users(index):
  users = db["users"]
  if len(users) > index:
    del users[index]
  db["users"] = users



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  tweets = pd.DataFrame(get_tweets(), columns= ['Datetime', 'URL'] )

  if len(tweets.index) < 1:
    return
  else:
    channel = client.get_channel(866364461786464259)
    async for message in channel.history(limit = 10, oldest_first=False):
      if message.author == client.user:
        lastMessageTime = message.created_at
        #print (lastMessageTime)
        break
    print (lastMessageTime)
    tweets = tweets[tweets['Datetime'] > lastMessageTime.strftime("%Y-%m-%d %H:%M:%S")]
    print(len(tweets.index))
    #print(tweets['Datetime'][0])
    
    if len(tweets.index) < 1:
      return
    else:
      for ind in tweets.index:
        print(tweets['URL'][ind])
        await channel.send(tweets['URL'][ind])


@client.event
async def on_message(message):
  if message.author == client.user:
    return


  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


client.run(my_secret)

