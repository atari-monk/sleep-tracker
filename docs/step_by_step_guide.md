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
    {% raw %} {% extends 'base.html' %} {% block content %}
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
    {% endblock %} {% endraw %}
    ```

    - Create `sleep/templates/sleep/add.html`:

    ```html
    {% raw %} {% extends 'base.html' %} {% block content %}
    <h1>Add Sleep Record</h1>
    <form method="post">
      {% csrf_token %} {{ form.as_p }}
      <button type="submit">Save</button>
    </form>
    {% endblock %} {% endraw %}
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

## Phase 7: Authentication

The error occurs because Django's built-in authentication views (which you're including with `path('accounts/', include('django.contrib.auth.urls'))`) are looking for templates in a `registration` directory, but you haven't created these templates yet.

Here's how to fix this:

1. First, create a `templates/registration` directory in your `sleep` app:

   ```
   mkdir -p sleep/templates/registration
   ```

2. Create a login template at `sleep/templates/registration/login.html`:

   ```html
   {% raw %} {% extends 'base.html' %} {% block content %}
   <h1>Login</h1>
   <form method="post">
     {% csrf_token %} {{ form.as_p }}
     <button type="submit">Login</button>
   </form>
   <p>Don't have an account? <a href="{% url 'signup' %}">Sign up</a></p>
   {% endblock %} {% endraw %}
   ```

3. Update your `settings.py` to tell Django where to find templates. Add this to `TEMPLATES` in `sleeptracker/settings.py`:

   ```python
   'DIRS': [os.path.join(BASE_DIR, 'templates')],
   ```

   The full TEMPLATES setting should look something like:

   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [os.path.join(BASE_DIR, 'templates')],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```

4. If you want to add signup functionality (which the login template references), you'll need to:

   - Create a signup view in `sleep/views.py`:

     ```python
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
     ```

   - Create a signup template at `sleep/templates/registration/signup.html`:

     ```html
     {% raw %} {% extends 'base.html' %} {% block content %}
     <h1>Sign up</h1>
     <form method="post">
       {% csrf_token %} {{ form.as_p }}
       <button type="submit">Sign up</button>
     </form>
     <p>Already have an account? <a href="{% url 'login' %}">Login</a></p>
     {% endblock %} {% endraw %}
     ```

   - Add the URL pattern to `sleep/urls.py`:
     ```python
     path('signup/', views.signup, name='signup'),
     ```

5. Also, you might want to add a redirect for after login. Add this to `settings.py`:
   ```python
   LOGIN_REDIRECT_URL = 'sleep_list'
   ```

After making these changes, the login page should work properly. The error occurred because Django's auth system has default views but expects you to provide the templates for those views.

Remember to restart your development server after making these changes:

```
python manage.py runserver
```

## Phase 8: How to Remove a Django Superuser

To remove a Django superuser, you have a few options:

### Method 1: Using Django's shell

1. Generate script to remove superuser

1. Open the Django shell:

   ```bash
   python manage.py shell
   ```

1. In the shell, run script:

   ```python
   exec(open(r'C:\atari-monk\code\my-scripts\django\delete_superuser.py').read())
   ```

### Method 2: Using Django's createsuperuser command (if you want to recreate)

1. First delete the user (as above)
2. Then create a new one:
   ```bash
   python manage.py createsuperuser
   ```

### Method 3: Using the Django admin interface

1. Log in to your Django admin interface (usually at `/admin`)
2. Go to "Users"
3. Find the superuser account you want to delete
4. Select it and choose "Delete" from the action dropdown

### Important Notes:

- Be absolutely sure you want to delete the superuser as this action is irreversible
- Make sure you have at least one superuser remaining if your application requires admin access
- If you accidentally delete all superusers, you'll need to create a new one using `createsuperuser`

Would you like more specific instructions for any of these methods?

I'll enhance the sleep tracker app to automatically calculate duration when the user enters sleep and wake times. Here's how to implement this:

## Phase 9: Enhanced Duration Calculation

We'll add JavaScript to calculate the duration in real-time as the user enters times. Here are the modifications needed:

1. **Update the add.html template**:

```html
{% raw %}{% extends 'base.html' %} {% block content %}
<h1>Add Sleep Record</h1>
<form method="post">
  {% csrf_token %} {{ form.as_p }}
  <div>
    <strong>Duration:</strong>
    <span id="duration-display">Not calculated yet</span>
  </div>
  <button type="submit">Save</button>
