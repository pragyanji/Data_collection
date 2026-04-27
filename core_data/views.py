import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import User_Details, Response_table, New_User

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def save_all_data(request):
    try:
        data = json.loads(request.body)
        Response_table.objects.create(metadata=data)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({
        'status': 'success',
    }, status=201)

@csrf_exempt
@require_POST
def kobo_webhook(request):
    """
    Webhook endpoint that receives form submissions from KoboToolbox.

    KoboToolbox sends a JSON payload via POST whenever a form is submitted.
    This view parses the payload and creates User_Details records.

    Expected JSON structure from KoboToolbox:
    {
        "_id": 12345,
        "How_many_members_are_there_in_your_family": "3",
        "Group": [
            {
                "Group/What_is_your_name": "Ram",
                "Group/Your_contact_number": "9800000000",
                "Group/What_is_your_Gender": "Male",
                "Group/Enter_your_age": "25"
            },
            ...
        ]
    }
    """
    try:
        data = json.loads(request.body)
        print(data)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    logger.info(f"Received KoboToolbox webhook: {json.dumps(data, indent=2)}")

    # --- Extract family number ---
    family_no = data.get('How_many_members_are_there_in_your_family')
    if family_no is None:
        return JsonResponse({'error': 'Missing family member count field'}, status=400)

    try:
        family_no = int(family_no)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid family member count'}, status=400)

    # --- Parse and create User_Details for each family member in the Group ---
    group_data = data.get('Group', [])
    members_created = 0

    for member_data in group_data:
        name = member_data.get('Group/What_is_your_name', '')
        contact_number = member_data.get('Group/Your_contact_number', '')
        gender = member_data.get('Group/What_is_your_Gender', '')
        age = member_data.get('Group/Enter_your_age')

        try:
            age = int(age) if age else 0
        except (ValueError, TypeError):
            age = 0

        User_Details.objects.create(
            family_no=family_no,
            name=name,
            contact_number=contact_number,
            gender=gender,
            age=age,
        )
        members_created += 1

    logger.info(f"Created {members_created} User_Details records (family_no={family_no})")

    return JsonResponse({
        'status': 'success',
        'family_no': family_no,
        'members_created': members_created,
    }, status=201)


def show_details(request):
    responses = Response_table.objects.all()
    key = ['name', 'contact', 'gender', 'age','_submitted_by','family_no']
    print(responses)
    return render(request, 'show_details.html', {'responses': responses, 'keys': key})


# api to create the user details in the database from the react js frontend
@csrf_exempt
def create_user(request):
    data = json.loads(request.body)
    user = New_User.objects.create(name=data['name'], age=data['age'])
    return JsonResponse({'status': 'success', 'id': user.id}, status=201)

@csrf_exempt
def update_user(request, user_id):
    if request.method != 'PUT':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    try:
        user = New_User.objects.get(id=user_id)
    except New_User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'User with id {user_id} does not exist.'}, status=404)

    data = json.loads(request.body)
    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.save()
    return JsonResponse({'status': 'success', 'message': f'User with id {user_id} updated.'}, status=200)

# api to get the user details from the database and send it to the react js frontend
def user_details(request):
    users = New_User.objects.all().values('id', 'name', 'age')
    # print(list(users))
    return JsonResponse(list(users), safe=False, status=200)

# api to delete the user details from the database and send it to the react js frontend
@csrf_exempt
def delete_user(request, user_id):
    if request.method != 'DELETE':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    try:
        user = New_User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': f'User with id {user_id} deleted.'}, status=200)
    except New_User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'User with id {user_id} does not exist.'}, status=404)