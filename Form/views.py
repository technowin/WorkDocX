from collections import defaultdict
from decimal import Decimal
from PyPDF2 import PdfReader
from django.db import connection
from django.shortcuts import render

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
from django.db.models import Max
import Db 
import bcrypt
from PyPDF2 import PdfReader
from django.contrib.auth.decorators import login_required
from Masters.views import extract_keywords, extract_text_from_pdf
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
from Form.models import *
from Account.db_utils import callproc
from django.views.decorators.csrf import csrf_exempt
import os
from django.urls import reverse
from WorkDocX.settings import *
import logging
from django.http import FileResponse, Http404
import mimetypes
from django.template.loader import render_to_string

from Workflow.models import workflow_matrix, workflow_action_master
from Workflow.models import *
from django.utils.timezone import now
from django.db.models import OuterRef, Subquery, F
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
def format_label_name(parameter_name):
    """Convert parameter name to a proper label format."""
    return " ".join(re.findall(r'[A-Za-z]+', parameter_name)).title()

def get_dublicate_name(request):
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        exists = Form.objects.filter(name=form_name).exists()  
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def form_builder(request):
    user  = request.session.get('user_id', '')
    try:
        form_id = request.GET.get('form_id')
        common_options = list(AttributeMaster.objects.values("id", "control_name", "control_value"))
        sub_control = list(ValidationMaster.objects.values("id", "control_name", "control_value", "field_type"))
        regex = list(RegexPattern.objects.values("id", "input_type", "regex_pattern", "description"))
        dropdown_options = list(ControlParameterMaster.objects.values("control_name", "control_value"))
        master_dropdown = list(MasterDropdownData.objects.values("id", "name", "query"))
        form_names = list(Form.objects.values("id","name"))
        section = list(SectionMaster.objects.values("id","name"))
        version_fields = [field.name for field in WorkflowVersionControl._meta.fields if field.name == 'file_name']
        version = [name.replace('_', ' ').title() for name in version_fields]


        if not form_id:
            return render(request, "Form/form_builder.html", {
                "regex": json.dumps(regex),
                "dropdown_options": json.dumps(dropdown_options),
                "common_options": json.dumps(common_options),
                "sub_control": json.dumps(sub_control),
                "master_dropdown": json.dumps(master_dropdown),
                "form_names":json.dumps(form_names),
                "section_names":json.dumps(section),
                "version":json.dumps(version)
            })

        try:
            form_id = dec(form_id)  # Decrypt form_id
            form = get_object_or_404(Form, id=form_id)
            fields = FormField.objects.filter(form_id=form_id).order_by('order')
            validations = FieldValidation.objects.filter(form_id=form_id)
            generative = FormGenerativeField.objects.filter(form_id=form_id)
        except Exception as e:
            print(f"Error fetching form data: {e}")
            tb = traceback.extract_tb(e.__traceback__)
            fun = tb[0].name
            callproc("stp_error_log", [fun, str(e), user])
            messages.error(request, 'Oops...! Something went wrong!')
            return JsonResponse({"error": "Something went wrong!"}, status=500)

        validation_dict = {}
        try:
            for validation in validations:
                field_id = validation.field.id

                if field_id not in validation_dict:
                    validation_dict[field_id] = []

                validation_entry = {
                    "validation_type": validation.sub_master.control_value,
                    "validation_value": validation.value
                }
                validation_dict[field_id].append(validation_entry)

        except Exception as e:
            print(f"Error fetching form data: {e}")
            tb = traceback.extract_tb(e.__traceback__)
            fun = tb[0].name
            callproc("stp_error_log", [fun, str(e), user])
            messages.error(request, 'Oops...! Something went wrong!')
            return JsonResponse({"error": "Something went wrong!"}, status=500)

        generative_list = {}
        for generate in generative:
            field_id = generate.field.id

            if field_id not in generative_list:
                generative_list[field_id] = []

            generative_list[field_id].append({
                "prefix": generate.prefix,
                "selected_field": generate.selected_field_id,
                "no_of_zero": generate.no_of_zero,
                "increment": generate.increment,
            })


        form_fields_json = json.dumps([
            {
                "id": field.id,
                "label": field.label,
                "type": field.field_type,
                "section":field.section,
                "options": field.values.split(",") if field.values else [], 
                "attributes": field.attributes if field.attributes else [],
                "validation": validation_dict.get(field.id, []),
                "generative_list": generative_list
            }
            for field in fields
        ])
    except Exception as e:
        traceback.print_exc()
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    return render(request, "Form/form_builder.html", {
        "form": form,
        "regex": json.dumps(regex),
        "form_fields_json": form_fields_json,
        "dropdown_options": json.dumps(dropdown_options),
        "common_options": json.dumps(common_options),
        "sub_control": json.dumps(sub_control),
        "master_dropdown": json.dumps(master_dropdown),
        "form_names":json.dumps(form_names),
        "section_names":json.dumps(section),
        "version":json.dumps(version)
    })


def format_label(label):
    """Format label to have proper capitalization."""
    words = re.split(r'[_ ]+', label.strip())
    return ' '.join(word.capitalize() for word in words)



@login_required
def save_form(request):
    user  = request.session.get('user_id', '')
    try:
        if request.method == "POST":
            form_name = request.POST.get("form_name")
            form_description = request.POST.get("form_description")
            form_data_json = request.POST.get("form_data")

            if not form_data_json:
                return JsonResponse({"error": "No form data received"}, status=400)

            try:
                form_data = json.loads(form_data_json)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

            
            form = Form.objects.create(name=form_name, description=form_description)
            index = 0
            generative_fields = [] 

            for  index,field in enumerate(form_data):
               
                if field.get("type") == "master dropdown":
                    value = field.get("masterValue")

                elif field.get("type") == "multiple":
                    value = field.get("multiMasterValue")

                elif field.get("type") == "field_dropdown":
                    dropdown_mappings = field.get("field_dropdown", [])
                    form_id_selected = dropdown_mappings.get("form_id","")
                    field_id_selected = dropdown_mappings.get("field_id","")
                    if form_id_selected and field_id_selected:
                        value = f"{form_id_selected},{field_id_selected}"
            
                    # value = dec(value)
                else:
                    value=",".join(option.strip() for option in field.get("options", []))

                
                formatted_label = format_label(field.get("label", ""))
                order = field.get("order","")

                form_field = FormField.objects.create(
                    form=form,
                    label=formatted_label, 
                    section = field.get("section",""), # Use formatted label here
                    field_type=field.get("type", ""),
                    attributes=field.get("attributes", "[]"),
                    values=value,
                    created_by=request.session.get('user_id', '').strip(),
                    order=order
                )
                
                field_id = form_field.id

               
                # Handle regex & max_length validation separately
                if "validation" in field and isinstance(field["validation"], list):
                    for validation_item in field["validation"]:
                        validation_type = validation_item.get("validation_type")
                        validation_value = validation_item.get("validation_value", "")
                        sub_master_id = validation_item.get("id")  # Get sub_master_id for regex

                        if validation_type and validation_value and sub_master_id:
                            FieldValidation.objects.create(
                                field=get_object_or_404(FormField, id=field_id),
                                form=get_object_or_404(Form, id=form.id),
                                sub_master_id=sub_master_id,  # Save regex/max_length master ID
                                value=validation_value,
                                created_by = request.session.get('user_id', '').strip()  # Save regex pattern or max_length
                            )


                # ✅ Save `file` validation (New Logic)
                if field.get("type") == "file" and "validation" in field:
                    file_validation_list = field["validation"]  # This is a list

                    if file_validation_list and isinstance(file_validation_list, list):
                        file_validation = file_validation_list[0]  # Get first item (dictionary)

                        file_validation_value = file_validation.get("validation_value", "")  # Extract ".jpg, .jpeg, .png"
                        sub_master_id = file_validation.get("id", None)  # Extract "2"

                        # Create FieldValidation record
                        FieldValidation.objects.create(
                            field=get_object_or_404(FormField, id=field_id),
                            form=get_object_or_404(Form, id=form.id),
                            sub_master_id=sub_master_id,  # Save only the ID
                            value=file_validation_value,
                            created_by = request.session.get('user_id', '').strip()
                        )

                if field.get("type") == "file multiple" and "validation" in field:
                    file_validation_list = field["validation"]  # This is a list of validation dicts

                    if file_validation_list and isinstance(file_validation_list, list):
                        for file_validation in file_validation_list:
                            file_validation_value = file_validation.get("validation_value", "")
                            sub_master_id = file_validation.get("id", None)

                            FieldValidation.objects.create(
                                field=get_object_or_404(FormField, id=field_id),
                                form=get_object_or_404(Form, id=form.id),
                                sub_master_id=sub_master_id,
                                value=file_validation_value,
                                created_by = request.session.get('user_id', '').strip()
                            )

                if field.get("type") == "generative":
                    generative_fields.append({
                        "form_field": form_field,
                        "prefix": field.get("prefix", ""),
                        "field_names": field.get("field_name", []),
                        "no_of_zero": field.get("no_of_zero", ""),
                        "increment": field.get("increment", "")
                    })

                

                    for gen_field in generative_fields:
                        
                        prefix = gen_field["prefix"]
                        if isinstance(prefix, (list, tuple)):
                            prefix = prefix[0] if prefix else ""

                        field_ids = FormField.objects.filter(
                            form=form,
                            label__in=gen_field["field_names"]
                        ).values_list("id", flat=True)

                        FormGenerativeField.objects.create(
                            prefix=gen_field["prefix"],
                            selected_field_id=",".join(map(str, field_ids)),  # Convert IDs to comma-separated string
                            no_of_zero=gen_field["no_of_zero"],
                            increment=gen_field["increment"],
                            form=form,
                            field=gen_field["form_field"]
                        )




            callproc('create_dynamic_form_views')
            messages.success(request, "Form and fields saved successfully!!")
            new_url = f'/masters?entity=form&type=i'
            return redirect(new_url) 

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    finally:
        Db.closeConnection()



