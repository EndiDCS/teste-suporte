from django.forms import ModelForm
from .models import Info,Voto

class InfoForm(ModelForm):
    class Meta:
        model = Info
        fields = ['information','is_true']
        labels = {
            'information': ('Informação:'),
            'is_true': ('Verdade'),
        }
        help_texts = {
            'is_true': ('Marque caso a sua informação seja verdadeira, caso seja falsa deixe desmarcado.'),
        }


class VotoForm(ModelForm):
    class Meta:
        model = Voto
        fields = ['is_true','info']
