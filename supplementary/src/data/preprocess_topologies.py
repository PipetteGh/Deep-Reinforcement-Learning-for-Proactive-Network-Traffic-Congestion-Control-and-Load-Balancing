import yaml
import os
import json
import networkx as nx
from topology_loader import TopologyLoader

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    config_path = os.path.join(base_dir, 'configs', 'topologies.yaml')
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    all_topologies = config['training_topologies'] + config['validation_topologies'] + config['test_topologies']
    
    raw_dir = os.path.join(base_dir, 'data', 'raw', 'graphml', 'graphml')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    for top_name in all_topologies:
        filepath = os.path.join(raw_dir, f"{top_name}.graphml")
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found.")
            continue
            
        print(f"Processing {top_name}...")
        loader = TopologyLoader(filepath)
        graph, paths = loader.process()
        
        # Save processed graph
        nx.write_graphml(graph, os.path.join(processed_dir, f"{top_name}_processed.graphml"))
        
        # Save candidate paths
        with open(os.path.join(processed_dir, f"{top_name}_paths.json"), 'w') as f:
            json.dump(paths, f)
            
    print("Data preprocessing complete.")

if __name__ == "__main__":
    main()
