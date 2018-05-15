import csv


class PeakFitParser:
    """
    Levi pre-processing PeakFit output files class
    """

    values = [
        'value', 'error'
    ]

    def __init__(self, filepath, encoding="utf-8", measures=('Amp', 'Ctr', 'Wid')):
        """
        :param filepath: path to input file
        :param encoding: default input file encoding
        :param measures: measures to get
        """
        self.measures = list(measures)
        self.encoding = encoding
        self.data = {}

        headers = ['Peak']

        # Define headers
        for measure in self.measures:
            for value in self.values:
                headers.append(measure + '-' + value)

        self.headers = headers

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

            row = [key]
            if len(peak.items()):
                for key, value in peak.items():
                    if key not in self.measures:
                        continue

                    for v in self.values:
                        row.append(value[v])

            writer.writerow(row)
            row = []

        del outputfile
        return True

    def parse(self):
        """
        Parses the input file
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
                                'error': float(splitted[2]),
                                'tvalue': float(splitted[3]),
                            }

                if line is "" and peak is not 0:
                    verify = False
                    self.data[peak] = peakdata
                    peakdata = {}

            except ValueError:
                peak = 0
                continue

        return self.data
