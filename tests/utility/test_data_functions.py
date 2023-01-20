import unittest
from datetime import datetime
import App.utility.util_functions as uf

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here
        assert 1 == 2

    def test_something2(self):
        self.assertEqual(True, False)

def test_add_location():
    assert 2 + 2 == 3

def test_check_location_exists():
    ...


def main():
    logdir = "logs"
    print("Logdir: ", uf.get_root_dir())
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    runner = unittest.TextTestRunner(
        open(f"test_result_{timestamp}.txt", 'w')
    )
    unittest.main(testRunner=runner, verbosity=2)


if __name__ == '__main__':
    main()
