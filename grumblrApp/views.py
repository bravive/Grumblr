from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.urlresolvers import reverse
from forms import *
from models import *
from grumblrApp.models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.contrib.auth.views import password_reset,password_reset_confirm
from django.template.loader import render_to_string

    
def index(request):
    context={}
    context['form_login']=LoginForm()
    context['form_reg']=RegistrationForm()
    return render(request,'Sign_In/Index.html',context)
 
def makeview(request,context):
    static_context={}
    static_context['form_login']=LoginForm()
    static_context['form_reg']=RegistrationForm()
    static_context['form_compose']=ComposeForm()
    static_context['form_comment']=CommentForm()
    static_context['form_search']=SearchForm()
    static_context['form_relation']=RelationshipForm()
    static_context['form_entry']=EntryForm()
    static_context['form_password']=PasswordForm()
    static_context['form_reset']=ResetForm()
    static_context['url_next']='Sign_In/Index.html'
    static_context.update(context)
    return render(request,static_context['url_next'],static_context)

def entry_id(User):
    users=Entry.objects.filter(owner=User)
    if not users:
        id=0
        return id
    for user in users:
        id=user.id
    return id

    
def relationGrumbls(request):
    items=[]
    ##if there is no object, get will arise an error
    #user=UserRelationship.objects.get(user=request.user)
    user=get_object_or_404(UserRelationship,user=request.user)
    ###when you want to use one-to-one and many-to-many, first step shall be to get all elements with.all() in many-to-many, because it is object rather than a list
    user_followings=user.followings.all()#then turn object into list
    items = Grumbls.objects.filter(user=user_followings).order_by('-id')#use the list to user
    ##return following grumbls
    return items
    
def unblockedGrumbls(request,all_grumbls):
    ##arg1:user,arg2:all grumbls should be filtered
    context={}
    items=[]
    context['temp']=[]
    context['items_grumbls_residuals']=[]
    user_object=get_object_or_404(User,username=request.user.username)
    persons=user_object.block_map.all()
    if not persons:
        return all_grumbls
    for person in persons:
        items_grumbls=Grumbls.objects.filter(user=person.user)
        ###grep all persons grumbls
        for item in items_grumbls:
            context['temp'].append(item)
    #not blocked grumbls
    for item in all_grumbls:
        if not item in context['temp']:
            context['items_grumbls_residuals'].append(item)
    items=context['items_grumbls_residuals']
    return items
#judge the specific user if be blocked

def isBlocked(request, username):
    context={}
    blocked_or_not=0
    user=get_object_or_404(UserRelationship,user=request.user)
    ###important,manytomany must be use all(),add(),set() and so on
    context['items_blocking_usernames'] = user.blockings.all()
    other_user=User.objects.filter(username=username)
    for other_user_name in other_user:
        if other_user_name in context['items_blocking_usernames']:
        #if username in blockings list, it denotes the username has been blocked
            blocked_or_not=1
    return blocked_or_not
    
def getUserNameById(requset,id):
    context={}
    context['username']=User.objects.filter(id=id)
    response_text = serializers.serialize('json', context['username'])
    return HttpResponse(response_text, content_type="JSON/username.json")
    

@login_required
@transaction.atomic
def dlike(request, id, page):
    context={}
    item=get_object_or_404(Grumbls,id=id)
    if page == '1':
        context['url_next']='Home/Home.html'
        items=relationGrumbls(request)
    context['items'] = items
    dlike_user=get_object_or_404(User,username=request.user.username)
    item.dislike_user.add(dlike_user)
    item.save()
    #context['dislikes'] = item.dislike_user.all()
    context['dislikes'] = Grumbls.objects.all()
    comments = Comment.objects.all()
    context['comments'] = comments
    context['id']=entry_id(request.user)
    #return makeview (request, context)
    context["dlikes"]=item.dislike_user.all().order_by('-id')
    response_text=render_to_string("JSON/dlike.json",context)
    return HttpResponse(response_text, content_type="application/json")




