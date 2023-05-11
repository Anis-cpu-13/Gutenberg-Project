#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth, MiniBatchKMeans, SpectralClustering
from sklearn.metrics import silhouette_score

def read_data(file_path):
    """Cette fonction lit le fichier csv et retourne un dataframe Pandas."""
    data = pd.read_csv(file_path)

    # Supprimer les colonnes inutiles
    data.drop(['URL', 'Author', 'LoC Class'], axis=1, inplace=True)

    # Renommer les colonnes
    data.columns = ['Title', 'Subject', 'Downloads', 'Num_Subject'] # Ajout de la colonne 'Num_Subject'

    # Extraire le nombre de téléchargements
    data['Downloads'] = pd.to_numeric(data['Downloads'], errors='coerce') # En supposant que 'Downloads' est déjà un nombre ou peut être converti en nombre

    return data

def kmeans_clustering(data):
    """Cette fonction effectue le clustering KMeans sur le dataframe donné en entrée et renvoie le modèle entraîné."""
    kmeans = KMeans(n_clusters=3, n_init=10).fit(data)
    print('Silhouette score pour KMeans:', silhouette_score(data, kmeans.labels_))
    return kmeans

def mean_shift_clustering(data):
    """Cette fonction effectue le clustering MeanShift sur le dataframe donné en entrée et renvoie le modèle entraîné."""
    bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=100)
    model = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(data)
    print('Silhouette score pour MeanShift:', silhouette_score(data, model.labels_))
    return model

def spectral_clustering(data):
    """Cette fonction effectue le clustering spectral sur le dataframe donné en entrée et renvoie les étiquettes de cluster."""
    spectral = SpectralClustering(n_clusters=3, affinity='nearest_neighbors', assign_labels='kmeans').fit(data)
    labels = spectral.labels_
    print('Silhouette score pour le clustering spectral:', silhouette_score(data, labels))
    return labels

def plot_clusters(data, kmeans_model, mean_shift_model, spectral_labels):
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))

    axs[0].set_title('KMeans')
    axs[0].scatter(data['Downloads'], data['Num_Subject'], c=kmeans_model.labels_, cmap='viridis')
    axs[0].set_xlabel('Downloads')
    axs[0].set_ylabel('Num_Subject')

    axs[1].set_title('MeanShift')
    axs[1].scatter(data['Downloads'], data['Num_Subject'], c=mean_shift_model.labels_, cmap='viridis')
    axs[1].set_xlabel('Downloads')
    axs[1].set_ylabel('Num_Subject')

    axs[2].set_title('Spectral Clustering')
    axs[2].scatter(data['Downloads'], data['Num_Subject'], c=spectral_labels, cmap='viridis')
    axs[2].set_xlabel('Downloads')
    axs[2].set_ylabel('Num_Subject')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    file_path = '/home/anis/Bureau/git-work /Gutenberg-Project/books_info.csv'
    data = read_data(file_path)
   
    spectral_labels = spectral_clustering(data[['Downloads', 'Num_Subject']])  # N'utiliser que les colonnes numériques pour le clustering
    kmeans_model = kmeans_clustering(data[['Downloads', 'Num_Subject']])  # N'utiliser que les colonnes numériques pour le clustering
    mean_shift_model = mean_shift_clustering(data[['Downloads', 'Num_Subject']])  # N'utiliser que les colonnes numériques pour le clustering
    plot_clusters(data, kmeans_model, mean_shift_model, spectral_labels)
