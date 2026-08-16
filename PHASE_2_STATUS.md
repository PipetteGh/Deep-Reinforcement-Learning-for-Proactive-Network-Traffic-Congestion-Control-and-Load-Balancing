# PHASE 2 STATUS

## What was done
- Built `src/data/topology_loader.py` to encapsulate logic for cleaning graphs, parsing capacities/latencies, and calculating paths.
- Built `src/data/preprocess_topologies.py` to ingest the `topologies.yaml` splits and process them.
- Extracted networkx attributes, handled strings vs ints, applied defaults (10 Gbps and 1 ms latency) where data was missing.
- Calculated up to 3 candidate shortest paths (k-shortest paths based on latency weight) for every source-destination pair to allow the MDP routing actions to choose or shift weights.
- Exported the normalized topologies and candidate paths to `data/processed/`.

## Files created
- `src/data/topology_loader.py`
- `src/data/preprocess_topologies.py`
- `data/processed/*_processed.graphml` (processed topology graphs)
- `data/processed/*_paths.json` (computed k-shortest paths for all pairs)
- `PHASE_2_STATUS.md`

## Experiments completed
- None.

## Problems encountered
- Topology bandwidths and latencies had highly irregular formatting (e.g., string labels like '10 Gbps', missing keys). A robust try-except parser was used to regex-extract numeric values.

## Decisions made
- We decided to precompute the candidate routing paths now, rather than recomputing them inside the Reinforcement Learning environment step loop, which would drastically slow down training.

## What remains
- Transitioning to Phase 3: Building the Gymnasium Network Environment (`src/environment/network_congestion_env.py`).