@login_required
def update_form(request, form_id):
    user = request.session.get('user_id', '')
    try:
        if request.method == "POST":
            form_name = request.POST.get("form_name")
            form_description = request.POST.get("form_description")
            form_data_json = request.POST.get("form_data")

            if not form_data_json:
                return JsonResponse({"error": "No form data received"}, status=400)

            try:
                form_data = json.loads(form_data_json)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)
            
            FieldValidation.objects.filter(form=form_id).delete()

            
            form = get_object_or_404(Form, id=form_id)
            form.name = form_name
            form.description = form_description
            updated_by = request.session.get('user_id', '').strip()
            form.save()
            index = 0
            # existing_field_ids = set(FormField.objects.filter(form=form).values_list("id", flat=True))
            # incoming_field_ids = set()

            existing_field_ids = set(FormField.objects.filter(form=form).values_list("id", flat=True))
            incoming_field_ids = set()

            for field in form_data:
                if field.get("id"):
                    incoming_field_ids.add(int(field["id"]))

            generative_fields = [] 

            for index,field in enumerate(form_data):
                attributes_value = field.get("attributes", "[]")
                field_id = field.get("id", "")
                formatted_label = format_label(field.get("label", ""))
                order = field.get("order","")

                if field.get("type") == "master dropdown":
                    value = field.get("masterValue")

                elif field.get("type") == "multiple":
                    value = field.get("multiMasterValue")
                
                elif field.get("type") == "field_dropdown":
                    dropdown_mappings = field.get("field_dropdown", [])
                    if dropdown_mappings:
                        form_id_selected = dropdown_mappings.get("form_id","")
                        field_id_selected = dropdown_mappings.get("field_id","")
                        if form_id_selected and field_id_selected:
                            value = f"{form_id_selected},{field_id_selected}"

                    else:
                        if field.get("options"):
                            # Assuming options is an array like ["91", "1206"]
                            value = f"{field['options'][0]},{field['options'][1]}"  # First option as form_id, second as field_id
                        else:
                            value = ""
                    
                    # Store the value
                    field["value"] = value

                else:
                    value = ",".join(option.strip() for option in field.get("options", []))

                if field_id:
                    try:
                        form_field = FormField.objects.get(id=field_id)
                        form_field.label = formatted_label
                        form_field.field_type = field.get("type", "")
                        form_field.section = field.get("section","")
                        form_field.attributes = attributes_value
                        form_field.values = value
                        form_field.order = order
                        form_field.updated_by = user
                        form_field.save()
                    except FormField.DoesNotExist:
                        # Field ID not found, create new
                        form_field = FormField.objects.create(
                            form=form,
                            label=formatted_label,
                            field_type=field.get("type", ""),
                            attributes=attributes_value,
                            values=value,
                            created_by=user,
                            order=order
                        )
                else:
                    # New field with no ID
                    form_field = FormField.objects.create(
                        form=form,
                        label=formatted_label,
                        field_type=field.get("type", ""),
                        attributes=attributes_value,
                        values=value,
                        created_by=user,
                        order=order
                    )

                field_id = form_field.id



                # ✅ Ensure 'subValues' exists
                if "validation" in field and isinstance(field["validation"], list):
                    for validation_item in field["validation"]:
                        validation_type = validation_item.get("validation_type")
                        validation_value = validation_item.get("validation_value", "")
                        sub_master_id = validation_item.get("id")  # Get sub_master_id for regex

                        if validation_type and validation_value and sub_master_id:
                            FieldValidation.objects.create(
                                field=get_object_or_404(FormField, id=field_id),
                                form=get_object_or_404(Form, id=form.id),
                                sub_master_id=sub_master_id,  # Save regex/max_length master ID
                                value=validation_value, 
                                created_by = user,
                                updated_by = user
                            )
                if field.get("type") == "file" and "validation" in field:
                    file_validation_list = field["validation"]  # This is a list

                    if file_validation_list and isinstance(file_validation_list, list):
                        file_validation = file_validation_list[0]  # Get first item (dictionary)

                        file_validation_value = file_validation.get("validation_value", "")  # Extract ".jpg, .jpeg, .png"
                        sub_master_id = file_validation.get("id", None)  # Extract "2"
                        FieldValidation.objects.filter(field_id=field_id, form_id=form.id).delete()

                        # Then insert new validation
                        FieldValidation.objects.create(
                            field=get_object_or_404(FormField, id=field_id),
                            form=get_object_or_404(Form, id=form.id),
                            sub_master_id=sub_master_id,
                            value=validation_value, 
                            created_by = user,
                            updated_by = user
                        )


                elif field.get("type") == "file multiple" and "validation" in field:
                    file_validation_list = field["validation"]  # This is a list of validation dicts

                    if file_validation_list and isinstance(file_validation_list, list):
                        file_validation = file_validation_list[0]  # Get first item (dictionary)

                        file_validation_value = file_validation.get("validation_value", "")  # Extract ".jpg, .jpeg, .png"
                        sub_master_id = file_validation.get("id", None)  # Extract "2"

                        FieldValidation.objects.filter(field_id=field_id, form_id=form.id).delete()

                        # Then insert new validation
                        FieldValidation.objects.create(
                            field=get_object_or_404(FormField, id=field_id),
                            form=get_object_or_404(Form, id=form.id),
                            sub_master_id=sub_master_id,
                            value=validation_value, 
                            created_by = user,
                            updated_by = user
                        )


                if field.get("type") == "generative":
                    generative_fields.append({
                        "form_field": form_field,
                        "prefix": field.get("prefix", ""),
                        "field_ids": field.get("field_name", []),
                        "no_of_zero": field.get("no_of_zero", ""),
                        "increment": field.get("increment", "")
                    })


                for gen_field in generative_fields:
                    prefix = gen_field["prefix"]
                    if isinstance(prefix, (list, tuple)):
                        prefix = prefix[0] if prefix else ""

                    field_ids = FormField.objects.filter(
                        form=form,
                        label__in=gen_field["field_ids"]
                    ).values_list("id", flat=True)

                    # Skip if all critical fields are empty
                    if not prefix and not field_ids and not gen_field["no_of_zero"] and not gen_field["increment"]:
                        continue
                    else:
                        FormGenerativeField.objects.filter(form_id=form.id).delete()

                        FormGenerativeField.objects.create(
                            prefix=prefix,
                            selected_field_id=",".join(map(str, field_ids)),  # Convert IDs to comma-separated string
                            no_of_zero=gen_field["no_of_zero"],
                            increment=gen_field["increment"],
                            form=form,
                            field=gen_field["form_field"]
                        )

                removed_field_ids = existing_field_ids - incoming_field_ids
                if removed_field_ids:
                    FormField.objects.filter(id__in=removed_field_ids).delete()
           

            callproc('create_dynamic_form_views')
            messages.success(request, "Form updated successfully!!")
            return redirect('/masters?entity=form&type=i')
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), request.user])
        messages.error(request, "Oops...! Something went wrong!")
        return JsonResponse({"error": "Something went wrong!"}, status=500)
    finally:
        Db.closeConnection()


@login_required
def form_action_builder(request):
    try:
        user  = request.session.get('user_id', '')
        action_id = request.GET.get('action_id')
        master_values = FormAction.objects.filter(is_master = 1).all()
        button_type = list(CommonMaster.objects.filter(type='button').values("control_value"))
        dropdown_options = list(ControlParameterMaster.objects.filter(is_action=1).values("control_name", "control_value"))

        if not action_id:  
            return render(request,  "Form/form_action_builder.html", {
                "master_values":master_values,
                "button_type":json.dumps(button_type),
                "dropdown_options": json.dumps(dropdown_options),
            })

        try:
            action_id = dec(action_id)  # Decrypt form_id
            form = get_object_or_404(FormAction, id=action_id) 
            fields = FormActionField.objects.filter(action_id=action_id)
        except Exception as e:
            print(f"Error fetching form data: {e}")  # Debugging
            return render(request, "Form/form_action_builder.html", {\
                "dropdown_options": json.dumps(dropdown_options),
                "error": "Invalid form ID"
            })


        form_fields_json = json.dumps([
            {
                "id": field.id,
                "label": field.label_name,
                "bg_color":field.bg_color,
                "text_color":field.text_color,
                "type": field.type,
                "options": field.dropdown_values.split(",") if field.dropdown_values else [],
                "button_type":field.button_type,
                "status":field.status,
                "value":field.button_name
            }
            for field in fields
        ])
    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)
    
    
    return render(request, "Form/form_action_builder.html", {
        "form": form,
        "master_values":master_values,
        "button_type":json.dumps(button_type),
        "form_fields_json": form_fields_json,
        "dropdown_options": json.dumps(dropdown_options),
    })

@login_required
def form_action_builder_master(request):
    user  = request.session.get('user_id', '')
    action_id = request.GET.get('action_id')
    try:

        if action_id:  # AJAX call to fetch form data
            try:
                form = get_object_or_404(FormAction, id=action_id)
                fields = FormActionField.objects.filter(action_id=action_id)

                form_fields_json = [
                    {
                        "id": field.id,
                        "label": field.label_name,
                        "bg_color": field.bg_color,
                        "text_color": field.text_color,
                        "type": field.type,
                        "options": field.dropdown_values.split(",") if field.dropdown_values else [],
                        "button_type": field.button_type,
                        "status": field.status,
                        "value": field.button_name
                    }
                    for field in fields
                ]

                return JsonResponse({"formFields": form_fields_json})
            
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

        # If no action_id: Initial full page render
        master_values = FormAction.objects.filter(is_master=1).all()
        button_type = list(CommonMaster.objects.filter(type='button').values("control_value"))
        dropdown_options = list(ControlParameterMaster.objects.filter(is_action=1).values("control_name", "control_value"))
    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)
    
    
    return render(request, "Form/form_action_builder.html", {
        "master_values": master_values,
        "button_type": json.dumps(button_type),
        "dropdown_options": json.dumps(dropdown_options),
    })




@login_required
def save_form_action(request):
    user  = request.session.get('user_id', '')
    try:

        if request.method == "POST":
            form_name = request.POST.get("action_name")
            form_master = 1 if request.POST.get("is_master") == "on" else 0
            form_data_json = request.POST.get("form_data")

            if not form_data_json:
                return JsonResponse({"error": "No form data received"}, status=400)

            try:
                form_data = json.loads(form_data_json)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

            
            form_action = FormAction.objects.create(name=form_name,is_master= form_master,created_by = user)


            for field in form_data:
                field_type = field.get("type", "")
                
                if field_type == "button":
                    label_name = None
                    dropdown_values = None
                    bg_color = field.get("bg_color", "")
                    text_color = field.get("text_color", "")
                    status = field.get("status","")
                    button_name = field.get("value", "")
                else:
                    label_name = field.get("label", "")
                    button_name= None
                    bg_color = None
                    text_color = None
                    status = field.get("status", None)
                    if status in ["", "[]", [], {}, None]:
                        status = None
                    

                # Create the form field entry
                FormActionField.objects.create(
                    action=form_action,
                    type=field_type,
                    label_name=label_name,
                    button_name= button_name,
                    bg_color=bg_color,
                    text_color=text_color,
                    button_type=field.get("button_type", ""),
                    status=status,
                    dropdown_values=",".join(option.strip() for option in field.get("options", [])),
                    created_by = user
                )

            messages.success(request, "Form Action and fields saved successfully!!")
            new_url = f'/masters?entity=action&type=i'
            return redirect(new_url) 

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    finally:
        Db.closeConnection()

@login_required
def update_action_form(request, form_id):
    user  = request.session.get('user_id', '')
    try:  # Decoding action_id if necessary

        if request.method == "POST":
            # Getting form data from POST request
            form_name = request.POST.get("action_name")
            form_master = 1 if request.POST.get("is_master") == "on" else 0
            form_data_json = request.POST.get("form_data")

            if not form_data_json:
                return JsonResponse({"error": "No form data received"}, status=400)

            try:
                form_data = json.loads(form_data_json)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

            # Update the FormAction instance
            form_action = FormAction.objects.filter(id=form_id).first() if form_id else None
            if not form_action:
                return JsonResponse({"error": "Form action not found"}, status=404)

            form_action.name = form_name
            form_action.is_master = form_master
            form_action.updated_by= user
            form_action.save()

            # Delete existing form fields for this action
            FormActionField.objects.filter(action_id=form_id).delete()

            # Insert the new form fields
            for field in form_data:
                field_type = field.get("type", "").strip()

                if field_type == "button":
                    label_name = None
                    bg_color = field.get("bg_color", "")
                    text_color = field.get("text_color", "")
                    status = field.get("status", None).strip() if field.get("status") else None
                    button_name = field.get("value", "").strip()
                else:
                    label_name = field.get("label", "").strip()
                    button_name = None
                    bg_color = None
                    text_color = None
                    status = field.get("status", None)
                    if status in ["", "[]", [], {}, None]:
                        status = None
                    

                # Create the form field entry
                FormActionField.objects.create(
                    action=form_action,
                    type=field_type,
                    label_name=label_name,
                    button_name=button_name,
                    bg_color=bg_color,
                    text_color=text_color,
                    button_type=field.get("button_type", ""),
                    status=status,
                    dropdown_values=",".join(option.strip() for option in field.get("options", [])),
                    updated_by = user,
                    created_by = user
                )

            messages.success(request, "Form Action and fields Updated successfully!!")
            new_url = f'/masters?entity=action&type=i'
            return redirect(new_url)

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    finally:
        Db.closeConnection()

