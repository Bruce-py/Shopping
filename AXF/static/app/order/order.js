$(function () {

    //支付
    /*支付宝，1.先以企业为单位申请使用支付宝，申请成功给一个商户id
    2.在支付宝创建应用（说明用途），生成appid
    3.点击支付按钮，需要提交信息（包括订单号，订单金额，订单名称，回调url）
    当支付结束（成功或者失败），支付宝自动调用回调url，并把支付结果告诉你的服务器端


     */

    //伪支付
    $('#pay').click(function () {

        //支付

        //支付完成，需要把订单状态改变
        var orderid = $(this).attr('orderid');
        var that = this;
        $.post('/axf/order_change_status/', {orderid: orderid, status: '1'}, function (data) {

            if (data.status == 1) {

                console.log(data.msg);
                $(that).html('支付成功');

                //location.href = '/axf/order_unpay/'

            }
            else {
                console.log(data.msg)
            }


        });

    });

});