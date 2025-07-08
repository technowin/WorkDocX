from django.conf import settings
from django.shortcuts import render

# Create your views here.
import string
from django.http import Http404, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import requests
from Form.models import FormFile
from Reports.models import *
from Account.models import *
import Db 
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from mysql.connector.errors import InterfaceError
import calendar
import pandas as pd
import xlwt
from django.http import HttpResponse
import os
import time
import xlsxwriter
import io
import os
# Create your views here.
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from flask import Flask, render_template
from django.shortcuts import render

from WorkDocX.settings import MEDIA_ROOT
app = Flask(__name__)
# Create your views here.

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import FileResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
import traceback
from Account.db_utils import callproc
from django.utils import timezone
from WorkDocX.encryption import *
# Report section
@login_required
def common_html(request):
    title,note ='',''
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            entity =request.GET.get('entity', '')  
            title,note ='',''
            if request.method=="GET":
                forms = callproc("stp_get_forms",['report',user]) 
                if entity == '' or None:
                   entity =  forms[0][0]         
                filter_name = callproc("stp_get_filter_names",[entity])          
                column_name = callproc("stp_get_column_names",[entity])        
                result = callproc("stp_get_report_title", [entity])
                if result and result[0]:
                    items = result[0] 
                    if isinstance(items, tuple):
                        if len(items) == 2:
                            title, note = items
                        elif len(items) == 1:
                            title = items[0]
                            note = ''
                    else:
                        title = items
                        note = ''
                saved_names = callproc("stp_get_saved_filters",[entity,user])        

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        return render(request,'Reports/common_reports.html', {'forms':forms,'filter_name':filter_name,'column_name':column_name,'saved_names':saved_names,'entity':entity,'title':title,'note':note})
    
