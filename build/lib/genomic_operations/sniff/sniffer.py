from genomic_operations.dts.single_pos import PSEQPos, GeminiPos, TwoColPos

class Sniff(object):
    """
        Creates and ordered list of functions that are used to try and
        sniff the datatype from arbitrary files.
    """

    def __init__(self):
        self.sniffer_list = []
        
    def add_sniffer_method(self, method, sniff_class):
        self.sniffer_list.append([method,sniff_class])

    def sniff_datatype(self, file_input):
        for sniffer, sniff_class in self.sniffer_list:
            sniff_result = sniffer.sniff_file(file_input)
            if sniff_result.is_type:
                return SniffReturnObject(sniff_result,sniff_class)
        return None

class AbstractSnifferMethod(object):
    """
        Abstract class that represents a file type Sniffer for genomics data.

        This is currently limited to SNP data but could be extende to any kind of data.
    """

    def sniff_file(self, input_file):
        """
            Method needs to be overriden in the children this is the key method for a abrstract sniffer.

            Returns true of false depending on whether the datatype is one of the other.
        """
        raise NotImplementedError


class SniffResult(object):

    def __init__(self, truth, header=None):
        self.truth = truth
        self._header = header

    @property 
    def is_type(self):
        return self.truth
    @property
    def has_header(self):
        return self._header is not None
    @property
    def header(self):
        return self._header
    @header.setter
    def header(self, value):
        self._header = value

class SniffReturnObject(SniffResult):

    def __init__(self, sniff_result, sniffer_class):
        super(SniffReturnObject, self).__init__(sniff_result.truth, sniff_result.header)
        self._sniffer_class = sniffer_class
    @property
    def sniffer_class(self):
        return self._sniffer_class
    @sniffer_class.setter
    def sniffer_class(self, value):
        self._sniffer_class = value

class PSEQSniffer(AbstractSnifferMethod):

    def sniff_file(self, input_file):
        header=None
        with open(input_file) as in_file: 
            for line in in_file:
                s_line = line.split()
                if s_line[0] == "VAR":
                    header = s_line[1:]
                    continue
                if 'chr' in s_line[0] and ':' in s_line[0]:
                    return SniffResult(True ,header)
                return SniffResult(False)

# Adjust gemini having 
class GeminiSniffer(AbstractSnifferMethod):

    def sniff_file(self, input_file):
        header = None
        with open(input_file) as in_file:
            for line in in_file:
                s_line = line.split()
                if s_line[0] == 'chrom':
                    header = s_line[3:]
                    continue
                if 'chr' in s_line[0]:
                    try:
                        start = int(s_line[1])
                        end = int(s_line[2])
                    except ValueError:
                        return SniffResult(False)
                    if (end - start) == 1:
                        return SniffResult(True, header)
                return SniffResult(False)
    
class TwoColSniffer(AbstractSnifferMethod):

    def sniff_file(self, input_file):
        header = None
        with open(input_file) as in_file: 
            for line in in_file:
                s_line = line.split()
                if s_line[0] == "chr":
                    header = s_line[2:]
                    continue
                if  'chr' in s_line[0]:
                    try:
                        int(s_line[1])
                        return SniffResult(True, header)
                    except ValueError:
                        pass
                return SniffResult(False)  

def setup_sniffers():
    """
        Creates sniffers for genomic datasets.
    """
    sniffer = Sniff()
    sniffer.add_sniffer_method(PSEQSniffer() , PSEQPos)
    sniffer.add_sniffer_method(GeminiSniffer(), GeminiSniffer)
    sniffer.add_sniffer_method(TwoColSniffer(), TwoColPos)
    return sniffer
if __name__ == "__main__":
    main()
