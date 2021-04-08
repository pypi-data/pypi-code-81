import json as __json
import re as __re

import requests as __requests
from requests.sessions import Session as __Session

__HEADERS: dict[str, str] = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 11.0; Windows 95; Trident/3.0)',
                             'referer': 'https://shanxi.xueanquan.com/'}


def __do_survey(course: str, soj_session: __Session) -> int:
    print('开始做', course)
    hd_url: str = course[-1][2:-2]
    url21: str = hd_url
    url22: str = hd_url
    if 'index.html' in hd_url:
        hd_dir: str = hd_url[0:hd_url.find('index')]
        url21: str = hd_dir + 'shipin.html'
        url22: str = hd_dir + 'video.html'

    try:
        spe_id: str = (__re.search(r'data-specialId ??="(.*?)"', soj_session.get(url21, headers=__HEADERS).text)
                       or __re.search(r'data-specialId ??="(.*?)"',
                                      soj_session.get(url22, headers=__HEADERS).text)).group()
    except AttributeError:
        print('匹配失败')
        return -1

    step: int
    for step in [1, 2]:
        soj_session.post('https://huodongapi.xueanquan.com/p/shanxi/Topic/topic/platformapi/api/v1/records/sign',
                         json={'specialId': spe_id, 'step': step}, headers=__HEADERS)

    return 0


def __do_li(course: str, soj_session: __Session) -> int:
    print('开始做', course)
    li: str = course[0]
    gid: str = course[3]
    video_data: str = soj_session.get(
        f'https://yangquan.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx?gid=789&li={li}', headers=__HEADERS).text

    # 步骤一
    vid: str = __re.search(r'VideoID == "(.*)"', video_data).group()
    soj_session.post(
        'https://yangquan.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,'
        'FamilyEduCenter.ashx?_method=SkillCheckName&_session=rw',
        data=dict(videoid=vid, gradeid=gid, courseid=li), headers=__HEADERS)

    # 步骤二
    # 准备好答案包
    strings: list[str] = __re.search(r'SeeVideo.TemplateIn2\((.*)\)',
                                     video_data).group().split(',')
    # 发答案
    soj_session.post(
        'https://yangquan.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,'
        'FamilyEduCenter.ashx?_method=TemplateIn2&_session=rw',
        data=dict(workid=strings[0][1:-1], fid=strings[1][2:-1], title="", require="", purpose="", contents="",
                  testwanser="0|0|0", testinfo="已掌握技能", testMark="100", testReulst="1", SiteAddrees="", SiteName="",
                  watchTime="", CourseID=strings[-1][2:-1]), headers=__HEADERS)

    return 0


def do(username: str, password: str) -> int:
    # 先登录
    soj_session: __Session = __requests.session()
    login_data: dict = __json.loads(soj_session.post(
        r'https://shanxilogin.xueanquan.com/LoginHandler.ashx', data={
            'userName': username,
            'password': password,
            'type': 'login',
        }, headers=__HEADERS).text)
    if login_data['ErrorMsg'] == '':
        print(username, '登录成功')
    else:
        print(username, '无法登录')
        return -1

    # 获得班级作业列表(包括自己已经做过的)
    courses: list[str] = __re.findall(r'showhdtcbox\((.*?)\)', __requests.get(
        'https://file.safetree.com.cn/webapi.shanxi/jt/MyHomeWork.html'
        f'?grade={login_data["UInfo"]["Grade"]}&classroom={login_data["UInfo"]["ClassRoom"]}'
        f'&cityid={login_data["UInfo"]["CityCode"]}').text)[1:]
    courses2: list[list[str]] = []
    course: str
    for course in courses:
        course: list[str] = course.split(', ')
        if course not in courses2:
            courses2.append(course)
    print(username, '作业清单获取成功')

    # 做作业
    for _, course in enumerate(courses2):
        if int(course[0]) == -1:
            __do_survey(course, soj_session)
        else:
            __do_li(course, soj_session)
    print('做完')

    return 0
