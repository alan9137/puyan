import datetime
import json
import random
import string
import urllib.parse

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.core.mail import send_mail
from django.db.models import Q

from potrip.settings import DEFAULT_FROM_EMAIL
from .models import *


# Create your views here.


@csrf_exempt
def register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user = UserProfile.objects.get(username=data["account"])
            user.account = data['account']
            user.is_active = False
            user.set_password(data["password"])
            check_code = True
            while check_code:
                code = ''.join(random.choices(string.digits, k=6))
                check_code = UserProfile.objects.filter(code=code).exists()
                if not check_code:
                    user.code = code
            user.save()
            UserSet.objects.create(user=user)
            Default.objects.create(user=user)
            UserSetting.objects.create(user=user)
            Medical.objects.create(user=user)
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_login(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            authorize = auth.authenticate(
                username=data["account"], password=data["password"])
            user = UserProfile.objects.get(account=data["account"])
            if not user.is_active:
                return JsonResponse({"status": "2"})
            auth.login(request, authorize)
            request.session.flush()
            request.session['id'] = user.id
            request.session.save()
            return JsonResponse({
                "status": "0",
                "token": request.session.session_key
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def send(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data['email']
            confirm_string = ''.join(random.choices(
                string.ascii_letters + string.digits, k=6))
            UserProfile.objects.create_user(
                username=email,
                email=email,
                confirm_string=confirm_string
            )
            send_mail(
                "帳號驗證",
                f"驗證碼:{confirm_string}",
                recipient_list=[email],
                from_email=DEFAULT_FROM_EMAIL
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def check(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = UserProfile.objects.filter(email=data['email'], confirm_string=data['confirm_string'])
            if not account.exists():
                raise
            account.update(is_active=True, confirm_string='-1')
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def register_check(request):
    try:
        if request.method == 'GET':
            if UserProfile.objects.filter(email=request.GET.get('account')).exists():
                raise
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def forgot(request):  # //
    try:
        if request.method == 'POST':
            email = urllib.parse.unquote(request.body.decode('utf-8').split('=')[1].split('&')[0])
            account = UserProfile.objects.get(email=email)
            password = (''.join(random.choices(string.ascii_letters + string.digits, k=10)))
            account.set_password(password)
            account.must_change_password = True
            account.save()
            send_mail(
                '新密碼',
                f'密碼:{password}',
                recipient_list=[email],
                from_email=DEFAULT_FROM_EMAIL
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def reset(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            user = UserProfile.objects.get(id=account.get_decoded().get('id'))
            user.set_password(data["password"])
            user.must_change_password = False
            user.save()
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_set(request):
    try:
        if request.method == 'PATCH':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            UserSet.objects.filter(
                user=account.get_decoded().get('id')
            ).update(
                name=data['name'],
                birthday=data['birthday'],
                height=data['height'],
                gender=data['gender'],
                address=data['address'],
                weight=data['weight']
            )
            UserProfile.objects.filter(
                account=account.get_decoded().get('id')
            ).update(
                phone=data["phone"], email=data["email"]
            )
            return JsonResponse({"status": "0"})
        elif request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            user = UserSet.objects.get(user=account.get_decoded().get('id'))
            default = Default.objects.get(user=account.get_decoded().get('id'))
            setting = UserSetting.objects.get(user=account.get_decoded().get('id'))
            return JsonResponse({
                'status': '0',
                'user': {
                    'id': user.user.id,
                    'name': user.name,
                    'account': user.user.account,
                    'email:': user.user.email,
                    'phone:': user.user.phone,
                    'fb_id': 1,
                    'status': 'Normal',
                    'group': 'null',
                    'birthday': user.birthday,
                    'height': user.height,
                    'weight': user.weight,
                    'gender': user.gender,
                    'address': user.address,
                    'unread_records': ['0', '0', '0'],
                    'verified': user.user.is_active,
                    'privacy_policy': user.user.privacy_policy,
                    'must_change_password': user.user.must_change_password,
                    'fcm_id': user.fcm_id,
                    'badge': 0,
                    'login_times': 0,
                    'created_at': user.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': user.user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                    'default': {
                        'id': default.id,
                        'user_id': default.user.id,
                        'sugar_delta_max': default.sugar_delta_max,
                        'sugar_delta_min': default.sugar_delta_min,
                        'sugar_morning_max': default.sugar_morning_max,
                        'sugar_morning_min': default.sugar_morning_min,
                        'sugar_evening_max': default.sugar_evening_max,
                        'sugar_evening_min': default.sugar_evening_min,
                        'sugar_before_max': default.sugar_before_max,
                        'sugar_before_min': default.sugar_before_min,
                        'sugar_after_max': default.sugar_after_max,
                        'sugar_after_min': default.sugar_after_min,
                        'systolic_max': default.systolic_max,
                        'systolic_min': default.systolic_min,
                        'diastolic_max': default.diastolic_max,
                        'diastolic_min': default.diastolic_min,
                        'pulse_max': default.pulse_max,
                        'pulse_min': default.pulse_min,
                        'weight_max': default.weight_max,
                        'weight_min': default.weight_min,
                        'bmi_max': default.bmi_max,
                        'bmi_min': default.bmi_min,
                        'body_fat_max': default.body_fat_max,
                        'body_fat_min': default.body_fat_min,
                        'created_at': default.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': default.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    'setting': {
                        'id': setting.id,
                        'user_id': setting.user.id,
                        'after_recording': setting.after_recording,
                        'no_recording_for_a_day': setting.no_recording_for_a_day,
                        'over_max_or_under_min': setting.over_max_or_under_min,
                        'after_meal': setting.after_meal,
                        'unit_of_sugar': setting.unit_of_sugar,
                        'unit_of_weight': setting.unit_of_weight,
                        'unit_of_height': setting.unit_of_height
                    }
                }
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def blood_pressure(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            UserProfile.objects.get(
                id=account.get_decoded().get('id')
            ).pressure.create(
                systolic=data['systolic'],
                diastolic=data['diastolic'],
                pulse=data['pulse'],
                recorded_at=data['recorded_at']
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_weight(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            UserProfile.objects.get(
                id=account.get_decoded().get('id')
            ).weight.create(
                weight=data['weight'],
                body_fat=data['body_fat'],
                bmi=data['bmi'],
                recorded_at=data['recorded_at']
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def blood_sugar(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            print(data)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            UserProfile.objects.get(
                id=account.get_decoded().get('id')
            ).sugar.create(
                sugar=data['sugar'],
                time_period=data['timeperiod'],
                recorded_at=data['recorded_at']
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_a1c(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            UserProfile.objects.get(
                id=account.get_decoded().get('id')
            ).a1c.create(
                a1c=data['a1c'], recorded_at=data['recorded_at'])
            return JsonResponse({"status": "0"})
        elif request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            a1cs = A1c.objects.filter(
                user=account.get_decoded().get('id')).order_by('-recorded_at').values_list()
            a1c_list = list()
            if a1cs.exists():
                for i in list(a1cs):
                    a1c_list.append({
                        'id': i[0],
                        'user_id': i[1],
                        'a1c': str(i[2]),
                        'recorded_at': i[3].strftime('%Y-%m-%d %H:%M:%S'),
                        'created_at': i[4].strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': i[5].strftime('%Y-%m-%d %H:%M:%S')
                    })
            return JsonResponse({
                'status': '0',
                'a1cs': a1c_list
            })
        elif request.method == 'DELETE':
            data = json.loads(request.body)
            ids = data['ids']
            A1c.objects.filter(id__in=ids).delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_default(request):
    try:
        if request.method == 'PATCH':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            user = Default.objects.filter(user=account.get_decoded().get('id'))
            user.update(
                sugar_delta_max=data.get('sugar_delta_max', user.get().sugar_delta_max),
                sugar_delta_min=data.get('sugar_delta_min', user.get().sugar_delta_min),
                sugar_morning_max=data.get('sugar_morning_max', user.get().sugar_morning_max),
                sugar_morning_min=data.get('sugar_morning_min', user.get().sugar_morning_min),
                sugar_evening_max=data.get('sugar_evening_max', user.get().sugar_evening_max),
                sugar_evening_min=data.get('sugar_evening_min', user.get().sugar_evening_min),
                sugar_before_max=data.get('sugar_before_max', user.get().sugar_before_max),
                sugar_before_min=data.get('sugar_before_min', user.get().sugar_before_min),
                sugar_after_max=data.get('sugar_after_max', user.get().sugar_after_max),
                sugar_after_min=data.get('sugar_after_min', user.get().sugar_after_min),
                systolic_max=data.get('systolic_max', user.get().systolic_max),
                systolic_min=data.get('systolic_min', user.get().systolic_min),
                diastolic_max=data.get('diastolic_max', user.get().diastolic_max),
                diastolic_min=data.get('diastolic_min', user.get().diastolic_min),
                pulse_max=data.get('pulse_max', user.get().pulse_max),
                pulse_min=data.get('pulse_min', user.get().pulse_min),
                weight_max=data.get('weight_max', user.get().weight_max),
                weight_min=data.get('weight_min', user.get().weight_min),
                bmi_max=data.get('bmi_max', user.get().bmi_max),
                bmi_min=data.get('bmi_min', user.get().bmi_min),
                body_fat_max=data.get('body_fat_max', user.get().body_fat_max),
                body_fat_min=data.get('body_fat_min', user.get().body_fat_min)
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_setting(request):
    try:
        if request.method == 'PATCH':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            user = UserSetting.objects.filter(
                user=account.get_decoded().get('id'))
            user.update(
                after_recording=data.get('after_recording', user.get().after_recording),
                no_recording_for_a_day=data.get('no_recording_for_a_day', user.get().no_recording_for_a_day),
                over_max_or_under_min=data.get('over_max_or_under_min', user.get().over_max_or_under_min),
                after_meal=data.get('after_meal', user.get().after_meal),
                unit_of_sugar=data.get('unit_of_sugar', user.get().unit_of_sugar),
                unit_of_weight=data.get('unit_of_weight', user.get().unit_of_weight),
                unit_of_height=data.get('unit_of_height', user.get().unit_of_height))
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt  #
def last_upload(request):
    try:
        if request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            weight = Weight.objects.filter(user=account.get_decoded().get('id')).order_by('-recorded_at')
            sugar = Sugar.objects.filter(user=account.get_decoded().get('id')).order_by('-recorded_at')
            pressure = Pressure.objects.filter(user=account.get_decoded().get('id')).order_by('-recorded_at')
            weight_recorded_at = str()
            sugar_recorded_at = str()
            pressure_recorded_at = str()
            if weight.exists():
                weight_recorded_at = weight[0].recorded_at.strftime('%Y-%m-%d %H:%M:%S')
            if sugar.exists():
                sugar_recorded_at = sugar[0].recorded_at.strftime('%Y-%m-%d %H:%M:%S')
            if pressure.exists():
                pressure_recorded_at = pressure[0].recorded_at.strftime('%Y-%m-%d %H:%M:%S')
            return JsonResponse({
                'status': '0',
                'last_upload': {
                    'blood_pressure': pressure_recorded_at,
                    'weight': weight_recorded_at,
                    'blood_sugar:': sugar_recorded_at
                }
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def records(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            weight = Weight.objects.filter(user=account.get_decoded().get('id')).order_by('-recorded_at')
            weights = dict()
            if weight.exists():
                weights = {
                    'weight': weight[0].weight,
                    'body_fat': weight[0].body_fat,
                    'bmi': weight[0].bmi,
                    'recorded_at:': weight[0].recorded_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            sugar = Sugar.objects.filter(
                user=account.get_decoded().get('id'),
                time_period=data['diets']
            ).order_by('-recorded_at')
            blood_sugars = dict()
            if sugar.exists():
                blood_sugars = {
                    'sugar': sugar[0].sugar,
                    'timeperiod': sugar[0].time_period,
                    'recorded_at:': sugar[0].recorded_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            pressure = Pressure.objects.filter(user=account.get_decoded().get('id')).order_by('-recorded_at')
            blood_pressures = dict()
            if pressure.exists():
                blood_pressures = {
                    'systolic': pressure[0].systolic,
                    'diastolic': pressure[0].diastolic,
                    'pulse': pressure[0].pulse,
                    'recorded_at:': pressure[0].recorded_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            return JsonResponse({
                'status': '0',
                'blood_sugars': blood_sugars,
                'blood_pressures': blood_pressures,
                'weights': weights
            })
        elif request.method == 'DELETE':
            data = json.loads(request.body)
            if 'blood_sugars' in data:
                Sugar.objects.filter(id__in=data['blood_sugars']).delete()
            if 'blood_pressures' in data:
                Pressure.objects.filter(id__in=data['blood_pressures']).delete()
            if 'weights' in data:
                Weight.objects.filter(id__in=data['weights']).delete()
            if 'diets' in data:
                Diet.objects.filter(id__in=data['diets']).delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_diary(request):
    try:
        if request.method == 'GET':
            date = datetime.date.today()
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            diary = list()
            pressures = Pressure.objects.filter(
                user=account.get_decoded().get('id'),
                recorded_at__contains=date
            ).order_by('-recorded_at').values_list()
            if pressures.exists():
                for i in list(pressures):
                    diary.append(
                        {
                            "id": i[0],
                            "user_id": i[1],
                            "systolic": i[2],
                            "diastolic": i[3],
                            "pulse": i[4],
                            "recorded_at": i[5].strftime('%Y-%m-%d %H:%M:%S'),
                            "type": "blood_pressure"
                        }
                    )
            weights = Weight.objects.filter(
                user=account.get_decoded().get('id'),
                recorded_at__contains=date
            ).order_by('-recorded_at').values_list()
            if weights.exists():
                for i in list(weights):
                    diary.append(
                        {
                            "id": i[0],
                            "user_id": i[1],
                            "weight": i[2],
                            "body_fat": i[3],
                            "bmi": i[4],
                            "recorded_at": i[5].strftime('%Y-%m-%d %H:%M:%S'),
                            "type": "weight"
                        }
                    )
            sugars = Sugar.objects.filter(
                user=account.get_decoded().get('id'),
                recorded_at__contains=date
            ).order_by('-recorded_at').values_list()
            if sugars.exists():
                for i in list(sugars):
                    diary.append(
                        {
                            "id": i[0],
                            "user_id": i[1],
                            "sugar": i[2],
                            "timeperiod": i[3],
                            "recorded_at": i[4].strftime('%Y-%m-%d %H:%M:%S'),
                            "type": "blood_sugar"
                        }
                    )
            diet = Diet.objects.filter(
                user=account.get_decoded().get('id'),
                recorded_at__contains=date
            ).order_by('-recorded_at').values_list()
            if diet.exists():
                for i in list(diet):
                    diary.append(
                        {
                            'id': i[0],
                            'user_id': i[1],
                            'tag': i[4],
                            'description': i[2],
                            'meal': i[3],
                            "image": ["https://i.imgur.com/4f5eELL.png"],
                            'location': {
                                'lat': str(i[6]),
                                'lng': str(i[7])
                            },
                            'recorded_at': i[8].strftime('%Y-%m-%d %H:%M:%S'),
                            'type': 'diet',
                            'reply': '安安'
                        }
                    )
            return JsonResponse({
                "status": "0",
                "diary": diary
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_medical(request):
    try:
        if request.method == 'PATCH':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            Medical.objects.filter(
                user=account.get_decoded().get('id')
            ).update(
                diabetes_typ=data['diabetes_typ'],
                oad=data['oad'],
                insulin=data['insulin'],
                anti_hypertensives=data['anti_hypertensives']
            )
            return JsonResponse({"status": "0"})
        elif request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            medical = Medical.objects.filter(
                user=account.get_decoded().get('id')).order_by('-updated_at').values_list()
            medical_info = list()
            if not medical.exists():
                for i in list(medical):
                    medical_info = {
                        'id': i[0],
                        'user_id': i[1],
                        'diabetes_type': i[3],
                        'oad': i[4],
                        'insulin': i[5],
                        'anti_hypertensives': i[6],
                        'created_at': i[7].strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': i[8].strftime('%Y-%m-%d %H:%M:%S')
                    }
            return JsonResponse({
                "status": "0",
                'medical_info': medical_info
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_drug(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            UserProfile.objects.get(
                id=account.get_decoded().get('id')
            ).drug.create(
                type=data['type'],
                name=data['name'],
                recorded_at=data['recorded_at']
            )
            return JsonResponse({"status": "0"})
        elif request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            drug = Drug.objects.filter(
                user=account.get_decoded().get('id')).order_by('-recorded_at').values_list()
            drug_list = list()
            if drug.exists():
                for i in list(drug):
                    drug_list.append(
                        {
                            'id': i[0],
                            'user_id': i[1],
                            'type': i[2],
                            'name': i[3],
                            'recorded_at': i[4].strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
            return JsonResponse({
                'status': '0',
                'drug_useds': drug_list
            })
        elif request.method == 'DELETE':
            data = json.loads(request.body)
            Drug.objects.filter(id__in=data['ids']).delete()
            return JsonResponse({'status': '0'})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_diet(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            Diet.objects.create(
                user=UserProfile.objects.get(id=account.get_decoded().get('id')),
                description=data['description'],
                meal=data['meal'],
                tag=data['tag'],
                image=data['image'],
                lat=data['lat'],
                lng=data['lng'],
                recorded_at=data['recorded_at']
            )
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_care(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            Care.objects.create(
                message=data['message'],
                user=UserProfile.objects.get(
                    id=account.get_decoded().get('id')))
            return JsonResponse({"status": "0"})
        elif request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            cares = Care.objects.filter(user=account.get_decoded().get('id')).values_list()
            cares_list = list()
            if cares.exists():
                for i in list(cares):
                    cares_list.append(
                        {
                            'id': i[0],
                            'user_id': i[1],
                            'member_id': i[2],
                            'reply_id:': i[3],
                            'message': i[4],
                            'created_at': i[5].strftime('%Y-%m-%d %H:%M:%S'),
                            'updated_at': i[6].strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
            return JsonResponse({
                'status': '0',
                'cares': cares_list
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def user_badge(request):
    return JsonResponse({"status": "0"})


@csrf_exempt
def friend_code(request):
    try:
        if request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            code = UserProfile.objects.filter(
                id=account.get_decoded().get('id')).get()
            return JsonResponse({
                'status': '0',
                'invite_code': code.code
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_send(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            inviter = UserProfile.objects.get(
                id=account.get_decoded().get('id'))
            invitees = UserProfile.objects.get(code=data['invite_code'])
            friend = Friend.objects.filter(
                Q(inviter=inviter, invitees=invitees) | Q(invitees=inviter, inviter=invitees)
            )
            if friend.exists():
                message = {'status': '2'}
            else:
                Friend.objects.create(
                    inviter=inviter,
                    invitees=invitees,
                    type=data['type']
                )
                message = {"status": "0"}
            return JsonResponse(message)
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_accept(request, id):
    try:
        if request.method == 'GET':
            Friend.objects.filter(id=id).update(accept=1)
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_refuse(request, id):
    try:
        if request.method == 'GET':
            Friend.objects.filter(id=id).update(accept=2)
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_remove(request, id):
    try:
        if request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            remove = Friend.objects.filter(
                inviter=account.get_decoded().get('id'), invitees=id)
            if not remove.exists():
                raise
            remove.delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friends_remove(request):
    try:
        if request.method == 'DELETE':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            data = json.loads(request.body)
            Friend.objects.filter(
                Q(inviter=account.get_decoded().get('id'), invitees=data['ids[]']) |
                Q(inviter=data['ids[]'], invitees=account.get_decoded().get('id'))
            ).delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_requests(request):
    try:
        if request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            sends = Friend.objects.filter(invitees=account.get_decoded().get('id'), accept=0).values()
            send_list = list()
            if sends.exists():
                for i in list(sends):
                    user = UserSet.objects.get(user=i['inviter_id'])
                    send_list.append(
                        {
                            'id': i['id'],
                            'user_id': user.user.id,
                            'relation_id': i['inviter_id'],
                            'type': i['type'],
                            'created_at': i['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                            'updated_at': i['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),
                            'user': {
                                'id': user.user.id,
                                'name': user.name,
                                'account': user.user.account,
                                'email': user.user.email,
                                'phone': user.user.phone,
                                'fb_id': user.user.fb_id,
                                'status': 'Normal',
                                'group': 'null',
                                'privacy_policy': user.user.privacy_policy,
                                'birthday': user.birthday,
                                'height': user.height,
                                'weight': user.weight,
                                'gender': user.gender,
                                'address': user.address,
                                'verified': user.user.is_active,
                                'must_change_password': user.user.must_change_password,
                                'badge': user.user.badge,
                                'created_at': user.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                                'updated_at': user.user.last_login.strftime('%Y-%m-%d %H:%M:%S')
                            }
                        }
                    )
            return JsonResponse({
                'status': '0',
                'requests': send_list
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_list(request):
    try:
        if request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            friends_list = list()
            friend = Friend.objects.filter(
                Q(invitees=account.get_decoded().get('id'), accept=1) |
                Q(inviter=account.get_decoded().get('id'), accept=1)
            ).order_by('id').values()
            if friend.exists():
                for i in list(friend):
                    if i['inviter_id'] == account.get_decoded().get('id'):
                        user = UserSet.objects.get(user=i['invitees_id'])
                    else:
                        user = UserSet.objects.get(user=i['inviter_id'])
                    friends_list.append(
                        {
                            'id': user.user.id,
                            'name': user.name,
                            'account': user.user.account,
                            'email:': user.user.email,
                            'phone:': user.user.phone,
                            'fb_id': user.user.fb_id,
                            'status': 'Normal',
                            'group': 'null',
                            'birthday:': user.birthday,
                            'height:': user.height,
                            'gender': user.gender,
                            'verified': user.user.is_active,
                            'privacy_policy': user.user.privacy_policy,
                            'must_change_password': user.user.must_change_password,
                            'badge': user.user.badge,
                            'created_at': user.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                            'updated_at': user.user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
                            'relation_type': i['type']
                        }
                    )
            return JsonResponse({
                'status': '0',
                'friends': friends_list
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def friend_results(request):
    try:
        if request.method == 'GET':
            account = Session.objects.get(session_key=request.headers['Authorization'].split(' ')[1])
            results_list = list()
            friend = Friend.objects.filter(
                inviter=account.get_decoded().get('id'), accept=1, read=False).order_by('id')
            for i in list(friend.values()):
                user = UserSet.objects.get(user=i['invitees_id'])
                results_list.append(
                    {
                        'id': i['id'],
                        'user_id': i['invitees_id'],
                        'relation_id': user.user.id,
                        'type:': i['type'],
                        'status': i['accept'],
                        'read': i['read'],
                        'created_at': i['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': i['updated_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        'relation': {
                            'id': user.user.id,
                            'name': user.name,
                            'account': user.user.account,
                            'email': user.user.email,
                            'phone': user.user.phone,
                            'fb_id': user.user.fb_id,
                            'status': 'Normal',
                            'group': 'null',
                            'privacy_policy': user.user.privacy_policy,
                            'birthday': user.birthday,
                            'height': user.height,
                            'weight': user.weight,
                            'gender': user.gender,
                            'address': user.address,
                            'verified': user.user.is_active,
                            'must_change_password': user.user.must_change_password,
                            'badge': user.user.badge,
                            'created_at': user.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                            'updated_at': user.user.last_login.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    }
                )
            friend.update(read=True)
            return JsonResponse({
                'status': '0',
                'results': results_list
            })
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@csrf_exempt
def share(request, type):
    return JsonResponse({"status": "0"})


@csrf_exempt
def news(request):
    return JsonResponse({"status": "0"})
