#!/usr/bin/env python3
"""
LOG_WEIGHTED PoS Experiment
Thí nghiệm với thuật toán LOG_WEIGHTED Proof-of-Stake
"""

import sys
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import json

# Thêm src và experiments vào path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parameters import Parameters, PoS, Distribution, NewEntry
from simulator import simulate
from utils import generate_peers, gini, HHI_coefficient
from experiment_utils import save_results_to_json, create_and_save_plot, print_experiment_results, get_experiment_config, get_scheduled_joins


# THIẾT LẬP LỊCH JOIN - Sửa trực tiếp ở đây
# Ví dụ: [(5000, 50000), (10000, 30000)] -> Epoch 5000 có validator join với 50k stake, epoch 10000 có validator join với 30k stake
SCHEDULED_JOINS = [
    # (5000, 10000),  
    # (15000, 50000),  
]

foldername = 'log_weighted_pos'

def run_log_weighted_experiment(starting_gini=0.3, n_epochs=50000):
    """Chạy thí nghiệm LOG_WEIGHTED PoS"""
    print("LOG_WEIGHTED PoS EXPERIMENT")
    print("=" * 50)
    
    # Lấy lịch join
    scheduled_joins = get_scheduled_joins(SCHEDULED_JOINS)
    
    # Thiết lập tham số
    params = Parameters(
        n_epochs=n_epochs,
        proof_of_stake=PoS.LOG_WEIGHTED,
        initial_stake_volume=5000.0,
        initial_distribution=Distribution.RANDOM,
        n_peers=10000,
        n_corrupted=50,
        p_fail=0.5,
        p_join=0.001,
        p_leave=0.001,
        join_amount=NewEntry.NEW_RANDOM,
        penalty_percentage=0.5,
        reward=20.0,
        scheduled_joins=scheduled_joins
    )
    
    # Tạo stake ban đầu
    stakes = generate_peers(
        params.n_peers, 
        params.initial_stake_volume, 
        params.initial_distribution, 
        starting_gini
    )
    
    # Tạo các peer bị tham nhũng
    corrupted = random.sample(range(params.n_peers), params.n_corrupted)
    
    print(f"Initial Gini: {gini(stakes):.3f}")
    print(f"Peers: {len(stakes)}, Corrupted: {len(corrupted)}")
    print(f"Epochs: {n_epochs}")
    
    # Chạy mô phỏng
    print("\nBắt đầu simulation...")
    gini_history, peers_history, nakamoto_history, hhi_history = simulate(stakes, corrupted, params)
    
    # In kết quả
    print_experiment_results("LOG_WEIGHTED PoS", gini_history, nakamoto_history, peers_history, hhi_history)
    
    # Vẽ và lưu các biểu đồ
    create_and_save_plot(gini_history, 'LOG_WEIGHTED PoS - Gini Coefficient Evolution', 
                        'Epoch', 'Gini Coefficient', 'log_weighted_gini.png', 'blue',foldername)
    
    create_and_save_plot(nakamoto_history, 'LOG_WEIGHTED PoS - Nakamoto Coefficient Evolution', 
                        'Epoch', 'Nakamoto Coefficient', 'log_weighted_nakamoto.png', 'red',foldername)
    
    create_and_save_plot(peers_history, 'LOG_WEIGHTED PoS - Peers Count Evolution', 
                        'Epoch', 'Number of Peers', 'log_weighted_peers.png', 'green',foldername)
    
    create_and_save_plot(hhi_history, 'LOG_WEIGHTED PoS - HHI Coefficient Evolution', 
                        'Epoch', 'HHI Coefficient', 'log_weighted_hhi.png', 'orange',foldername)
    
    # Lưu dữ liệu
    result = {
        'starting_gini': starting_gini,
        'final_gini': gini_history[-1],
        'final_nakamoto': nakamoto_history[-1],
        'final_peers': peers_history[-1],
        'final_hhi': hhi_history[-1],
        'gini_history': gini_history,
        'nakamoto_history': nakamoto_history,
        'peers_history': peers_history,
        'hhi_history': hhi_history
    }
    
    save_results_to_json({0: result}, 'log_weighted_results.json',foldername)
    
    return result


def main():
    """Chạy thí nghiệm LOG_WEIGHTED PoS"""
    print("LOG_WEIGHTED PoS Simulator")
    print("=" * 60)
    
    # Đặt seed ngẫu nhiên để tái tạo được kết quả
    random.seed(42)
    np.random.seed(42)
    
    try:
        # Lấy cấu hình từ user
        starting_gini, n_epochs = get_experiment_config()
        
        print(f"\nBắt đầu thí nghiệm với:")
        print(f"- Starting Gini: {starting_gini}")
        print(f"- Epochs: {n_epochs}")
        print()
        
        # Chạy thí nghiệm
        result = run_log_weighted_experiment(starting_gini, n_epochs)
        
        print("\n" + "=" * 60)
        print("Thí nghiệm LOG_WEIGHTED PoS hoàn thành thành công!")
        print(f"Kết quả được lưu trong folder 'results/'")
        
    except Exception as e:
        print(f"Lỗi khi thực thi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
