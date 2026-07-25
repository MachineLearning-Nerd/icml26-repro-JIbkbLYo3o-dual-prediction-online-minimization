import unittest

from repro.src.caching_instability import (
    belady_cost,
    build_instance,
    next_predictions,
    simulate_combiner,
)


class CachingInstabilityTests(unittest.TestCase):
    def test_prediction_perturbation_count(self):
        instance = build_instance(5, 2)
        self.assertEqual(instance["differing_requests"], 1)
        self.assertEqual(instance["incorrect_prediction_records"], 2)

    def test_belady_small_known_case(self):
        self.assertEqual(belady_cost([1, 2, 3, 1, 2, 3], 2), 2)

    def test_no_perturbation_control(self):
        instance = build_instance(8, 4, perturbed=False)
        run = simulate_combiner(
            instance["true"], instance["predictions"], 8, tie_leader="blind"
        )
        self.assertLess(run["combined_cost"] / belady_cost(instance["true"], 8), 3)

    def test_next_predictions(self):
        self.assertEqual(next_predictions([1, 2, 1], [1, 2, 1]), [2, 4, 4])


if __name__ == "__main__":
    unittest.main()
