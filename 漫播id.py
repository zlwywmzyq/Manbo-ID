# -- coding: utf-8 --**
import json
import re

import requests

# 复制粘贴要查的漫播剧集任意一集APP或PC端链接（免费付费皆可）
url = ""

if 'pc' in url:
    detail_id = url.split('Id=')[1]
    new_url = "https://manbo.hongdoulive.com/web_manbo/dramaSetDetail?dramaSetId=" + detail_id
    temp = 'data'
else:
    episode_id = url.split('id=')[1][:19]
    radio_id = url.split('DramaId=')[1][:19]
    new_url = "https://manbo.hongrenshuo.com.cn/api/v207/radio/drama/set/h5/detail?radioDramaSetId=%s&radioDramaId=%s" \
              % (episode_id, radio_id)
    temp = 'b'

r = requests.get(new_url).text
r = str(json.loads(r)[temp]['radioDramaResp']['setRespList'])
pattern1 = re.compile("'vipFree': (.+?),")
vipFree = re.findall(pattern1, r)
num = len(vipFree)
pattern2 = re.compile("'setId': (.+?), ")
setId = re.findall(pattern2, r)
episodes = [setId[i] for i in range(num) if vipFree[i] == '1']
if len(episodes) == 0:
    pattern3 = re.compile("'payType': (.+?),")
    payType = re.findall(pattern3, r)
    episodes = [setId[i] for i in range(num) if payType[i] == '1']
danmu = []
for each in episodes:
    next_url = "https://manbo.hongrenshuo.com.cn/api/v11/radio/drama/set/danmaku/h5/pull?radioDramaSetId=%s" \
               "&startTime=0&endTime=10000000" % each
    danmakuList = json.loads(requests.get(next_url).content)['b']['danmakuList']
    for j in danmakuList:
        danmu.append(j['eid'])

print("付费集ID数：%d" % len(set(danmu)))
print("付费集弹幕数：%d" % len(danmu))
