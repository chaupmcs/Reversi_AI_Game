# README

## 1. Cài đặt node.js và npm
### Windows
Tải nodejs về ở đường dẫn sau và cài đặt. [Node download](https://nodejs.org/en/download/stable/)
### Linux
Làm theo hướng dẫn ở trang [này](https://nodejs.org/en/download/package-manager) tùy vào hệ điều hành tương ứng mà cài đặt.
### MacOSX
Cài qua homebrew hoặc sử dụng package từ trang [nodejs](https://nodejs.org/en/download)

## 2. Cài các thư viện cần thiết
Giải nén file ass2_src.zip ra thư mục tương ứng.
> $ unzip ass2_src.zip ass2

Dùng npm để cài các thư viện phụ thuộc
> $ cd ass2 <br>
> $ npm install

## 3. Chạy server
Sau khi đã cài xong thư viện phụ thuộc thì chạy server theo lệnh sau.
> $ node reversiServer.js

Http server sẽ chạy trên localhost:8080. Server sử dụng thư viện socket.io làm giao thức giao tiếp chính. Sinh viên có thể đọc về cách sử dụng thư viện tại [socket.io](http://socket.io/). Xem thêm code và file video demo để rõ cách dùng. Nếu phát hiện ra bug server sinh viên có thể báo lại trên sakai.

## 4. Giao thức chương trình
Các bạn có thể đọc các file trong thư mục __examples/__ để hiểu rõ về các sự kiện (event) các bạn cần xử lý (socket.io là event-based protocol). Các bạn có thể đọc thêm file __public/index.html__ để coi thử một chương trình mẫu (đơn sơ) viết bằng javascript (được nhúng trong file html).

## 5. Các thư viện socket.io cho các ngôn ngữ
* Python SocketIO Client <https://pypi.python.org/pypi/socketIO-client>
* Java Socket.IO Client Library <https://github.com/socketio/socket.io-client-java>
* C++ Socket.IO client <https://github.com/socketio/socket.io-client-cpp>
* .NET (C#) Socket.IO Client Library <https://github.com/Quobject/SocketIoClientDotNet>
* Simple Ruby client for socket.io <https://github.com/shokai/ruby-socket.io-client-simple>
* Swift socket.io-client <https://github.com/nuclearace/Socket.IO-Client-Swift>
* Nodejs socket.io-client <https://www.npmjs.com/package/socket.io-client>

## Lưu ý
Sinh viên lưu ý, assignment bắt buộc làm bằng Python 2.7.
