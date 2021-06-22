import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class Cluster:
    def cluster_tft_matches(self, 
                            df_clustering: pd.DataFrame,
                            df_read: pd.DataFrame,
                            start_time: datetime, 
                            end_time: datetime, 
                            i_period_win_rate: int):
        # ----------------------------------------------------
        #
        # Cluster data
        #
        # ----------------------------------------------------
        df_cluster = df_clustering

        df_cluster = StandardScaler().fit_transform(df_cluster)
        model = DBSCAN(eps=7.142, min_samples=30).fit(df_cluster)
        pca_fit = PCA(n_components=3).fit_transform(df_cluster)

        labels = model.labels_
        dbscan_n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        dbscan_n_noise_ = list(labels).count(-1)

        print('Estimated number of clusters: %d' % dbscan_n_clusters_)
        print('Estimated number of noise points: %d' % dbscan_n_noise_)

        count_cluster_labels = []
        unique, counts = np.unique(labels, return_counts=True)
        for u, c in zip(unique, counts):
            print('label ' + str(u) + ": " + str(c))
            count_cluster_labels.append(dict({'label': u, 'counts': c}))

        df_labeled = pd.DataFrame(pca_fit)
        df_labeled['label'] = pd.Series(labels, name='label')
        df_labeled[['id', 'match_id', 'placement', 'champions', 'traits']] = df_read[['id', 'match_id', 'placement', 'champions', 'traits']]
        df_labeled = df_labeled
        count_cluster_labels = count_cluster_labels
        return (df_labeled, count_cluster_labels)
        