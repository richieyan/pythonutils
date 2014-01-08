# -*- coding: utf-8 -*-

import Queue, threading, sys
from threading import Thread
import urllib
import time


url = 'http://www.baidu.com'

def test_job(query):
    data = urllib.urlencode({'query':hello})
    result = None
    try:
        result = fetch(url,data)
        result = result.strip()
    except:
        print 'error',sys.exc_info()
        result = uids
    return result

def fetch(url,data):
    rt = urllib.urlopen(url,data)
    content = rt.read()
    rt.close()
    return content

process_count = 0

#working thread
class Worker(Thread):
    worker_count = 0
    def __init__(self,workQueue,resultQueue,timeout = 0, **kwds):
        Thread.__init__(self,**kwds)
        Worker.worker_count  = Worker.worker_count + 1;
        self.id = Worker.worker_count
        self.process_count = 0;
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()


    def run(self):
        ''' the get-some-work, do-some-work main loop of worker threads '''
        while True:
            try:
                print 'start worker',self.id
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args,**kwds)
                self.process_count  = self.process_count + 1;
                if self.process_count % 100 == 0:
                    print 'worker',self.id,'process_count:' + str(self.process_count)
                log(res)
            except Queue.Empty:
                break
            except :
                print 'worker[%2d]'%self.id,sys.exc_info()[:2]


class WorkerManager:
    def __init__(self, num_of_workers = 10, timeout = 1):
        self.workQueue = Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads( num_of_workers )

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)
    
    def wait_for_complete(self):
        #... then, wait for each of them to terminate
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)

    def add_job(self,callable, *args, **kwds):
        self.workQueue.put((callable,args,kwds))
        
    def get_result(self,*args,**kwds):
        return self.resultQueue.get(*args,**kwds)


def do_job():
    wm = WorkerManager(100)
    query_list = ['1','2','3','1','2','3']
    queue = []
    for query in query_list:
        wm.add_job(test_job,query)
    wm.wait_for_complete()
    
if __name__ == '__main__':
    do_job()
    # os.listdir, sys.argv[1]
    