@login_required
def form_master(request):
    user  = request.session.get('user_id', '')
    try:

        if request.method == "POST":
            form_id = request.POST.get("form")
            form = get_object_or_404(Form, id=form_id)

            raw_fields = FormField.objects.filter(form_id=form_id).values(
                "id", "label", "field_type", "values", "attributes", "form_id", "form_id__name", "section"
            ).order_by("order")

            sectioned_fields = {}

            for field in raw_fields:
                # Clean up values and attributes
                field["values"] = [v.strip() for v in field["values"].split(",")] if field.get("values") else []
                field["attributes"] = [a.strip() for a in field["attributes"].split(",")] if field.get("attributes") else []

                # Get section name
                section_id = field.get("section")
                if section_id:
                    try:
                        section = SectionMaster.objects.get(id=section_id)
                        section_name = section.name
                    except SectionMaster.DoesNotExist:
                        section_name = ""
                else:
                    section_name = ""

                field["section_name"] = section_name

                # Fetch validations
                validations = FieldValidation.objects.filter(
                    field_id=field["id"], form_id=form_id
                ).values("value")
                field["validations"] = list(validations)

                # Regex detection
                if any("^" in v["value"] for v in field["validations"]):
                    field["field_type"] = "regex"
                    pattern_value = field["validations"][0]["value"]
                    try:
                        regex_obj = RegexPattern.objects.get(regex_pattern=pattern_value)
                        field["regex_id"] = regex_obj.id
                        field["regex_description"] = regex_obj.description
                    except RegexPattern.DoesNotExist:
                        field["regex_id"] = None
                        field["regex_description"] = ""

                if field["field_type"] == "file_name":
                    queryset = WorkflowVersionControl.objects.filter(
                        ~Q(baseline_date__isnull=True) & ~Q(baseline_date=0)
                    )
                    filtered_records = queryset.values("file_name")
                    if queryset.exists():
                        field["file_name_options"] = [record["file_name"] for record in filtered_records]


                # Accept type (file/text)
                if field["field_type"] in ["file", "file multiple", "text"]:
                    file_validation = next((v for v in field["validations"]), None)
                    field["accept"] = file_validation["value"] if file_validation else ""

                # Field Dropdown (dynamic values)
                if field["field_type"] == "field_dropdown":
                    split_values = field["values"]
                    if len(split_values) == 2:
                        dropdown_form_id, dropdown_field_id = split_values
                        field_values = FormFieldValues.objects.filter(field_id=dropdown_field_id).values("value").distinct()
                        field["dropdown_data"] = list(field_values)

                # Master Dropdown
                if field["field_type"] == "master dropdown" and field["values"]:
                    dropdown_id = field["values"][0]
                    try:
                        master_data = MasterDropdownData.objects.get(id=dropdown_id)
                        query = master_data.query
                        result = callproc("stp_get_query_data", [query])
                        field["values"] = [{"id": row[0], "name": row[1]} for row in result]
                    except MasterDropdownData.DoesNotExist:
                        field["values"] = []

                # Group by section name
                sectioned_fields.setdefault(section_name, []).append(field)

            context = {
                "sectioned_fields": sectioned_fields,
                "type": "master",
                "form_name": form
            }
            html = render_to_string("Form/_formfields.html", context)
            return JsonResponse({'html': html}, safe=False)


        

        
        else:
        
            form_data_id = request.GET.get("form")
            button_type_id = request.GET.get("button_type_id")
            workflow_YN = request.GET.get('workflow_YN', '')
            step_id = request.GET.get('step_id', '')
            form_id_wf = request.GET.get('form_idWF', '')
            role_id = request.GET.get('role_id', '')
            wfdetailsID = request.GET.get('wfdetailsID', '')
            readonlyWF = request.GET.get('readonlyWF', '')
            viewStepWF = request.GET.get('viewStepWF', '')
            type = request.GET.get('type','')
            req_num = request.GET.get('req_num','')
            category_dropD = para_master.objects.filter(para_name='Category').values(value=F('para_details'), text=F('description'))

            
            if form_data_id:
                form_data_id = dec(form_data_id)
                form_instance = FormData.objects.filter(id=form_data_id).values("id","form_id", "action_id").first()
                file_ref = VersionControlFileMap.objects.filter(form_data=form_data_id)

                if file_ref:
                    reference_type = '1'
                    new_data_id = form_data_id
                else:
                    reference_type = '0'
                    new_data_id = form_data_id
                if step_id == '1' or step_id == '6' or readonlyWF == '1':
                    version_no = 1.0
                else:
                    version_no = get_object_or_404(WorkflowVersion, req_id=req_num).version

                step_name_subquery = Subquery(workflow_matrix.objects.filter(id=OuterRef('step_id')).values('step_name')[:1])
                custom_user_role_id_subquery = Subquery(CustomUser.objects.filter(id=OuterRef('created_by')).values('role_id')[:1])
                custom_email_subquery = Subquery(CustomUser.objects.filter(id=OuterRef('created_by')).values('email')[:1])
                comments_base = ActionData.objects.filter(form_data_id=form_data_id,version = version_no,field__type__in=['text', 'textarea', 'select']
                ).annotate(step_name=step_name_subquery,role_id=custom_user_role_id_subquery,email=custom_email_subquery)
                comments = comments_base.annotate(role_name=Subquery(roles.objects.filter(id=OuterRef('role_id')).values('role_name')[:1])
                ).values('field_id','value','step_id','created_at','created_by','step_name','role_name','email',)

                grouped_comments = defaultdict(list)

                for comment in comments:
                    key = (comment['step_name'], comment['role_name'], comment['email'])
                    grouped_comments[key].append({'value': comment['value'], 'created_at': comment['created_at']})

                grouped_data = []
                sr_no_counter = 1

                for (step_name, role_name, email), comment_list in grouped_comments.items():
                    grouped_data.append({
                        'sr_no': sr_no_counter,
                        'step_name': step_name,
                        'role_name': role_name,
                        'email': email,
                        'comments': comment_list,
                        'rowspan': len(comment_list)
                    })
                    sr_no_counter += 1

                
                if form_instance:
                    form_id = form_instance["form_id"]
                    form = get_object_or_404(Form, id=form_id)

                    action_id = form_instance["action_id"] if button_type_id is None else button_type_id

                    fields = FormField.objects.filter(form_id=form_id).values(
                        "id", "label", "field_type", "values", "attributes", "form_id", "form_id__name", "section"
                    ).order_by("order")
                    fields = list(fields)

                    if reference_type == '1':
                        field_values = FormFieldValuesTemp.objects.filter(form_data_id=form_data_id).values("field_id", "value")
                        if not field_values.exists():
                            field_values = FormFieldValues.objects.filter(form_data_id=form_data_id).values("field_id", "value")
                    else:
                        field_values = FormFieldValues.objects.filter(form_data_id=form_data_id).values("field_id", "value")
                    values_dict = {fv["field_id"]: fv["value"] for fv in field_values}

                    sectioned_fields = defaultdict(list)


                    for field in fields:
                        # Split values and attributes
                        field["values"] = field["values"].split(",") if field.get("values") else []
                        field["attributes"] = field["attributes"].split(",") if field.get("attributes") else []

                        # Section name logic
                        section_id = field.get("section")
                        if section_id:
                            try:
                                section = SectionMaster.objects.get(id=section_id)
                                section_name = section.name
                            except SectionMaster.DoesNotExist:
                                section_name = ""
                        else:
                            section_name = ""

                        # Validation rules
                        validations = FieldValidation.objects.filter(
                            field_id=field["id"], form_id=form_id
                        ).values("value")
                        field["validations"] = list(validations)

                        # Check for regex
                        if any("^" in v["value"] for v in field["validations"]):
                            field["field_type"] = "regex"
                            pattern_value = field["validations"][0]["value"]
                            try:
                                regex_obj = RegexPattern.objects.get(regex_pattern=pattern_value)
                                field["regex_id"] = regex_obj.id
                                field["regex_description"] = regex_obj.description
                            except RegexPattern.DoesNotExist:
                                field["regex_id"] = None
                                field["regex_description"] = ""

                        # File field logic
                        # if field["field_type"] in ["file", "file multiple", "text"]:
                        #     file_validation = next((v for v in field["validations"]), None)
                        #     field["accept"] = file_validation["value"] if file_validation else ""

                        #     if reference_type == '1':
                        #         file_exists = FormFileTemp.objects.filter(field_id=field["id"], form_data_id=form_data_id).exists()
                        #     else:
                        #         file_exists = FormFile.objects.filter(field_id=field["id"], form_data_id=form_data_id).exists()
                        #     field["file_uploaded"] = 1 if file_exists else 0


                        #     if file_exists and "required" in field["attributes"]:
                        #         field["attributes"].remove("required")
# Replace with your actual import path

                        if field["field_type"] in ["file", "file multiple", "text"]:
                            file_validation = next((v for v in field["validations"]), None)
                            field["accept"] = file_validation["value"] if file_validation else ""

                            if reference_type == '1':
                                file_qs = FormFileTemp.objects.filter(field_id=field["id"], form_data_id=form_data_id)
                            else:
                                file_qs = FormFile.objects.filter(field_id=field["id"], form_data_id=form_data_id)

                            file_exists = file_qs.exists()
                            field["file_uploaded"] = 1 if file_exists else 0

                            # ✅ Include encrypted path
                            field["files"] = [
                                {
                                    "name": file.uploaded_name,
                                    "encrypted_path": enc(file.file_path),  # still keep this if needed
                                    "url": request.build_absolute_uri(settings.MEDIA_URL + file.file_path)  # ⬅️ add this
                                }
                                for file in file_qs
                            ] if file_exists else []


                            if file_exists and "required" in field["attributes"]:
                                field["attributes"].remove("required")



                        # Set saved value
                        saved_value = values_dict.get(field["id"], "")
                        if field["field_type"] == "select multiple":
                            field["value"] = [val.strip() for val in saved_value.split(",") if val.strip()]
                        else:
                            field["value"] = saved_value


                        # field_dropdown logic
                        if field["field_type"] == "field_dropdown":
                            split_values = field["values"]
                            if len(split_values) == 2:
                                try:
                                    dropdown_field_id = int(split_values[1])
                                    dropdown_field_values = FormFieldValues.objects.filter(field_id=dropdown_field_id)
                                    field["dropdown_data"] = list(dropdown_field_values.values())
                                    field["saved_value"] = values_dict.get(field["id"])
                                except (ValueError, IndexError):
                                    field["dropdown_data"] = []
                                    field["saved_value"] = ""

                        if field["field_type"] == "file_name":
                            # 1️⃣ get the “baseline” options
                            qs = WorkflowVersionControl.objects.filter(
                                ~Q(baseline_date__isnull=True)
                            )
                            field["file_name_options"] = list(
                                qs
                                .values_list("file_name", flat=True)
                                .distinct()
                            )

                            # 2️⃣ pull the user’s *saved* value for this field (if any)
                            saved = (
                                FormFieldValuesTemp.objects
                                .filter(form_data_id=form_data_id, field_id=field["id"])
                                .values_list("value", flat=True)
                                .first()
                                or
                                FormFieldValues.objects
                                .filter(form_data_id=form_data_id, field_id=field["id"])
                                .values_list("value", flat=True)
                                .first()
                            )

                            # 3️⃣ keep it on the field dict so the template can see it
                            field["saved_value"] = saved

                            # 4️⃣ if it isn’t already in the baseline list, stick it on top
                            if saved and saved not in field["file_name_options"]:
                                field["file_name_options"].insert(0, saved)

                        # master dropdown logic
                        if field["field_type"] == "master dropdown" and field["values"]:
                            try:
                                dropdown_id = field["values"][0]
                                master_data = MasterDropdownData.objects.get(id=dropdown_id)
                                query = master_data.query
                                result = callproc("stp_get_query_data", [query])
                                field["values"] = [{"id": row[0], "name": row[1]} for row in result]
                            except (MasterDropdownData.DoesNotExist, IndexError):
                                field["values"] = []

                        # Group field by section name
                        sectioned_fields[section_name].append(field)

                    # ✅ Fetch action fields (no validations needed)
                    action_fields = list(FormActionField.objects.filter(action_id=action_id).values(
                        "id", "type", "label_name", "button_name", "bg_color", "text_color", 
                        "button_type", "dropdown_values", "status"
                    ))
                    action_fields = list(action_fields)

                    action_data = list(ActionData.objects.filter(form_data_id=form_data_id).values())

                    file_cat_val = WorkflowVersionControl.objects.filter(form_data_id=form_data_id).order_by('-id').values_list('file_category', flat=True).first()
                    

                    for af in action_fields:
                        af["dropdown_values"] = af["dropdown_values"].split(",") if af.get("dropdown_values") else []
                    if workflow_YN == '1E':
                        return render(request, "Form/_formfieldedit.html", {"sectioned_fields": dict(sectioned_fields),"fields": fields,"action_fields":action_fields,"type":"edit","form":form,"form_data_id":form_data_id,"workflow":workflow_YN,"reference_type":reference_type,
                                    "step_id":step_id,"form_id":form_id_wf,"action_detail_id":2,"role_id":role_id,"wfdetailsid":wfdetailsID,"viewStepWFSeq":viewStepWF,"action_data":action_data,"new_data_id":new_data_id,"grouped_data":grouped_data,"category_dropD":category_dropD,'file_cat_val': file_cat_val,})
                    else:
                        return render(request, "Form/_formfieldedit.html", {"sectioned_fields": dict(sectioned_fields),"fields": fields,"action_fields":action_fields,"type":"edit","form":form,"form_data_id":form_data_id,"readonlyWF":readonlyWF,"viewStepWFSeq":'0',"action_data":action_data,"type":type,"reference_type":reference_type,"grouped_data":grouped_data})
            else:
                type = request.GET.get("type")
                form = Form.objects.all().order_by('-id')
                return render(request, "Form/form_master.html", {"form": form,"type":type})
    
    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)
    

