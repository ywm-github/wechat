import itchat
from itchat.content import *

itchat.auto_login(hotReload=True)   # 登录
friends = itchat.get_friends(update=True)   # 获取好友
self_user = friends[0]['UserName']    # 获取自己的微信号
status = ''    # 定义自动回复语
itchat.send_msg('已启用,输入菜单查看可用指令')


def menu():
    itchat.send('可用指令如下:\n1.统计\n2.查询好友\n3.自动回复,输入状态:\n   骑车|休息|睡觉|结束\n4.防撤回\n5.分享', self_user)


def search_people(people_name):
    user = itchat.search_friends(people_name)   # 按备注名搜索好友
    # noinspection PyBroadException
    try:
        nickname = user[0]['NickName']    # 获取微信名名称
        username = user[0]['UserName']    # 获取用户ID
        head_img = itchat.get_head_img(username)   # 获取头像
        signature = user[0]['Signature']    # 获取个性签名
        py_name = user[0]['PYQuanPin']    # 获取微信名拼音
        remarkname = user[0]['RemarkName']
        image_name = 'head_img_'+py_name+'.jpg'    # 定义头像
        with open('files\\'+image_name, 'wb') as f:
            f.write(head_img)
            f.close()
            msg_bb = '你的好友'+people_name+'的详细信息如下:微信名:'+nickname+'\n备注名:'+remarkname+'\n签名:'+signature+'\n头像：'
        itchat.send_msg(msg_bb, toUserName=self_user)
        itchat.send_image(image_name, toUserName=self_user)
    except Exception:
        itchat.send_msg('好友'+people_name+'不存在,请重新输入', self_user)


def listen_msg():
    reply = '中，无法及时查看消息，有事打电话[自动回复]'
    reply_status = '自动回复开启:\n'\
    @itchat.msg_register(TEXT, isFriendChat=True)    # 注册消息监听

    def text_reply(msg):
        msg_re = msg['Text']
        global status    # 自动回复状态
        if msg_re == '查询好友':
            itchat.send_msg('输入要查询的好友名称', toUserName=self_user)
            listen_serach()
        elif msg_re == '骑车' and msg['FromUserName'] == self_user:
            status = '骑车'+reply
            itchat.send(reply_status+status, self_user)
        elif msg_re == '休息' and msg['FromUserName'] == self_user:
            status = '休息'+reply
            itchat.send(reply_status+status, self_user)
        elif msg_re == '睡觉' and msg['FromUserName'] == self_user:
            status = '睡觉'+reply
            itchat.send(reply_status+status, self_user)
        elif msg_re == '结束' and msg['FromUserName'] == self_user:
            status = ''
            itchat.send('自动回复已关闭')
        elif msg_re == '菜单' and msg['FromUserName'] == self_user:
            menu()
        elif msg_re == '分享' and msg['FromUserName'] == self_user:
            itchat.send_msg('输入要分享给的好友名称')
        if msg['FromUserName'] != self_user:
            itchat.send(status, toUserName=msg['FromUserName'])
   

def listen_serach():
    @itchat.msg_register(TEXT, isFriendChat=True)   # 注册消息监听
    def text_reply(msg):
        if msg['Text'] == '退出':
            itchat.send('退出查询', self_user)
            listen_msg()
        elif msg['Text'] != '' and msg['FromUserName'] == self_user:
            search_people(msg['Text'])


listen_msg()
itchat.run()   # 保持运行状态
