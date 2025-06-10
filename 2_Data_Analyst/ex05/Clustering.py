import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sqlalchemy as sa
from sklearn.preprocessing import StandardScaler
import seaborn as sns

def main():
    # Connexion à la base PostgreSQL
    engine = sa.create_engine("postgresql://mservage:mysecretpassword@localhost:5432/piscineds")

    query = """
    SELECT event_time, user_id, price
    FROM customers
    WHERE event_type = 'purchase';
    """
    print("Récupération des données")
    df = pd.read_sql(query, engine)
    df['event_time'] = pd.to_datetime(df['event_time'])
    df['year_month'] = df['event_time'].dt.to_period('M')
    last_month = df['event_time'].max().to_period('M')

    print("Création des features clients")
    user_stats = df.groupby('user_id').agg(
        total_purchases=('event_time', 'count'),
        total_spent=('price', 'sum'),
        last_purchase_month=('event_time', lambda x: x.max().to_period('M')),
        months_active=('year_month', pd.Series.nunique),
        months_list=('year_month', lambda x: sorted(x.unique()))
    ).reset_index()

    def classify_customer(row):
        months = row['months_list']
        total = row['total_purchases']
        spent = row['total_spent']
        last = row['last_purchase_month']
        active_months = row['months_active']
        recent_3 = [last_month - i for i in range(4)]
        recent_2 = [last_month - i for i in range(2)]

        if total >= 15 or spent >= 100 and all(m in months for m in recent_3):
            return 'platinum'
        elif total >= 5 or spent >= 25 and all(m in months for m in recent_2):
            return 'gold'
        elif last == last_month and active_months == 1:
            return 'new_customer'
        elif (last_month - last).n >= 3:
            return 'inactive'
        return 'bronze'

    print("Classification des clients")
    user_stats['segment'] = user_stats.apply(classify_customer, axis=1)

    print("Normalisation des données")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(user_stats[['total_purchases', 'months_active', 'total_spent']])

    print("Clustering avec KMeans")
    kmeans = KMeans(n_clusters=5, random_state=42, n_init='auto')
    kmeans.fit(X_scaled)
    
    # ✅ Ligne essentielle manquante dans ta version :
    segment_counts = user_stats['segment'].value_counts().sort_values(ascending=True)

    # Affichage horizontal : catégories sur Y, valeurs sur X
    plt.figure(figsize=(12, 8))
    segment_df = segment_counts.reset_index()
    segment_df.columns = ['segment', 'count']
    sns.barplot(data=segment_df, x='count', y='segment', hue='segment', palette='pastel', dodge=False, legend=False)

    # Afficher les valeurs numériques au bout des barres
    for i, v in enumerate(segment_counts.values):
        plt.text(v + 10, i, str(v), va='center')

    plt.xlabel('Number of customers')
    plt.tight_layout()
    plt.show()

    # graphique 2 : bubble chart
    user_stats['recency'] = (last_month - user_stats['last_purchase_month']).apply(lambda x: x.n)
    centroids = user_stats.groupby('segment').agg(
        median_recency=('recency', 'median'),
        median_frequency=('total_purchases', 'median'),
        avg_spent=('total_spent', 'mean')
    ).reset_index()

    # Affichage du bubble chart
    plt.figure(figsize=(9, 6))
    plt.scatter(
        centroids['median_recency'],
        centroids['median_frequency'],
        s=centroids['avg_spent'] * 5,  # ajuster l'échelle de la taille
        alpha=0.7,
        c=centroids['segment'].astype('category').cat.codes
    )

    # Ajouter les labels au bon format
    for _, row in centroids.iterrows():
        label = f'Average "{row["segment"]} {row["avg_spent"]:.1f}₳"'
        plt.text(
            row['median_recency'] + 0.1,
            row['median_frequency'],
            label,
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6)
        )

    plt.xlabel('Median Recency (month)')
    plt.ylabel('Median Frequency')
    plt.title('Segment Centroids')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
