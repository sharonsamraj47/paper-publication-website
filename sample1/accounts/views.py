from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignUpForm, LoginForm, UploadFileForm, PaperSubmissionForm
from .models import UploadedFile, UserProfile, User
from django.core.mail import send_mail
from django.conf import settings

def home2(request):
    return render(request, 'home2.html')

def indexing(request):
    return render(request, 'indexing.html')

def contact(request):
    return render(request, 'contactus.html')

def author(request):
    return render(request, 'authorguidelines.html')

def edit(request):
    return render(request, 'editorialboard.html')

def scope(request):
    return render(request, 'scope.html')


def about(request):
    return render(request, 'about.html')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('home')
    else:
        form = UploadFileForm()
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'home.html', {'form': form, 'files': files})


def home2(request):
    files = UploadedFile.objects.filter(uploaded_to_home2=True)
    return render(request, 'home2.html', {'files': files})

@login_required
def paper_submission(request):
    if request.method == 'POST':
        form = PaperSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.user = request.user
            paper.user_name = request.user.username
            paper.save()
            return redirect('home')
    else:
        form = PaperSubmissionForm()
    return render(request, 'paperSub.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_staff

def admin_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                return render(request, 'registration/admin_login.html', {'form': form, 'error': 'Invalid credentials or not an admin'})
    else:
        form = LoginForm()
    return render(request, 'registration/admin_login.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_home(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')
        reviewer_id = request.POST.get('reviewer_id')
        if file_id:
            file = UploadedFile.objects.get(id=file_id)
            if action == 'send_to_reviewer' and reviewer_id:
                reviewer = User.objects.get(id=reviewer_id)
                file.reviewer = reviewer
                file.reviewer_feedback = 'pending'
                file.save()
                
                # Send email to the reviewer
                subject = 'Paper needs to be reviewed'
                message = f'Paper Title: {file.title}\nAuthor: {file.user.username}\n\nPlease review the paper.'
                recipient_list = [reviewer.email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
                
            elif action == 'accept_home2':
                file.uploaded_to_home2 = True
            elif action == 'reject_home2':
                file.uploaded_to_home2 = False
            file.save()

    files = UploadedFile.objects.all()
    reviewers = User.objects.filter(userprofile__is_reviewer=True)
    return render(request, 'admin_home.html', {'files': files, 'reviewers': reviewers})

def is_reviewer(user):
    return hasattr(user, 'userprofile') and user.userprofile.is_reviewer

def reviewer_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and is_reviewer(user):
                login(request, user)
                return redirect('reviewer_home')
            else:
                return render(request, 'registration/reviewer_login.html', {'form': form, 'error': 'Invalid credentials or not a reviewer'})
    else:
        form = LoginForm()
    return render(request, 'registration/reviewer_login.html', {'form': form})

@login_required
@user_passes_test(is_reviewer)
def reviewer_home(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')
        if file_id and action in ['accept', 'minor_review', 'major_review', 'reject']:
            file = UploadedFile.objects.get(id=file_id)
            if action == 'accept':
                file.reviewer_feedback = 'accepted'
            elif action == 'minor_review':
                file.reviewer_feedback = 'minor_review'
            elif action == 'major_review':
                file.reviewer_feedback = 'major_review'
            elif action == 'reject':
                file.reviewer_feedback = 'rejected'
            file.save()
           

            return redirect('reviewer_home')  # Redirect to refresh the page
        
        if action == 'add_comment':
            comment = request.POST.get('comment')
            file.reviewer_comment = comment
            file.save()
            return redirect('reviewer_home')

    files = UploadedFile.objects.filter(reviewer=request.user, reviewer_feedback='pending')
    return render(request, 'reviewer_home.html', {'files': files})

@login_required
@user_passes_test(is_reviewer)
def reviewer_comment(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        comment = request.POST.get('comment')
        if file_id and comment:
            file = UploadedFile.objects.get(id=file_id)
            file.reviewer_comment = comment
            file.save()
            return redirect('reviewer_home')  # Redirect to refresh the page
    return redirect('reviewer_home')

def home2_view(request):
    if request.user.is_authenticated:
        return redirect('home2')
    else:
        return render(request, 'home2.html')

def user_dashboard(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')
