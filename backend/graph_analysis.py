import networkx as nx

def build_transaction_graph(df):
    graph = nx.DiGraph()

    for _, row in df.iterrows():
        graph.add_edge(
            row["input_address"],
            row["output_address"],
            txid=row["txid"],
            amount=row["output_amount"]
        )

    return graph

def detect_fan_out(graph, threshold=2):
    suspicious = []

    for wallet in graph.nodes:
        if graph.out_degree(wallet) >= threshold:
            suspicious.append({
                "wallet": wallet,
                "outgoing_connections": graph.out_degree(wallet),
                "pattern": "Fan-Out"
            })

    return suspicious

def detect_fan_in(graph, threshold=2):
    suspicious = []

    for wallet in graph.nodes:
        if graph.in_degree(wallet) >= threshold:
            suspicious.append({
                "wallet": wallet,
                "incoming_connections": graph.in_degree(wallet),
                "pattern": "Fan-In"
            })

    return suspicious

def detect_layering(graph, min_hops=3):
    suspicious = []

    for wallet in graph.nodes:
        paths = []

        for target in graph.nodes:
            if wallet != target:
                try:
                    length = nx.shortest_path_length(graph, wallet, target)
                    if length >= min_hops:
                        paths.append(length)
                except nx.NetworkXNoPath:
                    pass

        if paths:
            suspicious.append({
                "wallet": wallet,
                "max_hops": max(paths),
                "pattern": "Layering"
            })

    return suspicious