@login_required      
def get_filter(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method=="GET":
                entity =request.GET.get('entity', '')
                data4 = callproc("stp_get_filter_names",[entity])
                drop_down=[]
                data5 = []
                for items in data4:
                    data5=[]
                    data5=list(items)
                    unit = common_model(id1=data5[0], name=data5[1])
                    drop_down.append(common_dict(unit))
                if len(drop_down) == 0:
                    drop_down = 0
    except Exception  as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        return JsonResponse(drop_down, safe=False)
    

    
def common_dict(unit):
    return {
        'id1': unit.id1,
        'name': unit.name,
    }  
    
@login_required    
def get_sub_filter(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id 
            if request.method=="GET":
                filter_id =request.GET.get('filter_id', '')
                data4 = callproc("stp_get_sub_filter",[filter_id,user])
                drop_down=[]
                data5 = []
                for items in data4:
                    data5=[]
                    data5=list(items)
                    unit = common_model(id1=data5[0], name=data5[1])
                    drop_down.append(common_dict(unit))
                if len(drop_down) == 0:
                    drop_down = 0 
    except Exception  as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        return JsonResponse(drop_down, safe=False)  

@login_required
def add_new_filter(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method == "GET":
                filter_count =str(request.GET.get('filter_count', ''))
                entity =str(request.GET.get('entity', ''))
                filter_name = callproc("stp_get_filter_names",[entity])                
                fId = filter_count + 'filterId'           
                sfId = filter_count + 'subFilterId'           
                context = {'filter_name':filter_name,'fId':fId,'sfId':sfId,'fcount':filter_count}
                html = render_to_string('Reports/_add_new_filter.html', context)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        data = {'html': html}
        return JsonResponse(data, safe=False)
    
@login_required
def partial_report(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method == "GET":
                columnName =str(request.GET.get('columnName', ''))
                filterid =str(request.GET.get('filterid', ''))
                subFilterId =str(request.GET.get('subFilterId', ''))
                sft =str(request.GET.get('sft', ''))
                entity =str(request.GET.get('entity', ''))
                filterid1 = filterid.split(',')
                SubFilterId1 = subFilterId.split(',')
                sft1 = sft.split(',')
                data = common_fun(columnName,filterid1,SubFilterId1,sft1,entity,user,'0')
                headers = data['headers']
                emptycheck = data['emptycheck']
                data_list = data['data_list']
                display_name_list = data['display_name_list']
                # entityName = entity
                context = {'emptycheck':emptycheck,'columns':display_name_list,'rows':data_list,'entity':entity}
                html = render_to_string('Reports/_partial_report.html', context)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        data = {'html': html}
        return JsonResponse(data, safe=False)
    
def common_fun(columnName,filterid,SubFilterId,sft,entity,user,is_export):
    try:
        report_filters= []
        report_columns= []
        column_join_list= []
        mandatory_arr= []
        result_data = callproc("stp_get_report_filters", [entity])
        if result_data and result_data[0]:
            for row in result_data:
                report_filters.append(list(row))
        result_data =callproc("stp_get_report_columns", [entity])
        if result_data and result_data[0]:
            for row in result_data:
                report_columns.append(list(row))
        result_data = callproc("stp_get_column_join", [entity])
        if result_data and result_data[0]:
            for row in result_data:
                column_join_list.append(list(row))
        result_data = callproc("stp_get_mandatory", [entity])
        mandf = ''
        if result_data and result_data[0]: 
            mandf = result_data[0][0]
        if mandf != '':
            mandatory_arr = mandf.split(',')
      
        from_clause = ""
        language = ""
        where_clause = ""
        where_extra = ""
        join_query = ""
        join_clause = ""
        from_clause1 = ""
        where_clause1 = [""] * len(filterid)
        join_query1 = [""] * len(filterid)
        order_by = ""
        group_by = ""
        columns = ""
        b = 0
        for fid in filterid:
            from_clause = next((f[4] for f in report_filters if f[0] == int(fid)), '')
            if from_clause != '':
                from_clause1 = from_clause

            where_clause1[b] = next((f[5] for f in report_filters if f[0] == int(fid)), '')
            join_query1[b] = next((f[6] for f in report_filters if f[0] == int(fid)), '')
            group_by = next((f[7] for f in report_filters if f[0] == int(fid)), '')
            order_by = next((f[8] for f in report_filters if f[0] == int(fid)), '')
            
            where_clause1[b] = where_clause1[b] if where_clause1[b] is not None else ''
            join_query1[b] = join_query1[b] if join_query1[b] is not None else ''
            group_by = group_by if group_by is not None else ''
            order_by = order_by if order_by is not None else ''
            b += 1
        from_clause = from_clause1
        header_filter = []
        header_sub_filter = []
        filter_name = ""
        cnt1 = 0
        for i in range(len(filterid)):
                if sft[i] and sft[i].strip() not in ("", "0"):
                    filter_name = next((f[2] for f in report_filters if f[0] == int(filterid[i])), '')
                    if filter_name in header_filter:
                       idx = header_filter.index(filter_name)
                       header_sub_filter[idx] += '|' + sft[i]
                    else:
                       header_filter.append(filter_name)
                       header_sub_filter.append(sft[i])  
        b =0
        for sub in range(len(SubFilterId)):
            SubFilterId[sub] = SubFilterId[sub].replace("|", "','")
            if not SubFilterId[sub] or SubFilterId[sub] in ("0", "", " "):
                where_clause1[b] = ""
            else:
                where_clause1[b] = where_clause1[b].replace("BindPara1", SubFilterId[sub])
            b += 1
        
        column_name = callproc("stp_get_dispay_names",[entity])        
        
                
        if columnName == '': 
            column_name_arr = [col[0] for col in column_name] 
            display_name_arr = [col[1] for col in column_name]
            columns = " , ".join(column_name_arr)
        else :
            column_name_arr = columnName.split(',')
            for i, col in enumerate(column_name_arr):
                column_name_arr[i] = col.replace('|', ',')
            display_name_arr = []

            for item in column_name:
                if item[0] in column_name_arr:
                    display_name_arr.append(item[1])

            columns = " , ".join(column_name_arr)

        display_names = " , ".join(display_name_arr)

        for dr in column_join_list:
            check = dr[0]
            if check in columns:
                replace = dr[1]
                columns = columns.replace(check, replace)
            join_clause += dr[2] + " "
        for z in range(len(filterid)):
            if where_clause1[z] not in where_clause:
                if not where_clause:
                    where_clause = " where " + where_clause1[z]
                else:
                    where_clause += " and " + where_clause1[z]
                            
        if join_query1[z] not in join_clause:
            join_clause += join_query1[z]

        sql_query = "Select " + columns + " " + from_clause + " " + join_clause + " " + where_clause + " " + where_extra + " " + group_by + " " + order_by
        
        ch = 0
        for value in mandatory_arr:
            if value not in filterid:
                ch = 1
                break
        if ch == 0:
            if not all(value.strip() for value in SubFilterId[:len(mandatory_arr)]):
                ch = 1
            elif len(filterid) != len(SubFilterId):
                ch = 1
                
        data_list= []
        if ch == 0:
            result_data = callproc("stp_get_execute_report_query", [sql_query])
            if result_data and result_data[0]:
                data_list = preprocess_data_list(result_data,is_export)
      
        display_name_list = list(display_name_arr)

        if len(data_list) > 0:
            emptycheck = 0
        else : emptycheck = 1
        
        hl = []
        for filter_key, filter_value in zip(header_filter, header_sub_filter):
            if "|" in filter_value:
                values = filter_value.split("|")
                hl.append(f"{filter_key} :- ({','.join(values)})")
            else:
                hl.append(f"{filter_key} :- {filter_value}")
        hl_r = " , ".join(hl)

        data = {
               'headers': hl_r,
               'emptycheck': emptycheck,
               'data_list': data_list,
               'display_name_list': display_name_list,
               'sql_query': sql_query,
               'display_names': display_names
            }
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),user])  
    finally:
          return data

def dl_file(request, file_id):
    try:
        form_file = FormFile.objects.get(id=dec(file_id))
        file_path = os.path.join(MEDIA_ROOT, form_file.file_path)
        if not os.path.exists(file_path):
            raise Http404("File not found.")
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=form_file.uploaded_name)
    except FormFile.DoesNotExist:
        raise Http404("File not found.")

