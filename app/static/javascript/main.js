document.getElementById('loginForm').addEventListener('submit', function(event){
    event.preventDefault();
    // Thêm logic xử lý đăng nhập ở đây
    alert('Đăng nhập');
});


// Hiện thị hợp thoại thông báo khi nhân viên quên mật khẩu
document.getElementById('forgotPassword').addEventListener('click', function(e) {
    e.preventDefault(); // Ngăn không cho trình duyệt thực hiện hành động mặc định khi click vào liên kết
    alert('Hãy liên hệ với admin để cấp lại mật khẩu.');
});