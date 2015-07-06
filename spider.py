#-*- coding: utf-8 -*-
#
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import string 
import urllib
import urllib2  
import re
import MySQLdb
import jobDB
import socket
from hashlib import md5
import threading
socket.setdefaulttimeout(5)
mutex = threading.RLock()
db = jobDB.jobDB()
#form  con_mysql import con_mysql
class jobSpider():
    def __init__(self):
        '''
        self.url='http://search.51job.com/jobsearch/search_result.php?fromJs=1&funtype=0100%2C2500%2C2811%2C2600%2C2700&industrytype=01%2C40%2C32%2C38&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1'
        '''
        self.url = ''
        self.the_part_of_next_page_url = 'http://search.51job.com/list/000000%252C00,000000,0100%252C2500%252C2811%252C2600%252C2700,01%252C40%252C32%252C38,9,99,%2B,2,'
        #self.mymd5 = md5()  #function md5()
        #self.job_md5 = ''    
        self.company = ''          #公司名称
        self.position = ''         #岗位名称
        self.release_date = ''     #发布时间
        self.education = '没写明'        #教育要求
        self.description = ''      #岗位描述和要求
        self.workplace = '没写明'        #工作地点
	self.salary = '没写明'           #薪水 
	self.years_of_work = '没写明'    #工作范围
	self.the_num_of_recuritment= '没写明'     #招聘人数       
        self.job_course_set = ''   #课程集合
	self.page = ''             
        #self.page = urllib2.urlopen(self.url).read().decode('gbk')
        self.jobstr = ''   #let the informations of job connetct to a whole
        self.jobhref = ''
        #self.jobhref = re.findall('<td class="td1"><a adid="".*?href="(.*?)"',self.page)
        #print u'jobhreflength =',len(self.jobhref)
    
    
    def get_jobs(self,href):    
        #打开文件
        print "function get_jobs() start..."         
        try:
            self.job_course_set = ''  #课程列表先清空
            self.url = href
            urlinfo = href
            page = urllib2.urlopen(urlinfo)
            print type(page)
            pageinfo = page.read().decode("gbk")
            print type(pageinfo)
            company =re.findall('<a target="_blank" style=".*?" href=".*?">(.*?)</a>',pageinfo) 
            for com in company:
                self.company=com
            title = re.findall('<td class="sr_bt" colspan=".*?" >(.*?)</td>',pageinfo)
            for tit in title:
                self.position=tit.encode('utf-8')
            details = re.findall('<td class="txt_1" width="12%">(.*?)</td><td class="txt_2 ">(.*?)</td>',pageinfo)
            for det in details: 
                #print det.replace('&nbsp;','').encode('utf-8')
                
                det_0 = det[0].replace('&nbsp;','').encode('utf-8')   #项目名称，去掉空格
                det_1 = det[1].encode('utf-8')   #具项目体内容
                #确保具体内容不为空，如果为空，则为默认的(没写明)。
                if cmp('发布日期：',det_0) == 0 and cmp('',det_1) != 0 :
                    self.release_date =det[1].encode('utf-8')  
                if cmp('学历：',det_0) == 0 and cmp('',det_1) != 0 :
                    self.education = det[1].encode('utf-8')
                if cmp('工作地点：',det_0) == 0 and cmp('',det_1) != 0 :
                    self.workplace = det[1].encode('utf-8')
                if cmp('薪水范围：',det_0) == 0 and cmp('',det_1) != 0 :
                    self.salary = det[1].encode('utf-8')
                if cmp('招聘人数：',det_0) == 0 and cmp('',det_1) != 0 :
                    self.the_num_of_recuritment = det[1].encode('utf-8')
                if cmp('工作年限：',det_0) == 0 and cmp('',det_1) != 0 :
                    self.years_of_work = det[1].encode('utf-8')
                
            job_request = re.findall('<div style="padding-bottom:30px;">(.*?)</div>',pageinfo)
            
            #for job_req in job_request:
                #<P align=left>  <p style="MARGIN: 0cm 0cm 0pt">
                #f.writelines(job_req.replace('<br>','').replace('<div>','').encode('utf-8')+'\n\n\n')
            for job_req in job_request:
                r = re.compile('<.*?>')
                self.description = r.sub('',job_req)
            
	    self.job_course_set = db.get_one_job_course(self.description)   # 调用函数获取课程集合########
	    
	    print 'fucntion get_jobs done.'
                
        except urllib2.HTTPError,e:
            print 'Error code:',e.code
        except urllib2.URLError,e:
            print 'Reason:',e.reason
        except socket.timeout as e:
            return 0
        return 1
        #else:
        #    print 'No exception was raised.'
    
    def save_job_course_set_and_workplace(self):
        
        if re.search('-',self.workplace,re.I) != None:
            file_wplace = re.findall('(.*?)-',self.workplace)
	    file_wplace = file_wplace[0]
	    print 'if file_wplace =',file_wplace
        else:
            file_wplace = self.workplace
            print 'else file_wplace =',file_wplace
        
 #保存 地点 集合##############
        #fileName_part = "./save_analysis_result/course_result/"  #测试用的
        fileName_part = "./save_analysis_result/workplace_result/" 

        job_type_list =  ['IOS','Android','Python','Java','C\+\+','C#','.Net','测试','数据分析','数据库','架构师','人机交互','UI','游戏','网页设计','网站','安全','运维','Perl','Ruby','Hadoop','Node.Js','Php']
	for jtl in job_type_list:
            

            #print 'jtl =',jtl
            if re.search(jtl,self.position,re.I) != None:
                if cmp(jtl,'.Net') == 0 :
                    fileName_course = fileName_part + "Net" + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(file_wplace + '\n')
                    fnc.close()
                elif cmp(jtl,'Node.Js') == 0 :
                    fileName_course = fileName_part + "NodeJs" + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(file_wplace + '\n')
                    fnc.close()
                elif cmp(jtl,"C\+\+") == 0:
                    fileName_course = fileName_part + "C++" + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(file_wplace + '\n')
                    fnc.close()
                else:
                    fileName_course = fileName_part + jtl + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(file_wplace + '\n')
                    fnc.close()
        
        # 无论怎么样这个数据是要存到  全部岗位那里去的	
        fileName_course = fileName_part + "全部岗位" + ".txt"
        print fileName_course
        fnc = open(fileName_course,'a')
        fnc.write(file_wplace + '\n')
	print 'file_wplace ==============================',file_wplace
        fnc.close()


	fileName_part = "./save_analysis_result/apriori_course_result/" 

        job_type_list =  ['IOS','Android','Python','Java','C\+\+','C#','.Net','测试','数据分析','数据库','架构师','人机交互','UI','游戏','网页设计','网站','安全','运维','Perl','Ruby','Hadoop','Node.Js','Php']
	for jtl in job_type_list:
            #print 'jtl =',jtl
            if re.search(jtl,self.position,re.I) != None:
                if cmp(jtl,'.Net') == 0 :
                    fileName_course = fileName_part + "Net" + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(self.job_course_set + '\n')
                    fnc.close()
                elif cmp(jtl,'Node.Js') == 0 :
                    fileName_course = fileName_part + "NodeJs" + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(self.job_course_set + '\n')
                    fnc.close()
                elif cmp(jtl,"C\+\+") == 0:
                    fileName_course = fileName_part + "C++" + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(self.job_course_set + '\n')
                    fnc.close()
                else:
                    fileName_course = fileName_part + jtl + ".txt"
                    print fileName_course
                    fnc = open(fileName_course,'a')
                    fnc.write(self.job_course_set + '\n')
                    fnc.close()
        
        # 无论怎么样这个数据是要存到  全部岗位那里去的	
        fileName_course = fileName_part + "全部岗位" + ".txt"
        print fileName_course
	print 'self.job_course_set=',self.job_course_set
	print type(self.job_course_set)
        fnc = open(fileName_course,'a')
        fnc.write(self.job_course_set + '\n')
        fnc.close()

       



    def save_data(self):
        print "function save_data()..."
        '''
        print company
        print position
        print release_date
        print education
        print description
        print url
        '''
        try:
            conn = MySQLdb.connect (user='root',passwd='3288',host='127.0.0.1', port=3306,charset='utf8')
            cur = conn.cursor()
            conn.select_db('51job')
            #get the md5 of self.jobstr
            #self.mymd5.update(self.url)
            #self.job_md5 = self.mymd5.hexdigest()
            #print self.job_md5    
            sqlinsert = "insert into job_description (company,position,release_date,education,workplace,salary,years_of_work,the_num_of_recuritment,description,job_course_set,url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            job=(self.company,self.position,self.release_date,self.education,self.workplace,self.salary,self.years_of_work,self.the_num_of_recuritment,self.description,self.job_course_set,self.url)
            cur.execute(sqlinsert,job)
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "MySQLdb Error %d: %s" % (e.args[0], e.args[1])
       
		
	
	print 'self.company =',self.company
	print type(self.company.encode("utf-8"))
	print 'self.position =',self.position
	print type(self.position)
	print 'self.release-date =',self.release_date
	print type(self.release_date)
	print 'self.deucation =',self.education
	print type(self.education)
	print 'self.workplace =',self.workplace
	print type(self.workplace)
	print 'self.salary =',self.salary
	print type(self.salary)
	print 'self.years_of_work =',self.years_of_work
	print type(self.years_of_work)
	print 'self.the_num_of_recuritment =',self.the_num_of_recuritment
	print type(self.the_num_of_recuritment)
	print 'self.description =',self.description
	#jobInfo = unicode(self.company) + ',' + unicode(self.position) + ',' + unicode(self.release_date) + ',' + unicode(self.education) \
