"""
K-Means
"""
import random
from typing import Callable, Tuple

from pyske.core.interface import List
from pyske.core.list import SList
from pyske.core.util.point_2D import Point_2D


def cluster_index(point: Point_2D, centroids: SList[Point_2D]) -> Tuple[Point_2D, int]:
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


def assign_clusters(input_list: List[Point_2D], centroids: SList[Point_2D]) -> List[Tuple[Point_2D, int]]:
    """
    Assign each point to a cluster
    """
    return input_list.map(lambda x: cluster_index(x, centroids))


def update_centroids(clusters: List[Tuple[Point_2D, int]], centroids: SList[Point_2D]):
    """
    Update centroids of clusters
    """
    new_centroids = SList([])
    i = 0
    while i < len(centroids):
        cluster = clusters.filter(lambda x: x[1] == i)
        sum_cluster = cluster.map(lambda x: x[0]).reduce(lambda x, y: x + y)
        average_point = sum_cluster / cluster.length()
        centroid = clusters.reduce(
            lambda x, y: x if average_point.distance(x[0]) < average_point.distance(y[0]) else y)[0]
        new_centroids.append(centroid)
        i += 1
    return new_centroids


def max_dist(pair_a: Tuple[Point_2D, float], pair_b: Tuple[Point_2D, float]):
    """
    Return the tuple with the maximum distance
    """
    if pair_a[1] > pair_b[1]:
        return pair_a
    return pair_b


def k_means_init(input_list: List[Point_2D], n_cluster: int) -> SList[Point_2D]:
    """
    K-means++ initialisation

    :param input_list: a list of point
    :param n_cluster: number of cluster

    :return: n_cluster centroids
    """
    centroids = SList([])
    first_centroid = input_list.to_seq()[random.randint(0, input_list.length() - 1)]
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


def k_means(input_list: List[Point_2D], init_function: Callable[[List, int], List], n_cluster: int,
            max_iter: int = 10) -> SList[SList[Point_2D]]:
    """
    K-means algorithm on a list of point

    :param input_list: a list of point
    :param n_cluster: number of cluster
    :param max_iter: number of iteration
    :param init_function: a function that initialize centroids

    :return: 2 dimensions list of points
    """
    centroids = init_function(input_list, n_cluster)

    j = 0
    while j < max_iter:
        clusters = assign_clusters(input_list, centroids)

        centroids = update_centroids(clusters, centroids)

        j = j + 1

    clusters2d = SList([])
    for i in range(len(centroids)):
        clusters2d.append(clusters.filter(lambda x, num_cluster=i: x[1] == num_cluster)
                          .map(lambda x: x[0]).to_seq()
                          )
    return clusters2d
