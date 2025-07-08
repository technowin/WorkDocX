import json
import pydoc
import re
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout,get_user_model
from Account.forms import RegistrationForm
from Account.models import *
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


# utils/ocr_utils.py

import pytesseract
from pdf2image import convert_from_path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import tempfile
import string

def extract_text_from_pdf(pdf_path):
    # Convert PDF to images
    # images = convert_from_path(pdf_path, poppler_path=r'C:\poppler\poppler-24.08.0\Library\bin')
    # ✅ On Linux, no need to set path if tesseract and poppler-utils are installed globally
    images = convert_from_path(pdf_path)

    full_text = ""
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    
    return full_text.strip()

def extract_keywords(text, num_keywords=100):
    stop_words = set(stopwords.words('english'))
    from nltk.tokenize import word_tokenize
    words = word_tokenize(text.lower())

    words = [w for w in words if w.isalpha() and w not in stop_words]
    
    # Frequency distribution
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, _ in sorted_keywords[:num_keywords]]
    return top_keywords



def ocr_files(request):
    try:
        from django.utils.timezone import localdate
        from django.db.models import Max

        today = localdate()  
        latest_docs = (Document.objects.values('file_path').annotate(latest_id=Max('id')).values_list('latest_id', flat=True))
        Document.objects.exclude(id__in=latest_docs).delete()
        docs = Document.objects.filter(keywords__isnull=True,extracted_text__isnull=True)
        # docs = Document.objects.filter(uploaded_at__date=today,keywords__isnull=True,extracted_text__isnull=True).order_by('-uploaded_at')
        for doc in docs:
            if not doc.file_path:
                continue
            file_path = os.path.join(MEDIA_ROOT, str(doc.file_path))
            _, ext = os.path.splitext(file_path) 
            if ext.lower() != '.pdf':   
                continue
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                try:
                    with open(file_path, 'rb') as f:
                        reader = PdfReader(f)
                        num_pages = len(reader.pages)
                except Exception as e:
                    num_pages = None
                text = extract_text_from_pdf(file_path)
                keywords = extract_keywords(text)  
                Document.objects.filter(id=doc.id).update(
                    title=doc.uploaded_name,num_pages=str(num_pages),file_size=str(file_size),
                    pdf_file=doc.file_path,
                    extracted_text=text,
                    keywords=', '.join(keywords)
                )
        return HttpResponse(f"<div style='color:green; font-family: Arial;'> OCR Batch Processed Successfully </div>")
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        error_log.objects.create(method=fun,error=str(e),user="Batch Process")  
        return HttpResponse(f"<div style='color:red; font-family: Arial;'>Batch failed: {str(e)}</div>")
        # callproc("stp_error_log",[fun,str(e),user])

      
 

import os
from django.shortcuts import render, redirect
from .models import Document
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PyPDF2 import PdfReader

def upload_document(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        pdf_file = request.FILES.get('pdf_file')

        if title and pdf_file:
            # Save file to media/documents/
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'ocr_docs'))
            filename = fs.save(pdf_file.name, pdf_file)
            file_path = os.path.join(fs.location, filename)
            file_size = os.path.getsize(file_path)
            try:
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    num_pages = len(reader.pages)
            except Exception as e:
                num_pages = None
            # OCR + Keyword extraction
            text = extract_text_from_pdf(file_path)
            keywords = extract_keywords(text)

            # Save to DB
            document = Document.objects.create(
                title=title,num_pages=str(num_pages),file_size=str(file_size),
                pdf_file=os.path.join('ocr_docs', filename),
                extracted_text=text,
                keywords=', '.join(keywords)
            )
            return redirect('document_detail1', pk=document.pk)
    
    return render(request, 'Master/upload.html')



from django.shortcuts import get_object_or_404

def document_detail1(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'Master/document_detail.html', {'document': document})

from django.shortcuts import render
from django.db.models import Q
from .models import Document
from Form.models import WorkflowVersionControl
from django.db.models import OuterRef, Subquery, Value, Case, When, CharField
from django.db.models.functions import Coalesce


