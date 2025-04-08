
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