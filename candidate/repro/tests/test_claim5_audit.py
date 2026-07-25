import unittest

from repro.src.audit_claim5_real_data import image_manifest


class Claim5AuditTests(unittest.TestCase):
    def test_all_source_figures_are_pinned(self):
        manifest = image_manifest()
        self.assertEqual(set(manifest), {"parking_k", "parking_f", "bike_trip", "bike_minute"})
        self.assertTrue(all(len(row["sha256"]) == 64 for row in manifest.values()))


if __name__ == "__main__":
    unittest.main()
