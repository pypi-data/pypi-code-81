"""
This module helps in extracting all the data from a pdf file or a folder containing alot of pdf files into a dataframe.
Author: Rohit Thakur

"""

__version__ = "0.0.3"
__author__ = "Rohit Thakur"

import os 
import glob
import fitz
import pandas as pd 

import warnings
warnings.filterwarnings("ignore")

class Pdf2df:
    """
    A python class to get all the text in pdf files into a dataframe for further usage.

    Arguments:  - path (str) - Where the files are located. It could be a single file or a folder containing multiple pdf files
                - page (bool) - If True, the dataframe will contain each page of the pdf in a new row, if flase, all the text in the pdf will be in the same row.
                - single_file (bool) - This tell is method if the path is a folder containing multiple pdf files or a single pdf file.
    
    Outputs: A pandas dataframe that contains the data as per the arguments given.
    
    """
    def __init__(self, path, page=True, single_file=False):
        self.path = path
        self.page = page
        self.single_file = single_file
        
    def get_text(self):
        """
        This does not take any input but will outpus a dataframe according to the arguments passed while calling the class.
        """
        df = pd.DataFrame()
        if self.single_file == False:
            files = glob.glob(self.path + "\\*.pdf")
            if self.page == False:
                corpus = []
                for file in files:
                    doc = fitz.open(file)
                    pages = doc.pageCount
                    for i in range(pages):
                        page1 = doc.loadPage(i)
                        page1text = page1.getText("text")
                        pagetext = page1text.replace("\n", " ")
                        corpus.append(pagetext)  
                    filename = os.path.split(file)[1]
                    page1 = pd.Series(" ".join(corpus))
                    temp_df = page1.to_frame()
                    temp_df['Docname'] = filename
                    df = df.append(temp_df, ignore_index=True)
                return df
            elif self.page == True:
                for file in files:
                    head_tail = os.path.split(file)
                    docname = head_tail[1]
                    pdf_document = file
                    doc = fitz.open(pdf_document)
                    pages = doc.pageCount
                    for i in range(pages):
                        page1 = doc.loadPage(i)
                        page1text = page1.getText("text")
                        page1text = page1text.replace("\n", " ")
                        page = pd.Series(page1text)
                        temp_df = page.to_frame()
                        temp_df['Docname'] = docname
                        temp_df['Pagenumber'] = i
                        df = df.append(temp_df, ignore_index=True)
                return df
        if self.single_file == True:
            if self.page == False:
                corpus = []
                doc = fitz.open(self.path)
                pages = doc.pageCount
                for i in range(pages):
                    page1 = doc.loadPage(i)
                    page1text = page1.getText("text")
                    pagetext = page1text.replace("\n", " ")
                    corpus.append(pagetext)  
                filename = os.path.split(self.path)[1]
                page1 = pd.Series(" ".join(corpus))
                temp_df = page1.to_frame()
                temp_df['Docname'] = filename
                df = df.append(temp_df, ignore_index=True)
                return df
            elif self.page == True:
                head_tail = os.path.split(self.path)
                docname = head_tail[1]
                pdf_document = self.path
                doc = fitz.open(pdf_document)
                pages = doc.pageCount
                for i in range(pages):
                    page1 = doc.loadPage(i)
                    page1text = page1.getText("text")
                    page1text = page1text.replace("\n", " ")
                    page = pd.Series(page1text)
                    temp_df = page.to_frame()
                    temp_df['Docname'] = docname
                    temp_df['Pagenumber'] = i
                    df = df.append(temp_df, ignore_index=True)
                return df


if __name__ == "__main__":
    pass