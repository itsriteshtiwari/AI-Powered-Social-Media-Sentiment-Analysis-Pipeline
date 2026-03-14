import pandas as pd
import time
import re
import matplotlib.pyplot as plt
import seaborn as sns
from google import genai

# ==========================================
# 1. SETUP GEMINI API
# ==========================================
# PASTE YOUR BRAND NEW API KEY HERE
API_KEY = "API KEY HERE" 
client = genai.Client(api_key=API_KEY)

def get_gemini_sentiment(text):
    # PRE-PROCESSING: Convert to string and remove URLs from the tweet
    # This prevents the AI from getting confused or blocked by safety filters
    clean_text = str(text)
    clean_text = re.sub(r'http\S+', '', clean_text).strip()
    
    prompt = f"""
    You are an expert sentiment analysis tool. 
    Analyze the sentiment of the following text.
    Return ONLY one of the following exact words: Positive, Negative, or Neutral.
    
    Text: "{clean_text}"
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Check if the AI returned a valid text response
        if response.text:
            result = response.text.strip().capitalize()
            # Clean up just in case the AI adds a period (e.g., "Positive.")
            result = result.replace(".", "")
            
            # Ensure it only returns one of our 3 accepted words
            if result in ["Positive", "Negative", "Neutral"]:
                return result
            else:
                return "Neutral" # Fallback if the AI gives a weird answer
        else:
            return "Neutral"
            
    except Exception as e:
        # If it fails, print the EXACT reason to the terminal
        print(f"\n[API ERROR]: {e}")
        
        # If we hit a rate limit, force the script to pause longer
        if "429" in str(e) or "quota" in str(e).lower():
            print("Rate limit detected! Pausing for 15 extra seconds...")
            time.sleep(15)
            
        return "Error"

# ==========================================
# 2. LOAD YOUR CSV DATA
# ==========================================
print("Loading CSV file...")
df = pd.read_csv('ChatGPT tweets.csv')

# Slice the dataframe to test the first 50 rows
df = df.head(5) 
print(f"Loaded {len(df)} rows for analysis.\n")

# ==========================================
# 3. PROCESS WITH RATE LIMIT HANDLING
# ==========================================
print("Starting AI analysis (this will take a few minutes to avoid rate limits)...")

sentiments = []

for index, row in df.iterrows():
    # Grabbing the exact text column from your dataset
    text_to_analyze = row['text'] 
    
    result = get_gemini_sentiment(text_to_analyze)
    sentiments.append(result)
    
    # Sleep 5 seconds to stay under the 15 Requests Per Minute free tier limit
    time.sleep(5) 
    
    if (index + 1) % 5 == 0:
        print(f"Processed {index + 1} rows...")

df['sentiment'] = sentiments

# ==========================================
# 4. SAVE & VISUALIZE
# ==========================================
# Save the successfully analyzed data
df.to_csv('analyzed_social_data.csv', index=False)
print("\nAnalysis complete! Results saved to 'analyzed_social_data.csv'.")

# Visualize
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 5))

sns.countplot(
    data=df, 
    x='sentiment', 
    hue='sentiment', # <-- Added this to fix the warning
    palette={'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c', 'Error': '#34495e'},
    order=['Positive', 'Neutral', 'Negative', 'Error'],
    legend=False     # <-- Added this to keep the chart clean
)

plt.title('ChatGPT Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.tight_layout()
plt.show()