import json
import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django import forms
from json import loads
from .models import *
from datetime import date, timedelta, datetime




def base_context(request, **args):
    context = {}
    user = request.user

    context['title'] = 'none'
    context['header'] = 'none'
    context['error'] = 0

    if args != None:
        for arg in args:
            context[arg] = args[arg]
    return context


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home')

        context["mails"] = []
        for mail in os.listdir("Z:/Progs/Nezrena/Nezrena/NezrenaApp/modules/node_modules/MailModule/mail/in"):
            mail_content = ""
            with open("Z:/Progs/Nezrena/Nezrena/NezrenaApp/modules/node_modules/MailModule/mail/in/"+mail+"/mail.json", "r", encoding="UTF8") as mail:
                mail_content = mail.read()
            try:
                json_content = json.loads(mail_content)['messageHtml']
            except:
                json_content = json.loads(mail_content)['message']
            context['mails'].append(json_content)
        return render(request, "home.html", context)



class SettingsPage(View):
    def get(self, request):
        context = base_context(request, title='Home')
        settings_txt = ""
        with open("./NezrenaApp/modules/common/settings.json", "r", encoding="UTF8") as mail:
                settings_txt = mail.read()

        context["settings"] = json.loads(settings_txt)

        return render(request, "settings.html", context)

    def post(self, request):
        form_data = request.POST
        context = base_context(request, title='Home')
        mails_folder_path = form_data['mails_folder_path']
        text_analyzer_path = form_data['text_analyzer_path']
        text_parser_path = form_data['text_parser_path']
        settings_txt = ""
        with open("./NezrenaApp/modules/common/settings.json", "r", encoding="UTF8") as mail:
                settings_txt = mail.read()

        context["settings"] = json.loads(settings_txt)

        settings_json = {
            "paths": {
                "mails_folder_path": mails_folder_path,
                "text_analyzer_path" : text_analyzer_path,
			    "text_parser_path" : text_parser_path
            }
        }
        
        json.dump(settings_json, open("./NezrenaApp/modules/common/settings.json", "w"), indent = 6)

        return HttpResponseRedirect('./')
