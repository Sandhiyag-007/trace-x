import pandas as pd

def analyze_geoip(df, geoip_file="data/raw/geoip_database.csv"):
    geoip = pd.read_csv(geoip_file)

    result = df.merge(
        geoip,
        left_on="src_ip",
        right_on="ip",
        how="left"
    )

    result["geo_country"] = result["geo_country"].fillna("Unknown")
    result["ASN"] = result["ASN"].fillna("Unknown")

    return result[[
        "txid",
        "src_ip",
        "dst_ip",
        "geo_country",
        "ASN"
    ]]
