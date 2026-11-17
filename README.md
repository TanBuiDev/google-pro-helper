# Google Pro Helper

Công cụ hỗ trợ quản lý tác vụ tài khoản và theo dõi thông tin gói Google AI Pro. Repository gồm hai thành phần hoạt động độc lập: **Batch Tool** và **Chrome Extension**.

> **Lưu ý về bảo mật:** Mã nguồn chưa được kiểm toán đầy đủ. Không dùng tài khoản Google chính, khóa 2FA hay thẻ thanh toán thật trước khi kiểm tra tính an toàn. Mọi quyền lợi và chi phí đăng ký đều phụ thuộc vào xác nhận chính thức từ Google. Công cụ này không phải sản phẩm chính thức của Google.

## Thành phần

| Thành phần | Vị trí | Công dụng |
| --- | --- | --- |
| Batch Tool | [batch/](./batch/) | Giao diện web cục bộ, quản lý danh sách tài khoản, tiến trình và nhật ký |
| Chrome Extension | [extension/](./extension/) | Tiện ích trình duyệt hiển thị trạng thái và cảnh báo thông tin thanh toán |

## Yêu cầu

- Windows 10/11 (dành cho Batch Tool).
- Python 3.10 trở lên và Google Chrome.
- Trình duyệt Chromium hỗ trợ tiện ích Manifest V3 (dành cho Extension).

## Khởi chạy Batch Tool

1. Mở thư mục `batch/`.
2. Lần đầu: chạy `install-and-start.bat`.
3. Những lần sau: chạy `start-dashboard.bat`.
4. Mở bảng điều khiển ở `http://127.0.0.1:8765`.

Xem [hướng dẫn Batch Tool](./batch/README.md) để biết chi tiết.

## Sử dụng Chrome Extension

Mở `chrome://extensions/`, bật **Chế độ dành cho nhà phát triển**, chọn **Tải tiện ích đã giải nén** và trỏ tới thư mục `extension/`. Không cài đặt tiện ích trong trình duyệt có phiên đăng nhập nhạy cảm khi chưa hoàn tất kiểm toán.

## Quy ước phát triển

- Tên tệp, thư mục, biến, hàm, class và chú thích mã nguồn bằng tiếng Anh.
- Giao diện, trạng thái, thông báo và tài liệu dành cho người dùng bằng tiếng Việt.
- Giữ nguyên khóa cấu hình, API, selector và chuỗi nhận diện giao diện bên thứ ba khi Việt hóa.
- Không commit thông tin tài khoản, mật khẩu, khóa 2FA, thông tin thanh toán, cookie, ảnh chụp hoặc log cá nhân.

## Kiểm toán bảo mật thụ động (C1)

Thư mục [security/](./security/) chứa các công cụ chỉ kiểm tra: danh sách domain, quyền Chrome Extension, cấu hình cũ, secret và lỗ hổng thư viện. Xem [hướng dẫn C1](./security/README.md). Không can thiệp đăng nhập hoặc thanh toán.

## Trạng thái an toàn

Công cụ có khả năng truy cập dữ liệu đăng nhập và thanh toán. Các tính năng tự động hóa, phát hiện giá và trạng thái đăng ký **chưa được bảo đảm an toàn hoặc chính xác**. Chỉ sử dụng trong môi trường kiểm thử được kiểm soát.
