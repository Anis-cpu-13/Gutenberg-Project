import requests
import pdfkit
from bs4 import BeautifulSoup
import time

def get_book_titles_and_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_list = soup.select('ol li a[href^="/ebooks/"]')
    book_list = book_list[:10]  # Limiter aux 10 premiers livres
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

        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        subject = book_soup.find('th', string='Subject')
        if subject:
            book_info['Subject'] = subject.find_next('td').text.strip()

        loc_class = book_soup.find('th', string='LoC Class')
        if loc_class:
            book_info['LoC Class'] = loc_class.find_next('td').text.strip()

        downloads = book_soup.find('th', string='Downloads')
        if downloads:
            book_info['Downloads'] = downloads.find_next('td').text.strip()

        book_titles_and_authors.append(book_info)

    return book_titles_and_authors

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


def download_books(book_list):
    for book in book_list:
        book_id = book['URL'].split('/')[-1]  # Extraction de l'identifiant du livre à partir de l'URL
        url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"  # Construction de l'URL du fichier texte
        filename = f"{book['Title']}.txt"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Le livre '{book['Title']}' a été enregistré en tant que fichier texte.")
                pdf_filename = f"{book['Title']}.pdf"
                pdfkit.from_file(filename, pdf_filename)
                print(f"Le fichier texte '{filename}' a été converti en PDF : '{pdf_filename}'.")
            else:
                print(f"Impossible de télécharger le livre '{book['Title']}'.")
        except Exception as e:
            print(f"Une erreur s'est produite lors du traitement du livre '{book['Title']}' : {str(e)}")

        time.sleep(1)  # Attendre 1 seconde entre chaque téléchargement pour éviter de surcharger le serveur

url = "https://www.gutenberg.org/browse/scores/top#books-last30"
book_titles_and_authors = get_book_titles_and_authors(url)

# Affichage des informations des livres
for book in book_titles_and_authors:
    print(f"Title: {book['Title']}")
    print(f"Author: {book['Author']}")
    print(f"URL: {book['URL']}")
    print(f"Subject: {book['Subject']}")
    print(f"LoC Class: {book['LoC Class']}")
    print(f"Downloads: {book['Downloads']}")
    print("---")

# Téléchargement des livres et conversion en PDF
download_books(book_titles_and_authors)

# Appel de la fonction pour enregistrer les informations des livres dans un fichier CSV
save_book_info_to_csv(book_titles_and_authors)
