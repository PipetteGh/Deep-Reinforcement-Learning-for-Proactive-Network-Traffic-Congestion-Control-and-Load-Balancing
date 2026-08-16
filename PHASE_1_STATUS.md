# PHASE 1 STATUS

## What was done
- Analyzed the dataset inventory.
- Selected a subset of strictly connected GraphML topologies.
- Segmented topologies into small (10-25 nodes), medium (26-50 nodes), and large (>50 nodes) networks.
- Sampled training, validation, and test sets ensuring mutually exclusive test splits for generalization testing.
- Created `configs/topologies.yaml` holding the experimental topology splits and 5 random seeds (42, 100, 2024, 777, 1337).

## Files created
- `configs/topologies.yaml`
- `PHASE_1_STATUS.md`

## Experiments completed
- None. Setup phase.

## Problems encountered
- None.

## Decisions made
- We exclusively used GraphML formats to ensure parser consistency and filtered out any disconnected graphs, which would break routing algorithms.

## What remains
- Transitioning to Phase 2: Data Preprocessing (building a pipeline to load these selected topologies and normalize their attributes).
