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

**Các trường chứa thông tin cực kỳ nhạy cảm.** Không đưa dữ liệu thật vào môi trường chưa được kiểm toán. Tránh lưu mật khẩu, khóa bí mật 2FA hoặc dữ liệu thẻ dưới dạng văn bản rõ.

## Nguyên tắc bảo mật và dữ liệu

- Không commit `config*.json`, `.env`, thư mục phiên trình duyệt, nhật ký, ảnh chụp và dữ liệu cá nhân.
- Mỗi tài khoản có thể dùng cấu hình trình duyệt riêng; điều đó **không tương đương** môi trường sandbox bảo mật.
- Luôn kiểm tra số tiền, phí phát sinh, quốc gia/khu vực, thời điểm gia hạn và điều khoản chính thức trước khi chấp nhận đăng ký.
- Chưa có kết quả kiểm thử thực tế nào bảo đảm rằng ứng dụng không bị tính phí hoặc có thể kích hoạt quyền lợi theo mô tả.

## Phạm vi cập nhật ngôn ngữ

Các nội dung hiển thị cho người dùng được chuẩn hóa bằng tiếng Việt; tên file và cấu trúc kỹ thuật bằng tiếng Anh. Các chuỗi dùng để tương tác với website Google phải được giữ đúng nội dung ban đầu nhằm tránh làm hỏng selector.
