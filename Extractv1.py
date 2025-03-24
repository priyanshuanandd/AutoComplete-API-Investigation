import requests
import time
import json
import os

# API configuration
API_URL = "http://35.200.185.69:8000/v1/autocomplete?query="

# Global sets and counters
ALL_STRINGS = set()
VISITED_QUERIES = set()
API_CALLS = 0

# Character set: a-z only
CHARACTERS = "abcdefghijklmnopqrstuvwxyz"

# File paths
PROGRESS_FILE = "progressv1.json"
OUTPUT_FILE = "all_stringsv1running.txt"

def save_progress():
    """Save current state to JSON and update output file."""
    state = {
        "all_strings": list(ALL_STRINGS),
        "visited_queries": list(VISITED_QUERIES),
        "api_calls": API_CALLS
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(state, f)
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Total API calls made: {API_CALLS}\n")
        f.write("\n".join(sorted(ALL_STRINGS)))
    print(f"Progress saved: {API_CALLS} API calls, {len(ALL_STRINGS)} strings")

def load_progress():
    """Load saved state from JSON file if it exists."""
    global ALL_STRINGS, VISITED_QUERIES, API_CALLS
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            state = json.load(f)
            ALL_STRINGS = set(state["all_strings"])
            VISITED_QUERIES = set(state["visited_queries"])
            API_CALLS = state["api_calls"]
        print(f"Loaded progress: {API_CALLS} API calls, {len(ALL_STRINGS)} strings")
        return True
    return False

def call_autocomplete_api(query):
    global API_CALLS
    max_delay = 60  # Max wait time in seconds
    delay = 1  # Start with 1s delay
    while True:
        try:
            response = requests.get(API_URL + query, timeout=5)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            print(f"Query '{query}': count={data.get('count', 0)}, results={results}")
            API_CALLS += 1
            return results
        except requests.exceptions.RequestException as e:
            print(f"Error calling API for query '{query}': {e}")
            API_CALLS += 1
            if "429" in str(e):
                print(f"Rate limit exceeded, waiting {delay}s before retry...")
                save_progress()  # Save on rate limit hit
                time.sleep(delay)
                delay = min(delay * 2, max_delay)  # Exponential backoff
            else:
                return []  # Non-429 errors return empty list
        finally:
            time.sleep(0.6)  # Base delay for /v1/ (100 req/min)

def explore_strings(curr):
    if curr in VISITED_QUERIES:
        return
    
    VISITED_QUERIES.add(curr)
    data = call_autocomplete_api(curr)
    
    ALL_STRINGS.update(data)
    
    if API_CALLS % 10 == 0:
        save_progress()
    
    if len(data) < 10:  # Max count for v1
        return
    
    laststring = data[-1]
    n = len(curr)
    if len(laststring) <= n:
        return
    
    char_at_n_plus_one = laststring[n]
    next_query = laststring[:n + 1]
    explore_strings(next_query)
    
    try:
        start_index = CHARACTERS.index(char_at_n_plus_one)
    except ValueError:
        start_index = -1
    
    for i in range(start_index, len(CHARACTERS)):
        new_char = CHARACTERS[i]
        newstring = curr + new_char
        explore_strings(newstring)

def main():
    print("Starting exploration from 'a'...")
    start_time = time.time()
    
    resumed = load_progress()
    
    start_idx = 0
    if resumed and VISITED_QUERIES:
        last_char = max([q for q in VISITED_QUERIES if len(q) == 1], default='a')
        start_idx = CHARACTERS.index(last_char) + 1
    
    for c in CHARACTERS[start_idx:]:
        explore_strings(c)
    
    save_progress()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\nExploration complete!")
    print(f"Total unique strings found: {len(ALL_STRINGS)}")
    print(f"Total API calls made: {API_CALLS}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"First 10 strings (sample): {list(ALL_STRINGS)[:10]}")

if __name__ == "__main__":
    main()