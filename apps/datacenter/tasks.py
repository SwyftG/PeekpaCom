from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail


@task()
def webspider_start_peekpa():
    print("『皮爷撸码』这个号太干了")

@task()
def send_peekpa_email(item):
    title = "这是一封来自Peekpa.com的邮件"
    bodyhtml = '<html><body>' + \
               '<h1>日本实时地震报告： ' + \
               '地点：<a href="' + item['jp_url'] + '">' + item['jp_location'] + '</a>' + \
               '震级：<a href="' + item['jp_url'] + '">' + item['jp_level'] + '</a>' + \
               '</h1>' + \
               '<h3>ID：' + item['jp_id'] + '</h3>' + \
               '<h3>位置：<img src="' + item['jp_location_image_url'] + '"/></h3>' + \
               '<h3>时间：<a href="' + item['jp_url'] + '">' + item['jp_title'] + '</a></h3>' + \
               '<h3>强度：<a href="' + item['jp_url'] + '">' + item['jp_max_level'] + '</a></h3>' + \
               '<p> 点击上面的任意链接即可跳转到『日本气象厅』网站查看详情 </p>' + \
               '</body></html>'
    send_mail(
        title,
        "this is message",
        'xxxxxx@126.com',   #发送邮件，settings.py文件里配置
        ['xxxxxx@126.com'],     #收件人邮件
        fail_silently=False,
        html_message=bodyhtml
    )