@login_required
@transaction.atomic
def comment(request, id, page):
    context={}
    #1.get
    item=get_object_or_404(Grumbls,id=id)
    if page == '1':
        context['url_next']='Home/Home.html'
        items=relationGrumbls(request)
    elif page == '2':
        context['url_next']='Profile/Profile.html'
        context['user_name'] = item.user.username
        items = Grumbls.objects.filter(user=request.user)
    elif page == '3':
        context['url_next']='Profile/Profile_others.html'
        context['user_name'] = item.user.username
        items = Grumbls.objects.filter(user=item.user)

    if request.method == 'GET':
        comments = Comment.objects.filter(item=item)
        context['comments'] = comments
        return makeview(request,context)
    #2.generate SQL
    new_comment = Comment(item=item,user=request.user)
    #3.work in modelform
    form = CommentForm(request.POST, instance=new_comment)
    comments = Comment.objects.all()

    items_unblocked=unblockedGrumbls(request,items)
    context['items'] = items_unblocked
    context['comments'] = comments
    context['dislikes'] = Grumbls.objects.all().order_by('-id')
    context['id']=entry_id(request.user)
    
    if not form.is_valid():
        return makeview (request, context)
    #4.DEAL
    form.save()
    context['comments'] = str(item.id)
    #response_text = serializers.serialize("json", context["comments"])
    #return HttpResponse(response_text, content_type="application/json")
    return makeview (request, context)

@login_required
@transaction.atomic
def comment_js(request, id, page):
    context={}
    item=get_object_or_404(Grumbls,id=id)
    new_comment = Comment(item=item,user=request.user)
    form = CommentForm(request.POST, instance=new_comment)
    if form.is_valid():
        form.save()
    context["comments"]=Comment.objects.filter(item__id=id).order_by('-id')
    response_text = serializers.serialize("json", context["comments"])
    return HttpResponse(response_text, content_type="application/json")

@login_required
@transaction.atomic
def comment_dynamic(request, id, page):
    context={}
    item=get_object_or_404(Grumbls,id=id)
    input="comment_input_name"+str(id)
    if request.method == 'POST' and input in request.POST:
        if not (len(request.POST[input])<=0 and len(request.POST[input])>=400):
            commentform=Comment(text=request.POST[input],item=item,user=request.user)
            commentform.save()
    context["comments"]=Comment.objects.filter(item__id=id).order_by('-id')
    response_text = serializers.serialize("json", context["comments"])
    return HttpResponse(response_text, content_type="application/json")




@login_required
@transaction.atomic
def get_all_comments(request,id):
    context={}
    context["comments"]=Comment.objects.filter(item__id=id).order_by('-id')
    response_text = serializers.serialize("json", context["comments"])
    return HttpResponse(response_text, content_type="application/json")


@login_required
@transaction.atomic
def get_update_grumbls(request,id):
    context={}
    items=[]
    user=get_object_or_404(UserRelationship,user=request.user)
    user_followings=user.followings.all()
    items_following = Grumbls.objects.filter(user=user_followings).filter(pk__gt=id).order_by('-id')
    items_unblocked=unblockedGrumbls(request,items_following)
    context["items"]=items_unblocked
    response_text=render_to_string("JSON/grumblr.json",context)
    return HttpResponse(response_text, content_type="application/json")

@login_required
@transaction.atomic
def get_all_dlikes(request,id):
    context={}
    item=get_object_or_404(Grumbls,id=id)
    context["dlikes"]=item.dislike_user.all().order_by('-id')
    response_text=render_to_string("JSON/dlike.json",context)
    return HttpResponse(response_text, content_type="application/json")

@login_required
def home(request): 
    context={}
    context['url_next']='Home/Home.html'
    items_following=relationGrumbls(request)
    items_unblocked=unblockedGrumbls(request,items_following)
    context['dislikes'] = Grumbls.objects.all().order_by('-id')
    context['items'] = items_unblocked
    context['id']=entry_id(request.user)
    return makeview(request,context)
    
@login_required
def profile(request):
    context={}
    context['url_next']='Profile/Profile.html'
    #context['form_search']=SearchForm()
    items = Grumbls.objects.filter(user=request.user).order_by('-id')
    context['user_name'] = request.user.username
    context['user_email'] = request.user.email
    context['dislikes'] = Grumbls.objects.all().order_by('-id')
    context['items'] = items
    #context['comments'] = Comment.objects.filter(item__user=request.user).order_by('-id')
    context['id']=entry_id(request.user)
    return makeview(request,context)
    
@login_required
def profile_others(request,id):
    context={}
    context['url_next']='Profile/Profile_others.html'
    #context['form_search']=SearchForm()
    item = get_object_or_404(Grumbls,id=id)
    if item is None:
        context['url_next']='Home/Home.html'
        return makeview(request,context)
    context['user_name'] = item.user.username
    context['user_email'] = item.user.email
    context['items_all'] = Grumbls.objects.filter(user=item.user).order_by('-id')
    context['dislikes'] = Grumbls.objects.all().order_by('-id')
    context['items']=unblockedGrumbls(request,context['items_all'])
    #context['comments'] = Comment.objects.filter(item__user=item.user).order_by('-id')
    context['id']=entry_id(item.user)
    context['blocked_or_not']=isBlocked(request,item.user.username)
    return makeview(request,context)
    
