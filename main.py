#!/usr/env python3

from book_scraper import main as scrape_and_download_books
from data_analysis import main as data_analysis_main
from data_clustering import main as data_clustering_main
from colorama import Fore, Style

def main():
    # Exécute le scraper de livres
    scrape_and_download_books()

    # Exécute l'analyse de données
    data_analysis_main()

    # Exécute le clustering de données
    data_clustering_main()


if __name__ == "__main__":

    main()
