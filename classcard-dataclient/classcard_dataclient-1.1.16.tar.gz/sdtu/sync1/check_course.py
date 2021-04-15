from config import SDTU_PAGE_SIZE
from requester.sdtu import SDTURequester
import time


def check_it():
    sdtu_requester = SDTURequester()
    semester_res = sdtu_requester.get_bks_semester(page=1, pagesize=SDTU_PAGE_SIZE)
    data_list = semester_res["data"]["Rows"]
    data_list = sorted(data_list, key=lambda d: d["KSRQ"], reverse=True)
    xn, bks_xq = None, None
    if data_list:
        current_semester = data_list[0]
        table_begin_date, table_end_date = current_semester["KSRQ"], current_semester["JSRQ"]
        xn, bks_xq = current_semester["XN"], current_semester["XQDM"]
        print(table_begin_date)
        print(table_end_date)
        time.sleep(10)
    single_map = {"单": 1, "双": 2}
    page_index = 1
    course_map = {}
    space_container = {}
    info_list = []
    while True:
        course_res = sdtu_requester.get_teacher_course_table(page=page_index, pagesize=SDTU_PAGE_SIZE,
                                                             params={"XQ": str(bks_xq),
                                                                     "XN": str(xn)})
        total_count = course_res["total"]
        current_rows = course_res["data"]["Rows"]
        if not current_rows:
            print("get_bks_course current_rows is 0!!!!!!")
            time.sleep(3)
        for row in current_rows:
            subject_name, bks_subject_num = row["KCMC"], row["KCDM"]
            subject_name = bks_subject_num
            if not subject_name:
                print("get_bk_course not subject_name")
                continue
            class_number = row["SKBJH"]
            classroom_name = row["SKDD"]
            teacher_number = row["RKJSGH"]
            week_range = row["ZC"]
            week, num = row["XQJ"], row["JC"]
            single = single_map.get(row["DSZ"], 0)
            if not (week_range and classroom_name and week and num and teacher_number):
                print("get_bk_course not (week_range and classroom_name and week and num and teacher_number)")
                continue
            if "教学一楼1313" in classroom_name and (3 == int(week) or 1 == int(week)):
                info_list.append(row)
            classroom_num = classroom_name
            week_range = week_range.replace("周", "")
            if "(单)" in week_range or "(双)" in week_range or "," in week_range:
                week_range_list = week_range.split(",")
            else:
                week_range_list = [week_range]
            for week_range_item in week_range_list:
                if "(单)" in week_range_item or "(双)" in week_range_item:
                    single = single_map.get(week_range_item[-2], 0)
                    week_range_item = week_range_item[:-3]
                try:
                    begin_week, end_week = int(week_range_item.split("-")[0]), int(week_range_item.split("-")[-1])
                except (Exception,):
                    import traceback
                    print(week_range)
                    print(traceback.format_exc())
                    time.sleep(2)
                    continue
                try:
                    space_name = classroom_num + '|' + str(begin_week) + '-' + str(
                        end_week) + '|' + num + '|' + week + '|' + str(single)
                    course_name = classroom_name + '|' + subject_name + '|' + teacher_number + '|' + str(class_number)
                except (Exception,) as e:
                    import traceback
                    print(traceback.format_exc())
                    continue
                if space_name not in space_container:
                    space_container[space_name] = []
                if course_name not in space_container[space_name]:
                    space_container[space_name].append(course_name)
        if page_index * SDTU_PAGE_SIZE >= total_count:
            break
        page_index += 1
    for space_name, course_name_list in space_container.items():
        if "教学一楼1313" in space_name and "|3|" in space_name:
            print("==========================================================================")
            print("space_name| {}".format(space_name))
            for course_item in course_name_list:
                print("course_name| {}".format(course_item))
            print("==========================================================================")
            time.sleep(2)
    for info in info_list:
        print(info)
        print("=======================================================================")