def search_documents(request):
    documents = Document.objects.all().order_by('-uploaded_at')
     # Process documents to add keywords_list
    def process_documents(docs):
        processed = []
        for doc in docs:
            # Use pdf_file if it exists, otherwise fall back to file_path
            raw_path = str(doc.pdf_file) if doc.pdf_file else str(doc.file_path)
            file_path = os.path.join(MEDIA_ROOT, raw_path) if raw_path else ""
            file_exists = os.path.exists(file_path) if file_path else False
            processed.append({
                'id': doc.id,
                'title': doc.title,
                'pdf_file': enc(raw_path) if file_exists else None,
                'file_exists': file_exists,
                'keywords': doc.keywords,
                'uploaded_at': doc.uploaded_at,
                'keywords_list': doc.keywords.split(',') if doc.keywords else []
            })

        return processed
    context = {'documents': process_documents(documents),'search_type': None}
    if request.method == 'GET':
        # Simple search
        if 'simple_query' in request.GET:
            query = request.GET.get('simple_query', '').strip()
            if query:
                documents = documents.filter(
                    Q(title__icontains=query) | 
                    Q(keywords__icontains=query)
                )
                context['documents'] = process_documents(documents)
                context['search_type'] = 'simple'
                context['query'] = query
                context['show_results'] = True
        
        # Advanced search
        elif any(key in request.GET for key in ['title', 'keyword1', 'keyword2', 'keyword3']):
            title = request.GET.get('title', '').strip()
            keyword1 = request.GET.get('keyword1', '').strip()
            keyword2 = request.GET.get('keyword2', '').strip()
            keyword3 = request.GET.get('keyword3', '').strip()
            keyword4 = request.GET.get('keyword4', '').strip()
            keyword5 = request.GET.get('keyword5', '').strip()
            keyword6 = request.GET.get('keyword6', '').strip()
            match_all = request.GET.get('match_all', 'off') == 'on'
            if title or keyword1 or keyword2 or keyword3 or keyword4 or keyword5 or keyword6:
                documents = Document.objects.all()
                if title:
                    documents = documents.filter(title__icontains=title)

                keywords = [kw for kw in [keyword1, keyword2, keyword3, keyword4, keyword5, keyword6] if kw]
                if keywords:
                    if match_all:
                        for keyword in keywords:
                            documents = documents.filter(keywords__icontains=keyword)
                    else:
                        query = Q()
                        for keyword in keywords:
                            query |= Q(keywords__icontains=keyword)
                        documents = documents.filter(query)
                context['show_results'] = True

            context['documents'] = process_documents(documents)
            context['search_type'] = 'advanced'
            context['search_params'] = {'title': title,'keyword1': keyword1,'keyword2': keyword2,'keyword3': keyword3,'keyword4': keyword4,'keyword5': keyword5,'keyword6': keyword6,'match_all': match_all}

    
    return render(request, 'Master/search.html', context)

