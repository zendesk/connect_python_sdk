import unittest

import outbound

api_key = "testapikey"
first_run = True

class AnalyticsBasicTests(unittest.TestCase):
    def setUp(self):
        global first_run

        if first_run:
            first_run = False
            with self.assertRaises(outbound.NoApiKeyException):
                outbound.identify(1)
        outbound.init(api_key)

    def test_identify(self):
        with self.assertRaises(outbound.InvalidUserIdException):
            outbound.identify(None)

    def test_track(self):
        with self.assertRaises(outbound.InvalidUserIdException):
            outbound.track(None, "event")
        with self.assertRaises(outbound.InvalidEventException):
            outbound.track(1, None)

if __name__ == '__main__':
    unittest.main()
