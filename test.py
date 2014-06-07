import unittest

import outbound

api_key = "testapikey"
first_run = True

class AnalyticsBasicTests(unittest.TestCase):
    def setUp(self):
        global first_run

        if first_run:
            first_run = False
            def on_error(code, err):
                self.assertEqual(outbound.ERROR_INIT, code, "Expected init() error.")
            outbound.identify(1, on_error=on_error)
        outbound.init(api_key)

    def test_identify(self):
        def on_error(code, err):
            self.assertEqual(outbound.ERROR_USER_ID, code, "Expected user ID error.")
        outbound.identify(None, on_error=on_error)

    def test_track(self):
        def user_id_on_error(code, err):
            self.assertEqual(outbound.ERROR_USER_ID, code, "Expected user ID error.")
        def event_on_error(code, err):
            self.assertEqual(outbound.ERROR_EVENT_NAME, code, "Expected event name error.")
        outbound.track(None, "event", on_error=user_id_on_error)
        outbound.track(1, None, on_error=event_on_error)

if __name__ == '__main__':
    unittest.main()
