import turicreate as tc

def concat_sframes(list_of_sframes: tc.SFrame):
    sf_all = list_of_sframes[0]
    for sf in list_of_sframes[1:]:
        sf_all = sf_all.append(sf)
    return sf_all


def count_xstr_concat_ystr(sframe, column_x, column_y):
    return sframe.groupby(column_x,
                          {'count': tc.aggregate.COUNT(),
                           column_y: tc.aggregate.CONCAT(column_y)}
                         )


__all__ = ['concat_sframes', 'count_xstr_concat_ystr']
