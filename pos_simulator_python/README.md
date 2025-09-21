# Proof of Stake Simulator (Python)

Đây là phiên bản Python của Proof-of-Stake Simulator. Chúng tôi sử dụng simulator này để nghiên cứu xu hướng của hệ số Gini dưới các thuật toán đồng thuận khác nhau.

## Tổng quan

Dự án này mô phỏng các thuật toán Proof-of-Stake (PoS) khác nhau để phân tích:

- **Hệ số Gini**: Đo lường mức độ bất bình đẳng trong phân phối stake
- **Nakamoto Coefficient**: Đo lường mức độ phi tập trung của mạng
- **Độ ổn định**: Khả năng duy trì trạng thái cân bằng của hệ thống

## Các thuật toán PoS được hỗ trợ

1. **Weighted PoS**: Validator có stake cao hơn có xác suất được chọn cao hơn
2. **OppositeWeighted PoS**: Validator có stake thấp hơn có xác suất được chọn cao hơn
3. **GiniStabilized PoS**: Tự động điều chỉnh để duy trì hệ số Gini ở mức mục tiêu
4. **LogWeighted PoS**: Sử dụng logarit của stake để giảm ảnh hưởng của stake lớn
5. **LogWeightedUniform PoS**: Kết hợp logarit và phân phối đều
6. **DESW PoS**: Dynamic Exponential Stake Weighting - Sử dụng power-law động với p = 1 - Gini để cân bằng hệ thống
7. **SRSW Weighted PoS**: Sử dụng căn bậc hai của stake để giảm ảnh hưởng của stake lớn

## Tham số mô phỏng

### Tham số cơ bản

- **n_epochs**: Số lượng epochs được mô phỏng, tương ứng với số lượng blocks (ảo) được xác thực (mặc định: 50000)
- **proof_of_stake**: Loại PoS được sử dụng. Nhận các giá trị: `WEIGHTED`, `OPPOSITE_WEIGHTED`, `GINI_STABILIZED`, `LOG_WEIGHTED`
- **initial_stake_volume**: Tổng số lượng coins ban đầu (mặc định: 10000.0)
- **initial_distribution**: Phân phối ban đầu của coins giữa các validators. Nhận các giá trị: `UNIFORM`, `GINI`, `RANDOM`
- **initial_gini**: Hệ số Gini ban đầu (mặc định: 0.3)
- **n_peers**: Số lượng participants trong blockchain (mặc định: 1000)
- **n_corrupted**: Số lượng validators có thể thể hiện hành vi bị hỏng (mặc định: 20)

### Tham số về hành vi

- **p_fail**: Xác suất mà một corrupted validator cố gắng không xác thực đúng block (mặc định: 0.5)
- **penalty_percentage**: Phần trăm coins bị loại bỏ từ corrupted validators khi họ thất bại (mặc định: 0.5)
- **reward**: Số lượng coins thưởng cho validator thành công (mặc định: 10.0)

### Tham số về động thái mạng

- **p_join**: Xác suất, tại mỗi epoch, của một user mới tham gia vào validators (mặc định: 0.001)
- **p_leave**: Xác suất, tại mỗi epoch, của bất kỳ validator nào rời khỏi pool (mặc định: 0.001)
- **join_amount**: Số lượng coins sở hữu bởi một peer vừa tham gia. Nhận các giá trị: `NEW_AVERAGE`, `NEW_RANDOM`, `NEW_MAX`, `NEW_MIN`
- **scheduled_joins**: Lịch trình join của các validator lớn. Format: `[(epoch, stake_amount), ...]` (mặc định: None)

### Tham số cho GiniStabilized PoS

- **θ (theta)**: Hệ số Gini mục tiêu (mặc định: 0.3)
- **s_type**: Loại hàm cập nhật. Nhận các giá trị: `CONSTANT`, `LINEAR`, `QUADRATIC`, `SQRT`
- **k**: Hệ số điều chỉnh cho hàm cập nhật (mặc định: 0.001)

## Cách sử dụng

### Cài đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt package (tùy chọn)
pip install -e .
```

### Sử dụng cơ bản

```python
from src.simulator import simulate
from src.parameters import Parameters, PoS, Distribution, NewEntry
from src.utils import generate_peers
import random

