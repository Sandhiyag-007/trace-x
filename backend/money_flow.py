def trace_money_flow(graph, wallet, max_depth=5):
    flow = []

    def explore(current, path, depth):
        if depth > max_depth:
            return

        for next_wallet in graph.successors(current):
            if next_wallet not in path:
                flow.append({
                    "from": current,
                    "to": next_wallet,
                    "depth": depth
                })
                explore(next_wallet, path + [next_wallet], depth + 1)

    explore(wallet, [wallet], 1)
    return flow
