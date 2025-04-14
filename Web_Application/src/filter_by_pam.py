"""
Filter the oligo table based on the dist mut pam column
"""

def filter_rows(group, threshold):
    """
    Filter the rows of a group based on the smallest absolute 
    value of the dist mut pam column
    :param group: DataFrame group
    :param threshold: Maximum number of rows to keep
    :return: Filtered DataFrame
    """
    # Check if there are three different dist mut pam values
    unique_dist_mut_pam = group['dist mut pam'].unique()

    if len(unique_dist_mut_pam) > 0:
    # Keep the rows with the smallest absolute values of dist mut pam
        filtered_rows = group.groupby('dist mut pam').apply(lambda x: x.nsmallest(1,
                                                             'dist mut pam').iloc[0])
    if len(filtered_rows) > threshold:
        # If we have more than three rows, select the top three rows
        # based on the smallest absolute value
        # Use absolute values for selection
        filtered_rows = filtered_rows.nsmallest(threshold, 'dist mut pam')

    return filtered_rows



def filter_pam(oligo_table, threshold):
    """
    Filter the oligo table based on the dist mut pam column
    :param oligo_table: DataFrame containing the oligo table
    :param threshold: Maximum number of rows to keep
    :return: Filtered DataFrame
    """
    grouped = oligo_table.groupby(['gene', 'parent aa','mutated aa', 'aa position'])
    #Apply the filtering function to each group and concatenate the results
    filtered_df = grouped.apply(lambda group: filter_rows(group, threshold)).reset_index(drop=True)
    print("Filtering Table")
    return filtered_df
