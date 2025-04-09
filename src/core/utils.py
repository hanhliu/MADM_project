from enum import Enum

import numpy as np

class ItemType(Enum):
    REVIEWER = 0
    PAPER = 1

# Hàm tính Jaccard Similarity
def jaccard_similarity(set1, set2):
    # Chuyển danh sách thành tập hợp
    set1 = set(set1)
    set2 = set(set2)

    # Tính giao và hợp
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    # Tránh chia cho 0
    if union == 0:
        return 0.0

    # Tính Jaccard Similarity
    return intersection / union


# chuẩn hoá vector
def normalize_decision_matrix(matrix):
    matrix = np.array(matrix, dtype=float)
    column_squares = np.sum(np.square(matrix), axis=0)
    norm_matrix = matrix / np.sqrt(column_squares)
    return norm_matrix

def normalize_and_weight_matrix(matrix, weights):
    matrix = np.array(matrix, dtype=float)
    norm = np.sqrt(np.sum(matrix ** 2, axis=0))  # chuẩn hóa theo vector
    normalized_matrix = matrix / norm
    weighted_matrix = normalized_matrix * weights  # nhân trọng số
    return weighted_matrix
