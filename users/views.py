from django.urls import reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import logout, authenticate, login
from django.views.generic import FormView
from users import forms


# def login_view(request):
#     if request.method == "GET":
#         pass
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect(resolve_url("products:list"))
#     return render(request, "users/login.html")


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("products:list")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect(resolve_url("users:login"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("products:list")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
