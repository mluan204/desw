import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from pathlib import Path
from coefficient import calculate_gini_coefficient, calculate_nakamoto_coefficient, calculate_hhi_coefficient

# Cấu hình matplotlib
plt.rcParams['figure.figsize'] = (16, 6)
plt.rcParams['font.size'] = 10

class BlockchainDecentralizationMetrics:
    
    # Mảng các blockchain muốn phân tích
    BLOCKCHAIN_LIST = [
        'aptos', 'axelar', 'celestia', 'celo', 'ethereum', 'injective', 'polygon', 'sui'
    ]
    
    @staticmethod
    def calculate_metrics(date):
        """Tính toán metrics cho tất cả blockchain"""
        current_dir = Path(__file__).resolve().parent
        data_folder_path = current_dir.parent / 'data'
        file_pattern = f"{date}_*"
        files = glob.glob(os.path.join(data_folder_path, file_pattern))
        
        if not files:
            return pd.DataFrame()
        
        results = []
        
        for blockchain in BlockchainDecentralizationMetrics.BLOCKCHAIN_LIST:
            matching_files = [f for f in files if f"{date}_{blockchain}.csv" in f]
            
            if not matching_files:
                continue
            
            try:
                df = pd.read_csv(matching_files[0])
                
                if 'tokens' not in df.columns:
                    continue
                
                tokens = df['tokens'].dropna()
                tokens = tokens[tokens > 0]
                
                if len(tokens) == 0:
                    continue
                
                # Tính các chỉ số PoS truyền thống
                gini_coeff = calculate_gini_coefficient(df)
                nakamoto_coeff = calculate_nakamoto_coefficient(df)
                hhi_coeff = calculate_hhi_coefficient(df)
                
                # Tính SRSW (Square Root of Stake Weight)
                df_srsw = df.copy()
                df_srsw['tokens'] = np.sqrt(df_srsw['tokens'])
                gini_srsw = calculate_gini_coefficient(df_srsw)
                nakamoto_srsw = calculate_nakamoto_coefficient(df_srsw)
                hhi_srsw = calculate_hhi_coefficient(df_srsw)
                
                # Tính LOG (Logarithmic Weight)
                df_log = df.copy()
                df_log['tokens'] = np.log1p(df_log['tokens'])  # log1p để tránh log(0)
                gini_log = calculate_gini_coefficient(df_log)
                nakamoto_log = calculate_nakamoto_coefficient(df_log)
                hhi_log = calculate_hhi_coefficient(df_log)
                
                # Tính desw (Dynamic Power Law)
                p_dynamic = max(0, min(1, 1 - gini_coeff))
                df_desw = df.copy()
                df_desw['tokens'] = df_desw['tokens'] ** p_dynamic
                gini_desw = calculate_gini_coefficient(df_desw)
                nakamoto_desw = calculate_nakamoto_coefficient(df_desw)
                hhi_desw = calculate_hhi_coefficient(df_desw)
                
                total_validators = len(tokens)
                
                results.append({
                    'blockchain': blockchain,
                    'total_validators': total_validators,
                    'gini_coefficient': gini_coeff,
                    'nakamoto_coefficient': nakamoto_coeff,
                    'hhi_coefficient': hhi_coeff,
                    'gini_srsw': gini_srsw,
                    'nakamoto_srsw': nakamoto_srsw,
                    'hhi_srsw': hhi_srsw,
                    'gini_log': gini_log,
                    'nakamoto_log': nakamoto_log,
                    'hhi_log': hhi_log,
                    'gini_desw': gini_desw,
                    'nakamoto_desw': nakamoto_desw,
                    'hhi_desw': hhi_desw
                })
                
            except:
                continue
        
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        return df.sort_values(by='nakamoto_coefficient', ascending=True).reset_index(drop=True)
    
    @staticmethod
    def plot_gini_chart(df, date, save_path):
        """Vẽ biểu đồ Gini Index với 4 phương pháp"""
        if df.empty:
            return
            
        plt.figure(figsize=(12, 6))
        index = np.arange(len(df['blockchain']))
        
        # Tạo DataFrame cho plotting
        plot_data = pd.DataFrame({
            'blockchain': df['blockchain'],
            'G': df['gini_coefficient'],
            'srsw_G': df['gini_srsw'],
            'log_G': df['gini_log'],
            'desw_G': df['gini_desw']
        })
        
        plot_data[['G', 'srsw_G', 'log_G', 'desw_G']].plot(kind='bar', color=['#407F7F', '#A67F8E', '#8B4F7F', '#F2B134'])
        plt.xlabel('Blockchain')
        plt.xticks(index, df['blockchain'], rotation=0)  # rotation=0 để không xoay
        plt.ylabel('Gini Coefficients '+ r'($G$)')
        plt.legend(["$w=s \\ G$", "SRSW " +r'$G^*$', "LOG " +r'$G^{**}$', "DESW "+r'$G^{***}$'], fontsize='large')

        # Thêm đường lưới
        plt.grid(True, axis='y')
        
        plt.tight_layout()
        
        # Lưu biểu đồ
        gini_chart_path = save_path / f'{date}_gini_index_comparison.png'
        plt.savefig(gini_chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Đã lưu biểu đồ Gini: {gini_chart_path}")
        
        plt.show()
    
    @staticmethod
    def plot_nakamoto_chart(df, date, save_path):
        """Vẽ biểu đồ Nakamoto Coefficients với 4 cột (chỉ Safety)"""
        if df.empty:
            return
        
        # Cài đặt cho biểu đồ cột nhóm
        bar_width = 0.18
        index = np.arange(len(df['blockchain']))

        # Tạo biểu đồ
        plt.figure(figsize=(14, 6))

        # Màu sắc theo mẫu
        colors = ['#72B184', '#F2B134', '#8B4F7F', '#B26670']

        # Hệ số Nakamoto (An toàn)
        plt.bar(index - 1.5*bar_width, df['nakamoto_coefficient'], bar_width, label=r'w', color=colors[0])
        plt.bar(index - 0.5*bar_width, df['nakamoto_srsw'], bar_width, label='srsw', color=colors[3])
        plt.bar(index + 0.5*bar_width, df['nakamoto_log'], bar_width, label='log', color=colors[2])
        plt.bar(index + 1.5*bar_width, df['nakamoto_desw'], bar_width, label='desw', color=colors[1])

        # Thêm nhãn và tiêu đề
        plt.xlabel('Blockchain')
        plt.ylabel('Nakamoto Coefficients')
        plt.xticks(index, df['blockchain'])

        # Tăng kích thước chú thích
        plt.legend(fontsize='large')

        # Thêm đường lưới
        plt.grid(True, axis='y')

        plt.tight_layout()
        
        # Lưu biểu đồ
        nakamoto_chart_path = save_path / f'{date}_nakamoto_coefficients_combined.png'
        plt.savefig(nakamoto_chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Đã lưu biểu đồ Nakamoto: {nakamoto_chart_path}")
        
        plt.show()
    
    @staticmethod
    def plot_hhi_chart(df, date, save_path):
        """Vẽ biểu đồ HHI Coefficients với 4 phương pháp"""
        if df.empty:
            return
            
        plt.figure(figsize=(12, 6))
        index = np.arange(len(df['blockchain']))
        
        # Tạo DataFrame cho plotting
        plot_data = pd.DataFrame({
            'blockchain': df['blockchain'],
            'w_HHI': df['hhi_coefficient'],
            'srsw_HHI': df['hhi_srsw'],
            'log_HHI': df['hhi_log'],
            'desw_HHI': df['hhi_desw']
        })
        
        plot_data[['w_HHI', 'srsw_HHI', 'log_HHI', 'desw_HHI']].plot(kind='bar', color=['#407F7F', '#A67F8E', '#8B4F7F', '#F2B134'])
        plt.xlabel('Blockchain')
        plt.xticks(index, df['blockchain'], rotation=0)  # rotation=0 để không xoay
        plt.ylabel('HHI Coefficients')
        plt.legend(["w HHI", "srsw HHI", "log HHI", "desw HHI"], fontsize='large')

        # Thêm đường lưới
        plt.grid(True, axis='y')
        
        plt.tight_layout()
        
        # Lưu biểu đồ
        hhi_chart_path = save_path / f'{date}_hhi_coefficients_comparison.png'
        plt.savefig(hhi_chart_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Đã lưu biểu đồ HHI: {hhi_chart_path}")
        
        plt.show()
    
    @staticmethod
    def print_results(df):
        """In bảng kết quả với tất cả phương pháp"""
        if df.empty:
            return
        
        df_sorted = df.sort_values('nakamoto_coefficient')
        
        print("GINI COEFFICIENTS:")
        print(f"{'Blockchain':<12} {'Original':<10} {'SRSW':<10} {'LOG':<10} {'desw':<10}")
        print("-" * 60)
        
        for _, row in df_sorted.iterrows():
            blockchain = row['blockchain'].upper()
            gini = f"{row['gini_coefficient']:.3f}"
            gini_srsw = f"{row['gini_srsw']:.3f}"
            gini_log = f"{row['gini_log']:.3f}"
            gini_desw = f"{row['gini_desw']:.3f}"
            
            print(f"{blockchain:<12} {gini:<10} {gini_srsw:<10} {gini_log:<10} {gini_desw:<10}")
        
        print("\nHHI COEFFICIENTS:")
        print(f"{'Blockchain':<12} {'Original':<10} {'SRSW':<10} {'LOG':<10} {'desw':<10}")
        print("-" * 60)
        
        for _, row in df_sorted.iterrows():
            blockchain = row['blockchain'].upper()
            hhi = f"{row['hhi_coefficient']:.3f}"
            hhi_srsw = f"{row['hhi_srsw']:.3f}"
            hhi_log = f"{row['hhi_log']:.3f}"
            hhi_desw = f"{row['hhi_desw']:.3f}"
            
            print(f"{blockchain:<12} {hhi:<10} {hhi_srsw:<10} {hhi_log:<10} {hhi_desw:<10}")
        
        print("\nNAKAMOTO COEFFICIENTS:")
        print(f"{'Blockchain':<12} {'Original':<10} {'SRSW':<10} {'LOG':<10} {'desw':<10} {'Validators':<11}")
        print("-" * 75)
        
        for _, row in df_sorted.iterrows():
            blockchain = row['blockchain'].upper()
            nakamoto = f"{int(row['nakamoto_coefficient'])}"
            nak_srsw = f"{int(row['nakamoto_srsw'])}"
            nak_log = f"{int(row['nakamoto_log'])}"
            nak_desw = f"{int(row['nakamoto_desw'])}"
            validators = f"{int(row['total_validators']):,}"
            
            print(f"{blockchain:<12} {nakamoto:<10} {nak_srsw:<10} {nak_log:<10} {nak_desw:<10} {validators:<11}")
    
    @staticmethod
    def save_results_to_csv(df, date, save_path):
        """Lưu kết quả ra file CSV"""
        if df.empty:
            return
        
        csv_path = save_path / f'{date}_blockchain_metrics.csv'
        df.to_csv(csv_path, index=False)
        print(f"Đã lưu kết quả CSV: {csv_path}")

def main():
    date = '02092025'
    
    if len(date) != 8 or not date.isdigit():
        print("Format không đúng!")
        return
    
    # Tạo folder results
    current_dir = Path(__file__).resolve().parent
    results_folder = current_dir.parent / 'results'
    results_folder.mkdir(exist_ok=True)
    
    results_df = BlockchainDecentralizationMetrics.calculate_metrics(date)
    
    if not results_df.empty:
        BlockchainDecentralizationMetrics.print_results(results_df)
        
        print("\nVẽ biểu đồ Gini:")
        BlockchainDecentralizationMetrics.plot_gini_chart(results_df, date, results_folder)
        
        print("\nVẽ biểu đồ HHI:")
        BlockchainDecentralizationMetrics.plot_hhi_chart(results_df, date, results_folder)
        
        print("\nVẽ biểu đồ Nakamoto:")
        BlockchainDecentralizationMetrics.plot_nakamoto_chart(results_df, date, results_folder)
        
        print("\nLưu kết quả CSV:")
        BlockchainDecentralizationMetrics.save_results_to_csv(results_df, date, results_folder)
    else:
        print("Không có dữ liệu")

if __name__ == '__main__':
    main()