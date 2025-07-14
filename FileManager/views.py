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
from Form.models import FormFieldValues, WorkflowVersion
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

from Workflow.models import history_workflow_details, workflow_action_master, workflow_details, workflow_matrix
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
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

@login_required
def get_module_data(request):
    client = request.GET.get('client')
    department = request.GET.get('dept')
    module = request.GET.get('module')
    data_type = request.GET.get('type')
    
    if request.user.is_authenticated:
        user = request.user.id    
        role_id = str(request.user.role_id)

    # Add type-specific data
    if data_type == "documents":
        sf = request.GET.get('sf', '')
        file_name = callproc("stp_get_dropdown_values",['file_name']) 
        if sf == '' or None:
           sf =  file_name[0][0]   
        header = callproc("stp_get_masters", ['fm_doc', 'i', 'header',user])
        rows = callproc("stp_get_masters",['fm_doc','i','data',user])
        data = rows
        context = {'client': client,'department': department,'module': module,'data_type': data_type,'file_name':file_name,'header':header,'data':data}

    elif data_type == "metadata":
        sf = request.GET.get('sf', '')
        forms = callproc("stp_get_forms",['view_form',user])  
        if sf == '' or None:
           sf =  forms[0][0]   
        header = callproc("stp_get_view_form_header",[sf])          
        rows = callproc("stp_get_view_forms",[sf])
        data = []
        for row in rows:
            encrypted_id = enc(str(row[0]))
            data.append((encrypted_id,) + row[1:])
        context = {'client': client,'department': department,'module': module,'data_type': data_type,'forms':forms,'header':header,'data':data}

    elif data_type == "workflow":
        WFIndexdata = wf_list(request,user,role_id)
        context = {'client': client,'department': department,'module': module,'data_type': data_type,'WFIndexdata': WFIndexdata}
    
    return render(request, "FileManager/_partial_data.html", context)