@login_required
def profile_others_username(request,username):
    context={}
    context['url_next']='Profile/Profile_others.html'
    #context['form_search']=SearchForm()
    user = get_object_or_404(User,username=username)
    if user is None:
        context['url_next']='Home/Home.html'
        return makeview(request,context)
    context['user_name'] = user.username
    context['items_all'] = Grumbls.objects.filter(user=user).order_by('-id')
    context['items']=unblockedGrumbls(request,context['items_all'])
    #context['comments'] = Comment.objects.filter(item__user=user).order_by('-id')
    context['id']=entry_id(user)
    context['blocked_or_not']=isBlocked(request,username)
    return makeview(request,context)
    
@login_required
def profile_edit(request):
    context={}
    
    context['url_next']='Pro_edit/Pro_edit.html'
    context['id'] = request.user.id
    context['user_name'] = request.user.username
    context['user_email'] = request.user.email
    #entry_to_edit = Entry.objects.get(owner=request.user)
    context['entry']=Entry.get_entries(request.user)
    return makeview(request,context)



@login_required
@transaction.atomic
def edit_entry(request, id):
    context={}
    
    context['url_next']='Pro_edit/Pro_edit.html'
    user=get_object_or_404(User,username=request.user.username)
    entry_to_edit = Entry(owner=user, id=id)
    context['user_name'] = request.user.username
    context['user_email'] = request.user.email
    if request.method == 'GET':   
        form = EntryForm(instance=entry_to_edit)  # Creates form from
        context['form_entry'] = form
        context['id']=id
        return makeview(request,context)

    # if method is POST, get form data to update the model
    form = EntryForm(request.POST, request.FILES, instance=entry_to_edit)

    if not form.is_valid():
        context['form_entry'] = form
        context['id']=id
        return makeview(request,context)
    form.save()
    context['id']=id
    context['entry'] = form
    return makeview(request,context)

@login_required
def get_photo(request, id):
    #entry = get_object_or_404(Entry, owner=request.user, id=id)
    entry = get_object_or_404(Entry, id=id)
    if not entry.picture:
        raise Http404
    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, content_type=content_type)
@login_required
def get_photo_username(request, username):
    #entry = get_object_or_404(Entry, owner=request.user, id=id)
    entry = get_object_or_404(Entry, owner__username=username)
    if not entry.picture:
        raise Http404
    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, content_type=content_type)
@login_required
def get_photo_userid(request, userid):
    #entry = get_object_or_404(Entry, owner=request.user, id=id)
    entry = get_object_or_404(Entry, owner__id=userid)
    if not entry.picture:
        raise Http404
    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, content_type=content_type)
    
@login_required
@transaction.atomic
def search(request):
    user_to_username = lambda u: u.username
    context={}
    context['url_next']='Search/Search.html'
    context['following_usernames']=[]
    context['unfollowing_usernames']=[]
    context['items_grumbls_residuals']=[]
    #context['temp']=[]
    items_default = Grumbls.objects.filter(user=request.user)
    context['items_others'] = items_default
    form=SearchForm(request.GET)
    context['form_search']=form
    if not form.is_valid():
        return makeview(request,context)
    context['all_usernames'] = User.objects.filter(username__contains=request.GET['search']).exclude(username=request.user.username)

    items_grumbls=Grumbls.objects.filter(text__contains=request.GET['search']).order_by('-id')
    context['items_grumbls'] = items_grumbls
    ###-----------add following func for usernames--------------###
    #diagnose if there is a friend
    user=UserRelationship.objects.filter(user=request.user)
    if not user:
        context['unfollowing_usernames']=context['all_usernames']
        context['items_grumbls_residuals']=context['items_grumbls']
        return makeview(request,context)

    user=UserRelationship.objects.get(user=request.user)
    context['following_usernames'] = map(user_to_username, user.followings.all())
    context['unfollowing_usernames'] = User.objects.exclude(username__in=context['following_usernames']).exclude(username=request.user.username)
    #context['unfollowing_usernames'] = user.follow_map.exclude(username__contains=request.GET['search'])
    #context['unfollowing_usernames']=UserRelationship.objects.filter(username__contains=request.GET['search']).exclude(username__in=user.follow_map.all())
    #All following username   
