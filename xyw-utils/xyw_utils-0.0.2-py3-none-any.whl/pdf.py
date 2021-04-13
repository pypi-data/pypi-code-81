import img2pdf
from pikepdf import Pdf
from xyw_utils.path import FileName


A3 = (img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(420))
A4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
A5 = (img2pdf.mm_to_pt(148), img2pdf.mm_to_pt(210))
B4 = (img2pdf.mm_to_pt(257), img2pdf.mm_to_pt(364))
B5 = (img2pdf.mm_to_pt(182), img2pdf.mm_to_pt(257))


def img_to_pdf(imgs, pdf_path, page_size=None, reverse=False):
    """
    转换图片为pdf格式并合并，为了保证无损转换，不支持有alpha通道的图片
    :param imgs: 图片地址列表，需要按合并顺序排列
    :param pdf_path: pdf文件的保存地址
    :param page_size: pdf文件的页面尺寸，默认为A4
    :param reverse: 是否反转页面尺寸，即长宽尺寸互换
    :return:
    """
    # 检查保存地址是否为.pdf后缀
    pdf = FileName(pdf_path)
    if not pdf.is_ext('.pdf'):
        raise ValueError('type of saving file must be pdf')

    # 检查imgs参数
    if isinstance(imgs, str):
        imgs = [imgs]
    if isinstance(imgs, list):
        for img in imgs:
            if not FileName(img).is_ext(['.png', '.jpeg', '.jpg']):
                raise ValueError('\'{}\' is not image'.format(img))
    else:
        raise TypeError('param imgs must be str or list of str')

    # 默认页面尺寸A4
    if page_size is None:
        page_size = A4

    # 长宽反转
    if reverse:
        page_size = page_size[::-1]
    layout_fun = img2pdf.get_layout_fun(page_size)

    # 转换图片为pdf格式并合并到指定路径
    pdf.make_dir()
    with open(pdf.fullpath, 'wb') as f:
        f.write(img2pdf.convert(imgs, layout_fun=layout_fun))


def merge_pdfs(pdfs, pdf_path):
    """
    合并多个pdf文件
    :param pdfs: 待合并pdf文件地址列表
    :param pdf_path: 最终pdf文件保存地址
    :return: pikepdf.Pdf
    """
    # 检查保存地址是否为.pdf后缀
    pdf = FileName(pdf_path)
    if not pdf.is_ext('.pdf'):
        raise ValueError('type of saving file must be pdf')

    # 检查pdfs参数
    if isinstance(pdfs, list):
        for item in pdfs:
            if not FileName(item).is_ext('.pdf'):
                raise ValueError('\'{}\' is not pdf'.format(item))
    else:
        raise TypeError('param pdfs must be list')

    # 合并pdf
    merged_pdf = Pdf.new()
    for file in pdfs:
        src = Pdf.open(file)
        merged_pdf.pages.extend(src.pages)
    pdf.make_dir()
    merged_pdf.save(pdf_path)

    return merged_pdf
