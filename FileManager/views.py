import json
import pydoc
import re
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout,get_user_model
from Account.forms import RegistrationForm
from Account.models import *
from FileManager.models import client_module
from Masters.models import *
import Db 
import bcrypt
from django.contrib.auth.decorators import login_required
from WorkDocX.encryption import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from Account.utils import decrypt_email, encrypt_email
import requests
import traceback
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
import openpyxl
from openpyxl.styles import Font, Border, Side
import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
from Account.models import *
from Masters.models import *
from Account.db_utils import callproc
from django.views.decorators.csrf import csrf_exempt
import os
from django.urls import reverse
from WorkDocX.settings import *
import logging
from django.http import FileResponse, Http404
import mimetypes

from Workflow.models import workflow_action_master, workflow_matrix
logger = logging.getLogger(__name__)

# Create your views here.

def file_manager(request):
    # Get all client_module data and organize it hierarchically
    all_data = client_module.objects.all()
    
    # Create hierarchical structure
    clients = {}
    for item in all_data:
        if item.client not in clients:
            clients[item.client] = {'departments': {}}
        
        if item.department not in clients[item.client]['departments']:
            clients[item.client]['departments'][item.department] = {'modules': []}
            
        clients[item.client]['departments'][item.department]['modules'].append({
            'module': item.module,
            'status': item.status
        })
    
    # Convert to list format for template
    clients_list = [
        {
            'client': client,
            'departments': [
                {
                    'department': dept,
                    'modules': data['modules']
                }
                for dept, data in client_data['departments'].items()
            ]
        }
        for client, client_data in clients.items()
    ]
    return render(request, 'FileManager/file_manager.html', {'clients': clients_list})