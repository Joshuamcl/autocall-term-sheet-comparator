import unittest
from autocall import evaluate_autocall

class TestAutocall(unittest.TestCase):
    def test_autocall_barrier_changes_redemption(self):
        levels = [97, 90, 85, 75]

        result_100 = evaluate_autocall(levels=levels, nominal=1000, coupon_rate=0.076, autocall_barrier=100, protection_barrier=55)
        result_95 = evaluate_autocall(levels=levels, nominal=1000, coupon_rate=0.076, autocall_barrier=95, protection_barrier=55)

        self.assertEqual(result_100["outcome"], "protected")
        self.assertEqual(result_100["duration"], 5)
        self.assertAlmostEqual(result_100["redemption"], 1000)

        self.assertEqual(result_95["outcome"], "autocall")
        self.assertEqual(result_95["duration"], 1)
        self.assertAlmostEqual(result_95["redemption"], 1076)


    def test_protection_barrier_boundary(self):
        cases = [(60, "protected", 1000), (59.99, "capital_loss", 599.90),]

        for final_level, expected_outcome, expected_redemption in cases:
            with self.subTest(final_level=final_level):
                result = evaluate_autocall(
                    levels=[90, 85, 80, 75, final_level],
                    nominal=1000,
                    coupon_rate=0.08,
                    autocall_barrier=100,
                    protection_barrier=60,
                )

                self.assertIsNone(result["autocall_year"])
                self.assertEqual(result["duration"], 5)
                self.assertEqual(result["outcome"], expected_outcome)
                self.assertAlmostEqual(
                    result["redemption"], expected_redemption
                )


    def test_maturity_gain_boundary(self):
        cases = [(100, 1400), (99.99, 1000)]

        for final_level, expected_redemption in cases:
            with self.subTest(final_level=final_level):
                result = evaluate_autocall(
                    levels=[90, 85, 80, 75, final_level],
                    nominal=1000,
                    coupon_rate=0.08,
                    autocall_barrier=100,
                    protection_barrier=60,
                )

                self.assertIsNone(result["autocall_year"])
                self.assertEqual(result["duration"], 5)
                self.assertEqual(result["outcome"], "protected")
                self.assertAlmostEqual(
                    result["redemption"], expected_redemption
                )