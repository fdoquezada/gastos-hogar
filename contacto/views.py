from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm
from .models import Contacto

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Guardar el mensaje en la base de datos
            contacto = form.save()
            
            # Enviar correo electrónico
            subject = f'Nuevo mensaje de contacto: {contacto.asunto}'
            message = f'''
            Nombre: {contacto.nombre}
            Email: {contacto.email}
            Asunto: {contacto.asunto}
            
            Mensaje:
            {contacto.mensaje}
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],  # Enviar a tu correo
                    fail_silently=False,
                )
                messages.success(request, '¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.')
            except Exception as e:
                messages.error(request, 'Hubo un error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde.')
            
            return redirect('contacto:contacto')
    else:
        form = ContactoForm()
    
    return render(request, 'contacto/contacto.html', {'form': form})

