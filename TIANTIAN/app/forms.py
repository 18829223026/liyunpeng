from django.forms import ModelForm, widgets
from django import forms
from .models import User

"""
form 表单主要实现的功能：
1. 可以生成模板中的相应的表单控件标签
2. 对表单中填写的数据进行相应规则的验证
3. 验证不通过的非法数据进行错误提示并显示在模板中
form 表单的实现流程：
1. 根据需要的表单字段定义Form类
   a. 如果表单上的数据不是模型中的数据，则form类继承django.forms.Form类
   b. 如果表单上的数据是模型中的字段，则form类继承django.forms.ModelForm类
2. 定义Form类中的字段
   a. 如果是非模型Form，字段的定义方式与模型字段的定义方式基本一致
   b. 如果是模型Form，通过Meta类指定对应的模型类以及使用的模型字段
   c. 字段定义中，通过validators属性指定验证规则以及错误提示信息内容
3. 在视图中根据请求方式：
   a. 如果是get请求表单页面，则实例化一个空的Form对象，并传入模板中，在模板中
      输出该对象即可得到表单的控件标签
   b. 如果是post请求提交表单数据，则使用post数据实例化一个Form对象，然后调用
      form对象的is_valid()方法验证数据，该方法返回True则验证通过，否则验证
      失败
   c. 如果验证失败，再把form对象返回客户端浏览器，则展示带有错误提示的表单
      如果验证通过，通过form.cleaned_data属性可以得到表单数据的一个字典
      通过该属性获取数据继续后面的操作
"""


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': widgets.TextInput(attrs={'class': 'name_input', 'placeholder': '请输入用户名'}),
            'password': widgets.PasswordInput(attrs={'class': 'pass_input', 'placeholder': '请输入密码'})
        }


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    password2 = forms.CharField(max_length=10, label='确认密码')
