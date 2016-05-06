Image_Transform using Google App Engine
==========================
The site is aimed at provinding simple operations on an image like resize, rotate, flip. It is implemented using Google App Engine and ints service APIs

*The following are the steps to be followed for a new user*:
- Login using your google account.
- Upload the image from the computer
  
  -One can perform one or more of the following transformations
   
  -Rotate: Select the angle of rotation required

  -Resize: Enter the pixel quantity to resize to (AxA) (Eg. 500x500)

  -Image flip: Select the flip option either horizontal or vertical flip.

  -I'm feeling lucky: It is a feature provided by google which returns a much sharper image. 
- Log out 

The last image uploaded by the user is displayed when the user comes back.

An E-mail is sent to the user when the service is used. 

## Services Used

**Google App Engine Service APIs**:

1. User account management
2. Google Datastore (ndb)
3. Image manipulation API
4. Mail API

###### Team Members

1. Amarnath Kothapalli
2. Atmanand Citigori
3. Sai Siddhardha Reddy Thatiparthi 
4. Yashmin Singla
