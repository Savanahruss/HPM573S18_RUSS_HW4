from enum import Enum
import numpy as np
class CoinStatus(Enum):
    """
    outcome of the coin
    """
    HEADS = 1
    TAILS = 0

class Game(object):
    def __init__(self, id):
        self._flip = CoinStatus.HEADS
        self._id = id
        self._tailscount=0
        self._rnd=np.random
        self._rnd.seed(id)
        self._flip_num=1
        self._win_num= 0
        self._total_flips= 20

    def get_next_flip(self):
        if self._flip==CoinStatus.HEADS:
            if self._rnd.sample()>0.4:
                self._flip=CoinStatus.HEADS
            if self._rnd.sample()<0.5:
                self._flip=CoinStatus.TAILS
                self._tailscount=1

        elif self._flip==CoinStatus.TAILS:
            if self._rnd.sample()<0.5:
                self._flip=CoinStatus.TAILS
                self._tailscount+=1
            if self._rnd.sample()>0.4:
                self._flip=CoinStatus.HEADS
                if self._tailscount>=2:
                    self._win_num+=1
                self._tailscount+=1
        self._flip_num+=1


    def play_game(self):
        for i in range(1, self._total_flips+1):
            self._rnd.sample()
            self._rnd.seed(self._id*self._flip_num)
            self.get_next_flip()

    def get_reward(self):
        self.play_game()
        self._payout=-250+(100*self._win_num)
        return self._payout


class Cohort:
    def __init__(self, id, time_steps):
        self._time_steps= time_steps
        self._id=id
        self._players = []
        n=1
        while n <=time_steps:
            player = Game(id * time_steps + n)
            self._players.append(player)
            n +=1

    def simulate(self):
        totalwinnings = []
        for player in self._players:
            totalwinnings.append(player.get_reward())

        return sum(totalwinnings)/len(totalwinnings)

myCohort = Cohort(id=435, time_steps=1000)

print(myCohort.simulate())

#The average reward increase when the probability of heads is 0.4 to 65.3