def common_form_post(request):
    user = request.session.get('user_id', '')
    user_name = request.session.get('username', '')
    entity = request.POST.get('entity')
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)
        
        
        created_by = user
        form_name = request.POST.get('form_name', '').strip()
        type = request.POST.get('type','')

        workflow_YN = request.POST.get('workflow_YN', '')
        form_id = request.POST.get("form_id")
        editORcreate  = request.POST.get('editORcreate','')
        firstStep = request.POST.get("firstStep")
        
        
        form = get_object_or_404(Form, id=request.POST.get("form_id"))

        if type != 'master':
            action = get_object_or_404(FormAction,id  = request.POST.get("action_id"))

        if type == 'master':
            form_data = FormData.objects.create(form=form)
        else:
            form_data = FormData.objects.create(form=form,action=action)
            form_data.req_no = f"UNIQ-NO-00{form_data.id}"
        form_data.created_by = user
        form_data.save()
        
        form_dataID = form_data.id
        first_field_checked = False
        

        # Process each field
        for key, value in request.POST.items():
            if key.startswith("field_id_"):
                field_id = value.strip()
                field = get_object_or_404(FormField, id=field_id)

                if field.field_type == "select multiple":
                    selected_values = request.POST.getlist(f"field_{field_id}")
                    input_value = ','.join([val.strip() for val in selected_values if val.strip()])
                else:
                    input_value = request.POST.get(f"field_{field_id}", "").strip()
                    
                    
                if field.field_type == "generative":                   
                    continue
                
                if not first_field_checked and firstStep == '1':
                    totalStep_wf = workflow_matrix.objects.filter(
                        workflow_name='CIDCO File Scanning and DMS Flow'
                    ).count()

                    step_ids_list = list(
                        workflow_details.objects.filter(
                            file_number=input_value
                        ).values_list('step_id', flat=True)
                    )

                    already_exists = FormFieldValues.objects.filter(
                        value=input_value,
                        field_id=field_id
                    ).exists()
                    fileNumber_input_WF =input_value

                    # Logic:
                    # If any of the step_ids for this file are not the final step number, then stop
                    if already_exists:
                        if any(step_id != totalStep_wf for step_id in step_ids_list):
                            print("Same file is already in process and not at final step. Halting process.")
                            break
                        else:
                            print("Same file is at final step. Proceeding.")
                    else:
                        print("File number not found before. Proceeding.")

                    first_field_checked = True
                else:
                    already_exists = False
                         
                FormFieldValues.objects.create(
                    form_data=form_data,form=form, field=field, value=input_value, created_by=created_by
                )

                if field.field_type == "file_name":

                    form_data.file_ref = input_value
                    if input_value and input_value != 'New File':
                        VersionControlFileMap.objects.create(form_data=form_dataID,file_name= input_value,status= 0)
                    form_data.save()
                    if input_value and input_value != 'New File':

                        form_field_value_obj = FormFieldValues.objects.filter(value=input_value).first()
                        if form_field_value_obj:
                            form_data_id = form_field_value_obj.form_data_id
                        if form_data:
                            VersionControlFileMap.objects.create(form_data=form_data_id,file_name= input_value, status= 0)

                if field.field_type == 'field_dropdown':
                    values = field.values 
                    
                    if values:
                        parts = values.split(',')
                        if len(parts) == 2:
                            form_id = parts[0].strip()
                            field_id = parts[1].strip()

                            try:
                            # Lookup FormField with the extracted form_id and field_id
                                linked_field = FormField.objects.get(id=field_id, form_id=form_id)

                                if linked_field.label == "File Name":
                                    # Check if input_value exists in ControlFileMap
                                    if VersionControlFileMap.objects.filter(file_name=input_value).exists():
                                        VersionControlFileMap.objects.create(
                                            form_data=form_dataID,
                                            file_name=input_value
                                        )
                            except FormField.DoesNotExist:
                                pass  

        

        if already_exists is not True:
            handle_uploaded_files(request, form_name, created_by, form_data, user)
            if  type == 'master':
                if field.field_type == 'generative':
                    file_name = handle_generative_fields(form, form_data, created_by)
            else:
                file_name = handle_generative_fields(form, form_data, created_by)
        # else:
        #     messages.error(request, 'File Number Already Exists!')
        # callproc('create_dynamic_form_views')
        messages.success(request, "Form data saved successfully!") 
        if workflow_YN == '1' and already_exists is not True:
            wfdetailsid = request.POST.get('wfdetailsid', '')
            role_idC = request.POST.get('role_id', '')
            form_id = request.POST.get('form_id', '')
            step_id = request.POST.get('step_id', '')
            if wfdetailsid and wfdetailsid != 'undefined':
                wfdetailsid=dec(wfdetailsid)
            else:
                wfdetailsid = None  
            
            if step_id:
                matrix_entry = workflow_matrix.objects.filter(id=step_id).first()
                if matrix_entry:
                    status_from_matrix = matrix_entry.status  # adjust field name if needed
                    
            if wfdetailsid and workflow_details.objects.filter(id=wfdetailsid).exists():
                # Update existing record
                workflow_detail = workflow_details.objects.get(id=wfdetailsid)
                workflow_detail.form_data_id = form_dataID
                workflow_detail.role_id = request.POST.get('role_id', '')
                workflow_detail.action_details_id = request.POST.get('action_detail_id', '')
                workflow_detail.increment_id += 1
                workflow_detail.step_id = request.POST.get('step_id', '')
                workflow_detail.status = status_from_matrix or ''
                workflow_detail.user_id = user
                workflow_detail.updated_by = user  # Or use `modified_by` if applicable
                workflow_detail.updated_at = now()
                workflow_detail.save()    
            else:    
                workflow_detail = workflow_details.objects.create(
                form_data_id=form_dataID,
                role_id=request.POST.get('role_id', ''),
                action_details_id=request.POST.get('action_detail_id', ''),
                increment_id=1,
                # form_id=request.POST.get('form_id', ''),
                # action_id=request.POST.get('action_id', ''),
                status = status_from_matrix or '',
                step_id=request.POST.get('step_id', ''),
                operator=request.POST.get('selected_operator', ''),
                file_number=fileNumber_input_WF,
                user_id=user,
                created_by=user,
                created_at=now(),
                updated_by = user,
                updated_at = now()
                
                )

            # Now set and save req_id using the generated ID
            workflow_detail.req_id = f"REQNO-00{workflow_detail.id}"
            workflow_detail.save()
            if wfdetailsid and workflow_details.objects.filter(id=wfdetailsid).exists():
                history_workflow_details.objects.create(
                    form_data_id=workflow_detail.form_data_id,
                    role_id=workflow_detail.role_id,
                    action_details_id=workflow_detail.action_details_id,
                    increment_id=workflow_detail.increment_id,
                    step_id=workflow_detail.step_id,
                    status=workflow_detail.status,
                    user_id=workflow_detail.user_id,
                    req_id=workflow_detail.req_id,
                    form_id=request.POST.get('form_id', ''),
                    created_by=user,
                    # created_by=workflow_detail.updated_by,
                    created_at=workflow_detail.updated_at
                )
            else:
                history_workflow_details.objects.create(
                    form_data_id=workflow_detail.form_data_id,
                    role_id=workflow_detail.role_id,
                    action_details_id=workflow_detail.action_details_id,
                    increment_id=workflow_detail.increment_id,
                    step_id=workflow_detail.step_id,
                    status=workflow_detail.status,
                    user_id=workflow_detail.user_id,
                    req_id=workflow_detail.req_id,
                    operator=request.POST.get('selected_operator', ''),
                    form_id=request.POST.get('form_id', ''),
                    created_by=user,
                    # created_by=workflow_detail.updated_by,
                    created_at=workflow_detail.updated_at
                )
            if role_idC == '1':
                latest_record = WorkflowVersionControl.objects.filter(
                    file_name=form_data.file_ref
                ).order_by('-id').first()

                    # Determine the file_category and latest temp_version
                latest_file_category = latest_record.file_category if latest_record else None
                latest_temp_version = latest_record.temp_version if latest_record else None

                    # Determine new temp_version
                if latest_temp_version is None:
                    temp_version = Decimal('1.0')
                else:
                    temp_version = Decimal(str(latest_temp_version)) + Decimal('0.1')

                WorkflowVersion.objects.create(req_id = workflow_detail.req_id, version = temp_version)
            if role_idC == '2':
            # Check if any row with version_no=0 exists for the given file_name
                reject_case = WorkflowVersionControl.objects.filter(
                    file_name=file_name,
                    version_no=0
                ).exists()

                if not reject_case:
                    latest_record = WorkflowVersionControl.objects.filter(
                        file_name=file_name
                    ).order_by('-id').first()

                    # Determine the file_category and latest temp_version
                    latest_file_category = latest_record.file_category if latest_record else None
                    latest_temp_version = latest_record.temp_version if latest_record else None

                    # Determine new temp_version
                    if latest_temp_version is None:
                        temp_version = Decimal('1.0')
                    else:
                        temp_version = Decimal(str(latest_temp_version)) + Decimal('0.1')

                    # Create the new row
                    WorkflowVersionControl.objects.create(
                        file_name=file_name,
                        version_no=0,
                        temp_version=temp_version,
                        modified_by=user_name,
                        modified_at=now(),
                        file_category=latest_file_category,
                        form_data_id=form_dataID
                    )

                    # WorkflowVersion.objects.create(req_id = workflow_detail.req_id, version = temp_version)
            if role_idC == '5':
                count_row = WorkflowVersionControl.objects.filter(file_name=file_name).count()
                latest_row = WorkflowVersionControl.objects.filter(
                    file_name=file_name
                    ).order_by('-id').values_list('id', flat=True).first()
                if latest_row and count_row == 1:
                    latest_row.version_no = 1
                    latest_row.save()
                

            for key, value in request.POST.items():
                if key.startswith("action_field_") and not key.startswith("action_field_id_"):
                    match = re.match(r'action_field_(\d+)', key)
                    latest_row = WorkflowVersionControl.objects.filter(file_name=form_data.file_ref).order_by('-id').first()

                    if role_idC != '5' or role_idC != '6':
                        if latest_row and latest_row.temp_version is not None:
                            temp_vers = Decimal(str(latest_row.temp_version))
                        else:
                            temp_vers = Decimal('1.0')
                    else:
                        temp_vers = Decimal('1.0')
                    if match:
                        field_id = int(match.group(1))
                        action_field = get_object_or_404(FormActionField, pk=field_id)
                        if action_field.type in ['text', 'textarea', 'select']:
                            ActionData.objects.create(
                                value=value,
                                form_data=get_object_or_404(FormData, id= form_dataID),
                                field=action_field,
                                step_id=step_id,
                                version = temp_vers,
                                created_by=user,
                                updated_by=user,
                            )
            
            messages.success(request, "Workflow data saved successfully!")
        else:
            messages.error(request, 'File Number Already Exists!')
    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    finally:
        if workflow_YN == '1':
            return redirect('workflow_starts')
        else:
            return redirect('/masters?entity=form_master&type=i')

