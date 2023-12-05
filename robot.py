# -*- coding: utf-8 -*-
import random
import rstr

des_txt = '。套餐比较：'
print(des_txt[-1])
print(des_txt[0])
print(des_txt[1])

all_vip_list = ['腾讯', '优酷', '爱奇艺', '腾讯视频', '天猫超市', '哔哩哔哩', '网易云音乐', '全民K歌', '酷狗音乐', '芒果TV', '哔哩哔哩', 'PP视频', 'PP体育',
                '搜狐视频', '京东', '知乎盐选', '百度文库', '网易严选',
                '拼多多', '苏宁易购', '小红书', '唯品会', '考拉海购', '亚马逊', '肯德基', '麦当劳', 'qq绿钻', '饿了么', '盒马', '每日优鲜', '美团外卖', '开心消消乐',
                '小伴龙', '喜马拉雅',
                '樊登读书', '蜻蜓FM', '懒人读书', '哈罗出行', '青桔单车', '百度网盘', '微博', '陌陌', '探探', '凯叔讲故事', '崩坏3', '天天斗地主', '印象笔记']


num_vip = random.randint(2, 4)
vip_li = random.sample(all_vip_list, num_vip)

print(num_vip)
print(vip_li)

res_str = rstr.xeger('(优惠期|有效期)%d(个月|年|天)' % random.randint(1, 99))
print(res_str)

def gen_rdm_breach_regulations(none_ratio=0.5):
    num = random.random()
    return num  if num  < none_ratio else random.randint(1, 100)

print(gen_rdm_breach_regulations())