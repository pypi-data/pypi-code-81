
origin_csv_file = "省市区.csv"
save_path = "pca.csv"

import csv

csv_reader = csv.reader(open(origin_csv_file,'r',encoding='utf-8'))
csv_writer = csv.writer(open(save_path,'w',encoding='utf-8'))
csv_hearder = ['country','sheng','shi','qu','lat','lng']
csv_writer.writerow(csv_hearder)

for index, item in enumerate(csv_reader):
    assert len(item) == 3
    if index == 0 :
        continue

    insert_item = []
    insert_item.append("中国")

    insert_item.append(item[0])
    if item[1] == "市辖区":
        insert_item.append(item[0])
    else:
        insert_item.append(item[1])

    insert_item.append(item[2])

    # 经纬度默认为0
    insert_item.append(0)
    insert_item.append(0)

    csv_writer.writerow(insert_item)