def preprocess_data_list(result_data, is_export):
    data_list = []
    for row in result_data:
        processed_row = []
        for value in row:
            if isinstance(value, str) and 'tdmsformfiles_' in value:
                file_ids = [v.replace('tdmsformfiles_', '') for v in value.split(',') if v.startswith('tdmsformfiles_')]
                uploaded_names = []
                if is_export == '1':
                    for file_id in file_ids:
                        try:
                            form_file = FormFile.objects.get(id=file_id)
                            uploaded_names.append(form_file.uploaded_name)
                        except FormFile.DoesNotExist:
                            continue
                    processed_row.append(', '.join(uploaded_names))
                else:
                    file_links = []
                    for file_id in file_ids:
                        try:
                            form_file = FormFile.objects.get(id=file_id)
                            # form_file_id1 = callproc("stp_get_check_file",[form_file.id,user])
                            # if form_file_id1 and form_file_id1[0][0] == form_file.id:
                            file_path = os.path.join(MEDIA_ROOT, form_file.file_path)
                            file_exists = os.path.exists(file_path)
                            file_links.append({
                                'file_name': form_file.uploaded_name,
                                'exists': file_exists,
                                'id': enc(str(file_id)),
                            })
                            # else:
                            #     uploaded_names.append(form_file.uploaded_name)
                            #     processed_row.append(', '.join(uploaded_names))

                        except FormFile.DoesNotExist:
                            continue
                    if file_links:
                        processed_row.append({'file_links': file_links})
            else:
                processed_row.append(value)
        data_list.append(processed_row)
    return data_list


