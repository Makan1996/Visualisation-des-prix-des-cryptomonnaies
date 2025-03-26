import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Fonction pour récupérer les données des cryptomonnaies via l'API
def get_crypto_data(crypto, days=500):
    url = f'https://min-api.cryptocompare.com/data/histoday'
    params = {
        'fsym': crypto,    # Symbole de la cryptomonnaie
        'tsym': 'EUR',     # Nous récupérons le prix en euros
        'limit': days,     # Nombre de jours à récupérer
        'toTs': int(datetime.now().timestamp())  # Temps actuel en timestamp Unix
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()['Data']
        # Transformation des données pour les rendre exploitables
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'], unit='s')  # Convertir le temps en date
        return df[['time', 'close']]  # Nous gardons uniquement la date et le prix de clôture
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return None

# Fonction pour afficher le graphe des prix
def plot_crypto_price(df, crypto):
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df['close'], label=f'{crypto} Price', color='blue')
    plt.title(f"Prix de {crypto} sur les {len(df)} derniers jours")
    plt.xlabel('Date')
    plt.ylabel('Prix en EUR')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Fonction principale pour interagir avec l'utilisateur
def main():
    # Demander à l'utilisateur de choisir une ou plusieurs cryptomonnaies
    cryptos = input("Entrez la/les cryptomonnaie(s) séparée(s) par une virgule (ex : BTC, ETH, ADA): ").split(',')
    cryptos = [crypto.strip().upper() for crypto in cryptos]  # On s'assure que tout est en majuscules et sans espaces
    
    # Demander à l'utilisateur le nombre de jours
    days = int(input("Entrez le nombre de derniers jours pour récupérer les prix (ex : 500): "))
    
    # Récupérer et afficher les prix pour chaque cryptomonnaie choisie
    for crypto in cryptos:
        print(f"Récupération des données pour {crypto}...")
        df = get_crypto_data(crypto, days)
        if df is not None:
            plot_crypto_price(df, crypto)

# Exécution du programme
if __name__ == "__main__":
    main()
