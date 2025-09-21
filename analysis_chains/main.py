import importlib
import sys
from datetime import datetime

def main(blockchains):
    # Hàm chính để lấy dữ liệu validator cho nhiều blockchain
 
    print(f"Bắt đầu phân tích {len(blockchains)} blockchain...")
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {}
    failed_chains = []
    
    for i, blockchain in enumerate(blockchains, 1):
        print(f"\n[{i}/{len(blockchains)}] Đang xử lý {blockchain.upper()}...")
        print("-" * 40)
        
        try:
            # Import module động dựa trên tên blockchain
            module_name = f'chains.{blockchain}'
            module = importlib.import_module(module_name)
            
            # Giả định class có tên giống blockchain nhưng viết hoa chữ cái đầu
            class_name = blockchain.capitalize()
            blockchain_class = getattr(module, class_name, None)
            
            if blockchain_class is None:
                print(f"Không tìm thấy class {class_name} trong {module_name}")
                failed_chains.append(blockchain)
                continue
            
            # Gọi phương thức get_validators
            print(f"Đang lấy dữ liệu validators...")
            validators = blockchain_class.get_validators()
            
            if validators is not None:
                print(f"Hoàn thành {blockchain.upper()}: {len(validators)} validators")
                results[blockchain] = validators
            else:
                print(f"Không thể lấy dữ liệu validators cho {blockchain}")
                failed_chains.append(blockchain)
                
        except ImportError as e:
            print(f"Không thể import module {module_name}: {e}")
            failed_chains.append(blockchain)
        except Exception as e:
            print(f"Lỗi khi xử lý {blockchain}: {e}")
            failed_chains.append(blockchain)
    

    
    if failed_chains:
        print(f"\nThất bại ({len(failed_chains)} blockchain):")
        for blockchain in failed_chains:
            print(f" {blockchain.upper()}")
    
    
    return results

if __name__ == '__main__':

    blockchains = [
        'ethereum', 'aptos', 'axelar', 'celestia', 
        'celo', 'injective', 'polygon', 'sui'
    ]
    
    main(blockchains)