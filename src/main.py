# main.py

from data_collection import saved_links
from data_cleaning import clean_data

def main() -> None:
    # Define seed articles and other constants
    seed_articles = []  # user input of desired list of starting seed articles
    raw_data_file = 'wikipedia_links.json'
    cleaned_data_file = 'cleaned_wikipedia_links.json'
    
    # Fetch and save links
    saved_links(seed_articles, raw_data_file)

    # Clean the fetched data
    clean_data(raw_data_file, cleaned_data_file)

if __name__ == "__main__":
    main()
