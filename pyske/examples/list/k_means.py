"""
K-Means
"""
import random
from typing import Callable, Tuple

from pyske.core.interface import List
from pyske.core.list import SList
from pyske.core.util.point_Interface import Point_Interface
from pyske.core.util.par import procs


def cluster_index(point: Point_Interface, centroids: SList[Point_Interface]) -> \
        Tuple[Point_Interface, int]:
    """
    Get the centroid index of the closest centroid
    """
    min_dist = float("inf")
    p_centroid = centroids[0]
    for centroid in centroids:
        if point.distance(centroid) < min_dist:
            min_dist = point.distance(centroid)
            p_centroid = centroid
    return point, centroids.index(p_centroid)


def assign_clusters(input_list: List[Point_Interface], centroids: SList[Point_Interface]) -> \
        List[Tuple[Point_Interface, int]]:
    """
    Assign each point to a cluster
    """
    return input_list.map(lambda x: cluster_index(x, centroids))


def update_centroids(clusters: List[Tuple[Point_Interface, int]],
                     centroids: SList[Point_Interface]):
    """
    Update centroids of clusters
    """

    def centroids_list_update(list_to_update, item):
        if isinstance(item, SList):
            list_to_update = list_to_update.map2(lambda a_pair, b_pair: (a_pair[0] + b_pair[0],
                                                                         a_pair[1] + b_pair[1]),
                                                 item)
        else:
            index = item[1]
            point = item[0]
            list_to_update[index] = (list_to_update[index][0] + point,
                                     list_to_update[index][1] + 1)
        return list_to_update

    point_class = type(centroids[0])
    neutral_list = SList.init(lambda _: (point_class(), 0), len(centroids))
    new_centroids = clusters.reduce(lambda a_item, b_item:
                                    centroids_list_update(a_item, b_item), neutral_list)
    new_centroids = new_centroids.map(lambda x: x[0] / x[1])

    return new_centroids


def max_dist(pair_a: Tuple[Point_Interface, float], pair_b: Tuple[Point_Interface, float]):
    """
    Return the tuple with the maximum distance
    """
    if pair_a[1] > pair_b[1]:
        return pair_a
    return pair_b


def k_means_init(input_list: List[Point_Interface], n_cluster: int) -> SList[Point_Interface]:
    """
    K-means++ initialisation

    :param input_list: a list of points
    :param n_cluster: number of clusters

    :return: list of centroids
    """
    centroids = SList([])
    first_centroid = input_list.get_partition() \
        .map(lambda l: l[random.randint(0, l.length() - 1)]) \
        .to_seq()[random.randint(0, list(procs())[len(list(procs())) - 1])]
    centroids.append(first_centroid)

    for _ in range(n_cluster - 1):
        dist = input_list.map(lambda x: x.distance(centroids[0]))
        for i in range(1, len(centroids)):
            temp_dist = input_list.map(lambda x, index=i: x.distance(centroids[index]))
            dist = dist.map2(lambda x, y: y if y < x else x, temp_dist)

        zip_list = input_list.zip(dist)
        next_centroid = zip_list.reduce(max_dist)[0]
        centroids.append(next_centroid)

    return centroids


def k_means(input_list: List[Point_Interface], init_function: Callable[[List, int], List],
            n_cluster: int,
            max_iter: int = 10) -> List[Tuple[Point_Interface, int]]:
    """
    K-means algorithm on a list of points

    :param input_list: a list of points
    :param n_cluster: number of clusters
    :param max_iter: number of iterations
    :param init_function: a function that initialize centroids

    :return: a list of tuples with the point and his cluster index
    """
    centroids = init_function(input_list, n_cluster)

    j = 0
    while j < max_iter:
        clusters = assign_clusters(input_list, centroids)

        centroids = update_centroids(clusters, centroids)

        j = j + 1

    return clusters
