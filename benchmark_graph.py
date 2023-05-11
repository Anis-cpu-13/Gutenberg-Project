import graphviz
import csv

def load_data_from_csv(file_path):
    data = []
    
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    
    return data

# Charger les données à partir du fichier CSV
data = load_data_from_csv("/home/anis/Bureau/git-work /Gutenberg-Project/books_info.csv")  # Assurez-vous de remplacer "books_info.csv" par le nom de votre fichier CSV

# Créer un graphe distinct pour chaque critère
subject_graph = graphviz.Graph(format='png', engine='dot', graph_attr={'rankdir': 'LR'}, node_attr={'shape': 'box', 'style': 'filled', 'fillcolor': '#EFEFEF'})
loc_class_graph = graphviz.Graph(format='png', engine='dot', graph_attr={'rankdir': 'LR'}, node_attr={'shape': 'box', 'style': 'filled', 'fillcolor': '#EFEFEF'})
downloads_graph = graphviz.Graph(format='png', engine='dot', graph_attr={'rankdir': 'LR'}, node_attr={'shape': 'box', 'style': 'filled', 'fillcolor': '#EFEFEF'})

# Parcourir les données et ajouter les nœuds aux graphes correspondants
for row in data:
    subject = row["Subject"]
    loc_class = row["LoC Class"]
    downloads = row["Downloads"]

    # Ajouter un nœud pour chaque critère dans le graphe correspondant
    subject_graph.node(subject)
    loc_class_graph.node(loc_class)
    downloads_graph.node(downloads)

    # Créer des liens entre les critères et les nœuds correspondants dans les graphes
    subject_graph.edge(loc_class, subject)
    loc_class_graph.edge(downloads, loc_class)

# Appliquer le thème "modern" aux graphes
subject_graph.attr('graph', {'style': 'modern'})
loc_class_graph.attr('graph', {'style': 'modern'})
downloads_graph.attr('graph', {'style': 'modern'})

# Enregistrer les graphes dans des fichiers distincts
subject_graph.render("subject_graph", view=True)  # Le fichier sera enregistré au format PNG avec le nom "subject_graph.png"
loc_class_graph.render("loc_class_graph", view=True)  # Le fichier sera enregistré au format PNG avec le nom "loc_class_graph.png"
downloads_graph.render("downloads_graph", view=True)  # Le fichier sera enregistré au format PNG avec le nom "downloads_graph.png"
