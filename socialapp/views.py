from django.shortcuts import render, redirect
from .forms import CustomUserForm,  ProfileForm, PostForm
from .models import *
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='sign_in')
def home(request):
    profile = Profile.objects.get(user=request.user)
    user_sug = Profile.objects.all()
    following_post = []
    following_pro = []
    following_profiles = []

    followings = FollowersCount.objects.filter(user=profile)

    for users in followings:
        user = User.objects.get(username=users.following)
        following_profile = Profile.objects.get(user=user)
        post = Post.objects.filter(user=following_profile)
        following_post.extend(post)
        following_profiles.append(following_profile)

    user_post = Post.objects.filter(user=profile)
    following_post.extend(user_post)

    for a_user in user_sug:
        if a_user == profile:
            pass
        elif a_user in following_profiles:
            pass
        else:
            following_pro.append(a_user)
            print(a_user)

    print(post)
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            post = Post(
                image = new_post.image,
                caption = new_post.caption,
                user = profile,
            )
            post.save()
            messages.success(request, 'You have successfully upload a new post')
            return redirect('home')
    
    else:
        form = PostForm()
        
    context={
        'profile': profile,
        'form': form,
        'posts': following_post,
        'user_sug': following_pro,
    }
    return render(request, "index.html", context)

@login_required(login_url='sign_in')
def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    if LikePost.objects.filter(post=post, username=username).exists():
        likepost = LikePost.objects.get(post=post, username=username)
        likepost.delete()
        post.likes -= 1
        post.save()
    else:
        new_likepost = LikePost(
        username=username,
        post=post,
        )
        new_likepost.save()
        post.likes += 1
        post.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='sign_in')
def profile(request, pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user)
    user_profile = Profile.objects.get(user=request.user)
    post = Post.objects.filter(user=profile)

    no_of_post = len(post)

    if FollowersCount.objects.filter(following=pk, user=user_profile).exists():
        follow='Unfollow'
    else:
        follow='Follow'

    follower = len(FollowersCount.objects.filter(following=user_profile))
    following = len(FollowersCount.objects.filter(user=user_profile))
    context={
        'profile': profile,
        'posts': post,
        'follow': follow,
        'follower': follower,
        'following': following,
        'no_of_post': no_of_post,
    }
    return render(request, "profile.html", context)

@login_required(login_url='sign_in')
def follow(request):
    user = request.user
    following = request.GET.get('following')
    profile = Profile.objects.get(user=user)

    if FollowersCount.objects.filter(following=following, user=profile).exists():
        old_follower = FollowersCount.objects.get(following=following, user=profile)
        old_follower.delete()
    else:
        new_follower = FollowersCount(
        following=following,
        user=profile,
        )
        new_follower.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='sign_in')
def setting(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method =='POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated '+ (profile.user.username) + 'profile')
            return redirect('setting')

    context={
        'profile': profile,
        'form': form
    }
    return render(request, "setting.html", context)

def sign_up(request):
    if request.method =='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            user = User.objects.get(username=new_user.username)
            newprofile = Profile(
                user = user
            )
            newprofile.save()
            return redirect('home')
    else:
        form = CustomUserForm()
    context = {'form': form}
    return render(request, "sign-up.html", context)

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username,password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Hi {username}, you are now logged-in")
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credential')
            return redirect('sign_in')
    return render(request, "sign-in.html")

@login_required(login_url='sign_in')
def logout(request):
    auth.logout(request)
    return redirect('sign_in')