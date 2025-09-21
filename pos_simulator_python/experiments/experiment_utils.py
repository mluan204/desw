#!/usr/bin/env python3
"""
Experiment Utilities
Các hàm tiện ích chung cho tất cả experiments
"""

import os
import json
import matplotlib.pyplot as plt


def get_results_dir(foldername):
    """Lấy đường dẫn thư mục results tương ứng với file đang chạy"""
    # Lấy đường dẫn của file đang gọi hàm này
    import inspect
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_globals['__file__']
    
    # Tạo đường dẫn results trong cùng thư mục với file caller
    caller_dir = os.path.dirname(os.path.abspath(caller_file))
    results_dir = os.path.join(caller_dir,foldername,'results')
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(results_dir, exist_ok=True)
    
    return results_dir


def save_results_to_json(results, filename, foldername):
    """
    Lưu kết quả thí nghiệm dưới dạng JSON vào thư mục results tương ứng
    
    Args:
        results (dict): Dictionary chứa kết quả thí nghiệm
        filename (str): Tên file JSON để lưu
    """
    results_dir = get_results_dir(foldername)
    
    serializable_results = {}
    for key, value in results.items():
        result_data = {}
        
        if 'starting_gini' in value:
            result_data['starting_gini'] = value['starting_gini']
        if 'final_gini' in value:
            result_data['final_gini'] = value['final_gini']
        if 'final_nakamoto' in value:
            result_data['final_nakamoto'] = value['final_nakamoto']
        if 'final_peers' in value:
            result_data['final_peers'] = value['final_peers']
        if 'final_hhi' in value:
            result_data['final_hhi'] = value['final_hhi']
            
        serializable_results[key] = result_data
    
    json_path = os.path.join(results_dir, filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    print(f"Dữ liệu đã lưu: {json_path}")


def save_plot(foldername, filename, title_suffix=""):
    """
    Lưu biểu đồ matplotlib vào thư mục results tương ứng
    
    Args:
        filename (str): Tên file PNG để lưu (không cần đường dẫn)
        title_suffix (str): Phần mở rộng cho title (optional)
    """
    results_dir = get_results_dir(foldername)
    plot_path = os.path.join(results_dir, filename)
    
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Biểu đồ{title_suffix} đã lưu: {plot_path}")


def create_and_save_plot(history_data, title, xlabel, ylabel, filename, color='blue', foldername=''):
    """
    Tạo và lưu biểu đồ hoàn chỉnh
    
    Args:
        history_data (list): Dữ liệu lịch sử để vẽ
        title (str): Tiêu đề biểu đồ
        xlabel (str): Nhãn trục X
        ylabel (str): Nhãn trục Y  
        filename (str): Tên file để lưu
        color (str): Màu đường vẽ
    """
    plt.figure(figsize=(12, 8))
    plt.plot(history_data, linewidth=2, color=color, alpha=0.8)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    save_plot(foldername,filename, f" {ylabel}",)
    plt.show()


def print_experiment_results(algorithm_name, gini_history, nakamoto_history, peers_history, hhi_history):
    """
    In kết quả cuối của thí nghiệm
    
    Args:
        algorithm_name (str): Tên thuật toán
        gini_history (list): Lịch sử Gini coefficient
        nakamoto_history (list): Lịch sử Nakamoto coefficient
        peers_history (list): Lịch sử số peers
        hhi_history (list): Lịch sử HHI coefficient
    """
    print(f"\nKết quả cuối {algorithm_name}:")
    print(f"  Final Gini: {gini_history[-1]:.3f}")
    print(f"  Final Nakamoto: {nakamoto_history[-1]}")
    print(f"  Final Peers: {peers_history[-1]}")
    print(f"  Final HHI: {hhi_history[-1]:.3f}")


def get_experiment_config():
    """
    Hỏi người dùng cấu hình thí nghiệm
    
    Returns:
        tuple: (starting_gini, n_epochs)
    """
    print("\nCấu hình thí nghiệm:")
    
    # Hỏi starting Gini
    try:
        starting_gini = float(input("Starting Gini coefficient (0-1, default 0.3): ") or "0.3")
        if not (0 <= starting_gini <= 1):
            raise ValueError("Gini coefficient phải trong khoảng 0-1")
    except ValueError as e:
        print(f"Lỗi: {e}. Sử dụng giá trị mặc định 0.3")
        starting_gini = 0.3
    
    # Hỏi số epochs
    try:
        n_epochs = int(input("Số epochs (default 50000): ") or "50000")
        if n_epochs <= 0:
            raise ValueError("Số epochs phải lớn hơn 0")
    except ValueError as e:
        print(f"Lỗi: {e}. Sử dụng giá trị mặc định 50000")
        n_epochs = 50000
    
    return starting_gini, n_epochs


def get_scheduled_joins(scheduled_joins_list):
    """
    Hiển thị và trả về lịch trình join
    
    Args:
        scheduled_joins_list (list): Danh sách các tuple (epoch, stake)
        
    Returns:
        list hoặc None: Lịch trình join hoặc None nếu không có
    """
    if scheduled_joins_list:
        print("Lịch trình join:")
        for epoch, stake in scheduled_joins_list:
            print(f"   • Epoch {epoch}: Validator join với stake {stake:,.0f}")
        return scheduled_joins_list
    else:
        print("Không có lịch join nào được thiết lập.")
        return None
