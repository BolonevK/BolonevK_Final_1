from django import forms
from .models import *

class AddFeedbackForm(forms.Form):
    # class Meta:
    #     model = FeedBack
    #     field = '__all__'
    CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),]
    fb_text = forms.CharField(widget=forms.Textarea(attrs={'cols' : 60, 'rows' : 10}), label="Отзыв")       # текст отзыва
    fb_mark = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Выберите оценку')       # оценка отзыва