# Batch Tool — Bảng điều khiển Google Pro Helper

Batch Tool là ứng dụng web chạy cục bộ để quản lý danh sách tài khoản, cấu hình kết nối, tiến trình và nhật ký thực hiện.

> **Cảnh báo:** Chưa hoàn tất kiểm toán bảo mật. Không sử dụng tài khoản chính hoặc thông tin thẻ thật. Tuyên bố ưu đãi miễn phí hay thời hạn đăng ký trong ứng dụng là thông tin tham khảo, không phải cam kết của Google.

## Yêu cầu hệ thống

1. Windows 10 hoặc Windows 11.
2. Google Chrome đã cài đặt.
3. Python 3.10 trở lên, có trong PATH.
4. Kết nối mạng thích hợp với dịch vụ bạn được phép truy cập.

## Cách khởi chạy

1. Mở thư mục `batch/`.
2. Lần đầu, chạy **`install-and-start.bat`** để cài thư viện phụ thuộc và mở ứng dụng.
3. Các lần sau, chạy **`start-dashboard.bat`**.
4. Truy cập **http://127.0.0.1:8765** nếu trình duyệt không tự mở.

Các lệnh cài thư viện trong script sử dụng Python hiện tại; **không có môi trường ảo riêng**. Nên chạy thử trong môi trường cách ly trước khi đưa vào sử dụng.

## Các khu vực trong giao diện

- **Tổng quan:** số lượng tài khoản và tiến trình.
- **Cấu hình chung:** lựa chọn cấu hình, phương thức thanh toán và proxy tùy chọn.
- **Nhập tài khoản:** dán danh sách, mỗi tài khoản một dòng.
- **Danh sách tác vụ:** chọn tài khoản, xem trạng thái và thao tác.
- **Nhật ký:** theo dõi diễn biến hoặc lỗi.

Định dạng danh sách tài khoản mà chương trình hiện hỗ trợ:

```text
email----password----recovery_email
email----password----recovery_email----two_factor_secret
email----password----two_factor_secret
```

**Các trường chứa thông tin cực kỳ nhạy cảm.** Không đưa dữ liệu thật vào môi trường chưa được kiểm toán. Toàn bộ `config.json` sẽ được mã hóa bằng Windows DPAPI khi ứng dụng đọc cấu hình lần đầu. Không chia sẻ bản gốc chưa mã hóa.

## Bảo vệ cục bộ — Giai đoạn A

- Chỉ truy cập bảng điều khiển bằng `http://127.0.0.1:8765` hoặc `http://localhost:8765`.
- API và ảnh chụp yêu cầu **mã phiên cục bộ tạm thời** được tạo mới mỗi lần khởi động ứng dụng. Nếu khởi động lại chương trình, hãy tải lại trang để nhận phiên mới.
- Mật khẩu tài khoản được **ẩn mặc định** trong danh sách; nút **Hiện** cho phép xem khi cần. Lệnh sao chép thông tin tài khoản vẫn hoạt động theo yêu cầu người dùng.
- Thông báo và trạng thái được lọc để giảm nguy cơ lộ mật khẩu, khóa 2FA, mã xác minh, số thẻ và thông tin xác thực proxy.
- Nếu cổng Chrome Debugging đã bị chương trình khác sử dụng, tác vụ sẽ báo lỗi thay vì tự đóng tiến trình đang chiếm cổng.

**Giới hạn:** Mã phiên cục bộ chủ yếu ngăn truy cập chéo từ website khác, không thay thế cơ chế bảo vệ hệ điều hành trước mã độc chạy cùng máy. Thông tin nhạy cảm vẫn được giải mã trong bộ nhớ khi chạy và vẫn có thể xuất hiện trong hồ sơ Chrome/ảnh chụp; DPAPI không bảo vệ trước mã độc đang chạy dưới cùng tài khoản Windows. Kiểm tra bảo mật không đồng nghĩa bảo đảm không phát sinh chi phí hoặc bảo đảm quyền lợi đăng ký.

### Chạy kiểm thử (không dùng tài khoản thật)

Từ thư mục `batch/`:

