import urllib

from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail


import webapp2

class database(ndb.Model):
    """Models a Guestbook entry with an author, content, avatar, and date."""
    bomma = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
	
def db_key(username):
    """Constructs a Datastore key for a Guestbook entity with name."""
    return ndb.Key('User1', username or 'default')
	
class MainPage(webapp2.RequestHandler):
    def get(self):
		
	user=users.get_current_user()
	
	if user:
		mail.send_mail(sender="ImageTransform<team@smiling-duality-122605.appspotmail.com>",
              to=user.nickname()+ "<" +user.email()+">",
              subject="Thank You",
              body="""
Dear """ +user.nickname()+""",
Thank you for using our Image transform service. 

Have a good day!

Regards
-Image Transform team
""")
		username = user.nickname()
		self.response.out.write("""
              <form action="/sign?%s"
                  enctype="multipart/form-data"
                    method="post">             
                <div><label>Give your New Image:</label></div>
                <div><input type="file" name="img"/></div>
                <div><input type="submit" value="submit"></div>
              </form>
		
		
              
            """ % (urllib.urlencode({'username': username}))) #username is the key

		self.response.out.write('<a href="'+users.create_logout_url('/'))
		self.response.out.write('"style="color: #555; background: #ffc; position: fixed; right: 10px; top:10px">signout</a>')
									
		self.response.out.write('<h1><center>Welcome '+username+'</center></h1>')				
		last_image = database.query(ancestor=db_key(username)).order(-database.date).fetch(1)

		for i in last_image:
			self.response.out.write('<h3>Your last used image was</h3>')			
			self.response.out.write('<div><img src="/img?img_id=%s"></img>' % i.key.urlsafe())
			self.response.out.write(#"""<div><img src="/img1?img_id=%s"></img>
		"""<form action="/img1" method="get" style="float:right">             
                <div><label>Choose Transforms:</label></div><br>
                 Size(AxA):<br>
  		<input type="text" name="size"><br>
		Rotate degrees: <br>
		<select name="deg">
  <option value="0">0</option>
  <option value="90">90</option>
  <option value="180">180</option>
  <option value="270">270</option>
</select><br><br> Flip the Image <br>
		<input type="radio" name="flip" value="nothing" checked> Do nothing <br>
		<input type="radio" name="flip" value="flipH" > Flip Horizontal<br>
  		<input type="radio" name="flip" value="flipV"> Flip Vertical<br>
  		
		 <input type="checkbox" name="lucky" value="lucky"> I'm Feeling Lucky<br>

		<input type="hidden" name="img_id" value="%s"<br><br>
		<div><input type="submit" value="Transform"></div>
              </form>""" % (i.key.urlsafe()))#,i.key.urlsafe()))									
 
	else:
		self.response.out.write('<a href="'+users.create_login_url('/'))
		self.response.out.write('">Login</a>')
		self.response.out.write('</body></html>')
			
class User1(webapp2.RequestHandler):	
    def post(self):
	username = self.request.get('username')
	db=database(parent=db_key(username))
	db.bomma = self.request.get('img')
	db.put()
		
	self.redirect('/?' + urllib.urlencode(
            {'username': username}))
			
class Transform(webapp2.RequestHandler):
	def get(self):
		i_key = ndb.Key(urlsafe=self.request.get('img_id'))
		x= self.request.get('size')
		deg=self.request.get('deg')
		flip=str(self.request.get('flip'))
		lucky=str(self.request.get('lucky'))
		#flipV=self.request.get('flipV')
		#nothing=self.request.get('nothing')	
		#self.response.out.write(str(x)+"<br>")
        	greeting = i_key.get()
		if greeting.bomma:
        		if x == '' :
				x='500'
			x=int(x)
			deg=int(deg)
			self.response.headers['Content-Type'] = 'image/png'
			greeting.bomma = images.resize(greeting.bomma, x, x)							
					
			greeting.bomma = images.rotate(greeting.bomma,deg)	
			
			if flip == "flipH":
				greeting.bomma = images.horizontal_flip(greeting.bomma)
			if flip == "flipV":
				greeting.bomma = images.vertical_flip(greeting.bomma)
			if lucky == "lucky":
				greeting.bomma = images.im_feeling_lucky(greeting.bomma)
			self.response.out.write(greeting.bomma)
		else:
            		self.response.out.write('No image')
		
			
class Image(webapp2.RequestHandler):
    def get(self):
        i_key = ndb.Key(urlsafe=self.request.get('img_id'))
        greeting = i_key.get()
        if greeting.bomma:
            self.response.headers['Content-Type'] = 'image/png'
            greeting.bomma = images.resize(greeting.bomma, 500, 500)
	    self.response.out.write(greeting.bomma)
        else:
            self.response.out.write('No image')			
 
	  
app = webapp2.WSGIApplication([('/', MainPage),
			       ('/sign', User1),
				   ('/img', Image),
				   ('/img1', Transform)],
                              debug=True)
