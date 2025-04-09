__all__ = ["ClusterFetcherMixin"]
from tortoise import Model
from tortoise.queryset import QuerySet

from math import ceil


class ClusterFetcherMixin:

    @staticmethod
    async def _get_cluster_of_items_and_count_of_clusters(data: QuerySet[Model], cluster_index: int,
                                                          cluster_size: int) -> tuple[tuple[Model, ...], int]:
        cluster: list[Model]= await data.offset(cluster_size * cluster_index).limit(cluster_size)
        count_of_clusters: int = ceil(await data.count() / cluster_size)
        return tuple(cluster), count_of_clusters
