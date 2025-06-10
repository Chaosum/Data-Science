import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sqlalchemy as sa

def main():

    engine = sa.create_engine("postgresql://mservage:mysecretpassword@localhost:5432/piscineds")

    query = """
    SELECT user_id, event_time, event_type, product_id, price
    FROM customers
    WHERE event_type = 'purchase';
    """
    
    df = pd.read_sql(query, engine)

    # 2. Créer des features clients
    # Exemple : nombre d'achats, total dépensé, fréquence
    features = df.groupby('user_id').agg({
        'event_time': 'count',        # nombre d'achats
        'price': 'sum',               # total dépensé
        'product_id': pd.Series.nunique  # diversité des produits achetés
    }).rename(columns={
        'event_time': 'purchase_count',
        'price': 'total_spent',
        'product_id': 'unique_products'
    })

    # 3. Normaliser si nécessaire (important pour KMeans)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # 4. Appliquer la méthode du coude
    inertia = []
    K = range(1, 11)

    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    # 5. Tracer le graphe
    plt.plot(K, inertia, marker='o')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia (WCSS)')
    plt.title('Elbow Method For Optimal k')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()