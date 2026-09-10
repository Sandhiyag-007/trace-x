import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_wallets(df, clusters=2):
    features = df.groupby("input_address").agg(
        transaction_count=("txid", "count"),
        total_input=("input_amount", "sum"),
        total_output=("output_amount", "sum"),
        total_fee=("fee", "sum")
    ).reset_index()

    X = features.iloc[:, 1:]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=clusters, random_state=42, n_init=10)
    features["cluster"] = model.fit_predict(X_scaled)

    return features
