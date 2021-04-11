
def append(list,values):
	values,columns=list._convert_row(values)
	list.insert_with_values(-1,columns,values)