#    user=UserRelationship.objects.get(user=request.user)
    ###important,manytomany must be utse all(),add(),set() and so on


#    context['items_following_usernames'] = user.followings.all()


    ##in searched usernames that is in following,exclude self
#    for name in context['items_usernames'] :
#        if name in context['items_following_usernames']:
#            context['following_usernames'].append(name)
    ##in searched usernames that is in unfollowing,exclude self
#    for name in context['items_usernames']:
#        if name not in context['items_following_usernames']:
#            context['unfollowing_usernames'].append(name)
    
    #users = User.objects.filter(username__contains=request.GET['search'])
    #users = users.exclude(username_map_in=user.user_followings)


    ###-----------add blocking func for grumbls--------------###
    context['items_grumbls_residuals']=unblockedGrumbls(request,context['items_grumbls'])
    return makeview(request,context)
    
@login_required    
@transaction.atomic
def addfollowing(request):
    context= {}
    context['url_next']='Search/Search.html'

    if request.method == 'GET':
        #context['url_next']='Home/Home.html'
        return makeview(request,context)
    context['followed_username']=request.POST['followed_username']
    #1.get Who I Aam
    user = get_object_or_404(User,username=request.user.username)
    #1.get Whom I will follow
    follow = get_object_or_404(User,username=context['followed_username'])
    #2.generate the first object
    person=UserRelationship(user=user)
    #2.generate the seconde object
    person.followings.add(follow)
    #3.work in modelform
    form = RelationshipForm(request.POST, instance=person)
    if not form.is_valid():
        #context['url_next']='Home/Home.html'
        return makeview(request,context)
    #4.DEAL
    form.save()
    context['person_msgs']=UserRelationship.objects.filter(user=request.user)
    return makeview(request, context)
@login_required    
@transaction.atomic
def addunfollowing(request):
    context= {}
    context['url_next']='Search/Search.html'

    if request.method == 'GET':
        #context['url_next']='Home/Home.html'
        return makeview(request,context)
    context['unfollowed_username']=request.POST['unfollowed_username']
    #1.get Who I Aam
    user = get_object_or_404(User,username=request.user.username)
    #1.get Whom I will follow
    follow =get_object_or_404(User,username=context['unfollowed_username'])
    #2.generate the first object
    person=UserRelationship(user=user)
    #2.generate the seconde object
    person.followings.remove(follow)
    #3.work in modelform
    form = RelationshipForm(request.POST, instance=person)
    if not form.is_valid():
        #context['url_next']='Home/Home.html'
        return makeview(request,context)
    #4.DEAL
    form.save()
    context['person_msgs']=UserRelationship.objects.filter(user=request.user)
    return makeview(request, context)
    
@login_required    
@transaction.atomic
def addblocking(request):
    context= {}
    context['url_next']='Profile/Profile_others.html'
    if request.method == 'GET':
        #context['url_next']='Home/Home.html'
        return makeview(request,context)
    context['blocked_username']=request.POST['blocked_username']
    context['user_name'] = context['blocked_username']
    context['items'] = Grumbls.objects.filter(user__username=context['blocked_username']).order_by('-id')
    context['comments'] = Comment.objects.filter(item__user__username=context['blocked_username']).order_by('-id')    
    user = get_object_or_404(User,username=request.user.username)
    block = get_object_or_404(User,username=context['blocked_username'])
    context['id']=entry_id(block)
    person=UserRelationship(user=user)
    person.blockings.add(block)
    form = RelationshipForm(request.POST, instance=person)
    
    if not form.is_valid():
        return makeview(request,context)
    form.save()
    context['blocked_or_not']=isBlocked(request,request.POST['blocked_username'])
    return makeview(request, context)
    
@login_required    
@transaction.atomic
def addunblocking(request):
    context= {}
    context['url_next']='Profile/Profile_others.html'
    if request.method == 'GET':
     #context['url_next']='Home/Home.html'
        return makeview(request,context)
    context['unblocked_username']=request.POST['unblocked_username']
    context['user_name'] = context['unblocked_username']
    context['items'] = Grumbls.objects.filter(user__username=context['unblocked_username']).order_by('-id')
    context['comments'] = Comment.objects.filter(item__user__username=context['unblocked_username']).order_by('-id')

    user = get_object_or_404(User,username=request.user.username)
    unblock = get_object_or_404(User,username=context['unblocked_username'])
    context['id']=entry_id(unblock)
    person=UserRelationship(user=user)
    person.blockings.remove(unblock)
    form = RelationshipForm(request.POST, instance=person)

    if not form.is_valid():
        return makeview(request,context)
    form.save()
    context['blocked_or_not']=isBlocked(request,request.POST['unblocked_username'])
    return makeview(request, context)
    
