from __future__ import division
import itertools

range_x = 1000
repeat_times = 40


class data_point():
    newid = itertools.count().next

    def __init__(self, decisions=[], objectives=[]):
        self.id = data_point.newid()
        self.decisions = decisions
        self.objectives = objectives

    def euclidean_distance(self, list2):
        assert(len(self.decisions) == len(list2)), "The points don't have the same dimension"
        distance = sum([(i - j) ** 2 for i, j in zip(self.decisions, list2)]) ** 0.5
        assert(distance >= 0), "Distance can't be less than 0"
        return distance

    def distance(self, point):
        return self.euclidean_distance(point.decisions)

    def update_point(self, point):
        temp = []
        for i, j in zip(self.decisions, point.decisions): temp.append((i+j)/2)
        self.decisions = list(temp)
        assert(len(self.decisions) == len(point.decisions)), "Something is wrong"


def find_closest_point(point, points):
    distances = []
    for ps in points:
        if point.id == ps.id: pass
        else: distances.append([ps, point.euclidean_distance(ps.decisions)])
    sorted_list = sorted(distances, key=lambda x: x[-1])
    i = 0
    while i < len(points)-2 and sorted_list[i][1] < range_x/100 and sorted_list[i+1][1] < range_x/10: i += 1
    return sorted_list[i][0]


def draw_graph(points, count):
    import matplotlib.pyplot as plt
    x = [p.decisions[0] for p in points]
    y = [p.decisions[1] for p in points]

    # adding area into it
    set_values_dict = {}
    for xx, yy in zip(x, y):
        key = int(xx)*range_x + int(yy)
        if key not in set_values_dict.keys(): set_values_dict[int(xx)*range_x + int(yy)] = 1
        else: set_values_dict[int(xx)*range_x + int(yy)] += 1


    # new x, y, area
    x = []
    y = []
    area = []
    for key in set_values_dict.keys():
        x.append(key/range_x)
        y.append(key%range_x)
        area.append(3.14 * set_values_dict[key]**2)

    plt.scatter(x, y, s=area)
    plt.xlim(0, range_x)
    plt.ylim(0, range_x)
    plt.title(str(count))
    plt.savefig("./1_output_images/" +str(count) + ".png")
    # if count == 0: plt.savefig("initial.png")
    # elif count == repeat_times: plt.savefig("final.png")
    # plt.show()
    # print


def experiment(number_of_points, number_of_decisions):
    from random import randrange
    from sys import stdout
    points = [data_point([randrange(1, range_x) for _ in xrange(number_of_decisions)]) for _ in xrange(number_of_points)]
    for count in xrange(repeat_times+1):
        print ".",
        stdout.flush()
        for ps in points:
            nearest_point = find_closest_point(ps, points)
            ps.update_point(nearest_point)

        draw_graph(points, count)
        if count % 20 == 0: print


if __name__ == "__main__": experiment(200, 2)