def render_to_pdf(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

@login_required
def report_pdf(request):
    response = ''
    html_string = ''
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method == "POST":
                columnName = str(request.POST.get('columnName', ''))
                filterid = str(request.POST.get('filterid', ''))
                subFilterId = str(request.POST.get('subFilterId', ''))
                sft = str(request.POST.get('sft', ''))
                entity = str(request.POST.get('entity', ''))
                filterid1 = filterid.split(',')
                SubFilterId1 = subFilterId.split(',')
                sft1 = sft.split(',')
                data = common_fun(columnName, filterid1, SubFilterId1, sft1, entity, user, '1')

                headers = data['headers']
                emptycheck = data['emptycheck']
                data_list = data['data_list']
                column_list = data['display_name_list']

                result_data = callproc("stp_get_report_title", [entity])
                title = ''
                if result_data and result_data[0]:
                    for items in result_data:  
                        title = items[0]
                        
                html_string = render_to_string('Reports/report_template.html', {
                    'title': title,
                    'headers': headers,
                    'column_list': column_list,
                    'data_list': data_list,
                })
                pdf = render_to_pdf(html_string)
                filename = title+'.pdf'
                if pdf:
                    response = FileResponse(pdf, content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        return response
    
@login_required
def report_xlsx(request):
    response = ''
    try:
        if request.user.is_authenticated:                
            global user
            user = request.user.id
            if request.method == "POST":
                columnName = str(request.POST.get('columnName', ''))
                filterid = str(request.POST.get('filterid', ''))
                subFilterId = str(request.POST.get('subFilterId', ''))
                sft = str(request.POST.get('sft', ''))
                entity = str(request.POST.get('entity', ''))
                filterid1 = filterid.split(',')
                SubFilterId1 = subFilterId.split(',')
                sft1 = sft.split(',')
                data = common_fun(columnName, filterid1, SubFilterId1, sft1, entity, user, '1')

                headers = data['headers']
                emptycheck = data['emptycheck']
                data_list = data['data_list']
                column_list = data['display_name_list']

                result_data = callproc("stp_get_report_title", [entity])
                title = ''
                if result_data and result_data[0]:
                    for items in result_data:  
                        title = items[0]

                output = io.BytesIO()
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet(str(entity))
            
                # Insert logo
                worksheet.insert_image('A1', 'static/images/technologo.png', {
                    'x_offset': 1, 'y_offset': 1, 'x_scale': 0.04, 'y_scale': 0.04
                })
                
                # Formats
                header_format = workbook.add_format({'align': 'center','valign': 'vcenter', 'bold': True,'font_size': 14})
                data_format = workbook.add_format({'border': 1})
                filter_format = workbook.add_format({'bold': True})
                column_header_format = workbook.add_format({'bold': True, 'bg_color': '#7f9cf0', 'font_color': 'black'})
                from xlsxwriter.utility import xl_range
                merged_range = xl_range(1, 0, 1, len(column_list) - 1)  # A4 to ??4
                worksheet.merge_range(merged_range, title, header_format)
            
                # Write filters/info row
                worksheet.write(3, 0, headers, filter_format)
            
                # Column headers
                for i, column_name in enumerate(column_list):
                    worksheet.write(5, i, column_name, column_header_format)
            
                # Data rows
                for row_num, row_data in enumerate(data_list, start=6):
                    for col_num, col_data in enumerate(row_data):
                        worksheet.write(row_num, col_num, str(col_data), data_format)
            
                # Auto column width
                for col_num in range(len(column_list)):
                    col_cells = [str(row[col_num]) for row in data_list] + [column_list[col_num]]
                    max_width = max(len(cell) for cell in col_cells)
                    worksheet.set_column(col_num, col_num, max_width)
            
                workbook.close()
            
                # Response
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{title}.xlsx"'
                output.seek(0)
                response.write(output.read())
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), request.user.id])
        messages.error(request, f'Oops...! Something went wrong! {str(e)}')
    finally:
        return response
        
# @login_required
# def report_xlsx(request):
#     response = ''
#     try:
#         if request.user.is_authenticated ==True:                
#             global user
#             user = request.user.id
#             if request.method == "POST":
#                 columnName =str(request.POST.get('columnName', ''))
#                 filterid =str(request.POST.get('filterid', ''))
#                 subFilterId =str(request.POST.get('subFilterId', ''))
#                 sft =str(request.POST.get('sft', ''))
#                 entity =str(request.POST.get('entity', ''))
#                 filterid1 = filterid.split(',')
#                 SubFilterId1 = subFilterId.split(',')
#                 sft1 = sft.split(',')
#                 data = common_fun(columnName,filterid1,SubFilterId1,sft1,entity,user,'1')

#                 headers = data['headers']
#                 emptycheck = data['emptycheck']
#                 data_list = data['data_list']
#                 column_list = data['display_name_list']

#                 result_data = callproc("stp_get_report_title", [entity])
#                 title = ''
#                 if result_data and result_data[0]:
#                     for items in result_data:  
#                         title = items[0]

#                 output = io.BytesIO()
#                 workbook = xlsxwriter.Workbook(output)
#                 worksheet = workbook.add_worksheet(str(entity))
            
#                 # Inserting the logo with a reduced size, ensuring it doesn't overlap
#                 worksheet.insert_image('A1', 'static/images/technologo.png', {'x_offset': 1, 'y_offset': 1, 'x_scale': 0.04, 'y_scale': 0.04})  # Reduced size
            
#                 # Header Format
#                 header_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 14})
                
#                 # Data Format
#                 data_format = workbook.add_format({'border': 1})
            
#                 # Merge header cell for the title
#                 worksheet.merge_range('A4:{}'.format(chr(65 + len(column_list) - 1) + '2'), title, header_format)
            
#                 # Add the header row
#                 filter_format = workbook.add_format({'bold': True})
#                 worksheet.write(5, 0, headers, filter_format)
            
#                 # Header Row Format (Column Names)
#                 header_format = workbook.add_format({'bold': True, 'bg_color': '#7f9cf0', 'font_color': 'black'})
#                 for i, column_name in enumerate(column_list):
#                     worksheet.write(6, i, column_name, header_format)
            
#                 # Write the data rows
#                 for row_num, row_data in enumerate(data_list, start=7):
#                     for col_num, col_data in enumerate(row_data):
#                         worksheet.write(row_num, col_num, str(col_data), data_format)
            
