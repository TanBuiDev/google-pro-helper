# Google Pro Helper

Repository này bao gồm hai phiên bản độc lập: **tiện ích mở rộng trình duyệt (Chrome Extension)** và **phiên bản xử lý hàng loạt (Batch)**. Mỗi phiên bản được giữ nguyên cấu trúc thư mục và mã nguồn ban đầu.

| Phiên bản | Thư mục | Mô tả |
| --- | --- | --- |
| Tiện ích mở rộng trình duyệt | [extension](./extension/) | Tiện ích sử dụng trong trình duyệt, bao gồm tệp manifest, cửa sổ popup, các script và biểu tượng. |
| Phiên bản hàng loạt | [batch](./batch/) | Công cụ quản lý tác vụ cho nhiều tài khoản qua bảng điều khiển chạy cục bộ, gồm giao diện web, backend, script khởi chạy và kiểm thử. |

## Cấu trúc thư mục

```text
google-pro-helper/
├── extension/   # Tiện ích mở rộng trình duyệt
├── batch/       # Phiên bản xử lý hàng loạt
├── .gitignore
└── README.md
```

## Tiện ích mở rộng trình duyệt

Bài đăng gốc trên Linux.do:

[https://linux.do/t/topic/3123997](https://linux.do/t/topic/3123997)

(💰 Kích hoạt Google AI Pro miễn phí 12 / 24 tháng | chèn `offer token`)

(Phần lớn tài khoản của tôi được tạo hàng loạt bằng công cụ đăng ký tự động; nguyên lý đều giống nhau. Tổng cộng tôi đã làm bảy tài khoản, đến nay đều hoạt động được hơn nửa tháng. Tuy nhiên, với việc có quá nhiều người tận dụng ưu đãi theo cách này, tôi đoán cách làm này sẽ không tồn tại được lâu.)

> **Lưu ý: Không sử dụng tài khoản Google chính!!!!**

### **1. Trong Chrome, chọn “Load unpacked” (Tải tiện ích đã giải nén); nhớ bật Developer mode (Chế độ dành cho nhà phát triển)**

![image](https://i0.hdslb.com/bfs/new_dyn/f6ecc1314583543aedb82bf0d950213e3747579686817540.png@1192w.webp)

### **2. Mở `one.google.com/plans` và làm theo các bước trong tiện ích; kích hoạt gói 12 tháng trước, đồng thời chú ý thông báo màu xanh phía trên và thông báo ở góc dưới bên phải**

![image](https://i0.hdslb.com/bfs/new_dyn/5de4698ae0cd2a371a1ecb3e6727a8823747579686817540.png@1130w_1760h.webp)

![image](https://i0.hdslb.com/bfs/new_dyn/33147e398928380c614b5ae85bd50a903747579686817540.png@1192w.webp)

![image](https://i0.hdslb.com/bfs/new_dyn/2544ad49e1db82fb90999fe3355e6fbd3747579686817540.png@92h.webp)

### **3. Chọn gói Pro và liên kết thẻ thanh toán**

(Tài khoản thẻ cần có ít nhất 1 USD để xác minh. Theo tác giả, về cơ bản các loại thẻ USD đều dùng được. Những thẻ đã thử: starryblu/maya/bybit/mexc/Mastercard của China Merchants Bank/Mastercard 2233 của Bank of China/bitEU/wise/savo.)

**Trước khi thanh toán phải kiểm tra thật kỹ: theo hướng dẫn gốc, ở bước đầu tiên số tiền của tháng đầu phải là 0.**

> **P.S.** Nếu tài khoản đã được áp dụng ưu đãi giảm giá như hình dưới, khi thanh toán có khả năng rất cao sẽ phải trả tiền YouTube Premium của tháng đầu. Cẩn thận tránh bị trừ tiền ngoài ý muốn. Trường hợp bình thường sẽ hiển thị bắt đầu thu phí từ tháng sau.

![image](https://i0.hdslb.com/bfs/new_dyn/b24d7dc8773238dce8883de6ac8fb5a13747579686817540.png@1192w.webp)

![image](https://i0.hdslb.com/bfs/new_dyn/9b5d510ce927dc364d468eb82cc7182e3747579686817540.png@1046w_1590h.webp)

### **4. Nếu trang đăng ký gói không xuất hiện nữa, đừng vội lo lắng và cũng đừng hủy đăng ký (thực ra nếu đã hủy cũng không sao)**

Trước tiên, chuyển tiện ích sang tùy chọn 6 tháng, sau đó vào lại trang và chọn chuyển sang thanh toán theo năm.

Trang đăng ký sẽ xuất hiện trở lại. Tại đây có thể hiển thị ngày thanh toán là `2028.5.5` (chỉ là ngày ví dụ). Theo tác giả, điều này có nghĩa là chưa phải trả phí ngay, mà đến ngày `2028.5.5` mới phải thanh toán.

Làm tương tự một lần nữa, chuyển sang gói 6 tháng tiếp theo, để đạt tổng thời hạn Google AI Pro 2 năm như hướng dẫn gốc.

![image](https://i0.hdslb.com/bfs/new_dyn/59a750f80e575523398a3cee77f0ae343747579686817540.png@1192w.webp)

> **P.S.**
>
> Cuối cùng, nhất định phải chú ý hủy đăng ký để tránh bị tính phí ngoài ý muốn. Vì gói còn đi kèm YouTube Premium tính phí hằng tháng, nếu không hủy thì tháng sau có thể bị trừ tiền.

![image](https://i0.hdslb.com/bfs/new_dyn/c65340f450d8c110abd88de7f0faa99c3747579686817540.png@1192w.webp)

**Thông tin bổ sung từ thành viên cộng đồng LINUX DO:**

> **Fy6666:**
>
> “Không thể sử dụng YouTube Premium Individual Add On. Bạn có thể đăng ký riêng các sản phẩm khác trong gói này.” Nếu gặp thông báo như vậy thì phải làm sao? Sau khi tìm hiểu, tôi thấy quyền lợi YouTube Premium này chỉ khả dụng tại sáu quốc gia: Mỹ, Canada, Brazil, Pháp, Đức và Nhật Bản.

> **aikavvak12una:**
>
> Nếu khu vực tài khoản không đúng, có thể thêm phương thức thanh toán tại Mỹ trước, rồi đăng ký lại.
>
> Thậm chí có một tài khoản phụ của tôi có khu vực trong điều khoản là Trung Quốc 🤣

Theo ý kiến bổ sung trong bài gốc: chỉ cần thay đổi phương thức thanh toán trên cửa hàng Google Play, không liên quan đến quốc gia của tài khoản Google.

## Phiên bản xử lý hàng loạt

**Bảng điều khiển tự động hóa Google AI Pro (5 TB) với mục tiêu 2 năm không mất phí (US$0.00 → 24 tháng)**

> “Hai năm không mất phí” nêu trên là **mục tiêu của dự án**, không có nghĩa kết quả đăng ký đã được xác minh. Tuyên bố “không bị trừ tiền trong toàn bộ quá trình” của hướng dẫn gốc **không phải sự bảo đảm**. Chi phí và quyền lợi thực tế phụ thuộc vào trang thanh toán và kết quả từ hệ thống cung cấp dịch vụ.

### I. Yêu cầu môi trường

1. Hệ điều hành Windows 10 / 11.
2. Đã cài đặt Google Chrome (có thể dùng đường dẫn cài đặt mặc định).
3. Đã cài đặt Python 3.10 trở lên (khi cài đặt, chọn **Add Python to PATH**).
4. Môi trường mạng: cấu hình proxy khu vực Mỹ (US) trên máy, hoặc nhập mẫu proxy ở bên trái bảng điều khiển.

### II. Khởi chạy nhanh

1. Lần đầu sử dụng, nhấp đúp vào `1_首次运行_安装依赖并启动.bat` (cài đặt thư viện phụ thuộc và khởi chạy).
2. Những lần sử dụng sau, nhấp đúp vào `2_启动控制台.bat` (khởi chạy bảng điều khiển).
3. Trình duyệt sẽ tự động mở trang điều khiển tại: http://127.0.0.1:8765

### III. Nhập thẻ thanh toán tùy chỉnh và hướng dẫn chạy tài khoản

#### 1. Nhập thẻ thanh toán (bắt buộc)

- Trong khu vực **“Cấu hình toàn cục và liên kết thẻ trực tiếp với địa chỉ miễn thuế”** ở bên trái trang web, nhập thông tin thẻ Visa hoặc Mastercard hỗ trợ thanh toán ngoại tệ của bạn:
  - Số thẻ (16 chữ số).
  - Ngày hết hạn (tháng / năm, ví dụ `08 / 29`).
  - Mã bảo mật (CVC gồm 3 chữ số).
  - Họ tên chủ thẻ bằng tiếng Anh.
  - Mã ZIP được điền sẵn là `97201` (Oregon, Mỹ, được hướng dẫn gốc mô tả là bang miễn thuế), không cần thay đổi.
- Sau khi nhập, nhấn **“💾 Lưu cấu hình”**.
- **Lưu ý trong hướng dẫn gốc:** Script được mô tả là có cơ chế bảo vệ nghiêm ngặt để chỉ nhấn đăng ký khi cửa sổ thanh toán xác nhận số tiền `US$0.00`, nhằm tránh bị trừ tiền trong quá trình thực hiện. Đây là mô tả của tác giả, không phải bảo đảm về chi phí thực tế.

#### 2. Nhập hàng loạt tài khoản Google

- Trong khu vực **“Nhập danh sách tài khoản hàng loạt”** bên phải trang web, dán mỗi tài khoản trên một dòng, hỗ trợ các định dạng:
  - `email----mật khẩu----email khôi phục`
  - `email----mật khẩu----email khôi phục----khóa bí mật 2FA`
  - `email----mật khẩu----khóa bí mật 2FA`
- Nhấn **“➕ Nhập danh sách tài khoản”**.

#### 3. Bắt đầu thực thi tự động

- Nhấn **“▶ Thực thi”** ở bên phải một tài khoản, hoặc **“▶ Thực thi tự động hàng loạt”** ở phía trên.
- Theo mô tả của tác giả, script sẽ tự động thực hiện:
  - **Bước 1:** Đăng nhập Google và xác minh qua email khôi phục / 2FA.
  - **Bước 2:** Liên kết thẻ trực tiếp với địa chỉ miễn thuế và sử dụng gói miễn phí 12 tháng đầu (`US$0.00`).
  - **Bước 3:** Cộng thêm lớp ưu đãi 6 tháng thứ hai (`US$0.00` → 18 tháng).
  - **Bước 4:** Cộng thêm lớp ưu đãi 6 tháng thứ ba (`US$0.00` → tối đa 24 tháng).
  - **Bước 5:** Tự động truy cập Google Play để hủy gia hạn, giữ quyền lợi đến hết hạn 2 năm theo mô tả và chụp ảnh màn hình để xác minh.

### IV. Cách ly và dữ liệu nhạy cảm

- Tiện ích trình duyệt nằm trong `extension/`; phiên bản hàng loạt nằm trong `batch/`. Hai phiên bản được lưu trong các thư mục riêng. Script khởi chạy gốc của phiên bản hàng loạt cài đặt các thư viện vào môi trường Python hiện tại, không tạo môi trường ảo riêng; vì vậy **không thể khẳng định các thư viện phụ thuộc được cách ly hoàn toàn**.
- Phiên bản hàng loạt sử dụng thư mục cấu hình trình duyệt riêng cho từng tài khoản, nhưng điều đó **không tương đương máy ảo hoặc môi trường sandbox bảo mật**.
- Mật khẩu tài khoản, khóa bí mật 2FA, thông tin thẻ thanh toán và dữ liệu đăng nhập trình duyệt đều là **thông tin nhạy cảm**. Không được commit cấu hình cục bộ, thư mục hồ sơ trình duyệt, ảnh chụp màn hình, nhật ký và bộ nhớ đệm lên repository.

## Cách sử dụng

- **Tiện ích mở rộng trình duyệt:** Mở trang quản lý tiện ích Chrome, bật chế độ nhà phát triển, chọn **“Load unpacked” (Tải tiện ích đã giải nén)** rồi chọn thư mục `extension`.
- **Phiên bản hàng loạt:** Trên Windows, mở thư mục `batch`. Lần đầu chạy `1_首次运行_安装依赖并启动.bat`; những lần sau chạy `2_启动控制台.bat`.

Hai phiên bản hoạt động độc lập. Đợt sắp xếp ban đầu chỉ bổ sung phân chia thư mục và phần giới thiệu trong README, **không thay đổi mã nguồn dự án**.

Không commit cấu hình tài khoản và thanh toán cục bộ (`config*.json`), tệp biến môi trường, bộ nhớ đệm và dữ liệu phát sinh khi chạy lên repository. Cấu hình của phiên bản hàng loạt phải được nhập trên máy cục bộ.
