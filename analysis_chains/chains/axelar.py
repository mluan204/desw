import requests
import pandas as pd

import chains.utils as utils

class Axelar:
    BASE_URL = 'https://rpc-axelar.imperator.co/dump_consensus_state'

    @classmethod
    def get_validators(cls):
        print('Lấy dữ liệu cho Axelar')

        response = requests.get(cls.BASE_URL)
        
        if response.status_code != 200:
            print(f'Không thể lấy dữ liệu Axelar: {response.status_code}')
            return None

        data = response.json()
        validators_data = data.get('result', {}).get('round_state', {}).get('validators', {}).get('validators', [])

        validator_info_list = []
        for validator in validators_data:
            validator_info = {
                'address': validator.get('address', 'Unknown'),
                'tokens': int(validator.get('voting_power', 'Unknown'))
            }
            validator_info_list.append(validator_info)
        
        # Tạo DataFrame
        df = pd.DataFrame(validator_info_list)
        # Sắp xếp DataFrame dựa trên tokens
        sorted_df = df.sort_values(by='tokens', ascending=False)
        utils.write_csv(sorted_df, 'axelar')
        return sorted_df

if __name__ == '__main__':
    Axelar.get_validators()
