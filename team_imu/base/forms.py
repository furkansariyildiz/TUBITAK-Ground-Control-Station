from django import forms
from .models import Result, PhotoModel
from PIL import Image
from django.core.files import File

#modellerden form oluşturuldu.
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,label="Kullanıcı Adı")
    password = forms.CharField(max_length=20,label="Parola",widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20,label="Parola Onayı",widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if(password and confirm_password and password != confirm_password):
            raise forms.ValidationError(message="Parolalar eşleşmiyor!")

        values = {
            "username":username,
            "password":password,
            "confirm_password":confirm_password,
        }
        return values

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label ="Parola",widget=forms.PasswordInput)

class ResultForm(forms.ModelForm):
    x = forms.FloatField(widget = forms.HiddenInput())
    y = forms.FloatField(widget = forms.HiddenInput())
    width = forms.FloatField(widget = forms.HiddenInput())
    height = forms.FloatField(widget = forms.HiddenInput())
    class Meta:
        model = Result
        fields =  "__all__" 
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        photo = super(ResultForm,self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        
        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200,200),Image.ANTIALIAS)
        resized_image.save(photo.file.path)
        return photo

class PhotoForm(forms.ModelForm):
    img=forms.ImageField()
    class Meta:
        model = PhotoModel
        fields = "__all__"
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


    
