import sys

class SinglePositionList(object):

    def __init__(self, data_type=None, data_header=None):
        self.position_list = []
        self._header = data_header
        self._data_type = data_type
        self._data_len = None
    def __iter__(self):
        for position in self.position_list:
            yield position
    @property
    def header(self):
        return self._header
    @property 
    def data_len(self):
        return self._data_len 
    @property
    def data_type(self):
        return self._data_type
    @data_len.setter
    def data_len(self, value):
        self._data_len = value
    def __str__(self):
        return '\t'.join(["CHR","POS"]) + '\t' + '\t'.join(self.header)
    def append(self, val):
        # Must be the first data to be added
        if self.data_len is None:
            self.data_len = val.data_len
            if self.header is None:
                self.header = ["NA"] * self.data_len
        # Must have a problem
        if self.data_len != val.data_len:
            sys.stderr.write("Problem adding data, a line must have too many items\n")
            sys.exit(1)
        if not type(val) == self.data_type:
            sys.stderr.write("Problem adding data, trying to use two datatypes at once\n")
            sys.exit(1)
        self.position_list.append(val)

class SinglePosition(object):
   
    def __init__(self, chrom, pos, data):
        if 'chr' in chrom:
            # Remove a position that contains chromosome.
            chrom = chrom.split('chr')[1]
        self._chrom = chrom
        try:
            self._pos = int(pos)
        except TypeError:
            sys.stderr.write('Cannot convert position downstream problem.\n')
            sys.exit(1)
        self._data = data
        self._data_len = len(data)

    def __eq__(self, position2):
        if self.chrom == position2.chrom:
            if self.pos == position2.pos:
                return True
        return False

    @property
    def data_len(self):
        return self._data_len

    @data_len.setter
    def data_len(self, value):
        self._data_len = value

    @property
    def chrom(self):
        """
            Returns chromosome number
        """
        return self._chrom
    @property
    def pos(self):
        """
            Returns position string
        """
        return self._pos
    @property
    def data(self):
        """ 
            Returns data 
        """
        return self._data
    @data.setter
    def data(self, value):
        """
            Sets data field value
        """
        self._data = value
    def get_data_string(self):
        """
            Return Data
        """
        return '\t'.join(self.data)

    def __str__(self):
        return self.chrom + '\t' + str(self.pos) +'\t' + self.get_data_string()

class PSEQPos(SinglePosition): 
    def __init__(self, row):
        row = row.split()
        chrom = row[0].split(':')[0]
        pos = row[0].split(':')[1]
        data = row[1:]
        super(PSEQPos, self).__init__(chrom, pos, data)

class TwoColPos(SinglePosition):

    def __init__(self, row):
        row = row.split()
        chrom = row[0]
        pos = row[1]
        data = row[2:]
        super(TwoColPos, self).__init__(chrom, pos, data)

