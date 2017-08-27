# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request,'core_app/index.html')