"""
K-Means
"""
import random
from typing import Callable, Tuple
from pyske.core.interface import List
from pyske.core.list import SList
from pyske.core.util.point import Point


def cluster_index(point, centroids):
    """
    Get the centroid index of the closest centroid
    """
    min_dist = float("inf")
    p_centroid = centroids[0]
    for c in centroids:
        if point.distance(c) < min_dist:
            min_dist = point.distance(c)
            p_centroid = c
    return centroids.index(p_centroid)


def make_clusters(input_list, centroids):
    """
    Append all points to the cluster with the minimal distance from its centroid
    """
    clusters = [[] for c in centroids]
    for p in input_list.to_seq():
        index = cluster_index(p, centroids)
        clusters[index].append(p)
    return clusters


def coords_average(cluster):
    """
    Get the coordinates average of all points in one cluster
    """
    x_average = sum([p.x for p in cluster]) / len(cluster)
    y_average = sum([p.y for p in cluster]) / len(cluster)
    return Point(x_average, y_average)


def get_new_centroid(cluster):
    """
    Get closest point to average of point coordinates
    """
    average_point = coords_average(cluster)
    min_dist = float("inf")
    new_centroid = cluster[0]
    for p in cluster:
        if p.distance(average_point) < min_dist:
            min_dist = p.distance(average_point)
            new_centroid = p
    return new_centroid


def define_centroids(clusters):  # Pas utile car tuple ( num_cluster, point )
    """
    Redefine centroids of clusters
    """
    centroids = []
    for cluster in clusters:
        centroids.append(get_new_centroid(cluster))
    return centroids


def max_dist(pair_a: Tuple[Point, float], pair_b: Tuple[Point, float]):
    """
    Return the tuple with the maximum distance
    """
    if pair_a[1] > pair_b[1]:
        return pair_a
    else:
        return pair_b


def k_means_init(input_list: List, n_cluster: int):
    """
    K-means++ initialisation

    :param input_list: a list of point
    :param n_cluster: number of cluster

    :return: n_cluster centroids
    """
    centroids = SList([])
    c1 = input_list.to_seq()[random.randint(0, input_list.length() - 1)]
    centroids.append(c1)

    for _ in range(n_cluster - 1):
        dist = input_list.map(lambda x: x.distance(centroids[0]))
        for i in range(1, len(centroids)):
            temp_dist = input_list.map(lambda x, index=i: x.distance(centroids[index]))
            dist = dist.map2(lambda x, y: y if y < x else x, temp_dist)

        zip_list = input_list.zip(dist)
        next_centroid = zip_list.reduce(max_dist)[0]
        centroids.append(next_centroid)

    return centroids


def k_means(input_list: List, init_function: Callable[[List, int], List], n_cluster: int,
            max_iter: int = 10):
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
        clusters = make_clusters(input_list, centroids)  # assign_cluster
        centroids = define_centroids(clusters)  # update_centroids
        j = j + 1

    return clusters
