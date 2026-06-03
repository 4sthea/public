from __future__ import annotations

from datetime import date
import unittest

from dividend_window import (
    classify_capture_timing,
    days_to_ex_date,
    is_inside_capture_window,
)


class DividendWindowTests(unittest.TestCase):
    def test_days_to_ex_date_preserves_sign(self):
        self.assertEqual(days_to_ex_date(date(2026, 6, 1), date(2026, 6, 10)), 9)
        self.assertEqual(days_to_ex_date(date(2026, 6, 10), date(2026, 6, 10)), 0)
        self.assertEqual(days_to_ex_date(date(2026, 6, 12), date(2026, 6, 10)), -2)

    def test_capture_window_includes_before_and_after(self):
        ex_date = date(2026, 6, 10)
        self.assertTrue(is_inside_capture_window(date(2026, 6, 1), ex_date, 14, 14))
        self.assertTrue(is_inside_capture_window(date(2026, 6, 20), ex_date, 14, 14))
        self.assertFalse(is_inside_capture_window(date(2026, 5, 20), ex_date, 14, 14))
        self.assertFalse(is_inside_capture_window(date(2026, 6, 30), ex_date, 14, 14))

    def test_classify_capture_timing(self):
        ex_date = date(2026, 6, 10)
        self.assertEqual(classify_capture_timing(date(2026, 6, 1), ex_date), "before")
        self.assertEqual(classify_capture_timing(date(2026, 6, 10), ex_date), "ex-date")
        self.assertEqual(classify_capture_timing(date(2026, 6, 12), ex_date), "after")


if __name__ == "__main__":
    unittest.main()
