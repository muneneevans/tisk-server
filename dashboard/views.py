from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from members.models import Member


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members_no'] = Member.objects.count()
        context['new_members_last_seven_days'] = Member.objects.filter(created_at__day__gte=7).count()
        context['new_members_last_thirty_days'] = Member.objects.filter(created_at__day__gte=30).count()
        return context

