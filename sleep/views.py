from django.shortcuts import render, redirect
from .models import SleepRecord
from django.contrib.auth.decorators import login_required
from .forms import SleepRecordForm

@login_required
def sleep_list(request):
    records = SleepRecord.objects.filter(user=request.user).order_by('-sleep_time')
    return render(request, 'sleep/list.html', {'records': records})

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