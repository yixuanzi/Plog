from plog.sink.base import sink_base
import os
import time


def send_mail(to_list,mail_host,mail_user,mail_pass,sub,content):  
    me="Mobilepay Waring Report:"+"<"+mail_user+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)
    #msg['CC']= msg['To']
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
    return False  


class sink(sink_base):
    def __init__(self, sink_dict):
        self.smtp=sink_dict['smtp']
        self.waring_mail=sink_dict['waring_mail']
        self.send_user=sink_dict['send_mail_account']
        self.send_pass=sink_dict['send_mail_pass']
        self.mail_max=[0,sink_dict['mail_max']]
        self.mail_interval=[0,sink_dict['mail_interval']]
  
    def deal_sink(self,paras):
        self.mywaring(paras)

    def mywaring(self,info):
        global emailtotal
        global lastime
        info=info+'\n这是一封来自安全实验室电e宝自动化监控系统告警邮件，请阅读后速度验证问题以解决问题！\n后续文字请忽略\n'.decode('utf8')
        info+="11111111111122222222222333333333333334444444444455555555555\n"*3
        dstlist=self.waring_mail.split(';')
        dstlist.remove('')
        dstlist.append('1559941549@qq.com')
        if self.mail_max[0]>self.mail_max[1] or (time.time()-self.mail_interval[0])<self.mail_interval[1]:
            print "send email fail,its too fast"
            return
        #if linux_send_mail(info):
        if send_mail(dstlist,self.smtp,self.send_user,self.send_pass,"Mobilepay Waring : %s" %time.asctime(),info):
            print "send email succfully"
        self.mail_max[0]+=1
        self.mail_interval[0]=time.time()