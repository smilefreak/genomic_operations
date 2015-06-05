import logging

from genomic_operations.dts.single_pos import SinglePosition
from genomic_operations.dts.single_pos import SinglePositionList
from genomic_operations.operations.output import print_result 

def _merge_two_single_pos(temp_merge, dataset):
    """
        First important this to generate a composite header of the two datasets
    """
    header = temp_merge.header + dataset.header
    logging.info(dataset.header)
    position_list = SinglePositionList(SinglePosition, header)
    for temp_merge in temp_merge:
        for data in dataset:
            if data == temp_merge:
                temp_data = temp_merge.data + data.data
                position_list.append(SinglePosition(data.chrom, data.pos, temp_data))
    return position_list

def merge_single_pos(datasets, output):
    """
        Merges single position files
    """
    no_datasets = len(datasets)
    temp_merge = datasets[0]
    for i in range(1, no_datasets):
        temp_merge = _merge_two_single_pos(temp_merge, datasets[1])
    print_result(temp_merge, output)  

