import time

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import timer

CALLBACK_ARGS = []
CALLBACK_KWARGS = {}

def callback_function(*args, **kwargs):
    global CALLBACK_ARGS
    global CALLBACK_KWARGS
    CALLBACK_ARGS = args
    CALLBACK_KWARGS = kwargs


class TestFunctionCallbacks(unittest.TestCase):
    def setUp(self):
        self.duration = 5000 # 5 milliseconds

    def test_simple_timeout(self):
        callback = lambda: None

        t = timer.Timer(self.duration, callback)
        t.start()
        self.assertTrue(t.running)
        time.sleep(0.01)
        self.assertTrue(t.expired)
        self.assertEqual(self.duration, t.elapsed)
        self.assertFalse(t.running)
        return t

    def test_reset(self):
        t = self.test_simple_timeout()
        
        t.reset()
        self.assertEqual(t.elapsed, 0)
        self.assertFalse(t.running)
        self.assertFalse(t.expired)
        return t

    def test_reset_and_run(self):
        # Ensure that after resetting, we can keep running as normal.
        t = self.test_reset()
        t.start()
        time.sleep(0.002) # 1 millisecond
        # stop returns the elapsed time, as well as sets the elapsed attribute
        val = t.stop()
        # We can't really test that the value equals any specific value,
        # just that the value isn't zero, which it shouldn't be.
        self.assertNotEqual(val, 0)
        self.assertNotEqual(t.elapsed, 0)
        self.assertEqual(val, t.elapsed)

    def test_invalid_initialization(self):
        with self.assertRaises(TypeError):
            # The second parameter must be callable.
            t = timer.Timer(self.duration, self.duration)

    def test_callback_function_args(self):
        args = (1, 2, 3)
        t = timer.Timer(self.duration, callback_function, *args)
        t.start()
        time.sleep(0.1)
        self.assertEqual(args, CALLBACK_ARGS)

    def test_callback_function_args_and_kwargs(self):
        args = (1, 2, 3)
        kwargs = {"lol" : True, "hurf" : "durf"}
        t = timer.Timer(self.duration, callback_function, *args, **kwargs)
        t.start()
        time.sleep(0.1)
        self.assertEqual(args, CALLBACK_ARGS)
        self.assertEqual(kwargs, CALLBACK_KWARGS)


# Test cases where methods of a class would be used instead of functions.
# This is probably the most common case.
class TestMethodCallbacks(unittest.TestCase):
    def setUp(self):
        self.duration = 5000
        self.args = []
        self.kwargs = {}

    def callback(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def callback_no_args(self):
        self.args = [True]

    def _test_callbacks(self, cb, args=None, kwargs=None):
        if args and kwargs:
            t = timer.Timer(self.duration, cb, *args, **kwargs)
        elif args:
            t = timer.Timer(self.duration, cb, *args)
        else:
            t = timer.Timer(self.duration, cb)
        t.start()
        time.sleep(0.01)
        self.assertEqual(t.elapsed, self.duration)
        self.assertFalse(t.running)
        self.assertTrue(t.expired)

    def test_callback_args(self):
        args = (1, 2, 3)
        self._test_callbacks(self.callback, args)
        self.assertEqual(args, self.args)
    
    def test_callback_args_and_kwargs(self):
        args = (4, 5, 6)
        kwargs = {"lol" : "rofl"}
        self._test_callbacks(self.callback, args, kwargs)
        self.assertEqual(args, self.args)
        self.assertEqual(kwargs, self.kwargs)

    def test_callback_no_args(self):
        self._test_callbacks(self.callback_no_args)
        # Confirm that the callback actually happened.
        self.assertEqual([True], self.args)


if __name__ == "__main__":
    unittest.main()

