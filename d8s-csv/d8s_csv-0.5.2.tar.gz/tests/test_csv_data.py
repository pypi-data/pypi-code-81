from d8s_csv import csv_read_as_dict, csv_read_as_list

TEXT_COMMA_DELIMITED = "foo,bar\n1,2"
TEXT_TAB_DELIMITED = "foo\tbar\n1\t2"


def test_csv_read_docs_1():
    assert tuple(csv_read_as_list(TEXT_COMMA_DELIMITED)) == (['foo', 'bar'], ['1', '2'])
    assert tuple(csv_read_as_list(TEXT_TAB_DELIMITED, delimiter='\t')) == (['foo', 'bar'], ['1', '2'])


def test_csv_read_string_docs_1():
    assert tuple(csv_read_as_list(TEXT_COMMA_DELIMITED)) == (['foo', 'bar'], ['1', '2'])
    assert tuple(csv_read_as_list(TEXT_TAB_DELIMITED, delimiter='\t')) == (
        ['foo', 'bar'],
        ['1', '2'],
    )


def test_csv_read_as_dict_docs_1():
    assert tuple(csv_read_as_dict(TEXT_COMMA_DELIMITED)) == ({'foo': '1', 'bar': '2'},)


# @pytest.mark.network
# def test_csv_read_as_dict_url_argument():
#     """Make sure the csv_read_as_dict function will properly request the content from a url when given a url."""
#     result = tuple(
#         csv_read_as_dict(
#             'https://www.iana.org/assignments/iana-as-numbers-special-registry/special-purpose-as-numbers.csv'
#         )
#     )
#     assert isinstance(result, tuple)
#     assert len(result) == 10
#     assert 'AS Number' in result[0]
#     assert 'Reason for Reservation' in result[0]
#     assert 'Reference' in result[0]
#     assert result[0] == {'AS Number': '0', 'Reason for Reservation': 'Reserved by [RFC7607]', 'Reference': '[RFC7607]'}