@login_required
def common_form_edit(request):

    user = request.session.get('user_id', '')
    user_name = request.session.get('username', '')
    workflow_YN = request.POST.get("workflow_YN")
    step_id  = request.POST.get("step_id")
    
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)
        
        type = request.POST.get("type","")
        reference_type  = request.POST.get("reference_type","")
        if type == 'reference':
            workflow_YN = '1E'
            form_data_id = request.POST.get("new_data_id")
        else:
            form_data_id = request.POST.get("form_data_id")
        if not form_data_id:
            return JsonResponse({"error": "form_data_id is required"}, status=400)

        form_data = get_object_or_404(FormData, id=form_data_id)
        form_data.updated_by = user
        form_data.save()

        form = get_object_or_404(Form, id=request.POST.get("form_id"))

        created_by = request.session.get("user_id", "").strip()
        form_name = request.POST.get("form_name", "").strip()
        type = request.POST.get("type","")

        file_no_field = FormField.objects.filter(form=form, label__iexact='File No').first()
        file_no_field_id = str(file_no_field.id) if file_no_field else None
        
        
        for key, value in request.POST.items():
            if key.startswith("field_id_"):
                field_id = value.strip()
                field = get_object_or_404(FormField, id=field_id)

                if field_id == file_no_field_id:
                    continue

                if field.field_type == "select multiple":
                    selected_values = request.POST.getlist(f"field_{field_id}")
                    input_value = ','.join([val.strip() for val in selected_values if val.strip()])
                else:
                    input_value = request.POST.get(f"field_{field_id}", "").strip()

                if field.field_type == "generative":
                    file_name = get_object_or_404(FormFieldValues, form_data_id=form_data, field_id=field).value
                    continue

                if field.field_type in ['file', 'file multiple']:
                    continue

                if type != 'reference' or reference_type !='1':
                    existing_value = FormFieldValues.objects.filter(
                        form_data=form_data, form=form, field=field
                    ).first()
                    if existing_value:
                        existing_value.value = input_value
                        existing_value.save()
                    else:
                        FormFieldValues.objects.create(
                            form_data=form_data,
                            form=form,
                            field=field,
                            value=input_value,
                            created_by=created_by
                        )

            
        handle_uploaded_files(request, form_name, created_by, form_data, user)        
        # file_name = get_object_or_404(FormFieldValues, form_data_id=form_data, field_id=field).value
                    
        # Run only if type is reference
        if type == 'reference' or reference_type =='1':
            workflow_name = 'CIDCO File Scanning and DMS Flow'
            form_id = form.id

            last_step = workflow_matrix.objects.filter(
                workflow_name=workflow_name,
                form_id=form_id
            ).aggregate(max_step=Max('step_id_flow'))['max_step']

            current_step = int(step_id)

            if last_step and current_step == last_step:
                # Archive existing values
                old_values = FormFieldValues.objects.filter(form=form, form_data=form_data)
                for val in old_values:
                    FormFieldValuesHist.objects.create(
                        form=val.form,
                        form_data=val.form_data,
                        field=val.field,
                        value=val.value,
                        created_by=val.created_by,
                        updated_by=created_by,
                    )
                old_values.delete()

                # Move temp to main table
                temp_values = FormFieldValuesTemp.objects.filter(form_id=form.id, form_data_id=form_data.id)
                for temp in temp_values:
                    FormFieldValues.objects.create(
                        form_id=temp.form_id,
                        form_data_id=temp.form_data_id,
                        field_id=temp.field_id,
                        value=temp.value,
                        created_by=temp.created_by
                    )
                temp_values.delete()

                old_files = FormFile.objects.filter(form=form, form_data=form_data)
                for file in old_files:
                    FormFileHist.objects.create(
                        form=file.form,
                        file_name= file.file_name,
                        form_data=file.form_data,
                        file_size = file.file_size,
                        num_pages = file.num_pages,
                        file = file.file,
                        field=file.field,
                        file_path=file.file_path,
                        uploaded_name=file.uploaded_name,
                        created_by=file.created_by,
                        updated_by=created_by,
                    )
                old_files.delete()

                # --- Move Temp FormFile to Main FormFile ---
                temp_files = FormFileTemp.objects.filter(form_id=form.id, form_data_id=form_data.id)
                for temp_file in temp_files:
                    FormFile.objects.create(
                        file_name = temp_file.file_name,
                        form=get_object_or_404(Form, id =temp_file.form_id),
                        form_data=get_object_or_404(FormData, id = temp_file.form_data_id),
                        field=get_object_or_404(FormField, id = temp_file.field_id),
                        file_path=temp_file.file_path,
                        uploaded_name=temp_file.uploaded_name,
                        created_by=temp_file.created_by,
                    )
                callproc("stp_delete_temp_file",[form.id,form_data.id])

                file_objs = VersionControlFileMap.objects.filter(form_data=form_data_id)

                # If you want to update all matching rows:
                for obj in file_objs:
                    file_name = obj.file_name
                    VersionControlFileMap.objects.filter(file_name=file_name).update(status=1)
                
        # callproc('create_dynamic_form_views')
        messages.success(request, "Form data updated successfully!")
        if workflow_YN == '1E':
        
            wfdetailsid = request.POST.get('wfdetailsid', '')
            step_id = request.POST.get('step_id', '')
            role_idC = request.POST.get('role_id', '')
            if wfdetailsid and wfdetailsid != 'undefined':
                wfdetailsid=dec(wfdetailsid)
            else:
                wfdetailsid = None  
            
            if step_id:
                matrix_entry = workflow_matrix.objects.filter(id=step_id).first()
                if matrix_entry:
                    status_from_matrix = matrix_entry.status  # adjust field name if needed
                    
            if wfdetailsid and workflow_details.objects.filter(id=wfdetailsid).exists():
                # Update existing record
                workflow_detail = workflow_details.objects.get(id=wfdetailsid)
                workflow_detail.form_data_id = form_data_id
                workflow_detail.role_id = request.POST.get('role_id', '')
                workflow_detail.action_details_id = request.POST.get('action_detail_id', '')
                workflow_detail.increment_id += 1
                workflow_detail.step_id = request.POST.get('step_id', '')
                workflow_detail.status = status_from_matrix or ''
                workflow_detail.user_id = user
                workflow_detail.updated_by = user  # Or use `modified_by` if applicable
                workflow_detail.updated_at = now()
                workflow_detail.save()    
            else:    
                workflow_detail = workflow_details.objects.create(
                form_data_id=form_data_id,
                role_id=request.POST.get('role_id', ''),
                action_details_id=request.POST.get('action_detail_id', ''),
                increment_id=1,
                # form_id=request.POST.get('form_id', ''),
                # action_id=request.POST.get('action_id', ''),
                status = status_from_matrix or '',
                step_id=request.POST.get('step_id', ''),
                operator=request.POST.get('custom_dropdownOpr', ''),
                user_id=user,
                created_by=user,
                created_at=now()
                
                )

            # Now set and save req_id using the generated ID
            workflow_detail.req_id = f"REQNO-00{workflow_detail.id}"
            workflow_detail.save()
            if wfdetailsid and workflow_details.objects.filter(id=wfdetailsid).exists():
                history_workflow_details.objects.create(
                    form_data_id=workflow_detail.form_data_id,
                    role_id=workflow_detail.role_id,
                    action_details_id=workflow_detail.action_details_id,
                    increment_id=workflow_detail.increment_id,
                    step_id=workflow_detail.step_id,
                    status=workflow_detail.status,
                    user_id=workflow_detail.user_id,
                    req_id=workflow_detail.req_id,
                    form_id=request.POST.get('form_id', ''),
                    created_by=user,
                    sent_back='0',
                    # created_by=workflow_detail.updated_by,
                    created_at=workflow_detail.updated_at
                )
            else:
                history_workflow_details.objects.create(
                    form_data_id=workflow_detail.form_data_id,
                    role_id=workflow_detail.role_id,
                    action_details_id=workflow_detail.action_details_id,
                    increment_id=workflow_detail.increment_id,
                    step_id=workflow_detail.step_id,
                    status=workflow_detail.status,
                    user_id=workflow_detail.user_id,
                    req_id=workflow_detail.req_id,
                    operator=request.POST.get('custom_dropdownOpr', ''),
                    form_id=request.POST.get('form_id', ''),
                    created_by=user,
                    sent_back='0',
                    # created_by=workflow_detail.updated_by,
                    created_at=workflow_detail.updated_at
                )
            if role_idC == '1':
                reject_case = WorkflowVersionControl.objects.filter(
                    file_name=file_name,
                    version_no=0
                ).exists()

                if not reject_case:
                    latest_record = WorkflowVersionControl.objects.filter(
                        file_name=file_name
                    ).order_by('-id').first()

                    # Determine the file_category and latest temp_version
                    latest_file_category = latest_record.file_category if latest_record else None
                    latest_temp_version = latest_record.temp_version if latest_record else None

                    # Determine new temp_version
                    if latest_temp_version is None:
                        temp_version = Decimal('1.0')
                    else:
                        temp_version = Decimal(str(latest_temp_version)) + Decimal('0.1')

                    WorkflowVersion.objects.create(req_id = workflow_detail.req_id, version = temp_version)
            if role_idC == '2':
                reject_case = WorkflowVersionControl.objects.filter(
                    file_name=file_name,
                    version_no=0
                ).exists()

                if not reject_case:
                    latest_record = WorkflowVersionControl.objects.filter(
                        file_name=file_name
                    ).order_by('-id').first()

                        # Determine the file_category and latest temp_version
                    latest_file_category = latest_record.file_category if latest_record else None
                    latest_temp_version = latest_record.temp_version if latest_record else None

                        # Determine new temp_version
                    if latest_temp_version is None:
                        temp_version = Decimal('1.0')
                    else:
                        temp_version = Decimal(str(latest_temp_version)) + Decimal('0.1')

                        # Create the new row
                    WorkflowVersionControl.objects.create(
                        file_name=file_name,
                        version_no=0,
                        temp_version=temp_version,
                        modified_by=user_name,
                        modified_at=now(),
                        file_category=latest_file_category,
                        form_data_id=form_data_id
                    )
                

            if role_idC == '5':
                versions = WorkflowVersionControl.objects.filter(file_name=file_name).order_by('-id')
                count = versions.count()  # performs SELECT COUNT(*):contentReference[oaicite:5]{index=5}
                count_row = WorkflowVersionControl.objects.filter(file_name=file_name).count()
                latest_row = WorkflowVersionControl.objects.filter(
                        file_name=file_name
                        ).order_by('-id').first()
                if latest_row and count_row == 1:
                    latest_row.version_no = 1
                    latest_row.baseline_date = now()
                    latest_row.approved_by = user_name
                    latest_row.approved_at = now()
                    latest_row.save()
                elif latest_row and count_row > 1:
                        # latest_row.version_no = +0.1
                        second_latest = versions[1]   
                        latest_row.version_no = round(second_latest.version_no + 0.1, 1)
                        # latest_row.version_no = round(latest_row.version_no + 0.1, 1)
                        latest_row.baseline_date = now()
                        latest_row.approved_by = user_name
                        latest_row.approved_at = now()
                        latest_row.save()
            for key, value in request.POST.items():
                if key.startswith("action_field_") and not key.startswith("action_field_id_"):
                    match = re.match(r'action_field_(\d+)', key)
                    latest_row = WorkflowVersionControl.objects.filter(file_name=file_name).order_by('-id').first()

                    # Set temp_vers based on whether a row was found
                    if latest_row and latest_row.temp_version is not None:
                        temp_vers = Decimal(str(latest_row.temp_version))
                    else:
                        temp_vers = Decimal('1.0')

                    if match:
                        field_id = int(match.group(1))
                        action_field = get_object_or_404(FormActionField, pk=field_id)
                        if action_field.type in ['text', 'textarea', 'select']:
                            ActionData.objects.create(
                                value=value,
                                form_data=form_data,
                                field=action_field,
                                step_id=step_id,
                                version=temp_vers,
                                created_by=user,
                                updated_by=user,
                            )
            
            messages.success(request, "Workflow data saved successfully!")

    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    finally:
        #return redirect("/masters?entity=form_master&type=i")
        if workflow_YN == '1E':
            return redirect('workflow_starts')
        else:
            return redirect("/masters?entity=form_master&type=i")



