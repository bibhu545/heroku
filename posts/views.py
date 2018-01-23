from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect,Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.
from django.utils import timezone
from urllib.parse import quote_plus
from .forms import PostForm
from .models import Post




def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None ,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form":form
	}
	return render(request,"post_form.html",context)

def post_detail(request,id=None):
	instance = get_object_or_404(Post,id=id)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context={
		"title":"detail",
		"instance":instance,
		"share_string":share_string
	}	
	return render(request,"post_detail.html",context)



def post_list(request):
	today = timezone.now()
	queryset_list = Post.objects.active() #filter(draft=False).filter(publish__lte=timezone.now()) #all() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	#Search Filter
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
						Q(title__icontains=query) |
						Q(content__icontains=query
						))
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page

	#Paging
	page = request.GET.get('page')
	queryset = paginator.get_page(page)
	context={
		"object_list":queryset,
		"title":"All Posts",
		"today":today
	}
	return render(request,"post_list.html",context)



def post_update(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None,request.FILES or None,instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		instance.user = request.user
		messages.success(request,'<a href="#">Successfully Saved</a>', extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
		"title":"detail",
		"instance":instance,
		"form":form,
	}	
	return render(request,"post_form.html",context)

def post_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	# return redirect("posts:post_list")
	return redirect('/posts/') 