#                 # Auto-adjust columns based on content length (Auto width)
#                 for col_num in range(len(column_list)):
#                     worksheet.set_column(col_num, col_num, max(len(str(cell)) for cell in [row[col_num] for row in data_list] + [column_list[col_num]]))
            
#                 workbook.close()
            
#                 # Prepare the response to send the generated Excel file
#                 response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#                 response['Content-Disposition'] = f'attachment; filename="{title}.xlsx"'
#                 output.seek(0)
#                 response.write(output.read())
#     except Exception as e:
#         tb = traceback.extract_tb(e.__traceback__)
#         fun = tb[0].name
#         callproc("stp_error_log",[fun,str(e),request.user.id])  
#         messages.error(request, 'Oops...! Something went wrong!')
#     finally:
#         return response
    
def add_page_number(canvas, doc):
    canvas.saveState()
    page_num = canvas.getPageNumber()
    text = "Page %s" % page_num
    canvas.drawRightString(200*2.54, 1*2.54*2.54, text)
    canvas.restoreState()    

@login_required
def save_filters(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method == "GET":
                columnName =str(request.GET.get('columnName', ''))
                filterid =str(request.GET.get('filterid', ''))
                subFilterId =str(request.GET.get('subFilterId', ''))
                sft =str(request.GET.get('sft', ''))
                entity =str(request.GET.get('entity', ''))
                saved_name =str(request.GET.get('save_filter_name', ''))
                f_count =str(request.GET.get('f_count', ''))
                filterid1 = filterid.split(',')
                SubFilterId1 = subFilterId.split(',')
                sft1 = sft.split(',')
                data = common_fun(columnName,filterid1,SubFilterId1,sft1,entity,user,'0')
                sql_query = data['sql_query'] 
                display_names = data['display_names']       
                datalist = callproc("stp_save_report_filters",[saved_name,entity,filterid,subFilterId,columnName,f_count,display_names,sql_query,user])
                response_data = {'result': datalist[0][0]}                       
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
        response_data = {'result': 'fail'}       
    finally:
        return JsonResponse(response_data,safe=False)

@login_required
def delete_filters(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method == "GET":
                entity =str(request.GET.get('entity', ''))
                saved_id =str(request.GET.get('save_filter_name', ''))
                datalist = callproc("stp_delete_report_filters",[saved_id,entity,user])
                response_data = {'result': datalist[0][0]}                       
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
        response_data = {'result': 'fail','messages ':'something went wrong !'}       
    finally:
        return JsonResponse(response_data,safe=False)
    
@login_required
def saved_filters(request):
    try:
        if request.user.is_authenticated ==True:                
            global user
            user = request.user.id
            if request.method == "GET":
                entity =str(request.GET.get('entity', ''))
                saved_id =str(request.GET.get('saved_id', ''))
                result_data  = callproc("stp_get_saved_report_filters",[saved_id,entity,user])
                filters, sub_filters, selected_columns, f_count, display_name, sql_query = ('',) * 6  # Initialize variables
                if result_data and result_data[0]: 
                    for items in result_data: 
                        filters, sub_filters, selected_columns, f_count, display_name, sql_query = items 

                display_name_arr = display_name.split(',')
                display_name_list = list(display_name_arr)
                fil_arr = filters.split(',')
                sub_fil_arr = sub_filters.split(',')
                sel_col_arr = selected_columns.split(',')
                f_id = ''
                s_fid = ''
                if len(fil_arr) > 0:
                    f_id = fil_arr[0]
                    fil_arr = fil_arr[1:]
                if len(sub_fil_arr) > 0:
                    s_fid = sub_fil_arr[0]
                    sub_fil_arr = sub_fil_arr[1:]

                data_list= []
                result_data  = callproc("stp_get_execute_report_query", [sql_query])
                if result_data and result_data[0]:
                    for row in result_data:
                        data_list.append(list(row))

                if len(data_list) > 0:
                    emptycheck = 0
                else : emptycheck = 1

                table = render_to_string('Reports/_partial_report.html', {'emptycheck':emptycheck,'columns':display_name_list,'rows':data_list})

                context = {'result': 'success','filters':fil_arr,'sub_filters':sub_fil_arr,'sel_col_arr':sel_col_arr,
                           'sel_col':selected_columns,'f_count':f_count,'table':table,'f_id':f_id,'s_fid':s_fid}                       
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log",[fun,str(e),request.user.id])  
        messages.error(request, 'Oops...! Something went wrong!')
        context = {'result': 'fail'}       
    finally:
        return JsonResponse(context,safe=False)
 
 