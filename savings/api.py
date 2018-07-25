from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

import requests
import json


from .serializers import *
from .models import *
from users.models import User
from members.models import Member
from savings.lib import get_registration_total


class UserDepositsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    model = User
    serializer_class = UserDepositSerializer
    lookup_field = 'email'


class CreateDepositView(CreateAPIView):
    permission_classes = [AllowAny, ]
    # permission_classes = [IsAuthenticated, ]
    model = Deposit
    serializer_class = CreateDepositSerializer


class UserDepoistStatusView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        # get the user details from the request
        member = Member.objects.filter(user=request.user)[0]

        if member:
            # get mobile phone details and request for deposit status

            header = {"Authorization": "Bearer TestAPIKey"}
            payload = {
                "Request": {
                    "mobile_number": member.phone_number
                }
            }

            r = requests.post(settings.MFS_ENDPOINT+"/api/v1/depositstatus",
                              data=json.dumps(payload), headers=header)

            try:
                if(r.status_code == 200):
                    response = r.json()
                    if(response["Response"]['status_code'] == 200):
                        return JsonResponse(response['Response'])
                    else:
                        return JsonResponse(
                            {
                                'message': "unable to reach MFS"
                            },
                            status=400)

            except:
                return JsonResponse(
                    {
                        'message': "unable to reach MFS"
                    },
                    status=400)


class UserRegistrationStatusView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        # get the user details from the request
        member = Member.objects.filter(user=request.user)[0]

        if member:
            # get mobile phone details and request for deposit status

            header = {"Authorization": "Bearer TestAPIKey"}
            payload = {
                "Request": {
                    "mobile_number": member.phone_number
                }
            }

            r = requests.post(settings.MFS_ENDPOINT+"/api/v1/depositstatus",
                              data=json.dumps(payload), headers=header)

            try:
                if(r.status_code == 200):
                    response = r.json()
                    if(response["Response"]['status_code'] == 200):
                        # find all registration transactions
                        paid_registration_fees = get_registration_total(
                            response["Response"]['transactions'])

                        # import pdb
                        # pdb.set_trace()
                        registration_fee = float(
                            member.member_type.membership_category.registration_fee)
                        if paid_registration_fees > registration_fee:
                            member.is_registartion_fee_paid = True
                            member.save()
                            return JsonResponse(
                                {
                                    'status': "success",
                                    "is_registartion_fee_paid": True,
                                    'message': "Registration fees fully paid"
                                },
                                status=200)
                        else:
                            return JsonResponse(
                                {
                                    'status': "incomplete",
                                    "is_registartion_fee_paid": False,
                                    'message': "Registration fees unpaid",
                                    "areas": registration_fee - paid_registration_fees
                                },
                                status=200)

                    else:
                        return JsonResponse(
                            {
                                'message': "unable to reach MFS"
                            },
                            status=400)
            except:
                return JsonResponse(
                    {
                        'message': "unable to reach MFS"
                    },
                    status=400)


class MakeTransactionView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        # ensure all parameters are provided
        if request.data:
            filters = request.data
            required_filters = [
                'amount', 'transaction_type'
            ]
            for r_filter in required_filters:
                if not r_filter in filters.keys():
                    return JsonResponse(
                        {
                            'status': 'bad request',
                            'message': "missing attribute: " + r_filter
                        },
                        status=400)

        member = Member.objects.filter(user=request.user)[0]

        if member:
            # get mobile phone details and request for deposit status

            header = {"Authorization": "Bearer TestAPIKey"}
            payload = {
                "Request": {
                    "mobile_number": member.phone_number,
                    "amount": request.data["amount"],
                    "transaction_type": request.data["transaction_type"]
                }
            }

            r = requests.post(settings.MFS_ENDPOINT+"/api/v1/account_transaction",
                              data=json.dumps(payload), headers=header)

            try:
                if(r.status_code == 200):
                    response = r.json()
                    if(response["Response"]['status_code'] == 200):
                        return JsonResponse(response['Response'])
                    else:
                        return JsonResponse(
                            {
                                'message': "unable to reach MFS"
                            },
                            status=400)

            except:
                return JsonResponse(
                    {
                        'message': "unable to reach MFS"
                    },
                    status=400)
        else:
            return JsonResponse({'parameters': "empty"})
        # get the user details from the request
