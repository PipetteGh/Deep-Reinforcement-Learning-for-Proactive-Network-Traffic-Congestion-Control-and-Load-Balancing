# PHASE 0 STATUS

## What was done
- Extracted `graphml.tar.gz` and `gml.tar.gz` datasets into `data/raw/`.
- Created a Python script `src/data/analyze_datasets.py` to iterate through the datasets.
- Handled errors in specific GML files containing duplicate nodes/edges.
- Generated `data/dataset_inventory.csv` containing node/edge counts and graph attributes.
- Generated `data/dataset_summary.json` containing aggregate metrics.
- Generated matplotlib visualizations for node/edge distribution and format counts.

## Files created
- `data/raw/graphml/` and `data/raw/gml/`
- `src/data/analyze_datasets.py`
- `data/dataset_inventory.csv`
- `data/dataset_summary.json`
- `results/figures/dataset_nodes_edges.png`
- `results/figures/dataset_formats.png`

## Experiments completed
- None required for this phase. Dataset auditing is complete.

## Problems encountered
- Several GML files contained invalid formats (e.g., duplicate node labels such as 'None', 'London', etc., or duplicate edges). These errors were caught and the corrupted files were skipped to ensure the integrity of the downstream analysis.

## Decisions made
- We will rely heavily on the 276 valid GraphML topologies moving forward, as they parsed reliably without duplication errors and provide a large enough sample size for training, validation, and testing.

## What remains
- Transitioning to Phase 1: Selecting a subset of small, medium, and large topologies for the experiment splits.