```powershell
python -m unittest discover -s tests -p "test_security_controls.py"
python -m unittest discover -s tests -p "test_config_storage.py"
python -m unittest discover -s tests -p "test_maintenance.py"
python -m unittest discover -s tests -p "test_frontend_stability.py"
```

Bài kiểm thử giao diện cần Playwright và Chrome. Các kiểm thử trên **chưa thay thế** cho việc quan sát lưu lượng mạng trong môi trường ảo cách ly.

## Bảo vệ dữ liệu — Giai đoạn B

### Mã hóa cấu hình bằng Windows DPAPI

- Mã hóa **toàn bộ** nội dung `batch/config.json` với phạm vi **CurrentUser** của Windows, bao gồm email, mật khẩu, khóa 2FA, thẻ, proxy, trường bổ sung và dữ liệu trạng thái.
- File cấu hình dạng JSON cũ được **tự chuyển đổi khi đọc lần đầu**. Chương trình mã hóa xong mới tạo file tạm và thay thế nguyên tử; nếu DPAPI hoặc thao tác ghi thất bại, file ban đầu được giữ nguyên. Không cố tình tạo bản sao cấu hình cũ chưa mã hóa.
- Python vẫn nhận cấu trúc `dict` như trước; các bước tự động hóa không cần sửa. **Không** sửa trực tiếp nội dung mã hóa bằng trình soạn thảo văn bản.
- Không có cơ chế tự động lưu bản rõ khi DPAPI thất bại. Tính năng mã hóa chỉ hỗ trợ Windows.
- **Quan trọng:** File chỉ có thể giải mã với hồ sơ/tài khoản Windows tương ứng. Chuyển file sang máy khác hoặc chạy ứng dụng dưới tài khoản Windows khác thường sẽ không giải mã được. Sao lưu mã hóa không thay thế sao lưu khóa/hồ sơ Windows. Đây không phải cơ chế đồng bộ đa máy.

### Dọn ảnh chụp và sao lưu

Từ thư mục `batch/`, chạy:

```powershell
python maintenance.py --days 30
python maintenance.py --days 30 --apply
```

Lệnh đầu chỉ **xem trước** số ảnh có thể xóa; `--apply` mới thực hiện. Công cụ chỉ chọn ảnh PNG quá hạn không còn được tham chiếu trong cấu hình. Nó không đụng vào hồ sơ Chrome, ảnh đang được tham chiếu, hay file cấu hình. Nếu không đọc/giải mã được cấu hình, việc xóa phải dừng.

Vì mã hóa không xóa dấu vết dữ liệu đã từng lưu trên đĩa hoặc trong các bản sao trước đây, hãy kiểm tra và xử lý bản sao cũ theo quy trình bảo mật Windows. Không đưa bất kỳ bản sao nào lên GitHub.

### Thư viện phụ thuộc

`requirements.txt` được cố định phiên bản **trực tiếp**, với phiên bản FastAPI phù hợp cho Python 3.10. Các thư viện phụ thuộc gián tiếp và bản dựng Windows vẫn cần được xác minh; các phiên bản này chưa được thử chạy toàn bộ trên máy Windows thực.

## Nguyên tắc bảo mật và dữ liệu

- Không commit `config*.json`, `.env`, thư mục phiên trình duyệt, nhật ký, ảnh chụp và dữ liệu cá nhân.
- Mỗi tài khoản có thể dùng cấu hình trình duyệt riêng; điều đó **không tương đương** môi trường sandbox bảo mật.
- Luôn kiểm tra số tiền, phí phát sinh, quốc gia/khu vực, thời điểm gia hạn và điều khoản chính thức trước khi chấp nhận đăng ký.
- Chưa có kết quả kiểm thử thực tế nào bảo đảm rằng ứng dụng không bị tính phí hoặc có thể kích hoạt quyền lợi theo mô tả.

## Phạm vi cập nhật ngôn ngữ

Các nội dung hiển thị cho người dùng được chuẩn hóa bằng tiếng Việt; tên file và cấu trúc kỹ thuật bằng tiếng Anh. Các chuỗi dùng để tương tác với website Google phải được giữ đúng nội dung ban đầu nhằm tránh làm hỏng selector.
