from d8s_pdfs import pdf_read


def test_pdf_read_docs_1():
    result = pdf_read('http://africau.edu/images/default/sample.pdf')
    assert list(result) == [
        ' A Simple PDF File  This is a small demonstration .pdf file -  just for use in the Virtual Mechanics tutorials. More text. And more  text. And more text. And more text. And more text.  And more text. And more text. And more text. And more text. And more  text. And more text. Boring, zzzzz. And more text. And more text. And  more text. And more text. And more text. And more text. And more text.  And more text. And more text.  And more text. And more text. And more text. And more text. And more  text. And more text. And more text. Even more. Continued on page 2 ...',
        ' Simple PDF File 2  ...continued from page 1. Yet more text. And more text. And more text.  And more text. And more text. And more text. And more text. And more  text. Oh, how boring typing this stuff. But not as boring as watching  paint dry. And more text. And more text. And more text. And more text.  Boring.  More, a little more text. The end, and just as well. ',
    ]
