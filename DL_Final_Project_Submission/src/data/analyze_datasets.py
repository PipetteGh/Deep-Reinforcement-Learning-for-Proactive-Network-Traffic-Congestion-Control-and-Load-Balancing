import os
import glob
import networkx as nx
import csv
import json

def analyze_datasets(base_path):
    inventory = []
    summary = {
        "total_topologies": 0,
        "graphml_count": 0,
        "gml_count": 0,
        "total_nodes": 0,
        "total_edges": 0,
        "avg_nodes": 0,
        "avg_edges": 0,
        "directed_count": 0,
        "connected_count": 0,
        "with_bandwidth": 0,
        "with_latency": 0
    }
    
    files = glob.glob(os.path.join(base_path, 'data/raw/**/*.graphml'), recursive=True) + \
            glob.glob(os.path.join(base_path, 'data/raw/**/*.gml'), recursive=True)
            
    for f in files:
        try:
            if f.endswith('.graphml'):
                G = nx.read_graphml(f)
                fmt = "GraphML"
                summary["graphml_count"] += 1
            else:
                G = nx.read_gml(f)
                fmt = "GML"
                summary["gml_count"] += 1
                
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            
            is_directed = G.is_directed()
            if is_directed:
                is_connected = nx.is_weakly_connected(G) if num_nodes > 0 else False
            else:
                is_connected = nx.is_connected(G) if num_nodes > 0 else False
                
            has_bandwidth = False
            has_latency = False
            
            for u, v, d in G.edges(data=True):
                # Check for common bandwidth/latency attribute names
                keys = [k.lower() for k in d.keys()]
                if any('band' in k or 'cap' in k or 'bw' in k for k in keys):
                    has_bandwidth = True
                if any('lat' in k or 'delay' in k for k in keys):
                    has_latency = True
                if has_bandwidth and has_latency:
                    break
                    
            inventory.append({
                "topology_name": os.path.basename(f).replace('.graphml', '').replace('.gml', ''),
                "format": fmt,
                "number_of_nodes": num_nodes,
                "number_of_edges": num_edges,
                "connected": is_connected,
                "directed": is_directed,
                "bandwidth_available": has_bandwidth,
                "latency_available": has_latency,
                "source_file": os.path.relpath(f, base_path)
            })
            
            summary["total_topologies"] += 1
            summary["total_nodes"] += num_nodes
            summary["total_edges"] += num_edges
            if is_directed:
                summary["directed_count"] += 1
            if is_connected:
                summary["connected_count"] += 1
            if has_bandwidth:
                summary["with_bandwidth"] += 1
            if has_latency:
                summary["with_latency"] += 1
                
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    if summary["total_topologies"] > 0:
        summary["avg_nodes"] = summary["total_nodes"] / summary["total_topologies"]
        summary["avg_edges"] = summary["total_edges"] / summary["total_topologies"]
        
    csv_path = os.path.join(base_path, 'data', 'dataset_inventory.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "topology_name", "format", "number_of_nodes", "number_of_edges",
            "connected", "directed", "bandwidth_available", "latency_available", "source_file"
        ])
        writer.writeheader()
        writer.writerows(inventory)
        
    json_path = os.path.join(base_path, 'data', 'dataset_summary.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4)

if __name__ == "__main__":
    analyze_datasets(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
