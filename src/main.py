# main.py

from data_collection import saved_links
from data_cleaning import clean_data

def main() -> None:
    # Define seed articles and other constants
    seed_articles = ['Information_theory','Entropy_(information_theory)',
                     'Category_theory','Set_theory','Network_theory',
                     'Queue_theory','Graph_theory','Topology','Functional_Analysis',
                     'Coding_theory','Applied_mathematics','Algorthims','Mathematical_model',
                     'Simulations','Operations_research'
                     ] 
        
    raw_data_file = '/GraphTheoryProject/Wiki-Relations/src/wikipedia_links.json'
    cleaned_data_file = '/GraphTheoryProject/Wiki-Relations/src/cleaned_wiki_links.json'

    
    # Fetch and save links
    saved_links(seed_articles, raw_data_file)

    # Clean the fetched data
    clean_data(raw_data_file, cleaned_data_file)

if __name__ == "__main__":
    main()
