from datetime import datetime
from django.shortcuts import render, redirect
from .models import SleepRecord
from django.contrib.auth.decorators import login_required
from .forms import SleepRecordForm
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def sleep_list(request):
    records = SleepRecord.objects.filter(user=request.user).order_by('-sleep_time')

    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            records = records.filter(
                sleep_time__date=filter_date
            )
        except ValueError:
            pass

    return render(request, 'sleep/list.html', {
        'records': records,
        'date_filter': date_filter
    })

@login_required
def add_record(request):
    if request.method == 'POST':
        form = SleepRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('sleep_list')
    else:
        form = SleepRecordForm()
    return render(request, 'sleep/add.html', {'form': form})