def wf_list(request,user,role_id):  
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()


    workflow_para = "CIDCO File Scanning and DMS Flow"
    param = [workflow_para]
    
    workflow_value = roles.objects.filter(id=role_id).values_list('workflow_view', flat=True).first()

    reference_workflow_status = request.GET.get("reference_workflow_status")


    cursor.callproc("stp_getdataWorkflowIndex")
    WFIndexdata_raw = []
    for result in cursor.stored_results():
        WFIndexdata_raw = result.fetchall()

    latest_steps = {}
    for item in WFIndexdata_raw:
        req_num = item[0]        # request number
        increment_id = item[6]   # increment_id column (adjust index if different)  
        if req_num not in latest_steps or increment_id > latest_steps[req_num][6]:
            latest_steps[req_num] = item
    WFIndexdata_raw = list(latest_steps.values())

    # 2. Get ALL steps from matrix (the workflow path)
    cursor.callproc("stp_checkRoleForWorkflow", param)
    workflow_steps = []
    for result in cursor.stored_results():
        raw_steps = result.fetchall()

    for row in raw_steps:
        workflow_steps.append({
            'id': row[0],
            'step_name': row[1],
            'role_ids': [r.strip() for r in row[2].split(',')],
            'form_id': row[3],
            'but_type': row[4],
            'but_act': row[5],
            'status': row[6],
            'color_status': row[8],
            'step_id_flow': str(row[7]) if row[7] else None  
            
        })

    # Map of step_id to step info for quick lookup
    step_roles_map = {
        str(step['id']): step
        for step in workflow_steps
    }

    WFIndexdata = [] 
    
    # for handling involves person
    step_roles_map = {}
    for step in workflow_steps:
        step_roles_map[str(step['id'])] = step

    for item in WFIndexdata_raw:
        step_id_str = str(item[3])
        
        # to get edit or create
        req_num = item[0]    
               
        detail = workflow_details.objects.get(req_id=req_num)
        current_EditCrtStep = detail.step_id
        editcrt = current_EditCrtStep + 1
        next_step = current_EditCrtStep + 1
        
        try:
            form_data = history_workflow_details.objects.filter(
                req_id=req_num,
                step_id=1
            ).values_list('form_data_id', flat=True).first()

            if form_data:
                file_number = FormFieldValues.objects.filter(
                    form_data_id=form_data
                ).order_by('id').values_list('value', flat=True).first()
            else:
                    file_number = None
        except Exception as e:
            file_number = None
        
        try:
            next_matrix_entry = workflow_matrix.objects.get(id=next_step)
            forwarded_to_role = next_matrix_entry.role_id  
            
            #next_matrix_role1 = roles.objects.get(id=forwarded_to_role)
            #next_matrix_role = next_matrix_role1.role_name
            
            role_ids = [int(role_id.strip()) for role_id in forwarded_to_role.split(',')]
            role_names = roles.objects.filter(id__in=role_ids).values_list('role_name', flat=True)
            forwarded_to_display = ', '.join(role_names)
        except workflow_matrix.DoesNotExist:
            forwarded_to_display = "N/A"
        
            
        try:
            editORcreate = workflow_matrix.objects.get(id=editcrt).button_act_details
        except workflow_matrix.DoesNotExist:
            editORcreate = ''
        # editORcreate = workflow_matrix.objects.get(id=editcrt).button_act_details
        formDataId_Status= item[7]
        #revised_Status = VersionControlFileMap.objects.filter(form_data=formDataId_Status)
        revised_Status = WorkflowVersion.objects.filter(req_id=req_num).exclude(version=1)
        #revised_Status = WorkflowVersionControl.objects.filter(form_data_id=formDataId_Status).exclude(temp_version=1)
        rejectedCheckWF=None
        if revised_Status.exists():
            status = f"{item[1]}<br>Revised"
            rejectedCheckWF="rejectedCheck"
        else:
            status = item[1]
        form_data_id= enc(str(item[7]))
        updated_by= item[9]
        updated_at= item[10]
        
        latest_entry = history_workflow_details.objects.filter(
        req_id=req_num
        ).order_by('-id').first()  # latest entry, could be reject or forward

        if latest_entry and latest_entry.sent_back == '1':
            last_rejected_step = latest_entry.step_id
            last_rejected_status = latest_entry.status
            if rejectedCheckWF:
                status = f"{status}-Rejected"
            else:
                status = f"{status}<br>Rejected"
        else:
            last_rejected_step = None
            last_rejected_status = None
            
        current_step_info = step_roles_map.get(step_id_str)

        # Init vars
        include_for_current_user = False
        next_step_name = ''
        next_step_id = None
        
        
        if not current_step_info:
            continue

        current_step_flow = int(current_step_info['step_id_flow']) if current_step_info['step_id_flow'].isdigit() else None
        if current_step_flow is None:
            continue
        
        if role_id == '2':
            operator_user_id = item[8]  # item[8] is operator column
            if operator_user_id is None or operator_user_id != user:
                continue  # Skip this row if it's not assigned to the current operator
    
        for step in workflow_steps:
            step_flow = int(step['step_id_flow']) if step['step_id_flow'].isdigit() else None
            if step_flow is not None and step_flow <= current_step_flow:
                if role_id in step['role_ids']:
                    include_for_current_user = True
                    break
                
        next_flow_id = current_step_flow + 1
        for step in workflow_steps:
            if step.get('step_id_flow') and step['step_id_flow'].isdigit():
                if int(step['step_id_flow']) == next_flow_id:
                    next_step_name = step['step_name']
                    next_step_id = enc(str(step['id']))

                    if role_id in step['role_ids']:
                        include_for_current_user = True  # Show to next step user too
                    
                    break
          
        user_prev_step = None
        for step in workflow_steps:
            if role_id in step['role_ids']:
                user_prev_step = step
                break

        if last_rejected_step is not None and user_prev_step and user_prev_step.get('id') == last_rejected_step - 1:
            extra_flag = 'edit_again'
        else:
            extra_flag = 'view_only'
        
        if include_for_current_user:
            user_prev_step_id_val = user_prev_step['id'] if user_prev_step else ''
            WFIndexdata.append({
                "req_num": item[0],
                "status": status,
                "id_wfd": item[2],
                "step_id": item[3],
                "enc_id_wfd": enc(str(item[2])),
                "created_by": item[4],
                "created_at": item[5],
                "increment_id": item[6],
                "operator_email": item[11],
                "step_name": current_step_info['step_name'] if current_step_info else '',
                "form_id": current_step_info['form_id'] if current_step_info else '',
                "but_type": current_step_info['but_type'] if current_step_info else '',
                "but_act": current_step_info['but_act'] if current_step_info else '',
                "color_status": current_step_info['color_status'] if current_step_info else '',
                "idEncrypt": enc(str(current_step_info['id'])) if current_step_info else '',
               "form_data_id":form_data_id,
               "editORcreate":editORcreate,
               "reference_workflow_status":reference_workflow_status,
               
                "next_step_name": next_step_name if next_step_name else 'No next step',
                "next_step_id": next_step_id,
                "increment_idCheck": item[6] + 1,
                # "user_prev_step_id": user_prev_step['id'] if user_prev_step else '',
                "user_prev_step_id": enc(str(user_prev_step_id_val)) if user_prev_step_id_val != '' else '',
                 "user_prev_step_Check":user_prev_step_id_val,
                 "updated_at":updated_at,"updated_by":updated_by,
                "user_prev_step_name": user_prev_step['step_name'] if user_prev_step else '',
                "include_for_current_user": include_for_current_user,
                "last_rejected_step": last_rejected_step,
                "last_rejected_status": last_rejected_status,"file_number":file_number,
                'extra_flag': extra_flag,"next_matrix_role":forwarded_to_display,"workflow_value":workflow_value,
            })
            if last_rejected_step is not None:
                # This is where the backend resets rejection
                last_rejected_step = None
                last_rejected_status = None
            
    first_step = workflow_steps[0] if workflow_steps else None
    show_top_button = False
    top_button_context = {}

    if first_step and role_id in first_step['role_ids']:
        show_top_button = True
        top_button_context = {
            'step_name': first_step['step_name'],
            'form_id': first_step['form_id'],
            'but_type': first_step['but_type'],
            'but_act': first_step['but_act'],
            'id_firstStep': first_step['id'],
            'encid_FS': enc(str(first_step['id']))
               
        }
    if show_top_button == True:
        firstStep = '1'
    else:
        firstStep = '0'
    
    return WFIndexdata
