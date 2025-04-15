# Learning Django by Building a Sleep Tracker App

Great choice! Building a simple but useful sleep tracker is an excellent way to learn Django. Here's a step-by-step guide to create your app:

## Phase 1: Setup and Basic Structure

1. **Install Python** (3.8 or higher recommended)
2. **Create a virtual environment**: `python -m venv venv`
3. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. **Install Django**: `pip install django`
5. **Create a new Django project**: `django-admin startproject sleeptracker`

- already having project folder, cd it and use . to create the project in the current folder, not a new subfolder.
  ```sh
  django-admin startproject sleeptracker .
  ```

6. **Create a sleep app**: `python manage.py startapp sleep`
7. **Add 'sleep' to INSTALLED_APPS** in `sleeptracker/settings.py`

## Phase 2: Database Models

8. **Define your Sleep model** in `sleep/models.py`:

   ```python
   from django.db import models
   from django.contrib.auth.models import User

   class SleepRecord(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       sleep_time = models.DateTimeField()
       wake_time = models.DateTimeField()
       notes = models.TextField(blank=True, null=True)

       @property
       def duration(self):
           return self.wake_time - self.sleep_time
   ```

9. **Create and apply migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

## Phase 3: Views and URLs

10. **Create views** in `sleep/views.py`:

    ```python
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
    ```

11. **Create forms** in `sleep/forms.py`:

    ```python
    from django import forms
    from .models import SleepRecord

    class SleepRecordForm(forms.ModelForm):
        class Meta:
            model = SleepRecord
            fields = ['sleep_time', 'wake_time', 'notes']
            widgets = {
                'sleep_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                'wake_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            }
    ```

12. **Set up URLs**:

    - In `sleeptracker/urls.py`:

    ```python
    from django.contrib import admin
    from django.urls import path, include
    from django.contrib.auth import views as auth_views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('django.contrib.auth.urls')),
        path('', include('sleep.urls')),
    ]
    ```

    - Create `sleep/urls.py`:

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.sleep_list, name='sleep_list'),
        path('add/', views.add_record, name='add_record'),
    ]
    ```

## Phase 4: Templates

13. **Create templates**:

    - Create `templates` directory in `sleep` app
    - Create base template `sleep/templates/base.html`:

    ```html
    {% raw %}
    <!DOCTYPE html>
    <html>
      <head>
        <title>Sleep Tracker</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <nav>
          {% if user.is_authenticated %}
          <a href="{% url 'sleep_list' %}">Home</a> |
          <a href="{% url 'add_record' %}">Add Record</a> |
          <a href="{% url 'logout' %}">Logout</a>
          {% else %}
          <a href="{% url 'login' %}">Login</a>
          {% endif %}
        </nav>
        {% block content %}{% endblock %}
      </body>
    </html>
    {% endraw %}
    ```

    - Create `sleep/templates/sleep/list.html`:

    ```html
    {% raw %}
    {% extends 'base.html' %} {% block content %}
    <h1>Your Sleep Records</h1>
    <a href="{% url 'add_record' %}">Add New Record</a>
    <ul>
      {% for record in records %}
      <li>
        Slept: {{ record.sleep_time }} | Woke: {{ record.wake_time }} |
        Duration: {{ record.duration }} {% if record.notes %}
        <p>{{ record.notes }}</p>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
    {% endblock %}
    {% endraw %}
    ```

    - Create `sleep/templates/sleep/add.html`:

    ```html
    {% raw %}
    {% extends 'base.html' %} {% block content %}
    <h1>Add Sleep Record</h1>
    <form method="post">
      {% csrf_token %} {{ form.as_p }}
      <button type="submit">Save</button>
    </form>
    {% endblock %}
    {% endraw %}
    ```

## Phase 5: Mobile Optimization

14. **Add mobile-friendly styling**:
    - Add this to `base.html` in the `<head>` section:
    
    ```html
    <style>
      body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        padding: 10px;
      }
      input,
      textarea,
      button {
        width: 100%;
        padding: 8px;
        margin: 5px 0 15px;
        box-sizing: border-box;
      }
      button {
        background: #4caf50;
        color: white;
        border: none;
      }
      nav {
        margin-bottom: 20px;
      }
      ul {
        list-style: none;
        padding: 0;
      }
      li {
        padding: 10px;
        border-bottom: 1px solid #ddd;
      }
    </style>
    ```

## Phase 6: Testing and Deployment

15. **Create a superuser**: `python manage.py createsuperuser`
16. **Run the development server**: `python manage.py runserver`
17. **Test your app** at `http://127.0.0.1:8000`
18. **For production**:
    - Consider deploying to PythonAnywhere, Heroku, or Railway
    - Add `STATIC_ROOT` and `STATICFILES_DIRS` to settings
    - Set `DEBUG = False` and configure `ALLOWED_HOSTS`

## Next Steps for Enhancement

Once you have this basic version working, you could:

1. Add charts to visualize sleep patterns
2. Implement a "quick add" that assumes current time for sleep/wake
3. Add sleep quality ratings
4. Set up daily/weekly sleep reports
5. Add reminders to go to bed

Would you like me to elaborate on any of these steps or suggest additional features?