# Tạo tham số mô phỏng
params = Parameters(
    n_epochs=10000,
    proof_of_stake=PoS.WEIGHTED,
    initial_stake_volume=10000.0,
    initial_distribution=Distribution.GINI,
    initial_gini=0.3,
    n_peers=100,
    n_corrupted=5,
    p_fail=0.5,
    penalty_percentage=0.5,
    reward=10.0
)

# Tạo stake ban đầu
stakes = generate_peers(
    params.n_peers,
    params.initial_stake_volume,
    params.initial_distribution,
    params.initial_gini
)

# Tạo danh sách corrupted peers
corrupted = random.sample(range(params.n_peers), params.n_corrupted)

# Chạy mô phỏng
gini_history, peers_history, nakamoto_history = simulate(stakes, corrupted, params)

print(f"Final Gini: {gini_history[-1]:.3f}")
print(f"Final Nakamoto Coefficient: {nakamoto_history[-1]}")
print(f"Final number of peers: {peers_history[-1]}")
```

### Chạy các ví dụ

```bash
# Chạy tất cả các ví dụ
make run-examples

# Chạy demo nhanh
make quick-demo

# Chạy interactive menu với 7 experiments + 1 comparison
cd examples
python simple_example.py
```

Khi chạy `python simple_example.py`, bạn sẽ thấy menu tương tác:

1. Experiment 1: WEIGHTED PoS
2. Experiment 2: OPPOSITE_WEIGHTED PoS
3. Experiment 3: GINI_STABILIZED PoS
4. Experiment 4: LOG_WEIGHTED PoS
5. Experiment 5: DESW PoS
6. Experiment 6: SRSW_WEIGHTED PoS
7. So sánh tất cả 6 thuật toán
8. Thoát

### Tính năng Scheduled Joins

Trước khi chạy mỗi experiment, hệ thống sẽ hỏi bạn có muốn thiết lập lịch join cho các validator lớn hay không. Tính năng này cho phép:

- **Thiết lập epoch cụ thể**: Chọn epoch nào validator mới sẽ tham gia
- **Thiết lập stake amount**: Quyết định lượng stake của validator mới
- **Đánh giá impact**: Xem thuật toán PoS phản ứng như thế nào với sự thay đổi đột ngột
- **Mô phỏng real-world**: Mô phỏng các tình huống như exchange lớn stake vào mạng

Ví dụ sử dụng:

- Epoch 5000, Stake 100000: Một validator có stake rất lớn join ở giữa simulation
- Epoch 1000, Stake 50000: Validator join sớm để xem ảnh hưởng lâu dài

## Các thí nghiệm mẫu

File `examples/simple_example.py` cung cấp 7 thí nghiệm chính + 1 thí nghiệm so sánh:

### Experiment 1: WEIGHTED PoS

Sử dụng _Weighted PoS_ để thể hiện xu hướng cho hệ số Gini tiến đến 1 (bất bình đẳng cao). Validator có stake cao hơn có xác suất được chọn cao hơn.

### Experiment 2: OPPOSITE_WEIGHTED PoS

Sử dụng _OppositeWeighted PoS_ để thể hiện xu hướng cho hệ số Gini tiến đến 0 (bình đẳng cao). Validator có stake thấp hơn có xác suất được chọn cao hơn.

### Experiment 3: GINI_STABILIZED PoS

Sử dụng _GiniStabilized PoS_ để thể hiện khả năng kiểm soát hệ số Gini ở mức mục tiêu θ = 0.3. Thuật toán này tự động điều chỉnh để duy trì mức bất bình đẳng mong muốn.

### Experiment 4: LOG_WEIGHTED PoS

Sử dụng _LogWeighted PoS_ để giảm ảnh hưởng của stake lớn bằng cách sử dụng logarit của stake trong quá trình chọn validator.

### Experiment 5: DESW PoS

Sử dụng _DESW PoS (Dynamic Equilibrium Stake Weighting)_ để tạo ra một cơ chế đồng thuận động dựa trên power-law với p = 1 - Gini. Thuật toán này tự động điều chỉnh để cân bằng hệ thống dựa trên mức độ bất bình đẳng hiện tại.

### Experiment 6: SRSW_WEIGHTED PoS

Sử dụng _SRSW Weighted PoS_ để giảm ảnh hưởng của stake lớn bằng cách sử dụng căn bậc hai của stake trong quá trình tính xác suất chọn validator.

### Experiment 7: So sánh tất cả 6 thuật toán

Chạy đồng thời tất cả 7 thuật toán PoS với cùng tham số để so sánh hiệu quả:

- **WEIGHTED**: Ưu tiên stake cao
- **OPPOSITE_WEIGHTED**: Ưu tiên stake thấp
- **GINI_STABILIZED**: Duy trì Gini mục tiêu
- **LOG_WEIGHTED**: Giảm ảnh hưởng stake lớn
- **LOG_WEIGHTED_UNIFORM**: Kết hợp logarit và đều
- **DESW**: Power-law động với p = 1 - Gini (Dynamic Equilibrium Stake Weighting)
- **SRSW_WEIGHTED**: Căn bậc hai của stake để giảm ảnh hưởng stake lớn

### Tham số chung cho các thí nghiệm:

- **n_epochs**: 250,000 epochs
- **initial_stake_volume**: 5,000 coins
- **n_peers**: 10,000 validators
- **n_corrupted**: 50 malicious validators
- **p_fail**: 0.5 (xác suất thất bại)
- **reward**: 200 coins cho validator thành công
- **penalty_percentage**: 0.5 (50% stake bị phạt)

## Cấu trúc dự án

```
pos_simulator_python/
│
├── src/                  # Mã nguồn chính
│   ├── __init__.py      # Khởi tạo package
│   ├── parameters.py     # Định nghĩa các tham số và enums
│   ├── simulator.py      # Logic mô phỏng chính
│   └── utils.py          # Các hàm tiện ích (Gini, Nakamoto, consensus)
│
├── experiments/             # Các ví dụ sử dụng mô phỏng
│   └── comparison.py # Ví dụ đầy đủ với 6 experiments + 1 comparison
│   └── experiment_utils.py
│
├── requirements.txt      # Danh sách phụ thuộc Python
├── setup.py             # Script cài đặt package
├── Makefile             # Tự động hóa các tác vụ
└── README.md            # Tài liệu này
```

## Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Dependencies chính**:
  - `numpy>=1.21.0`: Tính toán số học
  - `matplotlib>=3.5.0`: Vẽ biểu đồ
  - `tqdm>=4.62.0`: Progress bars
  - `pandas>=1.3.0`: Xử lý dữ liệu
  - `seaborn>=0.11.0`: Visualization nâng cao

## Tính năng chính

### Metrics được tính toán

- **Hệ số Gini**: Đo lường bất bình đẳng trong phân phối stake
- **Nakamoto Coefficient**: Đo lường mức độ phi tập trung
- **HHI Coefficient**: Đo lường mức độ tập trung thị trường
- **Decentralization Score**: Điểm số phi tập trung tổng hợp

### Tính năng Scheduled Joins

- **Lịch trình Join**: Cho phép lên lịch các validator với stake lớn tham gia vào epoch cụ thể
- **Đánh giá độ ổn định**: Kiểm tra khả năng chống lại sự thay đổi đột ngột trong phân phối stake
- **Mô phỏng tấn công**: Có thể mô phỏng các cuộc tấn công bằng cách thêm validator có stake rất lớn
- **Giao diện tương tác**: UI cho phép dễ dàng thêm/xóa/quản lý lịch join

### Cơ chế đồng thuận

- **Weighted**: Ưu tiên validator có stake cao
- **OppositeWeighted**: Ưu tiên validator có stake thấp
- **GiniStabilized**: Tự động điều chỉnh để duy trì Gini mục tiêu
- **LogWeighted**: Sử dụng logarit để giảm ảnh hưởng stake lớn

### Tính năng động

- **Join/Leave**: Peers có thể tham gia/rời khỏi mạng
- **Corruption**: Mô phỏng hành vi malicious validators
- **Penalty/Reward**: Hệ thống thưởng phạt cho validators

## Dự án gốc

Đây là phiên bản Python của dự án gốc được viết bằng Julia:

**Dự án gốc (Julia)**: [https://github.com/lorenzorovida/PoS-Simulator](https://github.com/lorenzorovida/PoS-Simulator)
