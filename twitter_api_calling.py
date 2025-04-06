import tweepy
import pandas as pd
import re
from datetime import datetime
import json
import time
import os
import nltk
from dotenv import load_dotenv
from nltk.corpus import stopwords

# Download stopwords if not already present
nltk.download('stopwords')

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)


# Define keywords for filtering posts
keywords = ["depressed", "addiction help", "overwhelmed", "suicidal", 
            "mental health", "substance abuse", "helpless", "hurting myself",
            "anxiety", "stress", "panic attack", "self-harm"]

# Combine keywords into a single query (to reduce API calls)
query = " OR ".join(keywords) + " -filter:retweets"

# Function to fetch tweets with rate limit handling
def fetch_tweets(query, max_results=1000):
    tweets_data = []
    
    paginator = tweepy.Paginator(client.search_recent_tweets,query=query, 
                                             tweet_fields=["id", "text", "created_at", "public_metrics"], 
                                             max_results=100)
        
    for tweet_page in paginator:
        if tweet_page.data:
            tweets_data.extend(tweet_page.data)
        print(f"Fetched: {len(tweets_data)} tweets so far...")

        if len(tweets_data) >= max_results:
            break

    return tweets_data[:max_results]


# Text preprocessing function
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove mentions
    text = re.sub(r"#\w+", "", text)  # Remove hashtags  
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    words = text.lower().split()
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    return " ".join(words)

# Fetch and process tweets

tweets = fetch_tweets(query, max_results=1000)  # Fetch for all keywords at once
tweets_data = []
# Assuming tweets_data is a list of dictionaries


for tweet in tweets:
    cleaned_text = clean_text(tweet.text)
    tweets_data.append({
        "post_id": tweet.id,
        "timestamp": tweet.created_at.isoformat(),
        "content": cleaned_text,
        "likes": tweet.public_metrics["like_count"],
        "retweets": tweet.public_metrics["retweet_count"],
        "replies": tweet.public_metrics["reply_count"],
    })
    


# Save to CSV
df = pd.DataFrame(tweets_data)
df.to_csv("mental_health_tweets.csv", index=False)

# Save to JSON
with open("mental_health_tweets.json", "w") as f:
    json.dump(tweets_data, f, indent=4,default=str)

print("Data extraction and cleaning complete! Saved as CSV and JSON.")




