#from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_MATCH = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
	#for testing only - user creation without validation
	def add(self, post_data):
		self.create(
			name = post_data['name'],
			alias = post_data['alias'],
			email = post_data['email'],
			password = post_data['password'],
			dob = post_data['dob']
			)
		print(post_data)

	def validate_registration(self, post_data):
		print(post_data) 	
		errors = []
		user = None
		#check for empty fields
		for  key, value in post_data.items():
			if len(value) < 1:
				errors.append("All fields are required")
				break

		#min length for name /alias
		if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
			errors.append("all fields must be at least 2 characters") 
			
		#email valid
		if not re.match(EMAIL_MATCH, post_data['email']):
			errors.append("email not valid")
			
		#email already in DB
		if self.filter(email=post_data['email']):
			errors.append("email in use")	
			print(errors)
		
		#min length for password
		if len(post_data['password']) < 8:
			errors.append("password must be at least 8 characters") 
			
		#passwords match 
		if post_data['password'] != post_data['confirm_pw']:
			errors.append("Passwords do not match")
		  
		# user must be 18 or older
		years = (datetime.today() - datetime.strptime(post_data['dob'], "%Y-%m-%d")).days/365
		if years < 18:
			errors.append("Must be 18 or older to register")
			
		#if no errors, create a User
		if not errors:
			hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())
				
			user = self.create(
				name = post_data['name'],
				alias = post_data['alias'],
				email = post_data['email'],
				password = hashed_pw,
				dob = post_data['dob']
				)
				
		return  errors, user		
	
	def validate_login(self, post_data):
		print(post_data) 	
		errors = []
		user = None
		#check all fields for input- check for empty fields
		for  key, value in post_data.items():
			if len(value) < 1:
				errors.append("All fields are required")
				print(errors)
				break
			
		#Check DB for Existing email / password	
		if not self.filter(email=post_data['email']):
			errors.append("Invalid email/password")
		else:
			user = self.get(email=post_data['email'])
			# if email is in DB then check passwords
			if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
				errors.append("Invalid email/password")	
			
		return errors, user		

	def validate_book(self, post_data, user):
		print(post_data) 	
		errors = []
		#check for empty fields
		for  key, value in post_data.items():
			if len(value) < 1:
				errors.append("Please enter an Author and a Message")
				break

		#min length for author and quote
		if len(post_data['author']) < 2:
			errors.append("Name must be at least 2 characters") 
			
		if len(post_data['quote']) < 10:
			errors.append("Messages must be at least 10 characters") 
			
		#if no errors, create the Quote
		if not errors:
		
			the_quote = self.create(
				quote = post_data['quote'],
				author = post_data['author'],
				creator =  Users.objects.get(id = user)
				)	
					
		return errors		
			
class Users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=50)
	dob = models.DateField(auto_now=True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	
	objects = UserManager()
	
	def __repr__(self):
		return "<name: {}, alias: {}, email: {}, id: {}, created_at: {}>".format(self.name,self.alias,self.email,self.id, self.created_at)	
	
class Books(models.Model):
	name = models.CharField(max_length=255)
	desc = models.TextField(max_length=1000)
	author = models.ForeignKey(Users, default=0, related_name="author")
	reviewed = models.ManyToManyField(Users, null=True, related_name="reviewed") 
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True) 
	
	def __str__(self):
		return "{} {} {}" % (self.name, self.desc, self.author)	
		
class Reviews(models.Model):
	review = models.TextField(max_length=1000)
	rating = models.IntegerField()
	reviewer = models.ForeignKey(Users, null=True, related_name="reviewer") 
	the_book = models.ForeignKey(Books, related_name="the_book", null=True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True) 
	
	def __str__(self):
		return "{} {} {}" % (self.name, self.desc, self.author)			

