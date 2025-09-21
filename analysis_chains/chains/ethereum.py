import requests
import pandas as pd
import os
import numpy as np

import chains.utils as utils 

class Ethereum:
    URL = 'https://api.dune.com/api/v1/query/3383110/results'
    
    @classmethod
    def get_validators(cls):
        print('Lấy dữ liệu cho Ethereum')

        api_key = "AQZkw9X57HmBp2HeQDzbvw3m6FV7Y1Hn"
        if not api_key:
            print('Lỗi: API_KEY chưa được thiết lập')
            return None
            
        headers = {
            'X-Dune-API-Key': api_key
        }
        params = {
            'limit': 1000
        }
        
        response = requests.get(cls.URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f'Không thể lấy dữ liệu: {response.status_code}')
            return None
        
        response_data = response.json()
        rows = response_data.get('result', {}).get('rows', [])
        df = pd.DataFrame(rows)
        
        # Nhóm theo entity_just_name và tính tổng amount_staked
        grouped_df = df.groupby('entity_just_name', as_index=False).agg({
            'amount_staked': 'sum'
        })
        
        # Đổi tên cột để phù hợp với định dạng chuẩn
        result_df = grouped_df.rename(columns={
            'entity_just_name': 'address',
            'amount_staked': 'tokens'
        })
        
        # Chuyển đổi tokens thành số nguyên
        result_df['tokens'] = (result_df['tokens']).astype(int)
        
        # Sắp xếp theo tokens theo thứ tự giảm dần
        sorted_df = result_df.sort_values(by='tokens', ascending=False)
        utils.write_csv(sorted_df, 'ethereum')
        return sorted_df
    
if __name__ == '__main__':
    Ethereum.get_validators()
