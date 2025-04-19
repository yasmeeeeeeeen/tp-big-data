import time
import pandas as pd
import dask.dataframe as dd
import os
from pathlib import Path
import matplotlib.pyplot as plt
import json

# Configuration des chemins (adaptée à votre cas)
DATA_DIR = r"C:\Users\user\Desktop\TP BIG DATA\tp2 big data"
FILE_NAME = "2019-Nov.csv"
COMPRESSED_NAME = "2019-Nov.csv.gz"
FULL_PATH = os.path.join(DATA_DIR, FILE_NAME)
COMPRESSED_PATH = os.path.join(DATA_DIR, COMPRESSED_NAME)
RESULTS_DIR = os.path.join(DATA_DIR, "comparison_results")

# Paramètres de traitement
CHUNK_SIZE = 100000  # Pour Pandas chunking
DASK_BLOCKSIZE = "64MB"  # Taille des partitions Dask

# Création des dossiers nécessaires
os.makedirs(RESULTS_DIR, exist_ok=True)

def verify_file(file_path):
    """Vérifie que le fichier existe et retourne sa taille"""
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"Fichier trouvé : {file_path}")
    print(f"Taille : {size_mb:.2f} MB")
    return size_mb

def pandas_chunking_analysis(file_path):
    """Analyse avec Pandas en chunks"""
    print("\n[1/3] Début analyse Pandas (chunking)...")
    start_time = time.time()
    
    # Initialisation des résultats
    category_stats = pd.DataFrame()
    chunk_count = 0
    
    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
        chunk_count += 1
        # Exemple d'analyse : statistiques par catégorie
        chunk_stats = chunk.groupby('category_code')['price'].agg(['sum', 'count', 'mean'])
        category_stats = pd.concat([category_stats, chunk_stats])
    
    # Agrégation finale
    final_stats = category_stats.groupby(level=0).agg({
        'sum': 'sum',
        'count': 'sum',
        'mean': 'mean'
    })
    
    elapsed = time.time() - start_time
    print(f"Terminé en {elapsed:.2f} secondes (chunks traités: {chunk_count})")
    return {
        'time': elapsed,
        'stats': final_stats.to_dict(),
        'method': 'Pandas Chunking'
    }

def dask_analysis(file_path):
    """Analyse avec Dask"""
    print("\n[2/3] Début analyse Dask...")
    start_time = time.time()
    
    ddf = dd.read_csv(file_path, blocksize=DASK_BLOCKSIZE,
                     dtype={'price': 'float64'})  
    
   
    stats = ddf.groupby('category_code')['price'].agg(['sum', 'count', 'mean']).compute()
    
    elapsed = time.time() - start_time
    print(f"Terminé en {elapsed:.2f} secondes")
    return {
        'time': elapsed,
        'stats': stats.to_dict(),
        'method': 'Dask'
    }

def compressed_analysis(file_path):
    """Analyse avec fichier compressé"""
    print("\n[3/3] Début analyse avec compression...")
    start_time = time.time()
    
    
    if not Path(file_path).exists():
        print("Compression du fichier source...")
        pd.read_csv(FULL_PATH).to_csv(file_path, compression='gzip', index=False)
    
    df = pd.read_csv(file_path, compression='gzip')
    
    stats = df.groupby('category_code')['price'].agg(['sum', 'count', 'mean'])
    
    elapsed = time.time() - start_time
    print(f"Terminé en {elapsed:.2f} secondes")
    return {
        'time': elapsed,
        'stats': stats.to_dict(),
        'method': 'Pandas + Gzip'
    }

def save_and_visualize(results, original_size):
    """Sauvegarde et visualisation des résultats"""
    
    results_file = os.path.join(RESULTS_DIR, 'comparison_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'date': time.strftime("%Y-%m-%d %H:%M:%S"),
            'original_size_mb': original_size,
            'results': results
        }, f, indent=2)
    
    
    methods = [res['method'] for res in results]
    times = [res['time'] for res in results]
    
    plt.figure(figsize=(10, 5))
    plt.bar(methods, times, color=['blue', 'green', 'red'])
    plt.title("Comparaison des temps d'exécution")
    plt.ylabel("Secondes")
    plt.savefig(os.path.join(RESULTS_DIR, 'execution_time.png'))
    plt.show()
    
    print(f"\nRésultats sauvegardés dans : {RESULTS_DIR}")

def run_comparison():
    """Lance la comparaison complète"""
    print(f"\n{'='*40}")
    print("COMPARAISON DES METHODES DE TRAITEMENT")
    print(f"{'='*40}\n")
    
    # Vérification du fichier source
    original_size = verify_file(FULL_PATH)
    
    # Exécution des analyses
    results = [
        pandas_chunking_analysis(FULL_PATH),
        dask_analysis(FULL_PATH),
        compressed_analysis(COMPRESSED_PATH)
    ]
    
    # Affichage 
    print("\nRÉSULTATS :")
    print(f"{'Méthode':<20} | {'Temps (s)':>10}")
    print("-" * 32)
    for res in results:
        print(f"{res['method']:<20} | {res['time']:>10.2f}")
    
    # Sauvegarde et visualisation
    save_and_visualize(results, original_size)

if __name__ == "__main__":
    run_comparison()