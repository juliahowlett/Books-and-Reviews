from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users, Books, Reviews


def verify_session_user(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

def index(request): #login / register
	return render(request, 'review/index.html')	
	
def register(request):  #/quotes/create_user
	print(request.POST)	
	errors_or_user = Users.objects.validate_registration(request.POST)	
		
	if errors_or_user[0]:
		for fail in errors_or_user[0]:
			messages.error(request, fail)
		return redirect('/')
		
	request.session['id'] = errors_or_user[1].id	
	messages.error(request,"Registration confirmed! Please login to see your Reviews.")
	return redirect('/index')	
	
def login(request): 	
	print(request.POST)	
	errors_or_user = Users.objects.validate_login(request.POST)
	
	if errors_or_user[0]:
		for fail in errors_or_user[0]:
			messages.error(request, fail)
		return redirect('/')
		
	request.session['id'] = errors_or_user[1].id	
	return redirect('/dashboard')	
	
def dashboard(request):
	b = Books.objects.first()
	print("b= ", b)  
	#objects.get(id=15).comments.first()
	context = { 
		"the_user" : Users.objects.get(id=request.session['id']), 
		"recent_reviews" : Reviews.objects.all().order_by('-created_at')[:3],
		"other_reviews" : Reviews.objects.all().order_by('created_at')[:3]
	} 
	return render(request, "review/dashboard.html", context)

def show_reviewer(request, user_id): 
	print("user_id = ", user_id)
	context = {
	'the_user' : Users.objects.get(id=user_id),
	'user_books' : Books.objects.filter(author_id=user_id),
	'review_count' : Reviews.objects.filter(reviewer_id=user_id).count()
	}
	return render(request, 'quotes/show.html', context)			

def show_reviews(request, book_id): 
	print("book_id = ", book_id)
	context = {
	'the_book' : Book.objects.get(id=book_id),
	'reviews' : Reviews.objects.filter(the_book=book_id)
	}
	
	if len(request.POST['review']) > 1:
		Reviews.objects.create(
		review = request.POST['review'],
		rating = request.POST['rating'],
		book = request.POST['book_id'],
		reviewer = Users.objects.get(id = request.session['id'])
		)
		
	return render(request, 'review/show_book.html', context)		
	
def test_addbook(request): #not working
	print(request.POST)
	user = request.session['id']
	print("session_id = ", user)
	errors = Users.objects.validate_quote(request.POST, user)
	
	if errors:
		for fail in errors:
			messages.error(request, fail)
		return redirect('/')
	
	return redirect('/dashboard')	
	
def new_book(request):
	return render(request, 'review/new_book.html')	

def add_book(request):	
	print(request.POST)
	print("session_id = ", request.session['id'])
		
	Books.objects.create(
	title = request.POST['title'],
	desc = request.POST['desc'],
	author = request.POST['author']
	)
	
	if len(request.POST['review']) > 1:
		Reviews.objects.create(
		review = request.POST['review'],
		rating = request.POST['rating'],
		book = request.POST['book_id'],
		reviewer = Users.objects.get(id = request.session['id'])
		)
	
	return redirect('/show_book_profile')	
	
def add_review(request, book_id): #add quote to favorites list  
	print(book_id)
	#get reference to quote from quote_id
	b = Books.objects.get(id=book_id)
	#get reference to User from session_id
	user = Users.objects.get(id=request.session['id'])
	#add the association	
	b.reviewed.add(user)
	
	return redirect('/show_book_profile')		
   
def remove_review(request, book_id): #remove quote from favorites list  
	#get reference to quote from quote_id
	b = Books.objects.get(id=book_id)
	#get reference to User from session_id
	user = Users.objects.get(id=request.session['id'])
	#remove the association	
	b.reviewed.remove(user)
	
	return redirect('/')
	
def logout(request):
	del request.session['id']
	return redirect('/index')
