import unittest

from typing import List


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


def GetIntervalsBefore(intervals: List[Interval], beforeInterval: Interval):
    # Assumes |intervals| are sorted by end time
    cutoffTime = beforeInterval.begin
    retValue = []
    for interval in intervals:
        if interval.end < cutoffTime:
            retValue.append(interval)
        else:
            break
    return retValue


def GetBestSchedule(intervals: List[Interval]) -> (float, List[Interval]):
    def RecursiveBody(intervals: List[Interval]) -> (float, List[Interval]):
        if len(intervals) == 0:
            return (0.0, [])
        if len(intervals) == 1:
            return (intervals[0].weight, intervals)
        else:
            hasLastInterval = RecursiveBody(GetIntervalsBefore(intervals, intervals[-1]))
            hasLastInterval = (hasLastInterval[0] + intervals[-1].weight,
                               hasLastInterval[1] + [intervals[-1]])
            notHasLastInterval = RecursiveBody(intervals[:-1])
            return max(hasLastInterval, notHasLastInterval, key=lambda tuple: tuple[0])

    intervals.sort(key=lambda interval: interval.end)

    return RecursiveBody(intervals)


class GetIntervalsBeforeTest(unittest.TestCase):

    def test_basic(self):
        data = [
            Interval(1, 3, 1.0),
            Interval(2, 6, 1.0),
            Interval(5, 10, 1.0)
        ]
        answer = GetIntervalsBefore(data, Interval(5, 10, 1.0))
        self.assertEqual(answer, [Interval(1, 3, 1.0)])


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