def document_detail(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    keywords = document.keywords.split(',')[:20]  # Top 20
    full_path = os.path.join(MEDIA_URL,str(document.pdf_file)).replace('\\', '/')
    text = document.extracted_text
    for idx, keyword in enumerate(keywords):
        pattern = r'\b' + re.escape(keyword) + r'\b'
        span = f"<span class='kw kw{idx}'>{keyword}</span>"
        text = re.sub(pattern, span, text, flags=re.IGNORECASE)

    return render(request, 'Master/document_keyword.html', {
        'document': document,'full_path': full_path,'keywords': keywords,'highlighted_text': text
    })


def ks(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    keywords = document.keywords.split(',')[:20]  # Top 20
    keywords = [k.strip() for k in keywords]
    full_path = os.path.join(MEDIA_URL,str(document.pdf_file)).replace('\\', '/')
    return render(request, 'Master/keyword_search.html', {
        'document': document,'full_path': full_path,'keywords': keywords, 'pdfjs_url': '/static/pdfjs/web/viewer.html'
    })

@login_required
def masters(request):
    pre_url = request.META.get('HTTP_REFERER')
    header, data = [], []
    entity = type = name = id = text_name = dpl = dp = em = mb = forms = sf = ''

    try:
        if request.user.is_authenticated ==True:                
                global user,role_id
                user = request.user.id    
                role_id = request.user.role_id 
        if request.method=="GET":
            entity = request.GET.get('entity', '')
            sf = request.GET.get('sf', '')
            type = request.GET.get('type', '')
            datalist1= callproc("stp_get_masters",[entity,type,'name',user])
            name = datalist1[0][0]
            header = callproc("stp_get_masters", [entity, type, 'header',user])
            rows = callproc("stp_get_masters",[entity,type,'data',user])
            if entity == 'form_master':
                forms = callproc("stp_get_forms",['view_form',user])  
                type = 'i'
                if sf == '' or None:
                   sf =  forms[0][0]   
                header = callproc("stp_get_view_form_header",[sf])          
                rows = callproc("stp_get_view_forms",[sf])          
            if entity == 'su':
                dpl = callproc("stp_get_dropdown_values",['dept'])

            id = request.GET.get('id', '')
            if type=='ed' and id != '0':
                if id != '0' and id != '':
                    id = dec(id)
                rows = callproc("stp_get_masters",[entity,type,'data',id])
                text_name = rows[0][0]
                if entity == 'su':
                    em = rows[0][1]
                    mb = rows[0][2]
                    dp = rows[0][3]
                id = enc(id)
            data = []
            for row in rows:
                encrypted_id = enc(str(row[0]))
                data.append((encrypted_id,) + row[1:])

        if request.method=="POST":
            entity = request.POST.get('entity', '')
            id = request.POST.get('id', '')
            dp = request.POST.get('dp', '')
            em = request.POST.get('em', '')
            mb = request.POST.get('mb', '')
            if id != '0' and id != '':
                id = dec(id)
            name = request.POST.get('text_name', '')
            if entity == 'su':
                datalist1= callproc("stp_post_user_masters",[id,name,em,mb,dp,user])
            else: datalist1= callproc("stp_post_masters",[entity,id,name,user])

            if datalist1[0][0] == 'insert':
                messages.success(request, 'Data inserted successfully !')
            elif datalist1[0][0] == 'update':
                messages.success(request, 'Data updated successfully !')
            elif datalist1[0][0] == 'exist':
                messages.error(request, 'Data already exist !')
            
                          
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        Db.closeConnection()
        if request.method=="GET":
             return render(request,'Master/index.html',
              {'entity':entity,'forms':forms,'sf':sf,'type':type,'name':name,'header':header,'data':data,
              'id':id,'text_name':text_name,'dp':dp,'em':em,'mb':mb,'dpl':dpl})
        elif request.method=="POST":  
            new_url = f'/masters?entity={entity}&type=i'
            return redirect(new_url) 
 
def sample_xlsx(request):
    pre_url = request.META.get('HTTP_REFERER')
    response =''
    global user
    user  = request.session.get('user_id', '')
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Sample Format'
        columns = []
        if request.method=="GET":
            entity = request.GET.get('entity', '')
            type = request.GET.get('type', '')
        if request.method=="POST":
            entity = request.POST.get('entity', '')
            type = request.POST.get('type', '')
        file_name = {'em': 'Employee Master','sm': 'Worksite Master','cm': 'Company Master','r': 'Roster'}[entity]
        columns = callproc("stp_get_masters", [entity, type, 'sample_xlsx',user])
        if columns and columns[0]:
            columns = [col[0] for col in columns[0]]

        black_border = Border(
            left=Side(border_style="thin", color="000000"),
            right=Side(border_style="thin", color="000000"),
            top=Side(border_style="thin", color="000000"),
            bottom=Side(border_style="thin", color="000000")
        )
        
        for col_num, header in enumerate(columns, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.value = header
            cell.font = Font(bold=True)
            cell.border = black_border
        
        for col in sheet.columns:
            max_length = 0
            column = col[0].column_letter  
            for cell in col:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
                    
            adjusted_width = max_length + 2 
            sheet.column_dimensions[column].width = adjusted_width  
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="' + str(file_name) +" "+str(datetime.now().strftime("%d-%m-%Y")) + '.xlsx"'
        workbook.save(response)
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        return response      



    
def workflow_mapping(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    if request.user.is_authenticated ==True:                
                global user,role_id
                user = request.user.id    
                role_id = request.user.role_id
    try:
        if request.method == "GET":
            cursor.callproc("stp_getFormForMapping")
            for result in cursor.stored_results():
                form_dropdown = list(result.fetchall())
            cursor.callproc("stp_getButTypeForMapping")
            for result in cursor.stored_results():
                ButType_dropdown = list(result.fetchall())
            cursor.callproc("stp_getFormActForMapping")
            for result in cursor.stored_results():
                ButAct_dropdown = list(result.fetchall())
            cursor.callproc("stp_getworkflowD")
            for result in cursor.stored_results():
                workflow_dropdown = list(result.fetchall())
            cursor.callproc("stp_getRoleDD")
            for result in cursor.stored_results():
                role_dropdown = list(result.fetchall())
            cursor.callproc("stp_getEditCreateWFDD")
            for result in cursor.stored_results():
                wfEditCreate_dropdown = list(result.fetchall())
            # cursor.callproc("stp_getEditCrtForMapping")
            # for result in cursor.stored_results():
            #     EditCrt_dropdown = list(result.fetchall())
            getformdata = {'form_dropdown':form_dropdown,'ButType_dropdown':ButType_dropdown,
                           'ButAct_dropdown':ButAct_dropdown,'workflow_dropdown':workflow_dropdown,'role_dropdown':role_dropdown,
                           "wfEditCreate_dropdown":wfEditCreate_dropdown,}
            return render(request, "Master/workflow_mapping.html",getformdata)
        
    except Exception as e:
        print("error-"+e)
        response_data = "fail"
        messages.error(request,"Some Error Occured !!")
    
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        
def get_actions_by_button_type(request):
    button_type_id = request.GET.get("button_type_id")
    
    # Fetch actions based on the button type ID using stored procedure or query
    actions = workflow_action_master.objects.filter(action_id=button_type_id).values("id", "action_details")

    return JsonResponse(list(actions), safe=False)

def decrypt_parameter(encoded_cipher_text):
    # Decode the base64-encoded string before decrypting
    cipher_text = base64.urlsafe_b64decode(encoded_cipher_text.encode())
    cipher_suite = Fernet(get_encryption_key())
    plain_text = cipher_suite.decrypt(cipher_text).decode()
    return plain_text

def submit_workflow(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    if request.user.is_authenticated ==True:                
                global user,role_id
                user = request.user.id    
                role_id = request.user.role_id
    try:
        workflow_name = request.POST.get("workflowDropdown")
        step_name = request.POST.get("stepName")
        form_name = request.POST.get("formDropdown")
        button_type = request.POST.get("buttonTypeDropdown")
        action = request.POST.get("actionDropdown")
        customRoleDropdown = request.POST.get("roles")
        statusName = request.POST.get("statusName")
        favcolor = request.POST.get("favcolor")
        paramWN = [workflow_name]
        cursor.callproc("stp_getcountStepCountWF",paramWN)
        for result in cursor.stored_results():
            step_id_flow1 = list(result.fetchall())[0][0]
        step_id_flow2 = step_id_flow1+1
        step_id_flow = step_id_flow2
            
        param=(workflow_name,step_name,form_name,button_type,action,user,customRoleDropdown,step_id_flow,statusName,favcolor)
        cursor.callproc("stp_insertIntoWorkflow_matrix",param)   
        m.commit()  
        # return JsonResponse({"message": "Workflow submitted successfully!"}, status=200)
        return JsonResponse({"message": "Workflow submitted successfully!","redirect_url": "/masters/?entity=wfseq&type=i"}, status=200)

    except Exception as e:
            print("error-"+e)
            response_data = "fail"
            messages.error(request,"Some Error Occured !!")
        
    finally:
        cursor.close()        
        m.close()
        Db.closeConnection()
        
def workflow_Editmap(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()

    if request.user.is_authenticated:
        global user, role_id
        user = request.user.id
        role_id = request.user.role_id

    try:
        if request.method == "GET":
            workflow_idIncrypt = request.GET.get("wfseq_id")

            if workflow_idIncrypt:
                workflow_id = decrypt_parameter(workflow_idIncrypt) 
            
            param = [workflow_id] 

            
            cursor.callproc("stp_getFormForMapping")
            for result in cursor.stored_results():
                form_dropdown = list(result.fetchall())
            cursor.callproc("stp_getButTypeForMapping")
            for result in cursor.stored_results():
                ButType_dropdown = list(result.fetchall())
            cursor.callproc("stp_getFormActForMapping")
            for result in cursor.stored_results():
                ButAct_dropdown = list(result.fetchall())
            cursor.callproc("stp_getworkflowD")
            for result in cursor.stored_results():
                workflow_dropdown = list(result.fetchall())
            cursor.callproc("stp_getRoleDD")
            for result in cursor.stored_results():
                role_dropdown = list(result.fetchall())
            cursor.callproc("stp_getEditCreateWFDD")
            for result in cursor.stored_results():
                wfEditCreate_dropdown = list(result.fetchall())        
            cursor.callproc("stp_getworkflowEdit", param)
            workflow_data = []
            for result in cursor.stored_results():
                workflow_data = result.fetchall()  
            
           
            workflow_details = {}
            if workflow_data:
                role_string = workflow_data[0][6]
                role_list = role_string.split(',') if role_string else []
                workflow_details = {
                    "workflow_name": workflow_data[0][0], 
                    "form_id": workflow_data[0][1],
                    "step_name": workflow_data[0][2],
                    "button_type_id": workflow_data[0][3],
                    "button_act_details": workflow_data[0][4],
                    "statusV": workflow_data[0][7],
                    "status_color": workflow_data[0][8],
                    "workflow_idD": workflow_data[0][5],
                    
                    "role_id": role_string,
                    "role_list": role_list
                }

            getformdata = {
                    "form_dropdown": form_dropdown,
                    "ButType_dropdown": ButType_dropdown,
                    "ButAct_dropdown": ButAct_dropdown,
                    "workflow_dropdown": workflow_dropdown,
                    "workflow_details": workflow_details,
                    "role_dropdown":role_dropdown,
                    "wfEditCreate_dropdown":wfEditCreate_dropdown,
                    "workflow_id":workflow_idIncrypt,
                    "wfEditCreate_dropdown":wfEditCreate_dropdown,
                }

            return render(request, "Master/workflow_Editmap.html", getformdata)

        if request.method == "POST":
            workflow_idEncrypt = request.POST.get("workflow_idEncrypt")
            workflow_idDecryp = decrypt_parameter(workflow_idEncrypt)
            workflow_name = request.POST.get("workflowDropdown")
            step_name = request.POST.get("stepName")
            form_name = request.POST.get("formDropdown")
            button_type = request.POST.get("buttonTypeDropdown")
            action = request.POST.get("actionDropdown")
            roles = request.POST.get("roles")
            favcolor = request.POST.get("favcolor")
            statusName = request.POST.get("statusName")
            

            param = (workflow_name, step_name, form_name, button_type, action, workflow_idDecryp,user,roles,statusName,favcolor)
            cursor.callproc("stp_updateWorkflow_matrix", param)
            m.commit()
            
            return JsonResponse({"message": "Workflow submitted successfully!","redirect_url": "/masters/?entity=wfseq&type=i"}, status=200)

    except Exception as e:
        print("Error:", e)
        messages.error(request, "Some Error Occurred !!")
        return JsonResponse({"message": "Error Occurred!"}, status=500)

    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        
def view_access(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    if request.user.is_authenticated ==True:                
                global user,role_id
                user = request.user.id    
                role_id = request.user.role_id
    try:
        if request.method == "GET":
            cursor.callproc("stp_getRoleForAccessControl")
            for result in cursor.stored_results():
                roles_dropdown = list(result.fetchall())
                # roles_dropdown = [row[0] for row in result.fetchall()]
           
            
            roles_data_qs = roles.objects.all()
            roles_data_dict = {r.id: r for r in roles_data_qs}
            
            getformdata = {'roles':roles_dropdown,'roles_data': roles_data_dict,}
            return render(request, "Master/view_access.html",getformdata)
        if request.method == "POST":
            data = json.loads(request.body)
            name = data.get("name")  # like workflow_inward
            value = data.get("value")  # 1 or 0

            type_, role_slug = name.split("_")
            role = role_slug.replace("-", " ").title()  # reverse slugify
            
            if type_ == 'workflow':
                roles.objects.filter(id=role).update(workflow_view=value)
            elif type_ == 'form':
                roles.objects.filter(id=role).update(form_view=value)
            elif type_ == 'report':
                roles.objects.filter(id=role).update(report_view=value)
    except Exception as e:
        print("error-"+e)
        response_data = "fail"
        messages.error(request,"Some Error Occured !!")
    
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
