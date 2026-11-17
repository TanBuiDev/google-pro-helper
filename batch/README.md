# Google AI Pro (5 TB) — Bảng điều khiển tự động hóa với mục tiêu 2 năm không mất phí (US$0.00 → 24 tháng)

## I. Yêu cầu môi trường

1. Hệ điều hành **Windows 10 / 11**.
2. Đã cài đặt trình duyệt **Google Chrome** (có thể dùng đường dẫn cài đặt mặc định).
3. Đã cài đặt **Python 3.10** trở lên (khi cài đặt, chọn **Add Python to PATH**).
4. **Môi trường mạng:** Bật proxy khu vực Mỹ (US) trên máy hoặc điền mẫu proxy ở phía bên trái bảng điều khiển.

## II. Khởi chạy nhanh

1. **Lần đầu sử dụng:** Nhấp đúp chạy `1_首次运行_安装依赖并启动.bat` (cài đặt thư viện phụ thuộc và khởi chạy).
2. **Những lần sử dụng sau:** Nhấp đúp chạy `2_启动控制台.bat` (khởi chạy bảng điều khiển).
3. Trình duyệt sẽ tự động mở bảng điều khiển tại: http://127.0.0.1:8765

## III. Nhập thông tin thẻ thanh toán tùy chỉnh và hướng dẫn chạy tài khoản

### 1. Nhập thẻ thanh toán (bắt buộc)

- Tại khu vực **“Cấu hình toàn cục và liên kết thẻ trực tiếp với địa chỉ miễn thuế”** ở phía bên trái giao diện web, nhập thông tin thẻ Visa hoặc Mastercard hỗ trợ thanh toán ngoại tệ của bạn:
  - **Số thẻ:** 16 chữ số.
  - **Ngày hết hạn:** Tháng / năm, ví dụ `08 / 29`.
  - **Mã bảo mật:** CVC gồm 3 chữ số.
  - **Họ tên chủ thẻ:** Viết bằng tiếng Anh.
  - **Mã ZIP:** Mặc định điền sẵn `97201` (bang Oregon, Mỹ, được tác giả mô tả là khu vực miễn thuế); theo hướng dẫn gốc, không cần thay đổi.
- Sau khi nhập, nhấn **“💾 Lưu cấu hình”**.
- **Lưu ý theo tài liệu gốc:** Script được mô tả là có cơ chế bảo vệ nghiêm ngặt nhằm chỉ nhấn đăng ký khi cửa sổ thanh toán xác nhận số tiền `US$0.00`, với mục tiêu không bị trừ tiền trong suốt quá trình. Đây là tuyên bố của tác giả, không phải bảo đảm về giao dịch thực tế.

### 2. Nhập hàng loạt tài khoản Google

- Trong khu vực **“Nhập danh sách tài khoản hàng loạt”** ở bên phải giao diện web, dán danh sách tài khoản (**mỗi dòng một tài khoản**). Chấp nhận một trong các định dạng:
  - `email----mật khẩu----email khôi phục`
  - `email----mật khẩu----email khôi phục----khóa bí mật 2FA`
  - `email----mật khẩu----khóa bí mật 2FA`
- Nhấn **“➕ Nhập danh sách tài khoản”**.

### 3. Bắt đầu thực thi tự động

- Nhấn **“▶ Thực thi”** ở bên phải từng tài khoản hoặc **“▶ Thực thi tự động hàng loạt”** ở phía trên.
- Theo hướng dẫn gốc, script sẽ tự động thực hiện:
  1. **Bước 1:** Đăng nhập vào Google và xác minh qua email khôi phục / 2FA.
  2. **Bước 2:** Liên kết thẻ trực tiếp với địa chỉ miễn thuế và áp dụng lớp ưu đãi miễn phí 12 tháng đầu (`US$0.00`).
  3. **Bước 3:** Cộng thêm lớp ưu đãi miễn phí 6 tháng thứ hai (`US$0.00` → 18 tháng).
  4. **Bước 4:** Cộng thêm lớp ưu đãi miễn phí 6 tháng thứ ba (`US$0.00` → tối đa 24 tháng).
  5. **Bước 5:** Tự động truy cập Google Play để hủy gia hạn tự động, giữ quyền lợi đến hết hạn hai năm theo mô tả và chụp ảnh màn hình để xác minh.

## Thông tin từ tác giả gốc

- **Trang cung cấp thẻ:** https://faka.cdkey.si
- **Blog:** https://blog.caowo.de
- **Nhóm Telegram:** `@Hello_Florence`
