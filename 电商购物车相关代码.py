#视图函数：

def cart(request):
    cart = Cart.objects.get(user__username=request.session.get('user')).cartgoods_set.all()
    num = cart.count()
    return render(request, 'cart.html',{'cart':cart,'num':num,
                                        'user': request.session.get('user')})




#HTML 相关代码
<script src="{% static 'jquery-1.12.4.min.js' %}"></script>
    <script>
		$('.add').click(function(){
			// 获取原来的数量
			var n = parseInt($(this).next('.num_show').val())
			// 给数量加1
			$(this).next('.num_show').val(n+1)
			$('.num_show').change()
			// // 获取商品单价
			// price = parseFloat($(this).parent().parent().prev().html()) * 100
			// // 计算小计
			// sum = price * (n+1)
			// // 获取小计的元素并赋值
			// $(this).parent().parent().next().text(sum/100 + '元')
		});
		$('.minus').click(function(){
			var n = parseInt($(this).prev('.num_show').val())
			if(n>0){
				$(this).prev('.num_show').val(n-1)
				$('.num_show').change()
				// // 获取商品单价
				// price = parseFloat($(this).parent().parent().prev().html()) * 100
				// // 计算小计
				// sum = price * (n-1)
				// // 获取小计的元素并赋值
				// $(this).parent().parent().next().text(sum/100 + '元')
			}
		})
		$('.num_show').change(function() {
			// 获取商品单价
			price = parseFloat($(this).parent().parent().prev().html()) * 100
			// 计算小计
			sum = price * $(this).val()
			// 获取小计的元素并赋值
			$(this).parent().parent().next().text((sum/100).toFixed(2) + '元')

			// 计算总价
			var total = 0
			$('.col07').each(function(i, el){
				if($(this).parents('ul').find('.select').get(0).checked) {
					total += parseFloat($(el).text()) * 100
				}
			})
			$('#total').text((total/100).toFixed(2))
		})

		// 选择框改变，处理价格和数量计算
		$('.select').change(function() {
			n = parseInt($('#count').text())
			if(this.checked) {
				$('#count').text(n+1)
			} else {
				if(n > 0){
					$('#count').text(n-1)
				}
			}
			$('.num_show').change()
		})
		// 点击全选，计算价格和数量
		$('#selectAll').change(function(){
			checked = this.checked
			$('.select').each(function(i,el){
				el.checked = checked
			})
			$('.select').change()
		})
    </script>
