'''
Created on 22.08.2012

@author: APartilov
'''


class Constants:   # this class store initial data and constants

    class ConstError(TypeError):
        pass

    def __setitem__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError, "Can't unbind const(%s)" % name
        raise NameError + name

    def reset(self):
        self.__dict__.clear()


def timer(f):  # time benchmark
    from time import time

    def tmp(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print "Время выполнения функции: %f" % (time() - t)
        return res
    return tmp