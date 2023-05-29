#!/usr/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data_from_csv(file_path):
    data = pd.read_csv(file_path)
    # Convertir Downloads en nombre entier
    data['Downloads'] = data['Downloads'].str.extract('(\d+)').astype(int)
    return data


def data_analysis_main (data):
    # Créer un histogramme pour visualiser la distribution des téléchargements
    plt.figure(figsize=(12, 8))
    sns.histplot(data['Downloads'], kde=True, bins=30)
    plt.title('Distribution des téléchargements', fontsize=16)
    plt.xlabel('Téléchargements', fontsize=14)
    plt.ylabel('Fréquence', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('graphs/distribution_downloads.png')  # Sauvegarde du graphique
    plt.close()  
    
    # Créer un graphique en barres pour visualiser le nombre de livres par auteur (pour les 10 auteurs avec le plus de livres)
    plt.figure(figsize=(12, 8))
    data['Author'].value_counts().head(10).plot(kind='bar')
    plt.title('Nombre de livres par auteur (Top 10)', fontsize=16)
    plt.xlabel('Auteur', fontsize=14)
    plt.ylabel('Nombre de livres', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('graphs/books_per_author.png')  # Sauvegarde du graphique
    plt.close()  
    
    # Créer un graphique en barres pour visualiser le nombre de livres par sujet (pour les 10 sujets avec le plus de livres)
    plt.figure(figsize=(12, 8))
    data['Subject'].value_counts().head(10).plot(kind='bar')
    plt.title('Nombre de livres par sujet (Top 10)', fontsize=16)
    plt.xlabel('Sujet', fontsize=14)
    plt.ylabel('Nombre de livres', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('graphs/books_per_subject.png')  # Sauvegarde du graphique
    plt.close()  

def main():
    # Charger les données à partir du fichier CSV
    data = load_data_from_csv("/home/anis/Bureau/git-work /Gutenberg-Project/books_info.csv")  
    data_analysis_main(data)

if __name__ == "__main__":
    main()


