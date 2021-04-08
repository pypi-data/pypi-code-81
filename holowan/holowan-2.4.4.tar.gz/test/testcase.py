'''
Created on 2020-11-23

@author: zhanyifei
'''
import xlrd
from builtins import int
 

 
def excel_data(file):
    
    
    try:
        
        data = xlrd.open_workbook(file)        
        table = data.sheet_by_index(0)       
        nrows = table.nrows
        gggg = nrows
        print(gggg)
        
        ncols = table.ncols
        
        excel_list = []
        excel_list.append(gggg)
        for row in range(1, nrows):
            for col in range(ncols):
                
                cell_value = table.cell(row, col).value
                if(type(cell_value)==float):
                    cell_value = int(cell_value) 
                    
    
                excel_list.append(cell_value)
        return excel_list
    
        
    
    except Exception as e:
        print(e)
        
# if __name__ == '__main__':
#      list1=excel_data('qos.xlsx')
#           
#      print(list1)