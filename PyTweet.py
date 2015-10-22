__author__ = 'james.wyst'

#########################################################
#    This program was created as a four hour exercise   #
#  for brushing up on Python.                           #
#                                                       #
#   DRAFT ONE--Pending further cleanup and revision     #
#                                                       #
#   IDEAS:                                              #
#   --Access Key and Consumer secret grabbed via REST   #
#   call                                                #
#   --Automated retweeting                              #
#   --Learning algorithms(would need a database)        #
#                                                       #
#                                                       #
#########################################################



from Tkconstants import END, CENTER
import oauth2
import urllib
import json
import Tkinter as tk




#Create a user interface class

class Example(tk.Frame):
    #place your consumer secret here
    CONSUMER_SECRET = ''
    #place your consumer key here
    CONSUMER_KEY = ''

    #access token
    ACCESS_TOKEN = ''
    #access token secret
    ACCESS_TOKEN_SECRET = ''


    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        #Create Consumer, Token and Client
        #Client will be making the calls
        self.consumer = oauth2.Consumer(key=self.CONSUMER_KEY, secret=self.CONSUMER_SECRET)
        self.token = oauth2.Token(key=self.ACCESS_TOKEN, secret=self.ACCESS_TOKEN_SECRET)

        self.client = oauth2.Client(self.consumer, self.token)


        #set picture
        self.canvas = tk.Canvas(root, width=250, height=250)
        self.canvas.pack()
        #insert photo from path on computer
        self.background_image = tk.PhotoImage(file='')
        self.canvas.create_image(125, 125, image=self.background_image)

        # create a prompt, an input box, and buttons!
        self.author_text = tk.Label(self, fg="white", bg = "#4099FF", text="Created by James Wyst", font=("sans-serif", 14))
        self.spacer = tk.Label(self, text=" ", bg="#4099FF")
        self.prompt = tk.Label(self, text="Tweet!",font=("sans-serif", 24), fg="white", bg="#4099FF")
        self.entry = tk.Entry(self,highlightbackground="#4099FF")
        self.tweet_button = tk.Button(self, text="Tweet", command = self.tweet, highlightbackground="#4099FF")
        self.taylor_swift_button = tk.Button(self, text="'I knew you were trouble when you walked in...'", command = self.i_knew_you_were_trouble_when_you_walked_in, highlightbackground="#4099FF")
        self.search_button = tk.Button(self, text="Search", command = self.search, highlightbackground="#4099FF")
        self.reply_button = tk.Button(self, text="Reply", command = self.reply, highlightbackground="#4099FF")


        #change background to twitter blue
        self.configure(bg="#4099FF")

        # lay the widgets out on the screen.
        self.author_text.pack(fill="x")

        self.spacer.pack(fill="x")
        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="both", expand=True)
        #self.output.pack(side="top", fill="x", expand=True)

        self.tweet_button.pack(side="bottom")
        self.taylor_swift_button.pack(side="bottom")
        self.search_button.pack(side="bottom")
        self.reply_button.pack(side="bottom")


    def search(self, query, return_content):
        if return_content:
            search_data = {'q': query}
        else:
            search_data = {'q': self.entry.get()}
        encode_search_data = urllib.urlencode(search_data)
        search_url = 'https://api.twitter.com/1.1/search/tweets.json?'+encode_search_data
        search_results = self.get(search_url)
        parsed_search_results = json.loads(search_results)
        all_statuses = parsed_search_results['statuses']
        if return_content:
            return all_statuses
        else:
            for tweet in all_statuses:
                print tweet['text']
                print 'Tweeted by '+ tweet['user']['screen_name']


    #You cannot post duplicate tweets--otherwise Twitter returns Status Code 403
    def tweet(self, query):
        update_url = 'https://api.twitter.com/1.1/statuses/update.json'
        if query:
            update_data = {'status': query}
        else:
            update_data = {'status': self.entry.get()}
        encode_update_data = urllib.urlencode(update_data)
        print 'I made it here'
        response = self.post(update_url, encode_update_data)
        if response:
            print response


    def get(self, url):
        resp, content = self.client.request(url, "GET", "", None)
        if resp['status']=='200':
            return content
        else:
            return "GET Request Failed! with Code: "+resp['status']

    def post(self, url, data):
        resp, content = self.client.request(url, "POST", data, None)
        print resp
        if resp['status'] != '200':
            return 'POST Request Failed! with Code: '+resp['status']+"and Content :"+content

    #Taylor Swift Problem
    def i_knew_you_were_trouble_when_you_walked_in(self):
        taylor_results = self.search('\"open data\"', 'hey')
        for taylor in taylor_results:
            if taylor['text'].find("open data") or taylor['text'].find("#OpenData"):
                print 'Tweeted by '+ taylor['user']['screen_name']
                tweet_string = taylor['text'].replace('open data', 'Taylor Swift').replace('#OpenData', '#TaylorSwift')
                print "I'm tweeting!"
                print tweet_string
                print '@I347h4m573r5'+tweet_string
                self.tweet('@I347h4m573r5'+tweet_string.encode('utf-8'))
                break

    def reply(self):
        parsed_reply_content = json.loads(self.mentions_timeline(1))
        for mention in parsed_reply_content:
            self.tweet('@'+mention['user']['screen_name'].encode('utf-8')+' Hey, I remember you!')

    def mentions_timeline(self, count):
        mentions_data = {'count': count}
        encode_mentions_data = urllib.urlencode(mentions_data)
        url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?'+encode_mentions_data
        mentions_content = self.get(url)
        return mentions_content


# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    #set Title of Application
    root.wm_title("PyTweet")
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
