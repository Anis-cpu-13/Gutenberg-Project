# Projet Gutenberg

Ce projet est un script Python conçu pour extraire, analyser et regrouper des informations sur les livres populaires à partir du site web du Projet Gutenberg.

## Dépendances

Le script nécessite les dépendances suivantes :

- Python 3
- requests
- BeautifulSoup
- reportlab
- concurrent.futures
- progressbar
- pandas
- matplotlib
- seaborn
- sklearn
- tqdm

## Installation

1. Assurez-vous d'avoir Python 3 installé sur votre système.
2. Clonez ce dépôt Git sur votre machine.
3. Accédez au répertoire du projet.

## Utilisation

1. Ouvrez un terminal et accédez au répertoire du projet.
2. Exécutez la commande suivante pour lancer le script :  `python3 main.py`


Assurez-vous d'avoir les dépendances installées correctement.

## Résultats

Après avoir exécuté le script, vous trouverez les résultats dans les fichiers générés :

- `books.csv` : Fichier CSV contenant les informations sur les livres téléchargés.
- `distribution_downloads.png` : Histogramme montrant la distribution des téléchargements.
- `books_per_author.png` : Graphique à barres montrant le nombre de livres par auteur.
- `books_per_subject.png` : Graphique à barres montrant le nombre de livres par sujet.
- `clusters.png` : Graphique montrant les clusters formés à partir des données.

## Contribuer

Les contributions à ce projet sont les bienvenues. N'hésitez pas à ouvrir une issue ou à soumettre une demande de fusion pour proposer des améliorations, des corrections de bugs, etc.

## Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier [LICENSE](LICENSE) pour plus d'informations.
