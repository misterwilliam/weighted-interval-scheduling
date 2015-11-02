import unittest

from typing import List, Set


class Interval:

    def __init__(self, begin: float, end: float, weight: float):
        self.begin = begin
        self.end = end
        self.weight = weight

    def __eq__(self, other):
        return (
            self.begin == other.begin and self.end == other.end and
            self.weight == other.weight
        )

    def __str__(self):
        return "(%i, %i, %f)" % (self.begin, self.end, self.weight)

    def __repr__(self):
        return "Interval(%i, %i, %f)" % (self.begin, self.end, self.weight)


def GetFirstOverlappingIntervalIndex(intervals: List[Interval],
                                     withInterval: Interval) -> int:
    # Assumes |intervals| are sorted by end time
    cutoffTime = withInterval.begin
    i = 0
    while i < len(intervals):
        if intervals[i].end >= cutoffTime:
            return i
        i += 1
    else:
        return len(intervals)


def memoize(f):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            answer = f(*args)
            cache[args] = answer
            return answer
    return wrapper


def GetBestSchedule(intervals: List[Interval]) -> (float, List[Interval]):
    intervals.sort(key=lambda interval: interval.end)

    @memoize
    def RecursiveBodyByIndex(index) -> (float, List[int]):
        # Memoize converts from an exponential runtime to a polynomial because it is now
        # a dynamic programming based solution
        if index == -1:
            return (0, [])
        elif index == 0:
            return (intervals[index].weight, [0])
        else:
            lastInterval = intervals[index]
            firstOverlappingIndex = GetFirstOverlappingIntervalIndex(intervals,
                                                                     lastInterval)
            withoutLastIntervalScore, withoutLastIntervalSchedule = \
                RecursiveBodyByIndex(firstOverlappingIndex - 1)
            hasLastInterval = (withoutLastIntervalScore + lastInterval.weight,
                               withoutLastIntervalSchedule + [index])
            notHasLastInterval = RecursiveBodyByIndex(index - 1)
            return max(hasLastInterval, notHasLastInterval, key=lambda tuple: tuple[0])

    weight, indices = RecursiveBodyByIndex(len(intervals) - 1)
    return weight, [intervals[i] for i in indices]


class GetFirstOverlappingIntervalIndexTest(unittest.TestCase):

    def test_basic(self):
        data = [
            Interval(1, 3, 1.0),
            Interval(2, 6, 1.0),
            Interval(5, 10, 1.0)
        ]
        answer = GetFirstOverlappingIntervalIndex(data, Interval(5, 10, 1.0))
        self.assertEqual(answer, 1)

    def test_hitsEnd(self):
        data = [
            Interval(1, 3, 1.0),
            Interval(2, 6, 1.0),
            Interval(5, 7, 1.0)
        ]
        answer = GetFirstOverlappingIntervalIndex(data, Interval(8, 10, 1.0))
        self.assertEqual(answer, 3)


class MyTests(unittest.TestCase):

    def test_optimalInputReturnsInputSorted(self):
        data = [
            Interval(1, 2, 1.0),
            Interval(5, 6, 1.0),
            Interval(3, 4, 1.0),
        ]

        self.assertEqual(GetBestSchedule(data),
                         (3.0, [
                            Interval(1, 2, 1.0),
                            Interval(3, 4, 1.0),
                            Interval(5, 6, 1.0)
                          ]))

    def test_removesOverlappingInterval(self):
        data = [
            Interval(1, 4, 6.0),
            Interval(5, 6, 1.0),
            Interval(3, 4, 1.0),
        ]

        self.assertEqual(GetBestSchedule(data),
                         (7.0, [
                            Interval(1, 4, 6.0),
                            Interval(5, 6, 1.0)
                          ]))


if __name__ == '__main__':
    unittest.main()