from django import forms
from .models import *
from django.utils import timezone

class TransaccionForm(forms.ModelForm):
    es_recurrente = forms.BooleanField(
        required=False, 
        label='¿Es recurrente?',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    frecuencia_recurrencia = forms.ChoiceField(
        choices=[
            ('', 'No recurrente'),
            ('DIARIA', 'Diaria'),
            ('SEMANAL', 'Semanal'),
            ('MENSUAL', 'Mensual'),
            ('ANUAL', 'Anual')
        ],
        required=False,
        label='Frecuencia',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion', 'glosa', 'categoria', 'institucion_ahorro', 'fecha']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'glosa': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'institucion_ahorro': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if self.usuario:
            # Configurar queryset y hacer campos opcionales (permitir valor vacío)
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.usuario)
            self.fields['categoria'].required = False
            self.fields['categoria'].empty_label = "--------- (Ninguna)"
            
            self.fields['institucion_ahorro'].queryset = InstitucionAhorro.objects.filter(usuario=self.usuario)
            self.fields['institucion_ahorro'].required = False
            self.fields['institucion_ahorro'].empty_label = "--------- (Ninguna)"
        
        # Establecer fecha actual por defecto
        if not self.instance.pk:
            self.fields['fecha'].initial = timezone.now().date()

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = PresupuestoMensual
        fields = ['mes', 'categoria', 'monto_presupuestado']
        widgets = {
            'mes': forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
            'monto_presupuestado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if self.usuario:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.usuario, tipo='EGRESO')

class ObjetivoAhorroForm(forms.ModelForm):
    class Meta:
        model = ObjetivoAhorro
        fields = ['nombre', 'descripcion', 'monto_objetivo', 'fecha_objetivo', 'institucion_ahorro']
        widgets = {
            'fecha_objetivo': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'monto_objetivo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'institucion_ahorro': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        if self.usuario:
            self.fields['institucion_ahorro'].queryset = InstitucionAhorro.objects.filter(usuario=self.usuario)

class TraspasoForm(forms.Form):
    monto = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    glosa = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    mes_destino = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'month', 'class': 'form-control'},
            format='%Y-%m'
        )
    )
    
    def clean_mes_destino(self):
        mes_destino = self.cleaned_data['mes_destino']
        if mes_destino <= timezone.now().date().replace(day=1):
            raise forms.ValidationError("El mes destino debe ser futuro")
        return mes_destino

# Formulario para agregar/editar categorías
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'tipo', 'color']  # ← QUITAR 'descripcion', AGREGAR 'color'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Comida, Transporte, Salario...'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),  # ← Input de tipo color
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
# Formulario para agregar/editar instituciones de ahorro
class InstitucionAhorroForm(forms.ModelForm):
    class Meta:
        model = InstitucionAhorro
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Banco Estado, Fintual, etc.'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Descripción opcional...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