def handle_generative_fields(form, form_data, created_by):
    generative_fields = FormField.objects.filter(form=form, field_type="generative")

    for field in generative_fields:
        try:
            gen_settings = FormGenerativeField.objects.get(field=field, form=form)

            prefix = gen_settings.prefix or ''
            selected_ids = (gen_settings.selected_field_id or '').split(',')
            no_of_zero = int(gen_settings.no_of_zero or '0')
            initial_increment = int(gen_settings.increment or '1')

            increment_row, created = FormIncrementNo.objects.get_or_create(
                form=form,
                defaults={'increment': initial_increment}
            )

            if not created:
                increment_row.increment += 1
                increment_row.save()

            current_increment = increment_row.increment

            # Step 2: Gather selected field values
            selected_values = []
            for sel_id in selected_ids:
                selected_field = FormField.objects.filter(id=sel_id).first()
                if not selected_field:
                    continue

                value_obj = FormFieldValues.objects.filter(
                    form_data=form_data,
                    form=form,
                    field=selected_field
                ).first()

                if value_obj:
                    selected_values.append(value_obj.value)

            base_part = '-'.join(selected_values)
            padded_number = str(0).zfill(no_of_zero)
            final_value = f"{prefix}-{base_part}-{padded_number}{current_increment}"

            # Step 3: Save the generated value
            FormFieldValues.objects.create(
                form_data=form_data,
                form=form,
                field=field,
                value=final_value,
                created_by=created_by
            )

        except Exception as e:
            traceback.print_exc()
    return final_value


# def handle_uploaded_files(request, form_name, created_by, form_data, user):
#     try:
#         user = request.session.get('user_id', '')
#         for field_key, uploaded_files in request.FILES.lists():
#             if not field_key.startswith("field_"):
#                 continue

#             field_id = field_key.split("_")[-1].strip()
#             field = get_object_or_404(FormField, id=field_id)

#             file_dir = os.path.join(settings.MEDIA_ROOT, form_name, created_by, form_data.req_no)
#             os.makedirs(file_dir, exist_ok=True)
#             is_multiple = field.field_type == "file multiple"

#             for uploaded_file in uploaded_files:
#                 uploaded_file_name = uploaded_file.name.strip()
#                 original_file_name, file_extension = os.path.splitext(uploaded_file_name)
#                 timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
#                 saved_file_name = f"{original_file_name}_{timestamp}{file_extension}"
#                 save_path = os.path.join(file_dir, saved_file_name)
#                 relative_file_path = os.path.join(form_name, created_by, form_data.req_no, saved_file_name)
                

#                 if is_multiple:
#                     # Check if this file name already exists
#                     existing_file = FormFile.objects.filter(
#                         form_data=form_data,
#                         field=field,
#                         uploaded_name=uploaded_file_name
#                     ).first()

#                     if existing_file:
#                         old_file_path = os.path.join(settings.MEDIA_ROOT, existing_file.file_path)
#                         if os.path.exists(old_file_path):
#                             os.remove(old_file_path)

#                         with open(save_path, 'wb+') as destination:
#                             for chunk in uploaded_file.chunks():
#                                 destination.write(chunk)

#                         existing_file.file_name = saved_file_name
#                         existing_file.file_path = relative_file_path
#                         existing_file.updated_by = user
#                         existing_file.num_pages = num_pages
#                         existing_file.file_size = file_size
#                         existing_file.save()
#                         continue

#                 else:
#                     # 🔥 Single file logic: Delete old one (if any) for this field + form_data
#                     existing_files = FormFile.objects.filter(form_data=form_data, field=field)
#                     for old_file in existing_files:
#                         old_file_path = os.path.join(settings.MEDIA_ROOT, old_file.file_path)
#                         if os.path.exists(old_file_path):
#                             os.remove(old_file_path)
#                         old_file.delete()

#                 # Save new file
#                 with open(save_path, 'wb+') as destination:
#                     for chunk in uploaded_file.chunks():
#                         destination.write(chunk)

#                 form_file = FormFile.objects.create(
#                     file_name=saved_file_name,
#                     uploaded_name=uploaded_file_name,
#                     file_path=relative_file_path,
#                     form_data=form_data,
#                     form=form_data.form,
#                     file_size=file_size,
#                     num_pages= num_pages,
#                     created_by=user,
#                     updated_by=user,
#                     field=field
#                 )

#                 form_field_value = FormFieldValues.objects.filter(
#                     form_id=form_data.form.id,
#                     field_id=field.id,
#                     form_data = form_data
#                 ).first()

#                 if form_field_value:
#                     if form_field_value.value:
#                         existing_ids = [x.strip() for x in form_field_value.value.split(',') if x.strip()]
#                         new_id_str = str(form_file.id)
#                         if new_id_str not in existing_ids:
#                             existing_ids.append(new_id_str)
#                         form_field_value.value = ','.join(existing_ids)
#                     else:
#                         form_field_value.value = str(form_file.id)
#                     form_field_value.save()

#                     form_file.file_id = form_field_value.id
#                     form_file.save()


#                 # OCR + Keyword extraction
#                 # text = extract_text_from_pdf(os.path.join(MEDIA_ROOT,relative_file_path))
#                 # keywords = extract_keywords(text)
#                 # ocr_doc = Document.objects.create(
#                 #     title=saved_file_name,
#                 #     pdf_file=relative_file_path,
#                 #     extracted_text=text,
#                 #     keywords=', '.join(keywords)
#                 # ) 



#     except Exception as e:
#         traceback.print_exc()
#         messages.error(request, "Oops...! Something went wrong!")

def handle_uploaded_files(request, form_name, created_by, form_data, user):
    try:
        user = request.session.get('user_id', '')
        
        for field_key, uploaded_files in request.FILES.lists():
            if not field_key.startswith("field_"):
                continue

            field_id = field_key.split("_")[-1].strip()
            field = get_object_or_404(FormField, id=field_id)

            file_dir = os.path.join(settings.MEDIA_ROOT, form_name, created_by, form_data.req_no)
            os.makedirs(file_dir, exist_ok=True)
            is_multiple = field.field_type == "file multiple"

            for uploaded_file in uploaded_files:
                uploaded_file_name = uploaded_file.name.strip()
                original_file_name, file_extension = os.path.splitext(uploaded_file_name)
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
                saved_file_name = f"{original_file_name}_{timestamp}{file_extension}"
                save_path = os.path.join(file_dir, saved_file_name)
                relative_file_path = os.path.join(form_name, created_by, form_data.req_no, saved_file_name)

                # First save the file to disk
                with open(save_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Initialize metadata
                file_size = None
                num_pages = None
                file_size = os.path.getsize(save_path)

                if file_extension.lower() == '.pdf':
                    try:
                        # file_size = os.path.getsize(save_path)
                        with open(save_path, 'rb') as f:
                            reader = PdfReader(f)
                            num_pages = len(reader.pages)
                    except Exception as pdf_err:
                        print("Error reading PDF:", pdf_err)
                else:
                    num_pages = '1'

                if is_multiple:
                    # Check if this file name already exists
                    existing_file = FormFile.objects.filter(
                        form_data=form_data,
                        field=field,
                        uploaded_name=uploaded_file_name
                    ).first()

                    if existing_file:
                        old_file_path = os.path.join(settings.MEDIA_ROOT, existing_file.file_path)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)

                        existing_file.file_name = saved_file_name
                        existing_file.file_path = relative_file_path
                        existing_file.updated_by = user
                        existing_file.num_pages = num_pages
                        existing_file.file_size = file_size
                        existing_file.save()
                        continue

                else:
                    # Single file logic: Delete old one (if any) for this field + form_data
                    existing_files = FormFile.objects.filter(form_data=form_data, field=field)
                    for old_file in existing_files:
                        old_file_path = os.path.join(settings.MEDIA_ROOT, old_file.file_path)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                        old_file.delete()

                # Save new FormFile object
                form_file = FormFile.objects.create(
                    file_name=saved_file_name,
                    uploaded_name=uploaded_file_name,
                    file_path=relative_file_path,
                    form_data=form_data,
                    form=form_data.form,
                    file_size=file_size,
                    num_pages=num_pages,
                    created_by=user,
                    updated_by=user,
                    field=field
                )

                form_field_value = FormFieldValues.objects.filter(
                    form_id=form_data.form.id,
                    field_id=field.id,
                    form_data=form_data
                ).first()

                if form_field_value:
                    if form_field_value.value:
                        existing_ids = [x.strip() for x in form_field_value.value.split(',') if x.strip()]
                        new_id_str = str(form_file.id)
                        if new_id_str not in existing_ids:
                            existing_ids.append(new_id_str)
                        form_field_value.value = ','.join(existing_ids)
                    else:
                        form_field_value.value = str(form_file.id)
                    form_field_value.save()

                    form_file.file_id = form_field_value.id
                    form_file.save()

    except Exception as e:
        traceback.print_exc()
        messages.error(request, "Oops...! Something went wrong!")

    
@login_required
def form_preview(request):
    user  = request.session.get('user_id', '')
    id = request.GET.get("id")
    id = dec(id)  

    if not id:
        return render(request, "Form/_formfields.html", {"fields": []})  

    try:
        workflow = get_object_or_404(workflow_matrix, id=id)
        form_id = workflow.form_id
        action_id = workflow.button_type_id

        form = get_object_or_404(Form, id=form_id)

        # Fetch form fields with 'section'
        fields = list(FormField.objects.filter(form_id=form_id).values(
            "id", "label", "field_type", "values", "attributes", "form_id", "form_id__name", "order", "section"
        ).order_by("order"))

        # Initialize sectioned fields
        sectioned_fields = {}

        # Fetch action fields
        action_fields = list(FormActionField.objects.filter(action_id=action_id).values(
            "id", "type", "label_name", "button_name", "bg_color", "text_color", 
            "button_type", "dropdown_values", "status", "action_id"
        ))

        # Process action fields
        for action in action_fields:
            action["dropdown_values"] = action["dropdown_values"].split(",") if action["dropdown_values"] else []

        # Process form fields
        for field in fields:
            field["values"] = field["values"].split(",") if field.get("values") else []
            field["attributes"] = field["attributes"].split(",") if field.get("attributes") else []



            # Section name logic
            section_id = field.get("section")
            if section_id:
                try:
                    section = SectionMaster.objects.get(id=section_id)
                    section_name = section.name
                except SectionMaster.DoesNotExist:
                    section_name = ""
            else:
                section_name = ""

            if field["field_type"] == "field_dropdown":
                    split_values = field["values"]
                    if len(split_values) == 2:
                        dropdown_form_id, dropdown_field_id = split_values
                        field_values = FormFieldValues.objects.filter(field_id=dropdown_field_id).values("value").distinct()
                        field["dropdown_data"] = list(field_values)

            # Fetch validations
            validations = FieldValidation.objects.filter(
                field_id=field["id"], form_id=form_id
            ).values("value")
            field["validations"] = list(validations)

            # Handle file accept
            if field["field_type"] in ["file", "text", "file multiple"]:
                file_validation = next((v for v in field["validations"]), None)
                field["accept"] = file_validation["value"] if file_validation else ""

            # Group by section
            sectioned_fields.setdefault(section_name, []).append(field)

        return render(request, "Form/_formfieldedit.html", {
            "matrix_id": id,
            "sectioned_fields": sectioned_fields,
            "fields": fields,  # still passed if needed
            "form": form,
            "form_id": form_id,
            "action_id": action_id,
            "action_fields": action_fields,
            "type": "create"
        })

    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)

    

