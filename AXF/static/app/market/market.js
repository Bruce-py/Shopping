$(function () {

    //1.全部类型
    $('#all_type').click(function () {
        //切换
        $('#all_type_container').toggle();
        //切换icon的down/up
        $('#all_type_icon').toggleClass('glyphicon glyphicon-chevron-down').addClass('glyphicon glyphicon-chevron-up');

        //主动触发('#sort_rule_container')的click事件
        $('#sort_rule_container').trigger('click');
    });

    //全部类型-半透明区域加点击隐藏
    $('#all_type_container').click(function () {

        $(this).hide();
        $('#all_type_icon').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');

    });


    //2.排序规则
    $('#sort_rule').click(function () {
                //切换
        $('#sort_rule_container').toggle();
        //切换icon的down/up
        $('#sort_rule_icon').toggleClass('glyphicon glyphicon-chevron-down').addClass('glyphicon glyphicon-chevron-up');

        //主动触发
        $('#all_type_container').trigger('click');

    });

    //排序-半透明区
    $('#sort_rule_container').click(function () {

        $(this).hide();
        $('#sort_rule_icon').removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down');
    });



    //3.加入购物车
    $('.addtocart').click(function () {

        //先得到加入购物车的商品id
        var goodsid = $(this).attr('goodsid');

        //数量
        var num = parseInt($(this).prev().find('.num').html());
        //ajax请求
        $.get('/axf/cart_add/',{goodsid:goodsid,num:num},function (data) {
            console.log(data);

            //登录成功
            if(data.status==1){

            }
            //未登录,跳转登录
            else if(data.status==0){
                location.href('/axf/login/');

            }
        })

    });

    //+ 点击事件
    $('.add').click(function () {
        // var index = $(this).index('#add');
        // var num = $('.num').eq(index);
        // num.htmlparseInt((num.html()+1))
        var num = parseInt($(this).prev().html());
        $(this).prev().html(num+1)

    });
    //-
    $('.reduce').click(function () {
        var num = parseInt($(this).next().html());
        if(num>1){
            $(this).next().html(num-1)

        }


    })

});



