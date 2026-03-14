import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD AND CLEAN THE DATA
# ==========================================
print("Loading dataset...")
df = pd.read_csv('ChatGPT tweets.csv')

# Clean up the Date column so Python understands it as a real date/time
# We use 'format=mixed' to handle any weird date formatting automatically
df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')

# Drop rows where Date didn't parse correctly
df = df.dropna(subset=['Date'])

print(f"Successfully loaded {len(df)} tweets!")

# ==========================================
# 2. SETUP THE DASHBOARD
# ==========================================
# We are going to create a 2x2 grid of charts
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('ChatGPT Twitter Dataset Analysis', fontsize=20, fontweight='bold')

# ==========================================
# CHART 1: TIME ANALYSIS (Date column)
# ==========================================
print("Analyzing dates...")
# Extract just the date (ignoring the exact time) to see daily volume
df['Just_Date'] = df['Date'].dt.date
daily_counts = df['Just_Date'].value_counts().sort_index()

axes[0, 0].plot(daily_counts.index, daily_counts.values, marker='o', color='#3498db', linewidth=2)
axes[0, 0].set_title('Tweet Volume Over Time', fontsize=14)
axes[0, 0].set_ylabel('Number of Tweets')
axes[0, 0].tick_params(axis='x', rotation=45)

# ==========================================
# CHART 2: TOP LOCATIONS (user_location column)
# ==========================================
print("Analyzing locations...")
# Count the top 10 locations, dropping empty ones
top_locations = df['user_location'].dropna().value_counts().head(10)

sns.barplot(
    x=top_locations.values, 
    y=top_locations.index, 
    ax=axes[0, 1], 
    hue=top_locations.index,
    palette='viridis',
    legend=False
)
axes[0, 1].set_title('Top 10 User Locations', fontsize=14)
axes[0, 1].set_xlabel('Number of Tweets')

# ==========================================
# CHART 3: TOP USERS (user_name column)
# ==========================================
print("Analyzing most active users...")
top_users = df['user_name'].dropna().value_counts().head(10)

sns.barplot(
    x=top_users.values, 
    y=top_users.index, 
    ax=axes[1, 0], 
    hue=top_users.index,
    palette='magma',
    legend=False
)
axes[1, 0].set_title('Top 10 Most Active Users', fontsize=14)
axes[1, 0].set_xlabel('Number of Tweets')

# ==========================================
# CHART 4: INFLUENCER ANALYSIS (user_friends column)
# ==========================================
print("Analyzing friend counts...")

# THE FIX: Force the 'user_friends' column to be numeric numbers. 
# errors='coerce' tells Pandas: "If you find weird text you can't turn into a number, just make it blank (NaN)"
df['user_friends'] = pd.to_numeric(df['user_friends'], errors='coerce')

# Now that they are definitely numbers, we can safely do the math!
normal_users = df[df['user_friends'] < 10000]

# Check if we actually have data to plot to avoid empty graph errors
if not normal_users.empty:
    sns.histplot(normal_users['user_friends'], bins=30, ax=axes[1, 1], color='#e74c3c', kde=True)
    axes[1, 1].set_title('Distribution of User Friends (0-10k)', fontsize=14)
    axes[1, 1].set_xlabel('Number of Friends')
    axes[1, 1].set_ylabel('Frequency')
else:
    axes[1, 1].set_title('Not enough numeric data for Friends', fontsize=14)

# ==========================================
# 3. SHOW THE DASHBOARD
# ==========================================
plt.tight_layout()
# Adjust layout so the main title doesn't overlap with the charts
plt.subplots_adjust(top=0.92) 
print("\nGenerating charts... close the chart window to end the script.")
plt.show()