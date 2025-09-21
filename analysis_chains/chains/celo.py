import requests
import pandas as pd

import chains.utils as utils

class Celo:
    URL = 'https://thecelo.com/api/v0.1?method=groups'

    @classmethod
    def get_validators(cls):
        print('Lấy dữ liệu cho Celo')
        response = requests.get(cls.URL)

        if response.status_code != 200:
            print(f'Không thể lấy dữ liệu: {response.status_code}')
            return None
        
        data = response.json()
        groups = data.get('groups', {})
        # Thu thập các giá trị được chỉ định cho mỗi nhóm
        validator_info_list = [
            {
                'address': group[0],
                'tokens': float(group[1])
            }
            for address, group in groups.items()
        ]

        # # Tạo DataFrame
        df = pd.DataFrame(validator_info_list)

        # # Sắp xếp DataFrame dựa trên tokens
        sorted_df = df.sort_values(by='tokens', ascending=False)
        # Lưu DataFrame vào file CSV
        utils.write_csv(sorted_df, 'celo')
        print(sorted_df)
        return sorted_df
    
if __name__ == '__main__':
    Celo.get_validators()
