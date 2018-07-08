$(function () {
    //+按钮
    isAllselect();
    calculatePrice();
    $('.add').click(function () {
        //1.ajax请求服务器，让服务器改变数量
        //2.如果服务器修改成功，再修改浏览中数据

        //获取cartid
        var cartid = $(this).parents('li').attr('cartid');
        var that = this;

        $.get('/axf/cart_num_add/', {cartid: cartid}, function (data) {
            console.log(data);

            if (data.status == 1) {
                //location.reload  刷新当前页面
                $(that).prev().html(data.num)
            }

            //调用，计算总价
            calculatePrice();


        });
    });

    //-按钮
    $('.reduce').click(function () {

        var cartid = $(this).parents('li').attr('cartid');
        var that = this;

        //ajax
        $.post('/axf/cart_num_reduce/', {cartid: cartid}, function (data) {

            console.log(data);

            if (data.status == 1) {

                $(that).next().html(data.num)
            }
            else if (data.status == -1) {

                location.assign('/axf/login/')
            }
            else {
                console.log(data.msg)
            }

            //调用，计算总价
            calculatePrice();


        });


    });


    //删除按钮
    $('.delbtn').click(function () {

        var cartid = $(this).parents('li').attr('cartid');
        var that = this;
        $.post('/axf/cart_num_del/', {cartid: cartid}, function (data) {

            if (data.status == 1) {
                console.log(data);
                $(that).parents('li').remove()
            }
            else if (data.status == 0) {
                location.assign('/axf/login/')
            }
            else {
                console.log(data.msg)
            }
            //调用，计算总价
            calculatePrice();
            isAllselect();


        });


    });


    //单个商品勾选/取消
    $('.select').click(function () {

        var cartid = $(this).parents('li').attr('cartid');

        var that = this;

        $.post('/axf/cart_select/', {cartid: cartid}, function (data) {

            console.log(data);
            if (data.status == 1) {
                $(that).find('span').html(data.select ? '✔' : '');
            }

            //调用，计算总价
            calculatePrice();
            isAllselect();

        });

    });

    //全选按钮
    $('#allselect').click(function () {

        //先判断 全选还是取消全选
        //1.如果有未勾选 则全选
        //2.如果都勾选，则取消全选
        var select = [];//保存勾选的商品所在的cartid
        var unselect = []; //保存未勾选的商品所在购物车的cartid

        //遍历购物车所有商品节点,each实现遍历所有节点
        $('.menuList').each(function () {

            var isSelect = $(this).find('.select').children('span').html();
            if (isSelect) {
                select.push($(this).attr('cartid'));
            }
            else {
                unselect.push($(this).attr('cartid'));
            }

        });


        //取消全选
        if (unselect.length == 0) {
            //ajax
            $.post('/axf/cart_allselect/', {action: true}, function (data) {
                console.log(data);

                if (data.status == 1) {
                    //location.reload()
                    $('.select').find('span').html('');

                }
                else if (data.status == 0) {
                    location.href = '/axf/login/'
                }
                else {
                    console.log(data.msg)
                }


                //调用，全选按钮打钩
                isAllselect();
                //调用，计算总价
                calculatePrice();
            })

        }

        //全选
        else {
            //ajax
            $.post('/axf/cart_allselect/', {action: false}, function (data) {
                console.log(data);
                //location.reload()
                $('.select').find('span').html('✔');
                //$('#allselect').find('span').html('✔')


                //
                isAllselect();
                //调用，计算总价
                calculatePrice();

            })
        }

    });

    //全选打钩函数
    isAllselect();
    function isAllselect() {
        var s = 0;
        $('.select').each(function () {

            if ($(this).find('span').html()) {

                s++
            }

        });

        if (s == $('.select').length) {
            $('#allselect').find('span').html('✔')
        }
        else {
            $('#allselect').find('span').html('')
        }
    }


    //计算总价函数
    function calculatePrice() {

        //计算总价
        var total = 0;
        $('.menuList').each(function () {

            //如果勾选
            if ($(this).find('.select').children('span').html()) {

                var price = $(this).find('.price').html();
                var num = $(this).find('.num').html();
                total += parseFloat(price) * parseInt(num);
                //console.log(total)

            }
        });
        //显示总价
        $('#totalPrice').html(total.toFixed(2))
    }


    //结算
    $('#settlement').click(function () {

        $.post('/axf/order_add/', function (data) {

            //console.log(data);

            if (data.status == 1) {

                location.href = '/axf/order/' + data.orderid + '/'
            }
            else if(data.status == -2){
                //console.log(data.msg);
                location.href='/axf/market/'
            }

            else {
                //console.log(data.msg)
            }

        });

    });

});