@login_required
@transaction.atomic
def additem(request):
    context= {}
    context['url_next']='Home/Home.html'
    if request.method == 'GET':
        return makeview(request,context)
    new_item = Grumbls(user=request.user)
    form=ComposeForm(request.POST,instance=new_item)
    if not form.is_valid():
        return makeview (request, context)
    form.save()
    return redirect(reverse('grumblrApp_home'))

  
@login_required
@transaction.atomic
def deleteitem(request, id):
    errors = []
    # Deletes item if the logged-in user has an item matching the id
    try:
    	item_to_delete = get_object_or_404(Grumbls,id=id, user=request.user)
    	item_to_delete.delete()
    except ObjectDoesNotExist:
	    errors.append('The item did not exist in your todo list.')
    items = Grumbls.objects.filter(user=request.user)
    context = {'items' : items, 'errors' : errors}
    return render(request, 'Home/Home.html', context)

@login_required
@transaction.atomic
def changepassword(request):
    context={}
    context['id'] = request.user.id
    context['user_name'] = request.user.username
    context['entry']=Entry.get_entries(request.user)
    context['url_next']='Pro_edit/Pro_edit.html'
    if request.method == 'GET':
        return makeview (request, context)
    form=PasswordForm(request.POST)
    context['form_errors']=form
    if not form.is_valid():
        return makeview (request, context)
    u = get_object_or_404(User,id=request.user.id)
    u.set_password(request.POST['password2'])
    u.save()
    
    user = authenticate(username=request.user.username, password=request.POST['password2'])
    login(request, user)
    context['form_message']='Successful Change !'
    return makeview (request, context)

def forgotpassword(request):
    context={}
    context['url_next']='Sign_In/forgotPassword.html'
    return makeview (request, context)

@transaction.atomic  
def mylogin(request):
    context = {}
    errors = []
    context['errors_login'] = errors
    ###forms validation
    if request.method == 'GET':
        context['form_login']=LoginForm()
        return makeview(request,context)
    form=LoginForm(request.POST)
    context['form_login']=form
    if not form.is_valid():
        return makeview (request, context)
    ###models authentication
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return redirect(reverse('grumblrApp_home'))
            #return redirect(reverse('grumblrApp.views.home'))
        else:
            # Return a 'disabled account' error message
            errors.append('Account is disabled.')
            return makeview(request, context)
    else:
        # Return an 'invalid login' error message.
        errors.append('Incorrect user name and password.')
        return makeview(request, context)

@transaction.atomic       
def mylogout(request):
    logout(request)
    return redirect(reverse('grumblrApp_index'))
    
@transaction.atomic   
def myregister(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form_reg']=RegisterationForm()
        return makeview (request, context)
    
    form=RegistrationForm(request.POST)
    context['form_reg']=form
    if not form.is_valid():
        return makeview(request, context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()
    token = default_token_generator.make_token(new_user)
    email_body = """
Welcome to Grumblr.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="charlie+devnull@cs.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'Sign_In/needs-confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'Sign_In/confirmed.html', {})



@transaction.atomic
def reset(request):
    context = {}
    # Just display the registration form if this is a GET request
    #if request.method == 'GET':
    #    context['form_reset'] = ResetForm()
    #    return makeview (request, context)
    
    # form=ResetForm(request.POST)
    #context['form_reset']=form
    #if not form.is_valid():
    #    return makeview(request, context)

    return password_reset(request,
                          template_name='Sign_In/password_reset_form.html',
                          email_template_name='Sign_In/password_reset_email.html',
                          subject_template_name='Sign_In/password_reset_subject.txt',
                          from_email='ziyuans@andrew.cmu.edu',
                          #password_reset_form=ResetForm,
                          post_reset_redirect=reverse('grumblrApp_success_reset'))
@transaction.atomic
def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request,
                                  template_name='Sign_In/password_reset_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('grumblrApp_success_reset_confirm')
                                  )
def success_reset(request):
    return render(request, 'Sign_In/success_reset.html')
def success_reset_confirm(request):
    return render(request, 'Sign_In/success_reset_confirm.html')
    
    
    
    
    
    
    
    