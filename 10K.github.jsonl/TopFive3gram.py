import json
from collections.abc import Iterable
from collections import Counter
from collections import Counter
import re
import csv

def ngrams(words, n):
    return zip(*[words[i:] for i in range(n)])

def find_top_ngrams(strings, n=3, top=5):
    # Initialize a Counter to store the counts of all n-grams
    ngram_counts = Counter()

    # Process each string separately
    for string in strings:
        # Tokenize the string into words
        # words = re.findall(r'\w+', string.lower())
        punctuation_pattern= r'[^\w\s\'s#]|\b#\d+'
        removed_punctuation = re.sub(punctuation_pattern, '', string.lower())
        stripped_spaces=re.sub(r'\s+', ' ', removed_punctuation.strip())
        words=stripped_spaces.split(' ')

        # Generate 3-grams for the current string
        string_ngrams = ngrams(words, n)

        # Update the counts of 3-grams for the current string
        ngram_counts.update(string_ngrams)

    # Get the top n 3-grams sorted by frequency
    top_ngrams = ngram_counts.most_common(top)

    return top_ngrams

def generate_author_ngram_arr(author, top_5_ngrams):
    if top_5_ngrams:
        ngram_arr=[' '.join(t[0]) for t in top_5_ngrams]
        author_ngram_arr=[author]+ngram_arr
        return author_ngram_arr


filename='10K.github.jsonl'
commits =[]
with open(filename, encoding="utf8") as commits_file:
    for line in commits_file:
        commits.append(json.loads(line))

# filtered push event commits
push_event_commits=[commit for commit in commits if commit['type']=='PushEvent']

# create dict with author name as key, and messages array as value 
author_messages_dict={}

for commit in push_event_commits:
    push_commits=commit.get('payload').get('commits')
    if push_commits is not None and isinstance(push_commits, Iterable):
        for commit in push_commits:
            author_name=commit.get('author').get('name')
            message=commit.get('message')
            if author_name is not None and author_name not in author_messages_dict and message is not None:
                author_messages_dict[author_name]=[message]
            else:
                author_messages_dict[author_name].append(message)
    
data=[]

for author, messages in author_messages_dict.items():
    top_5_ngrams = find_top_ngrams(messages)
    new_ngram_line=generate_author_ngram_arr(author, top_5_ngrams)
    if new_ngram_line:
        data.append(new_ngram_line)

# Define the path to the CSV file
csv_file_path = 'output.csv'

# Write the data to the CSV file
with open(csv_file_path, 'w', newline='', encoding="utf8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print("CSV file has been created:", csv_file_path)
                

