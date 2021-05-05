"""
K-Means
"""

from pyske.core.interface import List
from pyske.core.list import SList
import random
import matplotlib.pyplot as plt
from pyske.core.util.point import Point


def cluster_index(p, centroids):
    """
    Get the centroid index of the closest centroid
    """
    min_dist = float("inf")
    p_centroid = centroids[0]
    for c in centroids:
        if p.distance(c) < min_dist:
            min_dist = p.distance(c)
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


def define_centroids(clusters):
    """
    Redefine centroids of clusters
    """
    centroids = []
    for cluster in clusters:
        centroids.append(get_new_centroid(cluster))
    return centroids


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

    for c in range(n_cluster - 1):
        dist = input_list.map(lambda x: x.distance(centroids[0]))
        for i in range(1, len(centroids)):
            temp_dist = input_list.map(lambda x: x.distance(centroids[i]))
            dist = dist.map2(lambda x, y: min(x, y), temp_dist)

        index_max = [i for i, x in enumerate(dist.to_seq()) if x == max(dist.to_seq())]
        next_centroid = input_list.to_seq()[index_max[0]]
        centroids.append(next_centroid)

    return centroids


def k_means(input_list: List, n_cluster: int, max_iter: int = 10):
    """
    K-means algorithm on a list of point

    :param input_list: a list of point
    :param n_cluster: number of cluster
    :param max_iter: number of iteration

    :return: a list of class
    """
    centroids = k_means_init(input_list, n_cluster)
    j = 0
    while j < max_iter:
        clusters = make_clusters(input_list, centroids)
        plt.scatter([point.x for point in input_list.to_seq()], [point.y for point in input_list.to_seq()],
                    c='yellow')
        clusters_color = ['green', 'blue', 'black', 'purple', 'brown']
        for i in range(len(clusters)):
            plt.scatter([point.x for point in clusters[i]], [point.y for point in clusters[i]],
                        c=clusters_color[i])

        centroids = define_centroids(clusters)
        plt.scatter([point.x for point in centroids], [point.y for point in centroids], c='red')
        plt.show()
        j = j + 1

    return clusters
