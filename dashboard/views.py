from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from members.models import Member
from member_types.models import MemberType


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members_no'] = Member.objects.count()
        context['new_members_last_seven_days'] = Member.objects.filter(created_at__day__lte=7).count()
        context['new_members_last_thirty_days'] = Member.objects.filter(created_at__day__lte=30).count()
        context['members_active'] = Member.objects.filter(is_msf_active=True).count()
        context['member_type_investor_business'] = MemberType.objects.get(name='Business Investor').member_set.count()
        context['member_type_investor_individual'] = MemberType.objects.get(name='Individual').member_set.count()
        context['member_type_business'] = MemberType.objects.get(name='Business').member_set.count()
        context['member_type_professional'] = MemberType.objects.get(name='Professional').member_set.count()
        context['member_type_student'] = MemberType.objects.get(name='Student').member_set.count()
        context['member_type_futures'] = MemberType.objects.get(name='Futures').member_set.count()
        return context

