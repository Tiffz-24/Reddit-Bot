import praw
import pdb
import re
import os
import random


class Bot:
    def __init__(self, bot_name):
        self.reddit = praw.Reddit(bot_name)  # create bot
        self.subreddit = None
        self.get_sub(self.reddit)
        self.commands()

    def commands(self):
        command = input("Enter command: ")
        if command == "reply":
            self.reply()
        if command == "automate" or command == "Marvin":
            self.automate()

    def get_sub(self, reddit):
        sub = input("Enter subreddit name: ")
        self.subreddit = reddit.subreddit(sub) #get a subreddit


    def getHotPosts(self, limit):
        for submission in self.subreddit.hot(limit=limit): #read the most popular posts
            print(submission.title + ": ")
            print(submission.selftext)
            print('\n')

    def reply(self):
        if not os.path.isfile("posts_replied_to.txt"):
            posts_replied_to = []
        else:
            with open("posts_replied_to.txt", "r") as f:
                posts_replied_to = f.read()
                posts_replied_to = posts_replied_to.split("\n")
                posts_replied_to = list(filter(None, posts_replied_to))

        self.get_sub(self.reddit)
        # Get the top 5 values from our subreddit
        post_title = input("Enter title of post: ")

        for submission in self.subreddit.hot(limit=10):
            # print(submission.title)

            # If we haven't replied to this post before
            if submission.id not in posts_replied_to:

                # Do a case insensitive search
                if re.search(post_title, submission.title, re.IGNORECASE):
                    # Reply to the post
                    reply_message = input("Enter reply message: ")
                    submission.reply(reply_message)
                    print("Bot replying to : ", submission.title)

                    # Store the current id into our list
                    posts_replied_to.append(submission.id)




        # Write our updated list back to the file
        with open("posts_replied_to.txt", "w") as f:
            for post_id in posts_replied_to:
                f.write(post_id + "\n")

    def automate(self):
        replies = []
        while 1:
            if len(replies) == 0:
                quote = input("Enter reply: ")
                replies.append(quote)
            choice = input("Enter possible bot reply? Yes or No ")
            if choice == "No":
                break
            elif choice == "Yes":
                quote = input("Enter reply: ")
                replies.append(quote)

        for comment in self.subreddit.stream.comments():
            if re.search("Marvin help", comment.body, re.IGNORECASE):
                print(comment.body)
                marvin_reply = "Marvin the Depressed Robot says: " + random.choice(replies)
                comment.reply(marvin_reply)
                print(marvin_reply)

Bot = Bot('bot1')


