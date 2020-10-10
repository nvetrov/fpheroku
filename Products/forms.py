from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from .models import FoundGoods, Catalog
# import q
# from bootstrap_datepicker_plus import DatePickerInput

from django.core.exceptions import ValidationError


class UpdateProductForm(forms.ModelForm):
    lm_code = forms.TextInput()

    class Meta:
        model = FoundGoods
        exclude = ['shop_num', 'user']
        fields = ['bar_code', 'lm_code', 'caption', 'amount_goods', 'note_add', 'shop_num', 'user', 'update_at']

        widgets = {
            'bar_code': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'lm_code': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'amount_goods': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'note_add': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'shop_num': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'user': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'update_at': forms.DateInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'type': "date"})
        }


class ProductForm(forms.ModelForm):
    # bar_code = forms.IntegerField(label='ШтрихКод', error_messages={'required': 'ШК или ЛМ'})
    lm_code = forms.TextInput()
    caption = forms.TextInput()
    amount_goods = forms.NumberInput()
    note_add = forms.TextInput
    shop_num = forms.NumberInput()
    user = forms.TextInput()
    update_at = forms.DateField(required=False)

    class Meta:
        model = FoundGoods
        fields = ['bar_code', 'lm_code', 'caption', 'amount_goods', 'note_add', 'shop_num', 'user']
        # labels = {
        #     'bar_code': _('ШтрихКод'),
        #     'lm_code': _('ЛМ'),
        #     'caption': _('Название'),
        #     'amount_goods': _('Количество'),
        # }
        # help_texts = {
        #     'bar_code': _('штрих-код или лм код'),
        # }
        # error_messages = {
        #     'bar_code': {
        #         'required': _("Заполните поле ."),
        #     },
        #     'lm_code': {
        #         'required': _("Заполните поле")
        #     }
        # }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProductForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        form = super(ProductForm, self).save(commit=False)
        # do custom
        self.instance.user_id = CustomUser.objects.get(email=self.user).id  # None
        self.instance.shop_num = CustomUser.objects.get(email=self.user).shop_num  # None
        if commit:
            form.save()
        return form

    def clean_amount_goods(self):
        amount_goods = self.cleaned_data.get("amount_goods")
        if 0 >= amount_goods:
            # print('true', amount_goods)
            print('Недопустимое значение в количестве')
            raise forms.ValidationError("Недопустимое значение в количестве")
        elif 100 <= amount_goods:
            # print('true', amount_goods)
            raise forms.ValidationError("Недопустимое значение в количестве")
        return amount_goods

    def clean_bar_code(self):
        bar_code = self.cleaned_data.get("bar_code")
        if not (str(bar_code).isdigit()):
            raise ValidationError('Только цифры')
        return bar_code

    def clean_update_at(self):
        update_at = self.cleaned_data.get("update_at")
        # qs = Catalog.objects.filter(ean=self.cleaned_data.get("bar_code"))
        # if qs.exists:
        #     q(qs.values)
        # if update_at is None:
        #     raise forms.ValidationError("Дата не выбрана")
        return update_at

    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(f'clean(self)')


class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['ean', 'lm', 'product_name']
        widgets = {
            'bar_code': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'lm_code': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        }

    def clean_bar_code(self):
        bar_code = self.cleaned_data.get("bar_code")
        if not (str(bar_code).isdigit()):
            raise ValidationError('Только цифры')
        return bar_code

# class CreateForm(UpdateView):
#     form_class = ProductForm
#     success_url = '/'
#     template_name = 'products/login.html'
#
#     def from_valid(self, form):
#         request = self.request
#


#
# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
