__author__ = 'houlei'
__date__ = '04/29/2018'

import re
import numpy as np
from io import BytesIO
import src.edml_log as log

class Loader:
    ''' Data Loader Class

    The class used to load input data according to the comm rank,
    which means that except comm_rank == 0, for other comm_rank i,
    the loader read data from different input(such as local, http and hdfs)
    whose id is the hash of comm_rank i.

    Attributes:
        logger: an object from the class Logger, given by the ML object
    '''

    def __init__(self, logger):
        ''' Inits the logger attribute '''
        self.logger = logger

    def fromLocal(self, comm_rank, comm_size, datadir, separator):
        ''' Load data from a local file

        Different processors load data from one local file according to th hash
        of their own id.

        Args:
            comm_rank: the id of the processor in MPI communication world
            comm_size: the size of the MPI communication world
            datadir: the dir of input file
        '''

        input = open(datadir)
        num = 0
        load_num = 0
        tmp = ''
        for line in input:
            # to decide whether this line of data should be loaded
            # according to an samole hash
            if num % (comm_size - 1) == comm_rank - 1:
                tmp = tmp + line
                load_num = load_num + 1
            num = num + 1
        data = np.genfromtxt(BytesIO(tmp.encode('utf8')), dtype=None, delimiter=separator)
        self.logger.info(
            '[Processor %d] loads %d lines of data from the local file.'
             %(comm_rank, load_num))
        return data

    def fromHttp(self, comm_rank, comm_size, data, datadir, separator):
        ''' Load data from http

        Different processors load data from one http file according to th hash
        of their own id.

        Args:
            comm_rank: the id of the processor in MPI communication world
            comm_size: the size of the MPI communication world
            datadir: the dir of input file
            separator: the separator of data
        '''
        pass

    def fromHdfs(self, comm_rank, comm_size, data, datadir, separator):
        ''' Load data from a hdfs file

        Different processors load data from one hdfs file according to th hash
        of their own id.

        Args:
            comm_rank: the id of the processor in MPI communication world
            comm_size: the size of the MPI communication world
            datadir: the dir of input file
            separator: the separator of data
        '''
        pass
