import pandas as pd
import re
from langdetect import detect


# Function to check if text is English
def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False
    
    
# Load your CSV
df = pd.read_csv(r"C:\Users\verma\OneDrive\Desktop\HumanAI task\mental_health_tweets.csv")

# Clean the 'content' column
def clean_content(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'^rt\s+', '', text)  # Remove "RT" at the start
    return text.strip()

# Apply language filter
# Remove non-English tweets
df = df[df["content"].apply(lambda x: is_english(str(x)))]

# Clean the content column
df["content"] = df["content"].apply(clean_content)

# Save cleaned CSV
df.to_csv("cleaned_mental_health_tweets.csv", index=False)

print("Cleaned CSV saved as 'cleaned_mental_health_tweets.csv'")
