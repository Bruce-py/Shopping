$(function () {

    var flag1 = false; //表示用户名是否合法
    var flag2 = false; //表示用户密码是否合法
    var flag3 = false; //表示用户确认密码是否合法
    var flag4 = false; //表示邮箱是否合法



    //1.用户名
    $('#username').change(function () {

        var username = $(this).val();

        if (/^[a-zA-Z_]\w{5,17}$/.test(username)){

            flag1 = true;

            $('#msg_username').html('用户名格式正确 ✔').css('color','green');

            //ajax判断
            //如果用户名匹配正则，检查数据库中用户名是否已存在
            $.get('/axf/check_username/',{username:$('#username').val()},function (data) {

                if(data.status == 1){
                    $('#msg').html(data.msg).css('color','green')
                }

                else if(data.status ==0){
                    $('#msg').html(data.msg).css('color','orange')

                }
                else if(data.status ==-1){
                    $('#msg').html(data.msg).css('color','red')

                }
            });

        }
        else {
            flag1 =false;
            $('#msg_username').html('用户名输入错误 ✘').css('color','red')
        }

    });


    //2.密码正则
    $('#password').change(function () {
        var password = $(this).val();
        if(/^.{8,}$/.test(password)) {
            //console.log('密码输入合法')
            flag2 = true;
            $('#msg_password').html('密码格式正确 ✔').css('color','green');
        }

        else {
            //console.log('密码不一致')
            flag2 = false;
            $('#msg_password').html('密码格式错误 ✘').css('color','red');
        }
    });

    //3.确认密码
    $('#repassword').change(function () {

        var password = $('#password').val();
        var repassword = $('#repassword').val();
        if(password == repassword){
            //console.log('密码正确')
            flag3 = true;
            $('#msg_repassword').html('密码确认正确 ✔').css('color','green');
        }

        else {
            //console.log('密码错误')
            flag3 = false;
            $('#msg_repassword').html('密码确认错误 ✘').css('color','red');
        }
    });


    //4.邮箱正则
    $('#email').change(function () {

        var email = $(this).val();

        if(/^.*@\w*\..*$/.test(email)){
            flag4 = true;
            $('#msg_email').html('邮箱格式正确 ✔').css('color','green');
            //console.log('邮箱正确')

        }
        else{
            flag4 = false;
             $('#msg_email').html('邮箱格式错误 ✘').css('color','red');
            //console.log('邮箱错误')
        }
    });


    //5.点击注册按钮-提交
    $('#register').click(function () {
        //  如果所有输入框都合法，可以提交注册
        //如果有输入不合法，不可以提交
        if(flag1 && flag2 && flag3 && flag4){

            console.log('所有都合法');
            //提交的密码 进行 mad5加密
            $('#password').val(md5($('#password').val()));
            $('#repassword').val(md5($('#repassword').val()));

            return true
        }

    })


});