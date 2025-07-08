from django.conf import settings
from Account.models import roles
from WorkDocX.encryption import dec
import Db
from .db_utils import callproc
from django.utils import timezone
def logged_in_user(request):
    user =''
    session_cookie_age_seconds = settings.AUTO_LOGOUT['IDLE_TIME']
    session_timeout_minutes = session_cookie_age_seconds 
    username = request.session.get('username', '')
    full_name = request.session.get('full_name', '')
    user_id = request.session.get('user_id', '')
    role_id = request.session.get('role_id', '')
    role_name = ''
    if request.user.is_authenticated ==True:
        user = str(request.user.id or '')
    reports = ''    
    menu_items = []
    
    if user_id!='' and role_id!='':
        # menu_data = callproc("stp_get_side_navbar_details", [user_id, role_id])
        # items = []
        # for row in menu_data:
        #     item = { 'id': row[1], 'name': row[2], 'action': row[3],  'is_parent': row[4],'parent_id': row[5],
        #             'is_sub_menu': row[6], 'sub_menu': row[7],'is_sub_menu2': row[8],'sub_menu2': row[9],'menu_icon': row[10]
        #     }
        #     items.append(item)
        # menu_dict = {}
        # for item in items:
        #     item['children'] = [i for i in items if i['parent_id'] == item['id']]
        #     if item['parent_id'] not in menu_dict:
        #         menu_dict[item['parent_id']] = []
        #     menu_dict[item['parent_id']].append(item)

        # menu_items = menu_dict.get(-1, []) 
        role_obj = roles.objects.get(id=role_id)
        role_name = role_obj.role_name
        menu_items = []
        menu_data = callproc("stp_get_side_navbar_details", [user_id, role_id])
        items = []
        for row in menu_data:
            item = {
                'id': row[1],
                'name': row[2],
                'action': row[3],
                'is_parent': row[4],
                'parent_id': row[5],
                'is_sub_menu': row[6],
                'sub_menu': row[7],
                'is_sub_menu2': row[8],
                'sub_menu2': row[9],
                'menu_icon': row[10],
                'badge': row[11] if len(row) > 11 else None  # Optional badge/count
            }
            items.append(item)

        # Build hierarchy
        for item in items:
            item['children'] = [i for i in items if i['parent_id'] == item['id']]
    
        # Get top level items (parent_id = -1 or your specific root indicator)
        menu_items = [item for item in items if item['parent_id'] == -1]

    return {'username':username,'full_name':full_name,'role_name':role_name,'session_timeout_minutes':session_timeout_minutes,'reports':reports, 'menu_items': menu_items}