import abc
import random


class LoadBalance(object):

    @abc.abstractmethod
    def get_slave(self, slave_mapper):
        raise NotImplementedError()


class FullRandom(LoadBalance):

    def get_slave(self, slave_mapper):
        con_list = list(slave_mapper.keys())
        return random.choice(con_list)


class WeightRandom(LoadBalance):

    def get_slave(self, slave_mapper):
        con_list = slave_mapper.keys()
        weight_list = [item["weight"] for item in slave_mapper.values()]
        v = []
        for con, weight in zip(con_list, weight_list):
            for _ in range(weight):
                v.append(con)
        return v[random.randint(0, len(v) - 1)]


class RoundRobin(LoadBalance):
    index = 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_slave(self, slave_mapper):
        if self.index >= len(slave_mapper):
            self.index = 0
        con_list = list(slave_mapper.keys())
        con = con_list[self.index]
        self.index = self.index + 1
        return con
