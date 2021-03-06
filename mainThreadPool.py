# !/usr/bin/env python
# -*- coding:utf-8 -*-
import spider
import workManager

class mainThreadPool():
    def __init__(self):
        self.jobhref_spider = spider.jobSpider()
        self.countThread = 1   # count the number Thread
        self.countPage = 20     #cout the number of page
        self.myHref = 0   # judge 'myHref' is none or not
        self.countJob= 1
        self.countAddJob = 2
        self.myThreadPool = workManager.WorkManager(200,5)

    def startCrawlerJob(self):
        while self.myHref == 0:   #myHref =0 表明获取jobhref 失败 或者第一次获取urls
            self.myHref = self.jobhref_spider.get_first_jobhref(self.countPage)
            print 'countPage = 失败 1' ,self.countPage
        self.countPage += 1
        for href in self.myHref:    #把url加入到任务队列中
            self.myThreadPool.my__init_work_queue(href,self.countJob)   #
            self.countThread += 1
            self.countJob += 1
	hello = 'hello'
        hello= self.myThreadPool.my__init_thread_pool()
	print 'hell0 =',hello
        #self.always_get_url()
    
        print 'start'
        while True:
            #print type(myThreadPool.check_queue())
            while self.myThreadPool.check_queue() >=0 and self.myThreadPool.check_queue() <= 100:
                print 'myThreadPool.check_queue() ' , self.myThreadPool.check_queue() 
                self.countAddJob += 1
                print 'countJob = ' , self.countJob
                self.myHref = 0
                while self.myHref == 0: 
                    self.myHref = self.jobhref_spider.get_first_jobhref(self.countPage)
                    if self.myHref != 0:
                        print 'countPage = 失败 2' ,self.countPage
                self.countPage += 1	
                for href in self.myHref:     #把url加入到任务队列中
                    self.myThreadPool.my__init_work_queue(href,self.countJob)
                    self.countJob += 1

                self.countThread += 1
                """
                while myThreadPool.check_queue() != 50:
                    myThreadPool.my__init_work_queue(str(countThread))
                    countThread += 1
                """
if __name__ == "__main__":
    mspider = mainThreadPool()
    mspider.startCrawlerJob()
