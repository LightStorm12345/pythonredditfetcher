import json
import urllib.request
from os import system
from sys import argv  # used to get the command line arguements

args = argv  # get all text
args.pop(0)  # remove first element because its the file name
subreddit = args[0]
num_of_media = int(args[1])

url = "https://www.reddit.com/r/{}.json?limit=102".format(subreddit) # url
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36/8mqQhSuL-09" # the user agent in the request, so reddit leaves us alone

req = urllib.request.Request(url, data=None, headers={"User-Agent": user_agent}) # the request to pass through
try:
    jsonString = urllib.request.urlopen(req) # make the url request
except urllib.error.HTTPError as reason: # if reddit is upsetti
    print(reason) # tell us why reddit upsetti
    exit()

# decode the json data
jsonString = jsonString.read()
jsonString = jsonString.decode("utf-8")
jsonDict = json.loads(jsonString)

if jsonDict["data"]["dist"] == 0: # check whether or not the subreddit exists
    print("Error Subreddit does not exist")
    exit()

urls = []
validEnds = (".jpg",".png",".gif",".vgif") # make sure we are receiving the correct file types

for postID in range(jsonDict["data"]["dist"]):
    if jsonDict["data"]["children"][postID]["data"]["url"].endswith(validEnds): # only add the correct urls
        urls.append(jsonDict["data"]["children"][postID]["data"]["url"])

    if len(urls) == num_of_media: # when we have all the media needed
        break

if len(urls) == 0:
    print("No images found")
    exit()

for url in urls:
    system("wget {}".format(url))
