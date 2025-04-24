__all__ = ["ClusterFetcherMixin"]
from tortoise import Model
from tortoise.queryset import QuerySet

from math import ceil


class ClusterFetcherMixin:
    """
    A mixin class that provides functionality for fetching data in clusters.
    
    This mixin is designed to work with Tortoise ORM models and provides a method
    to fetch a specific cluster of items from a queryset along with the total count
    of available clusters.
    """

    @staticmethod
    async def _get_cluster_of_items_and_count_of_clusters(data: QuerySet[Model], cluster_index: int,
                                                          cluster_size: int) -> tuple[tuple[Model, ...], int]:
        """Fetches a specific cluster of items from a queryset and calculates the total number of clusters.

        :param data: The queryset to fetch items from
        :param cluster_index: The index of the cluster to fetch (0-based)
        :param cluster_size: The number of items in each cluster
        :return: Tuple containing the cluster of models and the total count of clusters
        """
        cluster: list[Model] = await data.offset(cluster_size * cluster_index).limit(cluster_size)
        count_of_clusters: int = ceil(await data.count() / cluster_size)
        return tuple(cluster), count_of_clusters
