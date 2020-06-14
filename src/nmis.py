#!/bin/env python3

from math import log

import numpy as np
import pandas as pd
from scipy import sparse as sp

from sklearn.utils.validation import check_array, check_consistent_length
from sklearn.utils.validation import _deprecate_positional_args
from sklearn.utils.fixes import _astype_copy_false


def check_clusterings(labels_true, labels_pred):

    labels_true = check_array(
        labels_true, ensure_2d=False, ensure_min_samples=0, dtype=None,
    )
    labels_pred = check_array(
        labels_pred, ensure_2d=False, ensure_min_samples=0, dtype=None,
    )

    # input checks
    if labels_true.ndim != 1:
        raise ValueError(
            "labels_true must be 1D: shape is %r" % (labels_true.shape,))
    if labels_pred.ndim != 1:
        raise ValueError(
            "labels_pred must be 1D: shape is %r" % (labels_pred.shape,))
    check_consistent_length(labels_true, labels_pred)

    return labels_true, labels_pred


@_deprecate_positional_args
def contingency_matrix(labels_true, labels_pred, *, eps=None, sparse=False):
    if eps is not None and sparse:
        raise ValueError("Cannot set 'eps' when sparse=True")

    # classes, class_idx = np.unique(labels_true, return_inverse=True)
    classes, class_idx = unique_inverse(labels_true)
    # clusters, cluster_idx = np.unique(labels_pred, return_inverse=True)
    clusters, cluster_idx = unique_inverse(labels_pred)
    n_classes = classes.shape[0]
    n_clusters = clusters.shape[0]
    # Using coo_matrix to accelerate simple histogram calculation,
    # i.e. bins are consecutive integers
    # Currently, coo_matrix is faster than histogram2d for simple cases
    contingency = sp.coo_matrix((np.ones(class_idx.shape[0]),
                                 (class_idx, cluster_idx)),
                                shape=(n_classes, n_clusters),
                                dtype=np.int)
    if sparse:
        contingency = contingency.tocsr()
        contingency.sum_duplicates()
    else:
        contingency = contingency.toarray()
        if eps is not None:
            # don't use += as contingency is integer
            contingency = contingency + eps
    return contingency


@_deprecate_positional_args
def mutual_info_score(labels_true, labels_pred, *, contingency=None):

    if contingency is None:
        labels_true, labels_pred = check_clusterings(labels_true, labels_pred)
        contingency = contingency_matrix(labels_true, labels_pred, sparse=True)
    else:
        contingency = check_array(contingency,
                                  accept_sparse=['csr', 'csc', 'coo'],
                                  dtype=[int, np.int32, np.int64])

    if isinstance(contingency, np.ndarray):
        # For an array
        nzx, nzy = np.nonzero(contingency)
        nz_val = contingency[nzx, nzy]
    elif sp.issparse(contingency):
        # For a sparse matrix
        nzx, nzy, nz_val = sp.find(contingency)
    else:
        raise ValueError("Unsupported type for 'contingency': %s" %
                         type(contingency))

    contingency_sum = contingency.sum()
    pi = np.ravel(contingency.sum(axis=1))
    pj = np.ravel(contingency.sum(axis=0))
    log_contingency_nm = np.log(nz_val)
    contingency_nm = nz_val / contingency_sum
    # Don't need to calculate the full outer product, just for non-zeroes
    outer = (pi.take(nzx).astype(np.int64, copy=False)
             * pj.take(nzy).astype(np.int64, copy=False))
    log_outer = -np.log(outer) + log(pi.sum()) + log(pj.sum())
    mi = (contingency_nm * (log_contingency_nm - log(contingency_sum)) +
          contingency_nm * log_outer)
    return np.clip(mi.sum(), 0.0, None)


def unique_inverse(labels):
    """
    custom function to utilize pandas unique()
    :param labels:
    :return:
    """
    pd_labels = np.sort(pd.unique(labels))
    unique_arr = np.arange(pd_labels.size)
    B = np.array((unique_arr, pd_labels)).T
    ell = {row[1]: row[0] for row in B}
    new_array = np.array([v for j in labels for k, v in ell.items() if j == k])

    return pd_labels, new_array


def entropy(labels):
    """Calculates the entropy for a labeling.
    Parameters
    ----------
    labels : int array, shape = [n_samples]
        The labels
    Notes
    -----
    The logarithm used is the natural logarithm (base-e).
    """
    if len(labels) == 0:
        return 1.0

    label_idx = np.unique(labels, return_index=True)[1]
    # pd_label_idx = unique_inverse(labels)[1]
    pi = np.bincount(label_idx).astype(np.float64)
    pi = pi[pi > 0]
    pi_sum = np.sum(pi)
    # log(a / b) should be calculated as log(a) - log(b) for
    # possible loss of precision
    return -np.sum((pi / pi_sum) * (np.log(pi) - log(pi_sum)))


def _generalized_average(U, V, average_method):
    """Return a particular mean of two numbers."""
    if average_method == "min":
        return min(U, V)
    elif average_method == "geometric":
        return np.sqrt(U * V)
    elif average_method == "arithmetic":
        return np.mean([U, V])
    elif average_method == "max":
        return max(U, V)
    else:
        raise ValueError("'average_method' must be 'min', 'geometric', "
                         "'arithmetic', or 'max'")


@_deprecate_positional_args
def normalized_mutual_info_score(labels_true, labels_pred, *,
                                 average_method='arithmetic'):

    labels_true, labels_pred = check_clusterings(labels_true, labels_pred)
    classes = unique_inverse(labels_true)[0]
    clusters = unique_inverse(labels_pred)[0]

    # Special limit cases: no clustering since the data is not split.
    # This is a perfect match hence return 1.0.
    if (classes.shape[0] == clusters.shape[0] == 1 or
            classes.shape[0] == clusters.shape[0] == 0):
        return 1.0
    contingency = contingency_matrix(labels_true, labels_pred, sparse=True)
    contingency = contingency.astype(np.float64,
                                     **_astype_copy_false(contingency))
    # Calculate the MI for the two clusterings
    mi = mutual_info_score(labels_true, labels_pred,
                           contingency=contingency)
    # Calculate the expected value for the mutual information
    # Calculate entropy for each labeling
    h_true, h_pred = entropy(labels_true), entropy(labels_pred)
    normalizer = _generalized_average(h_true, h_pred, average_method)
    # Avoid 0.0 / 0.0 when either entropy is zero.
    normalizer = max(normalizer, np.finfo('float64').eps)
    nmi = mi / normalizer
    return nmi
