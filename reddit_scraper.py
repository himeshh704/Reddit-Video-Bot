import urllib.request
import json
import re

def clean_text(text):
    """Cleans the reddit post text for TTS consumption."""
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'(?i)Edit:.*', '', text)
    text = re.sub(r'(?i)Update:.*', '', text)
    text = ' '.join(text.split())
    return text.strip()

def get_top_story(subreddit_name="nosleep", time_filter="day", min_length=50, max_length=950):
    """Fetches the top story from a public subreddit without needing API keys."""
    print(f"Fetching top stories from r/{subreddit_name} ({time_filter})...")
    url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t={time_filter}&limit=100"
    
    # We use a standard web browser User-Agent so Reddit lets us read the public page
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        posts = data.get('data', {}).get('children', [])
        
        for post in posts:
            post_data = post['data']
            # We only want text posts that are not stickied
            if not post_data.get('is_self') or post_data.get('stickied'):
                continue
            
            selftext = post_data.get('selftext', '')
            text_length = len(selftext)
            
            if min_length <= text_length <= max_length:
                title = post_data.get('title', 'Unknown')
                print(f"Selected story: {title} (Length: {text_length})")
                
                return {
                    "title": title,
                    "text": clean_text(selftext),
                    "author": post_data.get('author', 'Unknown'),
                    "url": f"https://reddit.com{post_data.get('permalink', '')}"
                }
                
        print(f"No suitable story found analyzing {len(posts)} posts.")
        return None
        
    except Exception as e:
        print(f"Failed to fetch data from Reddit: {e}")
        return None

if __name__ == "__main__":
    story = get_top_story()
    if story:
        print("\nTitle:", story['title'])
        print("\nText Snippet:", story['text'][:200], "...")
