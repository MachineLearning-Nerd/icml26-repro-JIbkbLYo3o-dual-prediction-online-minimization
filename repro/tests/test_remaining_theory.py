import unittest

from repro.src.theory_certificates import (
    TheoryCertificateError,
    check_claim1,
    check_claim3,
    check_claim6,
    harmonic,
)


class RemainingTheoryTests(unittest.TestCase):
    def test_claims_verify(self):
        self.assertEqual(check_claim1()["verdict"], "VERIFIED")
        self.assertEqual(check_claim3()["verdict"], "VERIFIED")
        self.assertEqual(check_claim6()["verdict"], "VERIFIED")

    def test_harmonic_domain_is_enforced(self):
        with self.assertRaises(TheoryCertificateError):
            harmonic(0)

    def test_printed_c6_construction_is_not_accepted(self):
        result = check_claim6()
        row = result["printed_construction_diagnostic"][31]
        self.assertNotEqual(
            row["cost_lower_bound"],
            result["corrected_parametric_certificate"][31]["cost_lower_bound"],
        )


if __name__ == "__main__":
    unittest.main()
