
import unittest2
import os
from datetime import timedelta
import fix_subtitles_timings


# Expected output if our input file is offset by 3 seconds
expected = [
    "1",
    "00:00:04,000 --> 00:00:07,074",
    "starlets Domesday fertilize Websters",
    "",
    "2",
    "00:01:09,943 --> 00:01:12,194",
    "timely cobalt beekeepers",
    "",
    "3",
    "00:02:31,858 --> 00:02:33,400",
    "Heifetz aesthete",
    "",
    "4",
    "00:02:36,863 --> 00:02:38,447",
    "gentler barrio interchanging",
    "",
    "5",
    "00:04:33,146 --> 00:04:35,897",
    "disposition's ya Fay's adhesion Tessie's trowels",
]


class TestOffsetTimings(unittest2.TestCase):
    def test_offset_timings(self):
        """
        Verify that offsetting a sample file by 3 seconds produces expected results.
        """
        tests_dir, _, test_file = __file__.rpartition(os.path.sep)
        input_file = os.path.join(tests_dir, 'data', 'sample.srt') 
        offset = timedelta(seconds=3)
        g = fix_subtitles_timings.offset_timings(input_file, offset)
        actual = []
        for i, line in enumerate(g):
            actual.append(line.strip())

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest2.main()
     
