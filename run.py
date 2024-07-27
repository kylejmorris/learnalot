import anthropic
import os
from typing import List
import time
from tqdm import tqdm

# Initialize the Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

def generate_study_cards(prompt: str, topics: List[str], max_tokens: int = 1000):
    """
    Generate study cards using Claude AI for given topics and save them immediately.
    
    :param prompt: The base prompt to use for generating study cards
    :param topics: List of topics to generate study cards for
    :param max_tokens: Maximum number of tokens for each response
    """
    total_topics = len(topics)
    start_time = time.time()
    
    for i, topic in enumerate(tqdm(topics, desc="Generating study cards", unit="topic")):
        print(f"\nWorking on topic: {topic}")
        full_prompt = f"{prompt}\n\nTopic: {topic}"
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        content = response.content[0].text.strip()
        
        # Save the result immediately
        with open('results.txt', 'a') as f:
            f.write(f"\n--- Study Card for {topic} ---\n")
            f.write(content)
            f.write("\n----------------------------\n")
        
        # Calculate and display time estimate
        elapsed_time = time.time() - start_time
        avg_time_per_topic = elapsed_time / (i + 1)
        remaining_topics = total_topics - (i + 1)
        estimated_time_remaining = avg_time_per_topic * remaining_topics
        
        print(f"Estimated time remaining: {estimated_time_remaining:.2f} seconds")

def main():
    # Load prompt from prompt.txt
    with open('prompt.txt', 'r') as f:
        base_prompt = f.read().strip()
    
    # Load topics from topics.txt
    with open('topics.txt', 'r') as f:
        topics = [line.strip() for line in f if line.strip()]
    
    # Generate and save study cards
    generate_study_cards(base_prompt, topics)
    
    print("All study cards have been generated and saved to results.txt")

if __name__ == "__main__":
    main()