@login_required
def common_form_action(request):
    user = request.session.get('user_id', '')
    workflow_YN = request.POST.get("workflow_YN")
    type = request.POST.get("type")
    reference_type = request.POST.get("reference_type")
    try:
        if request.method == 'POST':
            form_data_id = request.POST.get('form_data_id')
            form_data = get_object_or_404(FormData, pk=form_data_id)
            button_type = request.POST.get('button_type')
            clicked_action_id = request.POST.get('clicked_action_id')
            if workflow_YN == '1E':
                step_id = request.POST.get('step_id', '')

            latest_row = WorkflowVersionControl.objects.filter(form_data=form_data).order_by('-id').first()

                    # Set temp_vers based on whether a row was found
            if latest_row and latest_row.temp_version is not None:
                temp_vers = Decimal(str(latest_row.temp_version))
            else:
                temp_vers = Decimal('1.0')
            
            # Process only if it's an Action button
            # if button_type == 'Action':
            clicked_action_id = request.POST.get('clicked_action_id')
            if clicked_action_id:
                try:
                    clicked_action_id = int(clicked_action_id)
                except ValueError:
                    messages.error(request, "Invalid action button identifier.")
                    return redirect('/masters?entity=form_master&type=i')
                
                # Save the clicked action button with its status
                action_field = get_object_or_404(FormActionField, pk=clicked_action_id)
                if action_field.button_type == 'Action':
                    ActionData.objects.create(
                        value=action_field.status,  # saving the status from FormActionField
                        form_data=form_data,
                        field=action_field,
                        step_id=step_id,
                        version = temp_vers,
                        created_by=user,
                        updated_by=user,
                    )
                
            # Now process the non-button fields (text, textarea, dropdown)
            for key, value in request.POST.items():
                if key.startswith("action_field_") and not key.startswith("action_field_id_"):
                    # Extract the numeric ID using a regular expression to avoid non-integer parts
                    match = re.match(r'action_field_(\d+)', key)
                    if match:
                        field_id = int(match.group(1))
                        action_field = get_object_or_404(FormActionField, pk=field_id)
                        if action_field.type in ['text', 'textarea', 'select']:
                            ActionData.objects.create(
                                value=value,
                                form_data=form_data,
                                field=action_field,
                                step_id=step_id,
                                created_by=user,
                                version = temp_vers,
                                updated_by=user,
                            )
            
        
            messages.success(request, "Action data saved successfully!")
            if workflow_YN == '1E':
        
                wfdetailsid = request.POST.get('wfdetailsid', '')
                step_id = request.POST.get('step_id', '')
                role_idC = request.POST.get('role_id', '')
                category_dropdownOpr = request.POST.get('category_dropdownOpr', '')

                if wfdetailsid and wfdetailsid != 'undefined':
                    wfdetailsid=dec(wfdetailsid)
                else:
                    wfdetailsid = None  
                
                if step_id:
                    matrix_entry = workflow_matrix.objects.filter(id=step_id).first()
                    if matrix_entry:
                        status_from_matrix = matrix_entry.status  # adjust field name if needed
                        
                if wfdetailsid and workflow_details.objects.filter(id=wfdetailsid).exists():
                    # Update existing record
                    workflow_detail = workflow_details.objects.get(id=wfdetailsid)
                    workflow_detail.form_data_id = form_data_id
                    workflow_detail.role_id = request.POST.get('role_id', '')
                    workflow_detail.action_details_id = request.POST.get('action_detail_id', '')
                    workflow_detail.increment_id += 1
                    workflow_detail.step_id = request.POST.get('step_id', '')
                    workflow_detail.status = status_from_matrix or ''
                    workflow_detail.user_id = user
                    workflow_detail.updated_by = user  # Or use `modified_by` if applicable
                    workflow_detail.updated_at = now()
                    workflow_detail.save()    
                else:    
                    workflow_detail = workflow_details.objects.create(
                    form_data_id=form_data_id,
                    role_id=request.POST.get('role_id', ''),
                    action_details_id=request.POST.get('action_detail_id', ''),
                    increment_id=1,
                    # form_id=request.POST.get('form_id', ''),
                    # action_id=request.POST.get('action_id', ''),
                    status = status_from_matrix or '',
                    step_id=request.POST.get('step_id', ''),
                    operator=request.POST.get('custom_dropdownOpr', ''),
                    user_id=user,
                    created_by=user,
                    created_at=now()
                    
                    )

                # Now set and save req_id using the generated ID
                workflow_detail.req_id = f"REQNO-00{workflow_detail.id}"
                workflow_detail.save()
                if wfdetailsid and workflow_details.objects.filter(id=wfdetailsid).exists():
                    history_workflow_details.objects.create(
                        form_data_id=workflow_detail.form_data_id,
                        role_id=workflow_detail.role_id,
                        action_details_id=workflow_detail.action_details_id,
                        increment_id=workflow_detail.increment_id,
                        step_id=workflow_detail.step_id,
                        status=workflow_detail.status,
                        user_id=workflow_detail.user_id,
                        req_id=workflow_detail.req_id,
                        form_id=request.POST.get('form_id', ''),
                        created_by=user,
                        # created_by=workflow_detail.updated_by,
                        created_at=workflow_detail.updated_at
                    )
                else:
                    history_workflow_details.objects.create(
                        form_data_id=workflow_detail.form_data_id,
                        role_id=workflow_detail.role_id,
                        action_details_id=workflow_detail.action_details_id,
                        increment_id=workflow_detail.increment_id,
                        step_id=workflow_detail.step_id,
                        status=workflow_detail.status,
                        user_id=workflow_detail.user_id,
                        req_id=workflow_detail.req_id,
                        operator=request.POST.get('custom_dropdownOpr', ''),
                        form_id=request.POST.get('form_id', ''),
                        created_by=user,
                        # created_by=workflow_detail.updated_by,
                        created_at=workflow_detail.updated_at
                    )
                    # field_values = FormFieldValues.objects.filter(form_data_id=form_data_id).values_list
            
                        
                if role_idC == '5':
                    field_ids = FormFieldValues.objects.filter(form_data_id=form_data_id).values_list('field_id', flat=True)
                    for field_id in field_ids:
                        matched_field = FormField.objects.filter(
                                id=field_id,
                                field_type='generative',
                                label='File Name'
                            ).first()
                        if matched_field:
                            value_entry = FormFieldValues.objects.filter(
                                form_data_id=form_data_id,
                                field_id=field_id
                            ).first()
                            if value_entry:
                                file_name = value_entry.value
                        
                    count_row = WorkflowVersionControl.objects.filter(file_name=file_name).count()
                    latest_row = WorkflowVersionControl.objects.filter(
                            file_name=file_name
                            ).order_by('-id').values_list('id', flat=True).first()
                    if latest_row and count_row == 1:
                        latest_row.version_no = 1
                        latest_row.save()
                    elif latest_row and count_row > 1:
                            # latest_row.version_no = +0.1
                            latest_row.version_no = round(latest_row.version_no + 0.1, 1)
                            latest_row.save()    
                
                if role_idC == '4' and category_dropdownOpr:
                    latest_obj = WorkflowVersionControl.objects.filter(form_data_id=form_data_id).order_by('-id').first()

                    if latest_obj:
                        latest_obj.file_category = category_dropdownOpr
                        latest_obj.save()
                    # WorkflowVersionControl.objects.filter(form_data_id=form_data_id).update(file_category=category_dropdownOpr)
    
                
                messages.success(request, "Workflow data saved successfully!")
        
        
        if workflow_YN == '1E':
            return redirect('workflow_starts')
        else:
            return redirect('/masters?entity=form_master&type=i')
    
    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)


@login_required
def download_file(request):
    try:
        encrypted_path = request.GET.get('file')
        if not encrypted_path:
            raise Http404("Missing file parameter")

        # Decrypt to get file_path
        filepath = dec(encrypted_path)  # This should match the `file_path` in the DB
        full_path = os.path.join(settings.MEDIA_ROOT, filepath)

        if not os.path.exists(full_path):
            raise Http404("File does not exist")

        # Lookup uploaded name from DB using file_path
        try:
            file_obj = FormFile.objects.get(file_path=filepath)
            uploaded_name = file_obj.uploaded_name
        except FormFile.DoesNotExist:
            uploaded_name = os.path.basename(filepath)  # fallback

        response = FileResponse(open(full_path, 'rb'), as_attachment=True, filename=uploaded_name)
        return response

    except Exception as e:
        raise Http404("Invalid or corrupted file path")
    
# def delete_file(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             enc_id = data.get("id")
#             enc_path = data.get("path")
#             reference_type = data.get("reference_type")
#             type = data.get("type")

#             file_id = dec(enc_id)
#             file_path = dec(enc_path)

#             # Delete the file record
#             form_file = FormFile.objects.get(id=file_id)
#             full_path = os.path.join(settings.MEDIA_ROOT, file_path)

#             if os.path.exists(full_path):
#                 os.remove(full_path)

#             form_file.delete()

#             return JsonResponse({"success": True})
#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({"success": False, "error": "Could not delete file"}, status=500)
#     return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
@login_required
def delete_file(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            enc_id = data.get("id")
            enc_path = data.get("path")
            reference_type = data.get("reference_type")
            type = data.get("type")

            file_id = dec(enc_id)
            file_path = dec(enc_path)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)

            # Only delete DB entry, not the file from filesystem
            if type == "reference" or reference_type == '1':
                # Delete from FormFileTemp
                FormFileTemp.objects.filter(id=file_id).delete()
            else:
                if os.path.exists(full_path):
                    os.remove(full_path)
                    FormFile.objects.filter(id=file_id).delete()

            return JsonResponse({"success": True})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"success": False, "error": "Could not delete file entry"}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)




@login_required
def get_uploaded_files(request):
    try:
        field_id = request.POST.get("field_id")
        form_data_id = request.POST.get("form_data_id")
        reference_type = request.POST.get("reference_type")
        type = request.POST.get("type")

        if reference_type == '1' or type == 'reference':
            files = FormFileTemp.objects.filter(
                field_id=field_id,
                form_data_id=form_data_id
            )
            if not files:
                files = FormFile.objects.filter(
                field_id=field_id,
                form_data_id=form_data_id
            )

        else:
            files = FormFile.objects.filter(
                field_id=field_id,
                form_data_id=form_data_id
            )
            #D:\Python Projects\Documents\METADATA AND UPLOAD FORM\19\UNIQ-NO-002

        file_list = []
        for f in files:
            # full_path = os.path.join(settings.MEDIA_ROOT, f.file_path)
            cleaned_path = f.file_path.strip()
            full_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, cleaned_path))
            exists = os.path.exists(full_path)

            file_id = str(f.id)

            if exists:
                encrypted_url = f.file_path
                status = 1
            else:
                encrypted_url = ''
                status = 0

            file_list.append({
                'name': f.uploaded_name,
                'status': status,
                'url': encrypted_url,
                'file_id': file_id  
            })

        return JsonResponse({'files': file_list})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': 'Something went wrong while fetching files'}, status=500)
        
def get_query_data(request):
    if request.method == "POST":
        try:
            id = request.POST.get("query")
            # id = dec(id)
            query = get_object_or_404(MasterDropdownData, id= id).query
            data = callproc("stp_get_query_data",[query])
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@login_required 
def check_field_before_delete(request):
    if request.method == "POST":
        field_id = request.POST.get("field_id")

        if  not field_id:
            return JsonResponse({"success": False, "error": "Missing form or field ID."})

        data_exists = FormFieldValues.objects.filter(field_id=field_id).exists()

        if data_exists:
            return JsonResponse({"exists": True})  # Indicates data is present; can't delete
        else:
            return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method."})

def get_field_names(request):
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        fields = FormField.objects.filter(form_id=form_id).values('id', 'label')
        return JsonResponse({'fields': list(fields)})
    
