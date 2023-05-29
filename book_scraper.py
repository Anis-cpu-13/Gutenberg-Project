#!/usr/env python3
import requests
import os
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
import concurrent.futures
import csv
import logging
import progressbar


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def get_book_titles_and_authors(url):
    response = requests.get(url, timeout=60)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_list = soup.select('ol li a[href^="/ebooks/"]')
    book_list = book_list[:100]  # Limiter aux 100 premiers livres
    book_titles_and_authors = []

    for book in book_list:
        title_and_author = book.text.strip()
        if ' by ' in title_and_author:
            title, author = title_and_author.rsplit(' by ', 1)
        else:
            title = title_and_author
            author = "Unknown"

        book_url = f"https://www.gutenberg.org{book['href']}"
        book_info = {
            'Title': title,
            'Author': author,
            'URL': book_url,
            'Subject': None,
            'LoC Class': None,
            'Downloads': None
        }

        book_titles_and_authors.append(book_info)

    return book_titles_and_authors

def get_book_info(book):
    try:
        book_response = requests.get(book['URL'])
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        subject = book_soup.find('th', string='Subject')
        if subject:
            book['Subject'] = subject.find_next('td').text.strip()

        loc_class = book_soup.find('th', string='LoC Class')
        if loc_class:
            book['LoC Class'] = loc_class.find_next('td').text.strip()

        downloads = book_soup.find('th', string='Downloads')
        if downloads:
            book['Downloads'] = downloads.find_next('td').text.strip()
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération des informations pour le livre '{book['Title']}': {str(e)}")


def text_to_html(filename_txt, filename_html):
    with open(filename_txt, 'r', encoding='utf-8') as file:
        text = file.read()
    
    html_content = f"<pre>{text}</pre>"

    with open(filename_html, 'w', encoding='utf-8') as file:
        file.write(html_content)

def convert_to_pdf(text_file, pdf_file):
    c = canvas.Canvas(pdf_file)

    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        y = 800  # Position verticale initiale pour le texte

        for line in lines:
            c.drawString(10, y, line.strip())
            y -= 12  # Décalage vertical entre les lignes

            if y < 50:  # Si la position verticale atteint le bas de la page
                c.showPage()  # Passage à la page suivante
                y = 800  # Réinitialisation de la position verticale pour la nouvelle page

    c.save()
    #print(f"Le fichier texte '{text_file}' a été converti en PDF : {pdf_file}")



def download_book(book):
    try:
        book_id = book['URL'].split('/')[-1]
        url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
        logging.info(f"Tentative de téléchargement du livre depuis l'URL: {url}")

        filename_txt = os.path.join('data', f"{book['Title']}.txt")
        filename_pdf = os.path.join('library_Top_100_last_30_Day', f"{book['Title']}.pdf")

        logging.info("Envoi de la requête GET")
        response = requests.get(url)
        logging.info(f"Code de statut HTTP de la réponse: {response.status_code}")

        if response.status_code == 200:
            content = response.text
            with open(filename_txt, 'w', encoding='utf-8') as file:
                file.write(content)
            #print(f"Le livre '{book['Title']}' a été enregistré en tant que fichier texte : {filename_txt}")

            # Conversion en PDF
            convert_to_pdf(filename_txt, filename_pdf)
            #print(f"Le fichier texte '{filename_txt}' a été converti en PDF : {filename_pdf}")
        else:
            logging.error(f"Impossible de télécharger le livre '{book['Title']}' (code de statut: {response.status_code}).")
    except Exception as e:
        logging.error(f"Une erreur s'est produite lors du téléchargement du livre '{book['Title']}': {str(e)}")

def save_book_info_to_csv(book_list):
    with open('books_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Author', 'URL', 'Subject', 'LoC Class', 'Downloads']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for book in book_list:
            writer.writerow({
                'Title': book['Title'],
                'Author': book['Author'],
                'URL': book['URL'],
                'Subject': book['Subject'],
                'LoC Class': book['LoC Class'],
                'Downloads': book['Downloads']
            })

def download_books(book_list, num_books, timeout_seconds):
    count = 0

    # Création d'une instance de ProgressBar
    bar = progressbar.ProgressBar(maxval=num_books)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for book in book_list:
            futures.append(executor.submit(download_book, book))
            count += 1

            # Mise à jour de la barre de progression
            bar.update(count)

            if count == num_books:
                break

        done, not_done = concurrent.futures.wait(futures, timeout=timeout_seconds)

        for future in not_done:
            future.cancel()

        if count < num_books:
            print("Le nombre de livres demandé a été téléchargé. Le programme s'arrête.")
        elif not_done:
            print("Le temps alloué pour le téléchargement est écoulé. Le programme s'arrête.")

    # Indiquer que la barre de progression est terminée
    bar.finish()




def scrape_and_download_books():
    url = "https://www.gutenberg.org/browse/scores/top#books-last30"
    book_titles_and_authors = get_book_titles_and_authors(url)

    # Récupération des informations détaillées des livres en parallèle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for book in book_titles_and_authors:
            futures.append(executor.submit(get_book_info, book))
        concurrent.futures.wait(futures)

    # Création du répertoire de destination
    destination_directory = 'library_Top_100_last_30_Day'
    os.makedirs(destination_directory, exist_ok=True)

    # Téléchargement des livres et conversion en PDF
    download_books(book_titles_and_authors,100, 60)

    # Enregistrement des informations des livres dans un fichier CSV
    save_book_info_to_csv(book_titles_and_authors)

    logging.info("Le script a terminé son exécution.")

def main():
    scrape_and_download_books()

if __name__ == "__main__":
    main()


