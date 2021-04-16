"""
计算公司员工薪资
"""

company = "北京尚学堂"


# 传入月（22.5天）薪，计算年薪（*12），日薪(/22.5)
def yearSalary(monthSalary):
    '''根据传入的月薪的值来计算：mothsalary*12计算出年薪'''
    return monthSalary * 12


def daySalary(monthSalary):
    """根据传入的值计算出一天的值"""
    return monthSalary / 22.5


if __name__ == "__main__":
    print("您的年薪是：", yearSalary(3000))
    print("您的日薪是：", daySalary(3000))