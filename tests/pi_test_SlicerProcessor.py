import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import unittest
import tempfile

import makerbot_driver


class SlicerProcessor(unittest.TestCase):

    def setUp(self):
        self.sp = makerbot_driver.GcodeProcessors.SlicerProcessor()

    def tearDown(self):
        self.sp = None

    def test_process_file(self):
        gcodes = [
            '; generated by Slic3r 0.9.3 on YYYY-MM-DD at HH:MM:SS\n',
            "G90\n",
            "G21\n",
            "M107 S500\n",
            "M106 S500\n",
            "M101\n",
            "M102\n",
            "M108\n",
            "G1 X0 Y0 Z0 A0 B0\n"
        ]
        expected_output = [
            '; generated by Slic3r 0.9.3 on YYYY-MM-DD at HH:MM:SS\n',
            'M73 P50 (progress (50%))\n',
            'G1 X0 Y0 Z0 A0 B0\n',
            'M73 P100 (progress (100%))\n'
        ]
        got_output = self.sp.process_gcode(gcodes)
        self.assertEqual(expected_output, got_output)

    def test_process_file_bad_version(self):
        gcodes = [
            '; generated by Slic3r 0.9.2 on YYYY-MM-DD at HH:MM:SS\n',
            'G90\n',
        ]
        self.assertRaises(makerbot_driver.GcodeProcessors.VersionError,
                          self.sp.process_gcode, gcodes)


class SlicerVersionChecker(unittest.TestCase):

    def setUp(self):
        self.version = '0.9.3'
        self.sv = makerbot_driver.GcodeProcessors.SlicerVersionChecker(
            self.version)

    def tearDown(self):
        self.sv = None

    def test_check_version_bad_version(self):
        line = '; generated by Slic3r 0.9.2 on YYYY-MM-DD at HH:MM:SS'
        self.assertRaises(makerbot_driver.GcodeProcessors.VersionError,
                          self.sv._transform_code, line)

    def test_check_version_good_version(self):
        line = '; generated by Slic3r 0.9.3 on YYYY-MM-DD at HH:MM:SS'
        output = self.sv._transform_code(line)
        self.assertEqual(output, [line])

if __name__ == '__main__':
    unittest.main()
