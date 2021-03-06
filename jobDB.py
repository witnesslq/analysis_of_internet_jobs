#-*- coding:utf-8 -*-
'''
job database of execute and query sql
'''
import re
import MySQLdb
from bloomFilter import bloomfilter

class jobDB():
    def __init__(self):
        try:
            self.conn = MySQLdb.connect (user='root',passwd='3288',host='127.0.0.1', port=3306,charset='utf8')
            self.cur = self.conn.cursor()
            self.conn.select_db('51job')
        except MySQLdb.Error,e:
            print "MySQLdb Error %d: %s" % (e.args[0], e.args[1])
    
        self.fsw = file

    def queryDescription(self,i = 1):   #import jobs' detail
        sql_description = "select description from job_description where job_id = %d" % i
        sql_url = "select url from job_description where job_id = %d" % i
        description_result = self.cur.execute(sql_description)
        des = self.cur.fetchone()
        self.conn.commit()
        url_result = self.cur.execute(sql_url)
        url = self.cur.fetchone()
        self.conn.commit()
        return url,des 
    #这个函数是查询表job_description中的数据导入岗位基本信息表格中   
    def query_job_details(self):
        sql = "select company,position,release_date,education,workplace,salary,years_of_work,the_num_of_recuritment,description,url from job_description"
        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        return res
    
    #这个函数是按照 岗位名称 来查询表job_description中的数据导入岗位基本信息表格中   
    def query_job_details_by_position(self,position):
        sql = "select company,position,release_date,education,workplace,salary,years_of_work,the_num_of_recuritment,description,url from job_description where position like " + "\"%"+ position + "%\"" 
        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        return res

    #这个函数是按 公司名称 照来查询表job_description中的数据导入岗位基本信息表格中   
    def query_job_details_by_company(self,company):
        sql = "select company,position,release_date,education,workplace,salary,years_of_work,the_num_of_recuritment,description,url from job_description where company like " + "\"%"+ company + "%\"" 
        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        return res

    #这个函数是按 岗位地点 来查询表job_description中的数据导入岗位基本信息表格中   
    def query_job_details_by_workplace(self,workplace):
        sql = "select company,position,release_date,education,workplace,salary,years_of_work,the_num_of_recuritment,description,url from job_description where workplace like " + "\"%"+ workplace + "%\"" 
        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        return res

    # 把课程名插入课程表中
    def insertCourse(self,course):    #import course
        sql = "insert into courses(course_name) values(%s)"
        self.cur.execute(sql,course)
        self.conn.commit()
    
    # 获得课程名称，用来做正则表达式，匹配出想要的课程
    def queryCourses(self):
        sql = "select course_name from courses "
        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        return res

    #建立表
    def create_courses(self):
        drop_sql = "DROP TABLE IF EXISTS courses"
        self.cur.execute(drop_sql)
        self.conn.commit()
        create_sql = "CREATE TABLE IF NOT EXISTS courses (\
                course_id int(20) NOT NULL PRIMARY KEY AUTO_INCREMENT,\
                course_name varchar(30) NOT NULL\
                ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';"
        self.cur.execute(create_sql)
        self.conn.commit()
    
    #这个函数用于爬虫爬取数据用的，一边爬数据，一边分析
    def get_one_job_course(self,description = ''):  
        if cmp(str(type(description)),"<type 'NoneType'>") != 0 :
            #print 'res=',result[0].encode('utf-8')
            bf_remain = bloomfilter.BloomFilter('./bloomFilter/singleCourseHash.txt',True)  #过滤多余的,True的话是会把这个文件清空，默认False
            des =description.encode('utf-8')
            course_file = open('courses/courses.txt','r+')
            #print type(des)
            #print 'des=',des
            courses = course_file.readlines()
            course_set = ''
            for cou in courses:
                #print cou.strip('\n')
                job_course1 = re.findall('(.*?)=',cou.strip('\n'))
                #if re.search(job_course1[0],des) != None:
                #new_courese1=r'[\u4e00-\u9fa5]' + job_course1[0] + r'[^a-zA-Z+]'
                new_courese1 = job_course1[0] + r'[^a-zA-Z+]'
                #if re.search(job_course1[0],des,re.I) != None:
                #print 'new_courese1=',new_courese1
                if re.search(new_courese1,des,re.I) != None:
                    #print cou.strip('\n')
                    #print 'jc[0]=',job_course1[0]
                    job_course2 = re.findall('=(.*?)$',cou.strip('\n'))
                    if bf_remain.isContaions(job_course2[0]) == False:
                        bf_remain.insert(job_course2[0])
                        course_set = course_set + ',' + job_course2[0]
                        #print 'course=',job_course2[0]
            r = re.compile(',')
            course_set = r.sub('',course_set,1) #利用正则表达式把第一个逗号去掉
            
            #jobCourseFile = open(fileName,'r+')  #打开文件
            #if count == 1:
            #    jobCourseFile.truncate()            #把文件清空
            #print 'fileNmae =',jobCourseFile
            #print 'course_set =',course_set
            

	    if cmp(course_set,'') != 0:
                #print 'des =',description
                #print 'course_set =',course_set
                return course_set
                    
        
            else:
                print 'no result'
                return	    

	res = ''        #return course_set
	return res 

    #这个函数可能以后用不到
    def get_all_course(self):
        
        sql = "select job_id,description from job_description"
        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        count = 0 
        for job_id,description in res:
            #count =count + 1
            #print 'count =',count
            print 'job_id =',job_id
            #print description
            #print type(job_id)
            #print type(description)
            if cmp(str(type(description)),"<type 'NoneType'>") != 0 :
                #print 'res=',result[0].encode('utf-8')
                bf_remain = bloomfilter.BloomFilter('./bloomFilter/singleCourseHash.txt',True)  #过滤多余的
                des =description.encode('utf-8')
                course_file = open('courses/courses.txt','r+')
                #print type(des)
                #print 'des=',des
                courses = course_file.readlines()
                course_set = ''
                for cou in courses:
                    #print cou.strip('\n')
                    job_course1 = re.findall('(.*?)=',cou.strip('\n'))
                    #if re.search(job_course1[0],des) != None:
                    #new_courese1=r'[\u4e00-\u9fa5]' + job_course1[0] + r'[^a-zA-Z+]'
                    new_courese1 = job_course1[0] + r'[^a-zA-Z+]'
                    #if re.search(job_course1[0],des,re.I) != None:
                    #print 'new_courese1=',new_courese1
                    if re.search(new_courese1,des,re.I) != None:
                        #print cou.strip('\n')
                        #print 'jc[0]=',job_course1[0]
                        job_course2 = re.findall('=(.*?)$',cou.strip('\n'))
                        if bf_remain.isContaions(job_course2[0]) == False:
                            bf_remain.insert(job_course2[0])
                            course_set = course_set + ',' + job_course2[0]
                            #print 'course=',job_course2[0]
                r = re.compile(',')
                course_set = r.sub('',course_set,1) #利用正则表达式把第一个逗号去掉
                
                #jobCourseFile = open(fileName,'r+')  #打开文件
                #if count == 1:
                #    jobCourseFile.truncate()            #把文件清空
                #print 'fileNmae =',jobCourseFile
                #print 'course_set =',course_set
                if cmp(course_set,'') != 0:
                    print 'des =',description
                    print 'course_set =',course_set
                    sql = 'update job_description set job_course_set = "%s" where job_id =%d' % (course_set,job_id)
                    self.cur.execute(sql)
                    self.conn.commit()
                    #self.insert_to_course_set(job_id,course_set)
                    #sql = "insert into job_description(job_course_set) values (%s) where job_id = %d" #% (%s,%d)
                    #print 'sql =',sql
                    #info =  (course_set,job_id)
                    ##self.cur.execute(sql)
                    #self.cur.execute(sql,info)
                    #self.conn.commit()
                #return course_set
            else:
                print 'no result'
                return

    # 把每个工作的描述转成课程 ，可能以后用不到   
    def insert_to_course_set(self,job_id,job_course_set):
        print 'insert job_id =',job_id
        print 'insert job_course_set =',job_course_set
        print type(int(job_id)),type(job_course_set)
        sql = 'update job_description set job_course_set = "%s" where job_id =%d' % (job_course_set,job_id)
        self.cur.execute(sql)
        self.conn.commit()

	
    def get_course_from_description(self,description = '',fileName = '',count = 1):
        bf_remain = bloomfilter.BloomFilter('./bloomFilter/singleCourseHash.txt',True)  #过滤多余的
        if cmp(str(type(description)),"<type 'NoneType'>") != 0:
            #print 'res=',result[0].encode('utf-8')
            des =description.encode('utf-8')
            course_file = open('courses/courses.txt','r+')
            #print type(des)
            #print 'des=',des
            courses = course_file.readlines()
            course_set = ''
            for cou in courses:
                #print cou.strip('\n')
                job_course1 = re.findall('(.*?)=',cou.strip('\n'))
                #if re.search(job_course1[0],des) != None:
                #new_courese1=r'[\u4e00-\u9fa5]' + job_course1[0] + r'[^a-zA-Z+]'
                new_courese1 = job_course1[0] + r'[^a-zA-Z+]'
                #if re.search(job_course1[0],des,re.I) != None:
                #print 'new_courese1=',new_courese1
                if re.search(new_courese1,des,re.I) != None:
                    #print cou.strip('\n')
                    #print 'jc[0]=',job_course1[0]
                    job_course2 = re.findall('=(.*?)$',cou.strip('\n'))
                    if bf_remain.isContaions(job_course2[0]) == False:
                        bf_remain.insert(job_course2[0])
                        course_set = course_set + ',' + job_course2[0]
                        #print 'course=',job_course2[0]
            r = re.compile(',')
            course_set = r.sub('',course_set,1) #利用正则表达式把第一个逗号去掉
            
            #jobCourseFile = open(fileName,'r+')  #打开文件
            #if count == 1:
            #    jobCourseFile.truncate()            #把文件清空
            #print 'fileNmae =',jobCourseFile
            #print 'course_set =',course_set
            if cmp(course_set,'') != 0:
                self.fsw.write(course_set + '\n')
            #return course_set
        else:
            print 'no result'
            return

    #得出工作发布的地点，主要以城市名为主。如：上海-浦东，则只是选择上海而已。保存到workplace.txt文件中去
    def get_job_workplace_by_condition(self,condition = '',fileName = ''):
        sql = "select workplace from job_description  where position like " + "\"%"+ condition + "%\""

        result = self.cur.execute(sql)
        res = self.cur.fetchall()
        self.conn.commit()
        
        fwp = open(fileName,'r+')
        fwp.truncate()
        for r in res:
            #fwp.write(r[0].encode('utf-8') + '\n')
            if re.search('-',r[0],re.I) != None:
                workplace = re.findall('(.*?)-',r[0])
                print 'workplace=',workplace[0]
                fwp.write(workplace[0].encode('utf-8') + '\n')
            else:
                fwp.write(r[0].encode('utf-8') + '\n')

        fwp.close()

    def get_job_course_by_position(self,condition = '',fileName = ''):
        sql = "select job_course_set from job_description where position like " + "\"%"+ condition + "%\"" 
        #print 'contiton 1',condition
        #print 'fileName 1',fileName
        fsw =  open(fileName,'r+')
        fsw.truncate()
        result = self.cur.execute(sql)
        course_set_result = self.cur.fetchall()
        self.conn.commit()
        count = 0
        for cs in course_set_result:
            #count = count + 1
            #print 'count =',count
            if cmp(str(type(cs[0])),"<type 'NoneType'>") != 0:
                fsw.write(cs[0].encode('utf-8') + '\n')
    #存储关联分析结果到表 apriori_all_result中     #存储到数据库很慢  可以考虑去了
    def save_to_apriori_all_result(self,support,confidence,apriori_x,apriori_y):
        sql = "insert into apriori_all_result(support,confidence,apriori_x,apriori_y) values (%s,%s,%s,%s)"
        info = 	(support,confidence,apriori_x,apriori_y)
        self.cur.execute(sql,info)
        self.conn.commit()

    def __del__(self):  #析构函数 
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    db = jobDB()
    #db.get_all_course()
    db.get_job_course_by_position('java','./save_analysis_result/apriori_course_result/Java.txt')
    #db.get_job_workplace_by_condition('','./save_analysis_result/workplace_result/全部岗位.txt')
    #db.get_job_course_by_condition('Python','./save_analysis_result/course_result/Python.txt')
    #url,description= db.queryDescription(9)
    #print type(url)
    #print type(description)
    #db.create_courses()
    print '------------------------------'
    print '------------------------------'


    #url = url[0].encode('utf-8')
    #print 'ulr=',url
    #db.insert_description_to_curses(url,course_set)

##################
    #jobSet=db.query_job_by_condition("%java%")
    #print type(jobSet)
    #countJob = 0
    #for job in jobSet:
    #    countJob = countJob + 1
    #    print 'countJob=',countJob
    #    description = job[0]
    #    db.get_course_from_description(description)
    #    #print 'couSet =',courseSet
    #print 'countJob=',countJob
#################



    #db.get_job_workplace()
    #res = db.query_job_details()
    #for r in res:
    #    for detail in r:
    #        print detail
    print 'Done.'


