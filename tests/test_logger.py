import unittest
import os
from datetime import datetime
from App.utility.util_functions import get_root_dir
from tests.utility.test_data_functions import Data_Functions_Tester
from tests.utility.test_map_functions import Map_Functions_Tester

"""
This is the test logger for the project.
Every time tests are run, they are logged in the tests/logs directory.

Each file is named test_result_<timestamp>.txt, where <timestamp> is the time
when the tests were run.
"""

def run_tests():
    # Create log directory if it doesn't exist

    path_to_logdir = get_root_dir() / "tests/logs"  # Path to the logs directory
    os.mkdir(path_to_logdir) if not os.path.exists(path_to_logdir) else None  # Create the logs directory if it doesn't exist

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Timestamp for the log file

    with open(path_to_logdir / f"test_result_{timestamp}.txt", 'w') as f:
        runner = unittest.TextTestRunner(f)  # Create a test runner
        suite = unittest.TestSuite()  # Create a test suite
        suite.addTests(  # Add all tests to the test suite
            unittest.TestLoader().loadTestsFromTestCase(Data_Functions_Tester)  # Load all tests from the Data_Functions_Tester class
        )
        # suite.addTests(  # Add all tests to the test suite
        #     unittest.TestLoader().loadTestsFromTestCase(Map_Functions_Tester)  # Load all tests from the Map_Functions_Tester class
        # )

        executor = input("Tests run by: ")  # Get the name of the test executor

        f.write(f"Tests run by: {executor}\n")  # Write the test executor to the log file
        f.write(f"Tests run at: {timestamp}\n")  # Write the timestamp to the log file
        f.write("Test suite: \n")  # Write the test suite to the log file
        f.write(str(suite) + "\n\n")  # Write the test suite to the log file
        f.write("Test results:\n")  # Write the test results to the log file

        runner.run(suite)  # Run the tests
