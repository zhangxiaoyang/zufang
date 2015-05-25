#!/usr/bin/env python
# coding: utf-8

import Queue
import threading
import time
import datetime

class MultiTasker(object):
    
    def __init__(self, **args):
        self._in = Queue.Queue()
        self._callback = args['callback']
        self._threadnum = args['threadnum']
        self._outlimit = args['outlimit']
        self._threads = []
        for task in args['tasklist']:
            self._in.put(task)
        self._out = Queue.Queue()

    def _run(self):
        while True:
            if self._out.qsize() <= self._outlimit:
                try:
                    task = self._in.get(block=False)
                except:#task empty
                    break
                result = self._callback(task)
                self._out.put(result)
                self._in.task_done()
            else:
                pass
                #print 'full...'

    def run(self):
        if self._threadnum:
            for i in range(self._threadnum):
                self._threads.append(threading.Thread(target=self._run))
                self._threads[i].start()
            self._in.join()
        else:
            self._run()
        #self._print_result()

    def stop(self):
        for thread in self._threads:
            thread.stop()

    def _print_result(self):
        pass#print self._out.qsize()

if __name__ == '__main__':
    def callback(task):
        with open('tmp.'+str(task), 'w') as f:
            for i in range(1000):
                f.write('haha')
        return task
    
    for i in range(5):
        print '\nthreadnum = '+str(i)
        tasklist=range(10000)
        tasker = MultiTasker(
            tasklist=tasklist,
            callback=callback,
            outlimit=10000,
            threadnum=i
        )
        starttime = datetime.datetime.now()
        tasker.run()
        endtime = datetime.datetime.now()
        print 'done! %lds' % (endtime-starttime).seconds
