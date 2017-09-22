import hashlib
import datetime
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.views.generic import FormView, View

from .models import HealthProfessional, User, ResetPasswordProfile
from .forms import (HealthProfessionalForm,
                    UserLoginForm,
                    ResetPasswordForm,
                    ConfirmPasswordForm)


def register_view(request):
    '''
    Function to register a user in the database.
    '''

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        user.save()
        return render(request, 'message.html', {"message": "usuário registrado"})
    else:
        # Nothing to do.
        pass

    return render(request, "register.html", {"form": form})


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = auth.authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                return self.user_authentication(request, user)
            else:
                return render(request, 'message.html', {"message": "usuário não none"})
        else:
            return render(request, self.template_name, {'form': form})

    def user_authentication(self, request, user):
        if user.is_active:
            auth.login(request, user)
            return redirect('/home')


class ResetPasswordView(FormView):
    '''
    Send an e-mail to reset user password.
    '''
    form_class = ResetPasswordForm
    template_name = 'reset_password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    # Get form information.
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

        # Search the user in database
        try:
            user = User.objects.get(email=email)
        except:
            return render(request, 'message.html', {"message": "usuário não encontrado"})

        # Create a hash with the 'salt' and the user e-mail and send the same to the user.

        try:
            new_profile = self._create_recover_profile(user)

            new_profile.save()

            # Standar e-mail text.
            email_subject = 'Recuperar senha'
            email_body = ('Segue sua chave de ativação http://0.0.0.0:8000/home/reset_confirm/%s.' % new_profile.activation_key)

            send_mail(email_subject,
                      email_body,
                      'medicalprescriptionapp@gmail.com',
                      [email],
                      fail_silently=False)

            messages.success(request,
                             'Verifique a caixa de entrada do seu email para recuperar sua senha.')

            return redirect('/home')
        except:

            messages.error(request, 'um email de recuperação de senha já foi enviado para este endereço!')
            return render(request, 'reset_password.html',
                          {"form": form})
        else:
            # nothing to do
            pass

    # return render(request, 'reset_password.html', {"form": form})

    def _create_recover_profile(self, user):
            email = user.email
            # Create a random sha1 code.
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]

            # Join 'salt' and 'email' to create the activation key.
            activation_key = hashlib.sha1(str(salt+email).encode('utf‌​-8')).hexdigest()

            # Make a expire parameter for the activation key.
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            new_profile = ResetPasswordProfile(user=user,
                                               activation_key=activation_key,
                                               key_expires=key_expires)

            return new_profile


class ConfirmPasswordView(FormView):

    form_class = ConfirmPasswordForm
    template_name = 'password_confirm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, activation_key, *args, **kwargs):

        form = ConfirmPasswordForm(request.POST or None)

        # Get reset object.
        user_profile = get_object_or_404(ResetPasswordProfile, activation_key=activation_key)

        user = user_profile.user

        if(self._validate_activation_key(user_profile) and request.method == 'POST'):

            # Change user password and save in database.
            self._save_user(user, form)
            user_profile.delete()
        else:
            return redirect('/')

        return render(request, 'password_confirm.html', {'form': form})

    def _validate_activation_key(user_profile):
        # Case key expires.
        if(user_profile.key_expires < timezone.now()):
            # key expires.
            user_profile.delete()
            return False
        else:
            return True

    def _save_user(user, form):
        if(form.is_valid()):
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('/')
        else:
            # Nothing to do.
            pass


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/home/login')


def register_health_professional(request):
    form = HealthProfessionalForm()
    context = {
        'form': form
    }
    return render(request, 'register_health_professional.html', context)


def view_health_professional(request):
    health_professionals = HealthProfessional.objects.all()
    context = {
        'health_professionals': health_professionals
    }
    return render(request, 'view_health_professional.html', context)


def edit_health_professional(request):
    return render(request, 'edit_health_professional.html')


def delete_health_professional(request):
    return render(request, 'delete_health_professional.html')
