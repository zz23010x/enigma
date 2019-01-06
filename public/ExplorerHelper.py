import multiprocessing
from multiprocessing import Pool, Manager, Lock
# r = requests.get('https://fe-api.zhaopin.com/c/i/sou', params=params)
# res = r.json()['data']['results']
# tasks = []
# result = []
# num = 1
# for item in res:
#     tasks.append((item, num))
#     num += 1

def aaa(item, num):
    a = Job()
    a.InitJobInfo(item)
    # print(num, a.positionURL)
    # sd.append(a)
    return a

def bbb(job):
    print(job.jobName, job.positionURL)
    result.append(job)

class ProcessManager:
    def __init__(self):
        self.__proMaximum = 40
        self.lock = Lock()

    def configProcess(self, funcName, funcArgs, cbfuncName=None, threadNumber=None):
        self.funcName = funcName
        self.funcArgs = funcArgs
        if threadNumber is None or threadNumber > self.__proMaximum:
            self.number = self.__proMaximum
        else:
            self.number = threadNumber
        self.cbfuncName = cbfuncName
        
    def startProcess(self):
        pool = Pool(processes=self.number)
        for args in self.funcArgs:
            pool.apply_async(self.funcName, args=args, callback=self.cbfuncName)
        pool.close()
        pool.join()

    def startProcessWithRes(self):
        with Manager() as pmer:
            result = pmer.list()
            pool = Pool(processes=self.number)
            for args in self.funcArgs:
                pool.apply_async(self.funcName, args=(result,) + args, callback=self.cbfuncName)
            pool.close()
            pool.join()
            return list(result)

if __name__ == '__main__':
    p1 = ProcessManager()
    p1.configProcess(aaa, tasks, cbfuncName=bbb, threadNumber=30)
    ap = p1.startProcess()