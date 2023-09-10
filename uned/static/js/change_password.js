function changePassword() {
    var password1 = document.getElementById('new_password_1').value;
    var password2 = document.getElementById('new_password_2').value;
    var old_password = document.getElementById('old_password').value;

    $.ajax({
        url: document.referrer + "uned/change_password/",
        type: "POST",
        data: {
          "new_password_1": password1,
          "new_password_2": password2,
          "old_password": old_password,
        },
        success: function(response) {
          console.log(response);
          if(response == 1) {
            alert('Password changed successfully');
            setTimeout(function() {
              window.location.href = document.referrer + "uned/login/";
            }, 1000);
          } else {
            alert('Error!');
          }
        }
      });
}
