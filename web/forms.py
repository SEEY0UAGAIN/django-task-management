from django import forms
from django.contrib.auth.models import User
from .models import Task, Product, Reservation, Group , Member
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        labels = {
            'name': 'ชื่อสินค้า',
            'price': 'ราคา',
            'description': 'รายละเอียด',
            'image': 'รูปภาพ',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ReservationForm(forms.ModelForm):
    reserved_date = forms.DateField(widget=forms.TextInput(attrs={'id': 'datepicker'}))

    class Meta:
        model = Reservation
        fields = ['reserved_date']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class MemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select User",
        widget=forms.Select,
        empty_label="---------",
    )

    class Meta:
        model = Member
        fields = ['user', 'group', 'is_leader']
        widgets = {
            'group': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['group'].widget = forms.HiddenInput()
        self.fields['user'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        
        if group:
            # กรองผู้ใช้ที่ยังไม่มีการเชื่อมโยงกับกลุ่มใดๆ
            existing_members = Member.objects.values_list('user', flat=True)
            self.fields['user'].queryset = User.objects.exclude(id__in=existing_members)


class UserFilterForm(forms.Form):
    user_id = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='เลือกผู้ใช้',
        empty_label='-- ทั้งหมด --',
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit();'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

class UserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label=_('อีเมล'),
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('ชื่อจริง'),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('นามสกุล'),
    )
    password1 = forms.CharField(
        label=_('รหัสผ่าน'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_('รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร และไม่สามารถเป็นรหัสผ่านที่ใช้บ่อยได้.'),
    )
    password2 = forms.CharField(
        label=_('ยืนยันรหัสผ่าน'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_('กรุณาป้อนรหัสผ่านเดียวกันอีกครั้ง เพื่อยืนยัน.'),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': _('อีเมล'),
            'first_name': _('ชื่อจริง'),
            'last_name': _('นามสกุล'),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')  # กำหนด username ด้วย email
        if commit:
            user.save()
        return user
    
class UserEditForm(UserChangeForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label=_('อีเมล'),
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('ชื่อจริง'),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_('นามสกุล'),
    )
    password = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        label=_('รหัสผ่าน')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        labels = {
            'username': _('ชื่อผู้ใช้'),
            'email': _('อีเมล'),
            'first_name': _('ชื่อจริง'),
            'last_name': _('นามสกุล'),
            'password': _('รหัสผ่าน'),
        }
