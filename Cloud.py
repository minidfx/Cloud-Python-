from abc import ABCMeta, abstractmethod


class Cloud(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.driver = None
        self.activeNodes = []

    @abstractmethod
    def create(self):
        raise Exception('Not implemented')

    @abstractmethod
    def destroy(self):
        raise Exception('Not implemented')
