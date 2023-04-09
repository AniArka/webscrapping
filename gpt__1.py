# Import libraries
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pprint


# Define a function to preprocess text
def preprocess(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = "".join([c for c in text if c.isalpha() or c == " "])
    # Tokenize words
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = stopwords.words("english")
    tokens = [t for t in tokens if t not in stop_words]
    # Stem words
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
    # Return tokens
    return tokens


# Define a function to compute cosine similarity between two texts
def cosine_similarity(text1, text2):
    # Preprocess texts
    tokens1 = preprocess(text1)
    tokens2 = preprocess(text2)
    # Create a set of unique words
    words = set(tokens1 + tokens2)
    # Create vectors of word counts
    vector1 = [tokens1.count(w) for w in words]
    vector2 = [tokens2.count(w) for w in words]
    # Compute dot product
    dot_product = sum([v1 * v2 for v1, v2 in zip(vector1, vector2)])
    # Compute magnitudes
    magnitude1 = sum([v ** 2 for v in vector1]) ** 0.5
    magnitude2 = sum([v ** 2 for v in vector2]) ** 0.5
    # Compute cosine similarity
    cosine_sim = dot_product / (magnitude1 * magnitude2)
    # Return cosine similarity
    return cosine_sim


# Define a function to search the query and give the best result from Google after analyzing different websites
def search_and_analyze(query):
    # Create a Google search URL with the query
    google_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    # Get the HTML content of the Google search page
    google_response = requests.get(google_url)
    google_html = google_response.text
    # Parse the HTML content with BeautifulSoup
    google_soup = BeautifulSoup(google_html, "html.parser")
    # Find all the links to websites from the Google search page
    links = google_soup.find_all("a", href=lambda x: x and x.startswith("/url?q="))
    # Initialize an empty list to store the results
    results = []
    # Loop through each link
    for link in links:
        # Get the URL of the website from the link
        url = link["href"].split("/url?q=")[1].split("&")[0]
        # Get the title of the website from the link text
        title = link.text.strip()
        # Skip if the title is empty or not relevant
        if not title or title == "Cached" or title == "Similar":
            continue
        # Get the HTML content of the website
        web_response = requests.get(url)
        web_html = web_response.text
        # Parse the HTML content with BeautifulSoup
        web_soup = BeautifulSoup(web_html, "html.parser")
        # Get the body text of the website by joining all the paragraphs
        body = " ".join([p.text.strip() for p in web_soup.find_all("p")])
        # Skip if the body is empty or too short
        if not body or len(body) < 100:
            continue
        # Compute the cosine similarity between the query and the title of the website
        similarity = cosine_similarity(query, title)
        # Append a tuple of (similarity, url, title, body) to the results list
        results.append((similarity, url, title, body))

    # Sort the results list by similarity in descending order
    results.sort(key=lambda x: x[0], reverse=True)

    # Return the best result (the first element of the sorted list) or None if no results found
    return results[0] if results else None


# Define a query to search
query = "how to make pizza dough"

# Call the search_and_an