</form>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const sleepTimeInput = document.getElementById('id_sleep_time');
    const wakeTimeInput = document.getElementById('id_wake_time');
    const durationDisplay = document.getElementById('duration-display');

    function calculateDuration() {
      const sleepTime = new Date(sleepTimeInput.value);
      const wakeTime = new Date(wakeTimeInput.value);

      if (isNaN(sleepTime) || isNaN(wakeTime)) {
        durationDisplay.textContent = 'Invalid times';
        return;
      }

      if (wakeTime <= sleepTime) {
        durationDisplay.textContent = 'Wake time must be after sleep time';
        return;
      }

      const durationMs = wakeTime - sleepTime;
      const hours = Math.floor(durationMs / (1000 * 60 * 60));
      const minutes = Math.floor((durationMs % (1000 * 60 * 60)) / (1000 * 60);

      durationDisplay.textContent = `${hours} hours ${Math.round(minutes)} minutes`;
    }

    sleepTimeInput.addEventListener('change', calculateDuration);
    wakeTimeInput.addEventListener('change', calculateDuration);
  });
</script>
{% endblock %}{% endraw %}
```

2. **Enhance the model's duration property** (in models.py):

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
        if self.sleep_time and self.wake_time:
            delta = self.wake_time - self.sleep_time
            total_seconds = delta.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        return "N/A"
```

3. **Update the list.html template** to show the formatted duration:

```html
{% raw %}{% extends 'base.html' %} {% block content %}
<h1>Your Sleep Records</h1>
<a href="{% url 'add_record' %}">Add New Record</a>
<ul>
  {% for record in records %}
  <li>
    <strong>Slept:</strong> {{ record.sleep_time|date:"Y-m-d H:i" }} |
    <strong>Woke:</strong> {{ record.wake_time|date:"Y-m-d H:i" }} |
    <strong>Duration:</strong> {{ record.duration }} {% if record.notes %}
    <p><strong>Notes:</strong> {{ record.notes }}</p>
    {% endif %}
  </li>
  {% endfor %}
</ul>
{% endblock %}{% endraw %}
```

### Additional Improvements

1. **Add form validation** in forms.py:

```python
from django import forms
from .models import SleepRecord
from django.core.exceptions import ValidationError
from datetime import datetime

class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['sleep_time', 'wake_time', 'notes']
        widgets = {
            'sleep_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'wake_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        sleep_time = cleaned_data.get('sleep_time')
        wake_time = cleaned_data.get('wake_time')

        if sleep_time and wake_time:
            if wake_time <= sleep_time:
                raise ValidationError("Wake time must be after sleep time")

            # Optional: Validate that sleep duration is reasonable
            duration = wake_time - sleep_time
            if duration.total_seconds() > 24 * 3600:
                raise ValidationError("Sleep duration cannot be more than 24 hours")
            if duration.total_seconds() < 1 * 3600:
                raise ValidationError("Sleep duration should be at least 1 hour")

        return cleaned_data
```

2. **Add date filtering** to the sleep list view:

```python
@login_required
def sleep_list(request):
    records = SleepRecord.objects.filter(user=request.user).order_by('-sleep_time')

    # Add date filtering
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
```

3. **Update the list template to include date filtering**:

```html
{% raw %}{% extends 'base.html' %} {% block content %}
<h1>Your Sleep Records</h1>
<a href="{% url 'add_record' %}">Add New Record</a>

<form method="get" style="margin: 20px 0;">
  <label for="date">Filter by date:</label>
  <input type="date" id="date" name="date" value="{{ date_filter }}" />
  <button type="submit">Filter</button>
  {% if date_filter %}
  <a href="{% url 'sleep_list' %}">Clear filter</a>
  {% endif %}
</form>

<ul>
  {% for record in records %}
  <li>
    <strong>Slept:</strong> {{ record.sleep_time|date:"Y-m-d H:i" }} |
    <strong>Woke:</strong> {{ record.wake_time|date:"Y-m-d H:i" }} |
    <strong>Duration:</strong> {{ record.duration }} {% if record.notes %}
    <p><strong>Notes:</strong> {{ record.notes }}</p>
    {% endif %}
  </li>
  {% empty %}
  <li>No sleep records found.</li>
  {% endfor %}
</ul>
{% endblock %}{% endraw %}
```

These enhancements will:

1. Show real-time duration calculation as the user enters times
2. Format durations in a human-readable way (e.g., "7h 30m")
3. Add client-side and server-side validation
4. Allow filtering records by date
5. Improve the mobile display of sleep records

The app will now be more user-friendly and provide immediate feedback about sleep durations.
