import http.client
import json
import requests
import pandas as pd

import chains.utils as utils

class Aptos:
    MAINNET_VALIDATORS_DATA_URL = "https://storage.googleapis.com/aptos-mainnet/explorer/validator_stats_v2.json?cache-version=0"
    MAINNET_FULLNODE_DATA_URL = "fullnode.mainnet.aptoslabs.com"

    @classmethod
    def get_validators(cls):
        print('Lấy dữ liệu cho Aptos')
        response = requests.get(cls.MAINNET_VALIDATORS_DATA_URL)

        if response.status_code != 200:
            print(f'Không thể lấy dữ liệu: {response.status_code}')
            return None
        
        validators_data = response.json()

        validator_info_list = [
            {
                'address': validator.get('owner_address', 'Unknown'),
                'tokens': cls.get_tokens(validator.get('owner_address', 'Unknown'))  
            }
            for index, validator in enumerate(validators_data, start=1)
        ]

        df = pd.DataFrame(validator_info_list)
        sorted_df = df.sort_values(by='tokens', ascending=False)
        utils.write_csv(sorted_df, 'aptos')
        return sorted_df

    @classmethod
    def get_tokens(cls, address):
        conn = http.client.HTTPSConnection(cls.MAINNET_FULLNODE_DATA_URL)
        headers = {'Accept': "application/json"}
        request_path = f"/v1/accounts/{address}/resource/0x1::stake::StakePool"
        try:
            conn.request("GET", request_path, headers=headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            json_object = json.loads(data)

            # Nên kiểm tra xem các key có tồn tại trước khi truy cập để tránh KeyError
            active_value = json_object.get('data', {}).get('active', {}).get('value')
            if active_value is not None:
                return int(active_value)
            else:
                raise KeyError("Không tìm thấy các key cần thiết trong phản hồi JSON")
        finally:
            conn.close() 

if __name__ == '__main__':
    Aptos.get_validators()