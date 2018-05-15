from .parser import PeakFitParser


class PeakFitPlot:
    """
    PeakFlitPlot class
    """

    def __init__(self, parser):
        """
        :param parser: PeakFit parser
        """
        if not isinstance(parser, PeakFitParser):
            raise ValueError

        self.parser = parser

    def plot_measure(self, measure):
        pass

    def plot_all(self):
        pass