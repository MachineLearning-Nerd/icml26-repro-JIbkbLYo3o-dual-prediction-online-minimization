"""Exact implementation of the deterministic Wei caching combiner."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass
class CacheState:
    cache: set[int]
    last_used: dict[int, int]
    predicted_next: dict[int, int]
    evictions: int = 0


def next_predictions(true_sequence: list[int], anticipated: list[int]) -> list[int]:
    """Prediction at t is the next anticipated occurrence of the true page."""
    positions: dict[int, deque[int]] = defaultdict(deque)
    for index, page in enumerate(anticipated):
        positions[page].append(index)
    result = []
    infinity = len(anticipated) + 1
    for index, page in enumerate(true_sequence):
        while positions[page] and positions[page][0] <= index:
            positions[page].popleft()
        result.append(positions[page][0] if positions[page] else infinity)
    return result


def _serve_lru(state: CacheState, page: int, time: int, k: int) -> None:
    if page not in state.cache:
        if len(state.cache) == k:
            victim = min(state.cache, key=lambda item: (state.last_used[item], item))
            state.cache.remove(victim)
            state.evictions += 1
        state.cache.add(page)
    state.last_used[page] = time


def _serve_blind(
    state: CacheState, page: int, prediction: int, time: int, k: int
) -> None:
    if page not in state.cache:
        if len(state.cache) == k:
            # Furthest predicted next arrival; ties broken by LRU, then id.
            victim = max(
                state.cache,
                key=lambda item: (
                    state.predicted_next[item],
                    -state.last_used[item],
                    -item,
                ),
            )
            state.cache.remove(victim)
            state.evictions += 1
        state.cache.add(page)
    state.last_used[page] = time
    state.predicted_next[page] = prediction


def simulate_combiner(
    sequence: list[int], predictions: list[int], k: int, tie_leader: str
) -> dict:
    blind = CacheState(set(), {}, {})
    lru = CacheState(set(), {}, {})
    combined = CacheState(set(), {}, {})
    stage_trace = []
    for time, (page, prediction) in enumerate(zip(sequence, predictions, strict=True)):
        _serve_blind(blind, page, prediction, time, k)
        _serve_lru(lru, page, time, k)
        if blind.evictions < lru.evictions:
            leader_name, leader = "blind", blind
        elif lru.evictions < blind.evictions:
            leader_name, leader = "lru", lru
        elif tie_leader == "blind":
            leader_name, leader = "blind", blind
        else:
            leader_name, leader = "lru", lru

        if page not in combined.cache:
            if len(combined.cache) == k:
                candidates = combined.cache - leader.cache
                if not candidates:
                    raise AssertionError("combiner invariant gives no legal eviction")
                victim = min(candidates)
                combined.cache.remove(victim)
                combined.evictions += 1
            combined.cache.add(page)
        combined.last_used[page] = time
        stage_trace.append(
            {
                "time": time,
                "page": page,
                "prediction": prediction,
                "blind_cost": blind.evictions,
                "lru_cost": lru.evictions,
                "combined_cost": combined.evictions,
                "leader": leader_name,
            }
        )
    return {
        "blind_cost": blind.evictions,
        "lru_cost": lru.evictions,
        "combined_cost": combined.evictions,
        "trace": stage_trace,
    }


def belady_cost(sequence: list[int], k: int) -> int:
    positions: dict[int, deque[int]] = defaultdict(deque)
    for index, page in enumerate(sequence):
        positions[page].append(index)
    cache: set[int] = set()
    evictions = 0
    infinity = len(sequence) + 1
    for index, page in enumerate(sequence):
        positions[page].popleft()
        if page in cache:
            continue
        if len(cache) == k:
            victim = max(
                cache,
                key=lambda item: (
                    positions[item][0] if positions[item] else infinity,
                    item,
                ),
            )
            cache.remove(victim)
            evictions += 1
        cache.add(page)
    return evictions


def build_instance(k: int, stage3_cycles: int, perturbed: bool = True) -> dict:
    if k < 3 or stage3_cycles < 1:
        raise ValueError("requires k>=3 and a positive horizon")
    stage1_anticipated = list(range(1, k + 1)) + [1]
    stage1_true = list(range(1, k + 1)) + ([2] if perturbed else [1])
    stage2_cycles = k * stage3_cycles
    stage2 = list(range(2, k + 2)) * stage2_cycles
    stage3 = list(range(2, k + 3)) * stage3_cycles
    anticipated = stage1_anticipated + stage2 + stage3
    true = stage1_true + stage2 + stage3
    differing_requests = sum(a != b for a, b in zip(true, anticipated, strict=True))
    predictions = next_predictions(true, anticipated)
    true_next = next_predictions(true, true)
    incorrect_prediction_records = sum(a != b for a, b in zip(predictions, true_next))
    return {
        "k": k,
        "stage2_cycles": stage2_cycles,
        "stage3_cycles": stage3_cycles,
        "stage3_start": len(stage1_true) + len(stage2),
        "true": true,
        "anticipated": anticipated,
        "predictions": predictions,
        "differing_requests": differing_requests,
        "incorrect_prediction_records": incorrect_prediction_records,
    }
