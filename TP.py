from scipy.stats import zscore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le fichier CSV
data = pd.read_csv("Sales.csv")

# Supprimer les colonnes inutiles
data.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], errors="ignore", inplace=True)

# Renommer les colonnes pour plus de clarté
data.rename(columns={"date_": "date", "total_weighted_landing_price": "sales"}, inplace=True)

# Vérifier les premières lignes
print("Aperçu des données :")
print(data.head())

# Vérifier les colonnes disponibles
print("\nColonnes disponibles après nettoyage :", data.columns)

print("\ninfo sur data:", data.info())
# Convertir la colonne "date" en format datetime
if "date" in data.columns:
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
else:
    print("\nErreur : La colonne 'date' est introuvable.")


# Suppression des valeurs manquantes
data.dropna(inplace=True)

# Suppression des doublons
data.drop_duplicates(inplace=True)

# Afficher les statistiques descriptives
print("\nStatistiques descriptives :")
print(data.describe())

# Sélectionner uniquement les colonnes numériques pour la matrice de corrélation
numeric_data = data.select_dtypes(include=['number'])

if numeric_data.shape[1] > 1:
    plt.figure(figsize=(8, 6))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Matrice de corrélation")
    plt.show()
else:
    print("\nErreur : Pas assez de colonnes numériques pour afficher une matrice de corrélation.")

# Tendances des ventes PAR RAPPORT AU unit_selling_price
if "unit_selling_price" in data.columns and "sales" in data.columns:
    plt.figure(figsize=(10, 5))
    data.groupby("unit_selling_price")["sales"].sum().plot(kind="line", marker="o", color="b")
    plt.title("Tendances des ventes")
    plt.xlabel("unit_selling_price")
    plt.ylabel("Total des ventes")
    plt.grid(True)
    plt.show()
else:
    print("\nErreur : Impossible de tracer les tendances des ventes. Vérifiez les colonnes 'date' et 'sales'.")

# Sauvegarder le fichier nettoyé pour Power BI
data.to_csv("Sales_Cleaned.csv", index=False)

print("Fichier Sales_Cleaned.csv enregistré avec succès.")

