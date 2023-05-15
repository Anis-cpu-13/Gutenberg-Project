#!/usr/env python3
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth
from sklearn.metrics import silhouette_score
import os
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm
import logging
import sys

# Configurer le module logging pour afficher les informations à la sortie standard
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_data(file_path):
    """ Cette fonction lit le fichier csv et retourne un dataframe Pandas."""
    print('Loading data...')
    data = pd.read_csv(file_path)
    print('Data loaded successfully.')
    
    # Convertir Downloads en nombre entier
    data['Downloads'] = data['Downloads'].str.extract('(\d+)').astype(int)
    
    # One-hot encoding pour les colonnes catégorielles
    print('Encoding categorical features...')
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(data[['Author', 'Subject', 'LoC Class']])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Author', 'Subject', 'LoC Class']))
    
    # Concaténer le dataframe encodé avec le dataframe original
    data = pd.concat([data, encoded_df], axis=1)
    print('Categorical features encoded successfully.')
    
    # Supprimer les colonnes non pertinentes
    data.drop(['Title', 'URL', 'Author', 'Subject', 'LoC Class'], axis=1, inplace=True)
    return data

def kmeans_clustering(data):
    """ Cette fonction effectue le clustering KMeans sur le dataframe donné en entrée et renvoie le modèle entraîné."""
    print('Performing KMeans clustering...')
    kmeans = KMeans(n_clusters=3, n_init=10).fit(data)
    score = silhouette_score(data, kmeans.labels_)
    print(f'Silhouette score for KMeans: {score}')
    return kmeans

def mean_shift_clustering(data):
    print('Performing MeanShift clustering...')
    bandwidth = estimate_bandwidth(data, quantile=0.2, n_samples=100)
    model = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(data)
    score = silhouette_score(data, model.labels_)
    print(f'Silhouette score for MeanShift: {score}')
    return model

def plot_clusters(data, kmeans_model, mean_shift_model):
    print('Plotting clusters...')
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    axs[0].set_title('kmeans')
    axs[0].scatter(data.iloc[:, 0], data.iloc[:, 1], c=kmeans_model.labels_, cmap='viridis')

    axs[1].set_title('MeanShift')
    axs[1].scatter(data.iloc[:, 0], data.iloc[:, 1], c=mean_shift_model.labels_, cmap='viridis')

    plt.tight_layout()
    
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    
    plt.savefig('graphs/clusters.png')
    print('Clusters plotted and saved successfully.')
    plt.close()

def perform_data_clustering():
    print('Starting data clustering...')
    data = read_data('/home/anis/Bureau/git-work /Gutenberg-Project/books_info.csv')
    kmeans_model = kmeans_clustering(data)
    mean_shift_model = mean_shift_clustering(data)
    plot_clusters(data, kmeans_model, mean_shift_model)
    print('Data clustering completed successfully.')

def main():
    perform_data_clustering()

if __name__ == '__main__':
    main()
