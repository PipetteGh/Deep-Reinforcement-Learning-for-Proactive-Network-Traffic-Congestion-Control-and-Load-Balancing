import networkx as nx
import numpy as np
from itertools import islice

DEFAULT_BANDWIDTH = 10.0 # e.g. 10 Gbps
DEFAULT_LATENCY = 1.0 # e.g. 1 ms

def k_shortest_paths(G, source, target, k, weight='weight'):
    try:
        return list(
            islice(nx.shortest_simple_paths(G, source, target, weight=weight), k)
        )
    except nx.NetworkXNoPath:
        return []

class TopologyLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.graph = nx.read_graphml(filepath)
        
    def validate_and_clean(self):
        # Convert to simple undirected graph if it's not already
        self.graph = nx.Graph(self.graph)
        self.graph.remove_edges_from(nx.selfloop_edges(self.graph))
        
        # Keep only the largest connected component to ensure routing works
        if not nx.is_connected(self.graph):
            largest_cc = max(nx.connected_components(self.graph), key=len)
            self.graph = self.graph.subgraph(largest_cc).copy()
            
    def normalize_attributes(self):
        # Extract existing bandwidth and latency or apply defaults
        bws = []
        lats = []
        
        for u, v, d in self.graph.edges(data=True):
            # Parse bandwidth
            bw = d.get('bandwidth', d.get('Capacity', DEFAULT_BANDWIDTH))
            try:
                # Naive attempt to extract float from string like "10 Gbps"
                if isinstance(bw, str):
                    bw = float(''.join(c for c in bw if c.isdigit() or c == '.'))
                    if bw == 0: bw = DEFAULT_BANDWIDTH
            except:
                bw = DEFAULT_BANDWIDTH
                
            # Parse latency
            lat = d.get('latency', d.get('Delay', DEFAULT_LATENCY))
            try:
                if isinstance(lat, str):
                    lat = float(''.join(c for c in lat if c.isdigit() or c == '.'))
                    if lat == 0: lat = DEFAULT_LATENCY
            except:
                lat = DEFAULT_LATENCY
                
            d['bw_raw'] = bw
            d['lat_raw'] = lat
            d['weight'] = lat # Use latency as weight for shortest paths
            bws.append(bw)
            lats.append(lat)
            
        # Normalize
        max_bw = max(bws) if bws else 1
        max_lat = max(lats) if lats else 1
        
        for u, v, d in self.graph.edges(data=True):
            d['bw_norm'] = d['bw_raw'] / max_bw
            d['lat_norm'] = d['lat_raw'] / max_lat

    def calculate_paths(self):
        paths = {}
        nodes = list(self.graph.nodes())
        
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                src, dst = nodes[i], nodes[j]
                
                # Get up to 3 shortest paths
                candidate_paths = k_shortest_paths(self.graph, src, dst, k=3, weight='weight')
                if candidate_paths:
                    paths[f"{src}_{dst}"] = candidate_paths
                    paths[f"{dst}_{src}"] = [p[::-1] for p in candidate_paths]
                    
        return paths

    def process(self):
        self.validate_and_clean()
        self.normalize_attributes()
        paths = self.calculate_paths()
        return self.graph, paths
