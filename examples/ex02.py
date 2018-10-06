"""

Example 02

Process an directory with many prn files
"""
import leviutils

# Pass the directory with input files
parser = leviutils.parser.PeakFitDirectory(dir="path/to/directory")

# Export output files ( puts in the same directory given)
parser.export_files()