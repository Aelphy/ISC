'''
As you know, every philosopher can be in one of two states: he either thinks or eats. And then one day the philosophers decided to get together to eat and think.

Legend has it that five silent philosophers sit around a round table, with a plate of spaghetti in front of each philosopher. Forks lie on the table between each pair of nearby philosophers. i.e., on the table there are 5 plates and 5 forks.
The problem is that the spaghetti is very slippery and you need two forks to hold it. Therefore, when each of the philosophers tries to eat, he also takes a fork lying
on the right, and a fork on the left.

If we move on to technical terminology, then philosophers are threads, and forks are some kind of shared limited resource.
The following situation is theoretically possible:
The streams are launched simultaneously, each "Philosopher" raises the right fork, there are no forks on the table and no one can take the left one.
Everyone puts back the right one. They are waiting. Then again, the right one is simultaneously raised and everything is repeated.

Thus, it is theoretically possible that all threads are completely deadlocked.
In practice, complete blocking occurs very rarely, because other programs are running in the system and the probability that all threads will do these actions synchronously is very small. But from the point of view of computer science, we are concerned about the fact that such a situation is theoretically possible. We need to fix this.
'''

from threading import Thread, Lock
import time
import random

class Fork:
    def __init__(self):
        self.m = Lock();

    def take(self):
        self.m.acquire()

    def put(self):
        self.m.release()


class Philosopher:
    def __init__(
            self,
            id: int,
            fork_left: Fork,
            fork_right: Fork,
            debug_flag: bool):
        self.id = id
        self.fork_left = fork_left
        self.fork_right = fork_right
        self.eat_count = 0
        self.wait_time = 0
        self.wait_start = 0
        self.stop_flag = False
        self.debug_flag = debug_flag

    def think(self):
        if self.debug_flag:
            print('{} thinking'.format(self.id))

            time.sleep(random.randint(0, 100) / 1000.)

            if self.debug_flag:
                print('{} hungry'.format(self.id))

            self.wait_start = time.time()

    def eat(self):
        self.wait_time += time.time() - self.wait_start
        if self.debug_flag:
            print('{} eating'.format(self.id))

        time.sleep(random.randint(0, 100) / 1000.)

        self.eat_count += 1

    def run(self):
        while not self.stop_flag:
            self.think()

            self.fork_left.take()
            if self.debug_flag:
                print('{} took left fork'.format(self.id))

            self.fork_right.take()
            if self.debug_flag:
                print('{} took right fork'.format(self.id))

            self.eat()

            self.fork_right.put();
            if self.debug_flag:
                print('{} put right fork'.format(self.id))

            self.fork_left.put();
            if self.debug_flag:
                print('{} put left fork'.format(self.id))

    def stop(self):
        self.stop_flag = True

    def print_stats(self):
        print('{} {} {}'.format(self.id, self.ea_count, self.wait_time))


def main():
    N = 5
    dbg = False
    duration = 60000
    forks = [Fork() for _ in range(N)]
    phils = [Philosopher(i + 1, forks[(i + 1) % N], forks[i], dbg) for i in range(N)]
    runners = [Thread(target=phils[i].run()) for i in range(N)]
    [runner.start() for runner in runners]
    time.sleep(duration / 1000.)
    [phil.stop() for phil in phils]
    [runner.join() for runner in runners]
    [phil.print_stats() for phil in phils]


if __name__ == '__main__':
    main()
