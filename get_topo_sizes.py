import pandas as pd

df = pd.read_csv('data/dataset_inventory.csv')
for name in ['Abilene', 'Janetbackbone', 'Janet', 'Bellcanada', 'Colt', 'Renater2001']:
    match = df[df['topology_name'].str.contains(name, case=False, na=False)]
    for _, row in match.iterrows():
        print(f"{row['topology_name']}: {row['number_of_nodes']} nodes, {row['number_of_edges']} edges")
