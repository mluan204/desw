import pandas as pd
import numpy as np
import os
from datetime import datetime
import glob

def calculate_gini_coefficient(df, col='tokens'):
    """
    Tính Gini coefficient theo công thức đúng với Lorenz curve
    
    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu
        col (str): Tên cột chứa stake values
    
    Returns:
        float: Chỉ số Gini (0 = hoàn toàn bình đẳng, 1 = hoàn toàn bất bình đẳng)
    """
    # Đảm bảo dữ liệu là mảng numpy để tối ưu hiệu suất
    weights = df[col].to_numpy()

    # Sắp xếp các giá trị
    weights_sorted = np.sort(weights)

    # Tính tổng tích lũy của tokens và số lượng validators tích lũy
    cum_weights = np.cumsum(weights_sorted, dtype=float)
    total_weight = cum_weights[-1]

    # Đường cong Lorenz là tổng tích lũy của tokens chia cho tổng số tokens
    lorenz_curve = cum_weights / total_weight

    # Diện tích dưới đường cong Lorenz
    B = np.trapz(lorenz_curve, dx=1/len(weights))

    # Hệ số Gini sử dụng công thức G = 1 - 2B
    gini_coefficient = 1 - 2 * B
    
    return gini_coefficient

def calculate_nakamoto_coefficient(df, col='tokens'):
    """
    Tính Nakamoto coefficient - số lượng validators tối thiểu cần thiết để kiểm soát > 50% stake
    
    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu
        col (str): Tên cột chứa stake values
    
    Returns:
        int: Số lượng validators cần thiết để đạt > 50% tổng stake
    """
    tokens = df[col].to_numpy()
    tokens_sorted = np.sort(tokens)[::-1]  # Sắp xếp giảm dần
    
    total_stake = np.sum(tokens_sorted)
    threshold = total_stake / 2
    
    cumulative_stake = 0
    for i, stake in enumerate(tokens_sorted):
        cumulative_stake += stake
        if cumulative_stake > threshold:
            return i + 1
    
    return len(tokens_sorted)

def calculate_hhi_coefficient(df, col='tokens', normalize=False):
    """
    Tính HHI coefficient (Herfindahl-Hirschman Index) - đo mức độ tập trung thị trường
    
    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu
        col (str): Tên cột chứa stake values
        normalize (bool): Có chuẩn hóa HHI theo số lượng validator hay không
    
    Returns:
        float: Chỉ số HHI (0 = hoàn toàn phân tán, 1 = hoàn toàn tập trung)
    """
    # Xử lý giá trị NaN và giá trị <= 0
    weights = df[col].fillna(0).to_numpy()
    weights = weights[weights > 0]

    total_weight = weights.sum()
    if total_weight == 0:
        return 0.0

    market_shares = weights / total_weight
    hhi_index = np.sum(market_shares ** 2)

    if normalize and len(weights) > 1:
        n = len(weights)
        hhi_index = (hhi_index - 1/n) / (1 - 1/n)
    
    return hhi_index
