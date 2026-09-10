def correlate_network_blockchain(df):
    results = []

    for _, row in df.iterrows():
        results.append({
            "txid": row["txid"],
            "src_ip": row["src_ip"],
            "dst_ip": row["dst_ip"],
            "src_port": row["src_port"],
            "dst_port": row["dst_port"],
            "wallet": row["input_address"],
            "amount": row["output_amount"],
            "timestamp": row["timestamp"]
        })

    return results
