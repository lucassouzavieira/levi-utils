"""

Example 01

Process an sigle prn file
"""
import leviutils

# Pass the filename and the measures to get from input file
parser = leviutils.parser.PeakFitParser("EXAMPLE.PRN", measures=("Amp", "Ctr", "Wid"))

# Export for an file
parser.to_columns(filename="PROCESSED.TXT")