# + ',' + unicode(self.workplace) + ',\n' + unicode(self.salary) + ',' + unicode(self.years_of_work) + ',' + unicode(self.the_num_of_recuritment) \
# + ',\n' + unicode(self.description) + ',\n' #+ unicode(self.job_course_set) + '\n'
	jobInfo = self.company.encode('utf-8') + ',' + self.position + ',' + self.release_date + ',' + self.education \
 + ',' + self.workplace + ',\n' + self.salary + ',' + self.years_of_work + ',' + self.the_num_of_recuritment \
 + ',\n' + self.description + ',\n' #+ unicode(self.job_course_set) + '\n'
	
	#jobInfo = self.company.encode('utf-8') + ',' + self.position	
	jobInfo = unicode(jobInfo)	
	print 'jonInfo spider.py =*************',type(jobInfo)
	print "function save_data() done."
	return jobInfo
   

    
    #get self.jobstr
    def get_jobstr(self):
        return self.url
        #return self.jobstr
    
    
    def get_jobhref(self):
        return self.jobhref
    
    def get_first_jobhref(self,countPage = 10):
	self.url = self.the_part_of_next_page_url + str(countPage) + '.html'
	print "function get_first_jobhref()"        
        print 'first url = ' , self.url
	try:
            self.page = urllib2.urlopen(self.url).read().decode('gbk')
            self.jobhref = re.findall('<td class="td1"><a adid="".*?href="(.*?)"',self.page)
            print u'jobhreflength =',len(self.jobhref)
	    print "function get_first_jobhref() done."        
            return self.jobhref
	except urllib2.HTTPError,e:
            print 'Error code:',e.code
	    #return 'httpError'
            return 0
        except urllib2.URLError,e:
            print 'Reason:',e.reason
            return 0
	    #return 'Error code'
        except socket.timeout as e:
            print "first_get_jobhref() timeout! Again"
            return 0
        return ''

    def judge_is_connect_network(self,url= 'http://www.baidu.com'):
        print "function get_next_jobhref() start..."
     
        #get the url page        
        self.url = url
        #print "next_page url = ",self.url
        try:
            self.page = urllib2.urlopen(self.url).read()
       
            return self.page
	except urllib2.HTTPError,e:
            #print 'Error code:',e.code
	    return 0
        except urllib2.URLError,e:
            #print 'Reason:',e.reason
	    return 0
        except socket.timeout as e:
            #print "timeout! Again"
            return 0
        return 1

        """
        for h in next_jobhref:
            print "h==",h
            print "\n\n"
        print "end"
        """
	

if __name__ ==  '__main__':
    print "main"
    #js=jobSpider()
    #js.save_job_course_set_and_workplace()
    #js.get_jobs('http://search.51job.com/job/65144721,c.html')
    #js.save_data()
