"""
Filter the oligo table based on the child codon column
"""

def filter_rows(group, threshold):
    """
    Filter the rows of a group based on the smallest absolute
    value of the child codon column
    """
    filtered_rows = group.drop_duplicates('child codon').head(threshold)
    return filtered_rows


def filter_codon(oligo_table, threshold):
    """
    Filter the oligo table based on the child codon column
    """
    grouped = oligo_table.groupby(['gene', 'parent aa','mutated aa', 'aa position'])
    filtered_df = grouped.apply(lambda group: filter_rows(group, threshold)).reset_index(drop=True)
    print("Filtering Table")
    return filtered_df
