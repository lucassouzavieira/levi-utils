import csv


class Levi:
    """
    Levi pre-processing PeakFit output files class
    """

    headers = [
        'Peak',
        'Amp-value', 'Amp-error',
        'Ctr-value', 'Ctr-error',
        'Wid-value', 'Wid-error'
    ]

    measures = [
        'Amp', 'Ctr', 'Wid', 'Shpe'
    ]

    values = [
        'Value', 'Std-error', 't-value'
    ]

    def __init__(self, filepath, encoding="utf-8", ):
        """
        :param filepath: path to input file
        :param encoding: default input file encoding
        """
        self.encoding = encoding
        self.data = {}

        try:
            self.file = open(filepath)
        except IOError:
            print("Read error. Please verify the file path.")

    def to_columns(self, filename="export.txt"):
        """
        Exports to an column file format
        :param filename: output file
        :return: True if the operation is done, False otherwise
        """
        data = self.parse()
        outputfile = open(filename, "w+", newline="\n")
        writer = csv.writer(outputfile, delimiter="\t")

        # Headers
        writer.writerow(self.headers)

        # data
        for key, peak in data.items():
            print(peak)

            if len(peak.items()):
                row = [key,
                       peak['Amp']['value'], peak['Amp']['error'],
                       peak['Ctr']['value'], peak['Ctr']['error'],
                       peak['Wid']['value'], peak['Wid']['error']]

                writer.writerow(row)

        del outputfile
        return True

    def parse(self):
        """
        :return: an dict with classified peaks data
        """
        if not hasattr(self, 'file'):
            print("File not defined for this instance")
            return

        verify = False
        peakdata = {}
        peak = 0

        for line in self.file.read().split("\n"):
            try:
                splitted = line.split(" ")

                if "Peak" in splitted and int(splitted[1]):
                    peak = int(splitted[1])
                    verify = True
                    continue

                if verify:
                    splitted = list(filter(None, splitted))

                    for measure in self.measures:
                        if measure in splitted:
                            peakdata[measure] = {
                                'value': float(splitted[1]),
                                'std-error': float(splitted[2]),
                                't-value': float(splitted[2]),
                            }

                if line is "" and peak is not 0:
                    verify = False
                    self.data[peak] = peakdata
                    peakdata = {}

            except ValueError:
                peak = 0
                continue

        return self.data
