import csv
from os import listdir
from os.path import isfile, isdir, join

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
        
        if not len(self.data):
            self.parse()

        try:
            outputfile = open(filename, "w+", newline="\n")
            writer = csv.writer(outputfile, delimiter="\t")

            # Headers
            writer.writerow(self.headers)

            # data
            for key, peak in self.data.items():

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

        except Exception:
            return False
    
    def get_data(self):
        """
        Returns the parsed data
        :return: None
        """
        if not len(self.data):
            self.parse()
        
        return self.data

    def parse(self):
        """
        Parses the input file
        :return: None
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
                    if len(peakdata.items()):
                        self.data[peak] = peakdata

                    peakdata = {}

            except ValueError:
                peak = 0
                continue

        return


class PeakFitDirectory:
    """
    Levi process directory with a PeakFit output files
    """

    def __init__(self, dir = "."):
        self.path = dir
        if not isdir(self.path):
            raise EnvironmentError
        
        self.files = [ifile for ifile in listdir(self.path) if isfile(join(self.path, ifile)) and ifile.lower().endswith(".prn")]
        self.data = []

    def process(self):
        """
        Gets data from each input file in directory
        :return: None
        """

        for f in self.files:
            parser = PeakFitParser(join(self.path, f))
            self.data.append(parser.get_data())
    
    def export_files(self):
        """
        Exports each input file to column file format
        :return: Post-processed files
        """

        for f in self.files:
            parser = PeakFitParser(join(self.path, f))
            parser.to_columns(join(self.path, f + ".txt"))

    def export_peaks(self):
        """
        Exports the data grouping by Peak number
        :return: Post-processed files
        """

        if not len(self.data):
            self.process()
        
        data = {}
        
        for filedata in self.data:
            for peak, peakdata in filedata:
                if not peak in data: 
                    data[peak] = []
                
                data[peak].append(peakdata)
        
        print(data)


