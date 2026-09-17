from abc import ABC, abstractmethod


class LiveTrainProvider(ABC):

    @abstractmethod
    def get_live_trains(self):
        pass

    @abstractmethod
    def get_train_live_position(self, train_number):
        pass