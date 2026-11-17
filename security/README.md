# Giai đoạn C1 — Kiểm toán bảo mật thụ động

Các công cụ trong thư mục này chỉ kiểm tra mã nguồn và báo cáo. **Không chạy quy trình Google, không đăng nhập, không thanh toán, không tự đổi proxy hay chặn mạng, không xóa dữ liệu.**

## Nội dung kiểm tra

| Công cụ | Chức năng | Giới hạn |
| --- | --- | --- |
| `network_inventory.py` | Phát hiện tên host cố định trong Batch và Extension, so với danh sách chuẩn | Không thể quan sát proxy động hoặc lưu lượng thực tế |
| `extension_audit.py` | Kiểm tra Manifest V3, quyền và các dấu hiệu API nhạy cảm mới | Quét tĩnh, không chứng minh Extension an toàn tuyệt đối |
| `legacy_config_scan.py` | Chỉ đọc tên và loại file cấu hình/bản sao có thể chứa thông tin nhạy cảm | Không giải mã, sao chép hay xóa file; không in secret |
| `tests/` | Kiểm thử các công cụ bằng dữ liệu giả | Không thay thế kiểm thử sandbox |

GitHub Actions chạy pip-audit để phát hiện CVE trong thư viện Python, Gitleaks v3 để dò secret trong lịch sử Pull Request và Node để kiểm tra cú pháp JavaScript.

## Chạy thủ công tại máy

Tại thư mục gốc repository:

```powershell
python security/network_inventory.py --check
python security/extension_audit.py
python security/legacy_config_scan.py --root batch
python -m unittest discover -s security/tests -p "test_*.py" -v
python -m unittest discover -s batch/tests -p "test_security_controls.py" -v
```

Chỉ truyền --root tới thư mục khác nếu bạn muốn quét thêm. Công cụ không tự quét cả ổ đĩa, không có lệnh xóa, không gửi kết quả ra mạng.

## Xử lý kết quả

- Domain mới: xem lại nguồn gốc và loại dữ liệu trao đổi, rồi mới sửa `network_destinations.json` theo quy trình duyệt mã.
- CVE: đánh giá mức độ ảnh hưởng, kiểm thử phiên bản vá. Không tự nâng cấp thư viện.
- Secret: xác minh, thu hồi hoặc xoay khóa nếu là bí mật thật. Chỉ xóa ở commit mới không loại bỏ dữ liệu trong lịch sử Git.
- File cấu hình cũ: chỉ đưa ra đường dẫn tương đối và phân loại, người dùng quyết định xử lý.
- Cảnh báo Extension: đánh giá quyền và hành vi trước khi điều chỉnh danh sách được phép.

CI chỉ chạy khi có Pull Request chạm vào các file liên quan, hoặc khi chạy thủ công; không quét định kỳ và không tạo tác vụ nền. Các kiểm tra có thể thất bại khi phát hiện vấn đề và cần xem xét trước khi merge.

**Giới hạn còn lại:** API state có thể chứa dữ liệu nhạy cảm trong phiên đã xác thực; Chrome Extension có khả năng sửa yêu cầu Google, và một số kết nối Safe Browsing có thể bị giới hạn khi dùng proxy. C1 không thay đổi những thành phần này.