def get_regex_pattern(request):
    if request.method == "POST":
        regex_id = request.POST.get("regex_id")

        try:
            regex = RegexPattern.objects.get(id=regex_id)
            return JsonResponse({
                "regex_id":regex_id,
                "pattern": regex.regex_pattern,
                "description": regex.description
            })
        except RegexPattern.DoesNotExist:
            return JsonResponse({"error": "Pattern not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def create_new_section(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            section = SectionMaster.objects.create(name=name)
            return JsonResponse({"id": section.id, "name": section.name})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def reference_workflow(request):
    user = request.session.get('user_id', '')
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)

        matched_form_data_id = request.POST.get('matched_form_data_id')
        if not matched_form_data_id:
            form_data_id = request.POST.get("new_data_id")
            matched_form_data_id = form_data_id

        form_id = request.POST.get("form_id")
        form_name = request.POST.get("form_name", "").strip()
        created_by = user.strip()
        type = request.POST.get("type")
        reference_type = request.POST.get("reference_type")

        form = get_object_or_404(Form, id=form_id)

        step_id = enc(str(request.POST.get("step_id")))
        wfdetailsid = request.POST.get("wfdetailsid")
        editORcreate = request.POST.get("editORcreate")
        form_data_id = matched_form_data_id

        file_no_field = FormField.objects.filter(form=form, label__iexact='File No').first()
        file_no_field_id = str(file_no_field.id) if file_no_field else None

        # Clear temp values for this form_data_id and form_id
        FormFieldValuesTemp.objects.filter(form_data_id=matched_form_data_id, form_id=form_id).delete()
        FormFileTemp.objects.filter(form_data_id=matched_form_data_id, form_id=form_id).delete()

        form_files = FormFile.objects.filter(form_data_id=matched_form_data_id, form_id=form_id)
        for file_obj in form_files:
            FormFileTemp.objects.create(
                form_data_id=file_obj.form_data.id,
                file_name = file_obj.file_name,
                form_id=file_obj.form.id,
                field_id=file_obj.field.id,
                file_path = file_obj.file_path,
                file_size = file_obj.file_size,
                num_pages = file_obj.num_pages,
                uploaded_name=file_obj.uploaded_name,
                created_by=created_by,
                updated_by=created_by
            )

        for key, value in request.POST.items():
            if key.startswith("field_id_"):
                field_id = value.strip()
                field_type = FormField.objects.filter(id=field_id).values_list('field_type', flat=True).first()

                if field_type == "generative" or field_type in ['file', 'file multiple'] or field_id == file_no_field_id:
                    existing_value_obj = FormFieldValues.objects.filter(
                        form_data_id=matched_form_data_id,
                        form_id=form_id,
                        field_id=field_id
                    ).first()

                    if existing_value_obj and existing_value_obj.value:
                        FormFieldValuesTemp.objects.create(
                            form_data_id=matched_form_data_id,
                            form_id=form_id,
                            field_id=field_id,
                            value=existing_value_obj.value,
                            created_by=created_by,
                            updated_by=created_by
                        )

                    continue


                if field_type == "select multiple":
                    selected_values = request.POST.getlist(f"field_{field_id}")
                    input_value = ','.join([val.strip() for val in selected_values if val.strip()])
                else:
                    input_value = request.POST.get(f"field_{field_id}", "").strip()

                FormFieldValuesTemp.objects.create(
                    form_data_id=matched_form_data_id,
                    form_id=form_id,
                    field_id=field_id,
                    value=input_value,
                    created_by=created_by,
                    updated_by=created_by
                )

        handle_uploaded_files_temp(request,form_name,created_by, matched_form_data_id, user)

        reference_type = '1'
        data_save_status = '1'
        messages.success(request, "Workflow Data has been saved successfully!")
        url = reverse('workflow_form_step') + f'?id={step_id}&wfdetailsID={wfdetailsid}&editORcreate={editORcreate}&new_data_id={matched_form_data_id}&reference_type={reference_type}&data_save_status={data_save_status}'
        return redirect(url)

    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)




def handle_uploaded_files_temp(request, form_name, created_by, matched_form_data_id, user):
    try:
        user = request.session.get('user_id', '')
        for field_key, uploaded_files in request.FILES.lists():
            if not field_key.startswith("field_"):
                continue

            field_id = field_key.split("_")[-1].strip()
            field_type = FormField.objects.filter(id=field_id).values_list('field_type', flat=True).first()
            is_multiple = field_type == "file multiple"
            form = get_object_or_404(Form,name = form_name)
            req_no = get_object_or_404(FormData, id = matched_form_data_id).req_no
            form_id = form.id

            file_dir = os.path.join(settings.MEDIA_ROOT, form_name, created_by, req_no)
            os.makedirs(file_dir, exist_ok=True)

            for uploaded_file in uploaded_files:
                uploaded_file_name = uploaded_file.name.strip()
                original_file_name, file_extension = os.path.splitext(uploaded_file_name)
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
                saved_file_name = f"{original_file_name}_{timestamp}{file_extension}"
                save_path = os.path.join(file_dir, saved_file_name)
                relative_file_path = os.path.join(form_name,created_by,req_no, saved_file_name)

                with open(save_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Initialize metadata
                file_size = None
                num_pages = None
                file_size = os.path.getsize(save_path)

                if file_extension.lower() == '.pdf':
                    try:
                        # file_size = os.path.getsize(save_path)
                        with open(save_path, 'rb') as f:
                            reader = PdfReader(f)
                            num_pages = len(reader.pages)
                    except Exception as pdf_err:
                        print("Error reading PDF:", pdf_err)
                else:
                    num_pages = '1'

                form_file_temp = FormFileTemp.objects.create(
                    file_name=saved_file_name,
                    uploaded_name=uploaded_file_name,
                    file_path=relative_file_path,
                    form_data_id=matched_form_data_id,
                    form_id=form_id,  
                    file_size=file_size,
                    num_pages=num_pages,
                    created_by=user,
                    updated_by=user,
                    field_id=field_id
                )
                
                temp_field_value = FormFieldValuesTemp.objects.filter(
                    form_id=form_id,
                    field_id=field_id,
                    form_data_id=matched_form_data_id
                ).first()

                if temp_field_value:
                    if temp_field_value.value:
                        file_ids = temp_field_value.value.split(',')
                        file_ids.append(str(form_file_temp.id))
                        temp_field_value.value = ','.join(file_ids)
                    else:
                        temp_field_value.value = str(form_file_temp.id)
                    temp_field_value.save()

                    form_file_temp.file_id = temp_field_value.id
                    form_file_temp.save()
                
            

    except Exception:
        traceback.print_exc()
        messages.error(request, "Oops...! Something went wrong!")

@login_required
def get_compare_data(request, final_id):
    user  = request.session.get('user_id', '')
    try:
        form_data_id = final_id

        old_values = FormFieldValues.objects.filter(form_data_id=form_data_id).select_related('field')
        new_values = FormFieldValuesTemp.objects.filter(form_data_id=form_data_id)

        old_files = FormFile.objects.filter(form_data_id=form_data_id)
        new_files = FormFileTemp.objects.filter(form_data_id=form_data_id)

        temp_versions = WorkflowVersionControl.objects.filter(form_data_id=form_data_id).order_by('-modified_at')[:2]
        latest_version = None
        previous_version = None

        if temp_versions:
            if len(temp_versions) == 1:
                previous_version = temp_versions[0]
            else:
                latest_version = temp_versions[0]
                previous_version = temp_versions[1]


        new_data_grouped = get_grouped_comments(latest_version.temp_version, form_data_id) if latest_version else []
        old_data_grouped = get_grouped_comments(previous_version.temp_version, form_data_id) if previous_version else []



        # Build file maps
        old_file_map = {}
        for f in old_files:
            file_info = {'path': enc(str(f.file_path)), 'name': os.path.basename(f.uploaded_name)}
            old_file_map.setdefault(f.field_id, []).append(file_info)

        new_file_map = {}
        for f in new_files:
            file_info = {'path': enc(str(f.file_path)), 'name': os.path.basename(f.uploaded_name)}
            new_file_map.setdefault(f.field_id, []).append(file_info)

        comparison_data = []
        file_comparison_data = []

        for old in old_values:
            field = old.field
            label = field.label if field else "Unknown Field"
            field_type = field.field_type if field else ""

            new_val = new_values.filter(field_id=field.id).first()

            if field_type in ['file', 'file multiple']:
                file_comparison_data.append({
                    'label': label,
                    'old_files': old_file_map.get(field.id, []),
                    'new_files': new_file_map.get(field.id, []),
                })
            else:
                comparison_data.append({
                    'label': label,
                    'old_value': old.value,
                    'new_value': new_val.value if new_val else "",
                    'is_file': False
                })

        context = {
            'comparison_data': comparison_data,
            'file_comparison_data': file_comparison_data,
            'old_data_grouped':old_data_grouped,
            'new_data_grouped':new_data_grouped
        }
        return render(request, 'Form/compare_data.html', context)

    except Exception as e:
        print(f"Error fetching form data: {e}")
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')
        return JsonResponse({"error": "Something went wrong!"}, status=500)
    
def get_versiondata(request):
    newFormDataId = request.GET.get('newFormDataId')
    if newFormDataId == '':
        
        newFormDataId = request.GET.get('newFormDataId_op')
    else:
        newFormDataId = request.GET.get('newFormDataId')
        
    try:
        if newFormDataId != '' and newFormDataId != "None":
            qs = WorkflowVersionControl.objects.filter(form_data_id=newFormDataId).select_related('modified_by', 'approved_by')
            result = []
            # result = qs.values(
            #         'file_name',
            #         'version_no',
            #         'baseline_date',
            #         'modified_at',
            #         'approved_by',
            #         'approved_at',
            #         'modified_by',
            #     )
            result = list(qs.values(
                'file_name',
                'version_no',
                'baseline_date',
                'modified_at',
                'approved_by',
                'approved_at',
                'modified_by',
            ))
            for row in result:
                if row['modified_at']:
                    # row['modified_at'] = row['modified_at'].strftime('%d-%m-%Y, %I:%M %p')
                    row['modified_at'] = row['modified_at'].strftime('%d-%m-%Y')
                if row['approved_at']:
                    # row['approved_at'] = row['approved_at'].strftime('%Y-%m-%d %H:%M:%S')
                    row['approved_at'] = row['approved_at'].strftime('%Y-%m-%d')
                if row['baseline_date']:
                    row['baseline_date'] = row['baseline_date'].strftime('%d-%m-%Y')
            return JsonResponse({'data_versions': result})
        else:
            return JsonResponse({'error': 'Invalid form data ID'}, status=400)
    except Exception as e:
        print(f"Error in get_versiondata: {e}")
        return JsonResponse({'error': 'An unexpected error occurred!'}, status=500)
    # return JsonResponse({'error': 'Version Not Found!'}, status=404)
    
@login_required
def preview_file(request):
    if request.method == 'POST':
        try:
            encrpt_path = request.POST.get("encrypted_path")
            decrypted_path = dec(encrpt_path)  # your custom decrypt function
            full_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, decrypted_path))

            if os.path.exists(full_path):
                # Create a file URL using MEDIA_URL
                file_url = os.path.join(settings.MEDIA_URL, decrypted_path).replace('\\', '/')
                return JsonResponse({'success': True, 'file_url': file_url})
            else:
                return JsonResponse({'success': False, 'error': 'File does not exist'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})



def check_fileNameExistsInVersion(request): 
    
    if request.method == 'POST':
        
        file_name = request.POST.get("id")  # Make sure this matches your AJAX
        exists = WorkflowVersionControl.objects.filter(
            file_name=file_name,
            baseline_date__isnull=False
        ).order_by('-id').exists()
        
        return JsonResponse({'status': 1 if exists else 0})        

def get_grouped_comments(version_no, form_data_id):
    try:
        step_name_subquery = Subquery(workflow_matrix.objects.filter(id=OuterRef('step_id')).values('step_name')[:1])
        custom_user_role_id_subquery = Subquery(CustomUser.objects.filter(id=OuterRef('created_by')).values('role_id')[:1])
        custom_email_subquery = Subquery(CustomUser.objects.filter(id=OuterRef('created_by')).values('email')[:1])

        comments_base = ActionData.objects.filter(
            form_data_id=form_data_id,
            version=version_no,
        ).annotate(
            step_name=step_name_subquery,
            role_id=custom_user_role_id_subquery,
            email=custom_email_subquery
        )

        comments = comments_base.annotate(
            role_name=Subquery(roles.objects.filter(id=OuterRef('role_id')).values('role_name')[:1])
        ).values(
            'field_id', 'value', 'step_id', 'created_at', 'created_by', 'step_name', 'role_name', 'email'
        )

        grouped_comments = defaultdict(list)
        for comment in comments:
            key = (comment['step_name'], comment['role_name'], comment['email'])
            grouped_comments[key].append({'value': comment['value'], 'created_at': comment['created_at']})

        grouped_data = []
        sr_no_counter = 1
        for (step_name, role_name, email), comment_list in grouped_comments.items():
            grouped_data.append({
                'sr_no': sr_no_counter,
                'step_name': step_name,
                'role_name': role_name,
                'email': email,
                'comments': comment_list,
                'rowspan': len(comment_list),
                'form_data_id': form_data_id,  # Include here
            })
            sr_no_counter += 1
    except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return grouped_data
@login_required
def check_file_status(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        try:
            # Get the latest entry for the given file
            latest_entry = WorkflowVersionControl.objects.filter(file_name=file_name).order_by('-id').first()
            
            if latest_entry and latest_entry.baseline_date:
                return JsonResponse({"status": 1})  # Valid file with baseline data
            else:
                return JsonResponse({"status": 0, "message": "This file version is ongoing (no baseline data)."})
        
        except Exception as e:
            return JsonResponse({"status": -1, "error": str(e)})

    return JsonResponse({"status": -1, "error": "Invalid request method"})



