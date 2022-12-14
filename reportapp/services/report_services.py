from django.db.models import Avg, Sum
from datetime import datetime
from django.contrib import messages
from django.utils.safestring import mark_safe
from reportapp.models import ReportData, Area


def contact_center_view_service(date: str) -> list:
    data = ReportData.objects.filter(date=date)
    contact_centers = list(Area.objects.order_by().values_list('area_name', flat=True).distinct())
    res = []
    for center in contact_centers:
        i = 0
        contact_center_res = {
            'contact_center': center,
            'scheduled_time': 0,
            'ready': 0,
            'share_ready': 0,
            'adherence': 0,
            'sick_leave': 0,
            'absenteeism': 0
        }
        for d in data:
            if str(d.contact_center) == center:
                contact_center_res['scheduled_time'] += d.scheduled_time
                contact_center_res['ready'] += d.ready
                contact_center_res['share_ready'] += d.share_ready
                contact_center_res['adherence'] += d.adherence
                contact_center_res['sick_leave'] += d.sick_leave
                contact_center_res['absenteeism'] += d.absenteeism
                i += 1

        if i > 0:
            contact_center_res['share_ready'] /= i
            contact_center_res['adherence'] /= i
            res.append(contact_center_res)
    return res


def contact_center_detail_service(pk: int, start_date: str = None, end_date: str = None):
    if start_date and end_date:
        data = ReportData.objects.filter(contact_center=pk,
                                         date__range=[start_date, end_date], job__calculated=True).values(
            'date',
            'contact_center__area_name', 'contact_center').annotate(
            scheduled_time_sum=Sum('scheduled_time'),
            ready_sum=Sum('ready'),
            rating_avg=Avg('rating'),
            adherence_avg=Avg('adherence'),
            sick_leave_sum=Sum('sick_leave'),
            absenteeism_sum=Sum('absenteeism'))
    else:
        date = ReportData.objects.order_by('-date').values('date').first()
        date = date['date'].strftime('%Y')
        data = ReportData.objects.filter(contact_center=pk, date__year=date, job__calculated=True).values(
            'date',
            'contact_center__area_name', 'contact_center').annotate(
            scheduled_time_sum=Sum('scheduled_time'),
            ready_sum=Sum('ready'),
            rating_avg=Avg('rating'),
            adherence_avg=Avg('adherence'),
            sick_leave_sum=Sum('sick_leave'),
            absenteeism_sum=Sum('absenteeism'))
    return data


def group_detail_service(pk: int, start_date: str = None, end_date: str = None):
    if start_date and end_date:
        data = ReportData.objects.filter(group=pk,
                                         date__range=[start_date, end_date],
                                         job__calculated=True).values('date',
                                                                      'group__group_name',
                                                                      'group').annotate(
            scheduled_time_sum=Sum('scheduled_time'),
            ready_sum=Sum('ready'),
            rating_avg=Avg('rating'),
            adherence_avg=Avg('adherence'),
            sick_leave_sum=Sum('sick_leave'),
            absenteeism_sum=Sum('absenteeism'))
    else:
        date = ReportData.objects.order_by('-date').values('date').first()
        date = date['date'].strftime('%Y')
        data = ReportData.objects.filter(group=pk,
                                         date__year=date, job__calculated=True).values('date',
                                                                                       'group__group_name',
                                                                                       'group').annotate(
            scheduled_time_sum=Sum('scheduled_time'),
            ready_sum=Sum('ready'),
            rating_avg=Avg('rating'),
            adherence_avg=Avg('adherence'),
            sick_leave_sum=Sum('sick_leave'),
            absenteeism_sum=Sum('absenteeism'))
    return data


def employee_detail_service(name: str, start_date: str = None, end_date: str = None):
    if start_date and end_date:
        data = ReportData.objects.filter(full_name=name,
                                         date__range=[start_date, end_date],
                                         ).values('date').annotate(
            scheduled_time_sum=Sum('scheduled_time'),
            ready_sum=Sum('ready'),
            rating_avg=Avg('rating'),
            adherence_avg=Avg('adherence'),
            sick_leave_sum=Sum('sick_leave'),
            absenteeism_sum=Sum('absenteeism'))
    else:
        date = ReportData.objects.order_by('-date').values('date').first()
        date = date['date'].strftime('%Y')
        data = ReportData.objects.filter(full_name=name,
                                         date__year=date, ).values('date').annotate(
            scheduled_time_sum=Sum('scheduled_time'),
            ready_sum=Sum('ready'),
            rating_avg=Avg('rating'),
            adherence_avg=Avg('adherence'),
            sick_leave_sum=Sum('sick_leave'),
            absenteeism_sum=Sum('absenteeism'))
    return data


def data_parse(request, start_date: str = None, end_date: str = None):
    try:
        start_date_check = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        end_date_check = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
        if end_date_check >= start_date_check:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
        else:
            messages.add_message(request, messages.WARNING,
                                 mark_safe("???????????????? ???????? ???? ?????????? ???????? ???????????? ??????????????????"))
    except ValueError:
        messages.add_message(request, messages.WARNING, mark_safe("???????????????? ???????? ???????????? ?? ???????? ?????????? ??????????????"))
    return start_date, end_date


def rating_leaders(leaders: dict) -> list:
    res = []
    for leader in leaders:
        if len(res) < 10:
            res.append(leader)
        else:
            if res[-1]['rating'] == leader['rating']:
                res.append(leader)
            else:
                break
    return res
