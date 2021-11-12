from flask import Flask, render_template, request,redirect, url_for
import sqlite3, os
app = Flask(__name__)

UPLOAD_FOLDER = '/static/profiles'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#----------------First home page----------------
@app.route('/')
def greeting():
   return "Artist table - Get ready for some mindblowing koding"

#----------------Creating the DB---------------- 

@app.route("/createdb", methods=['POST'])
def createdb():
  
   print ("making a connection")
   connection = sqlite3.connect('artistss.db')

   print ("Getting a Cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute('''CREATE TABLE IF NOT EXISTS artistss
            (id INTEGER PRIMARY KEY, name TEXT,email VARCHAR, about TEXT, date_created DATE, Profile TEXT, appr INTEGER)''') #add date modified later

   print ("Commiting the changes")
   connection.commit()

   print ("Closing the datbase")
   connection.close()

   return ("Datbase Created Succssffully")
#----------------Creating the Artists' profiles---------------- 
@app.route("/artist_create", methods=['GET','POST'])
def artist_create():

   if request.method == 'POST':
      name = request.form['name']
      email = request.form['email']
      about = request.form['about']
      createdate = request.form['createdate']
      image = request.files['File']  
      appr = 0

      try:
         # file url is used for storing images at an absolute location on the os file folder.
         file_url = os.path.join(os.getcwd()+ UPLOAD_FOLDER, image.filename)

         # static url is required for serving images from a static folder. store this on SQL DB
         staic_url = os.path.join(UPLOAD_FOLDER, image.filename)

         image.save(file_url)

         print(staic_url)

         print ("making a connection")
         connection = sqlite3.connect('artistss.db')

         print ("Getting a Cursor")
         cursor = connection.cursor()
         
         print ("Executing the DML")
         cursor.execute("INSERT into artistss (name, email, about, date_created, Profile, appr) values (?,?,?,?,?,?)",(name,email,about,createdate,staic_url,appr))  
         
         print ("Commiting the changes")
         connection.commit()

         print ("Closing the datbase")
         connection.close()

         return redirect(url_for('profilelist'))
   
      except Exception as error:
         return_message = str(error)
         return(return_message)

   else:
      return render_template("profile_create.html")

#----------------Displaying the Artists' profiles---------------- 
@app.route("/profilelist", methods=['GET'])
def profilelist():
   print ("making a connection")
   connection = sqlite3.connect('artistss.db')

   print ("Getting a Cursor")
   cursor = connection.cursor()
   
   print ("Executing the DML")
   cursor.execute("select * from artistss")

   print ("Get the Rows from cursor")
   all_profiles = cursor.fetchall() 

   print ("Closing the datbase")
   connection.close()

   print(all_profiles)
   
   return render_template("profile_list.html", profile = all_profiles)

#----------------Updating the Artists' profiles----------------
@app.route("/profileupdate/<int:id>", methods=['GET','POST'])
def profileupdate(id):
   
   if request.method == 'POST':
      name = request.form['name']
      email = request.form['email']
      about = request.form['about']
      createdate = request.form['createdate']
      image = request.files['file']  
  
      if(len(image.filename)!=0):

         old_image = request.form['image_file']
         current_dir = os.getcwd()

         old_image_url = current_dir +old_image
         print(old_image_url)
         try:
            # file url is used for storing images at an absolute location on the os file folder.
            file_url = os.path.join(os.getcwd()+ UPLOAD_FOLDER, image.filename)

            # static url is required for serving images from a static folder. store this on SQL DB
            static_url = os.path.join(UPLOAD_FOLDER, image.filename)

            image.save(file_url)

            # Lets delete old image
            os.remove(old_image_url)

            print ("making a connection", id)
            connection = sqlite3.connect('artistss.db')
         
            print ("Getting a Cursor")
            cursor = connection.cursor()
            
            print ("Executing the DML")
            cursor.execute("UPDATE artistss SET name=?, email=?, about=?, date_created=?, Profile=? WHERE id=?",(name,email,about,createdate,static_url,id))  
            
            print ("Commiting the changes")
            connection.commit()
            return redirect(url_for('profilelist'))
      
         except Exception as error:
            return_message = str(error)
            return(return_message)
      else:
         print ("making a connection", id)
         connection = sqlite3.connect('artistss.db')
         
         print ("Getting a Cursor")
         cursor = connection.cursor()
            
         print ("Executing the DML")
         cursor.execute("UPDATE artistss SET name=?, email=?, about=?, date_created=? WHERE id=?",(name,email,about,createdate,id))  
            
         print ("Commiting the changes")
         connection.commit()
         return redirect(url_for('profilelist'))

   else:
      
      print ("making a connection")
      connection = sqlite3.connect('artistss.db')
   
      print ("Getting a Cursor")
      cursor = connection.cursor()
      
      print ("Executing the DML")
      cursor.execute("select * from artistss where id=(?)", (id,))

      print ("Get the Rows from cursor")
      show_data = cursor.fetchall()
      
      print ("Closing the datbase")
      connection.close()

      return render_template("profile_update.html", show_data = show_data)

#----------------Deleting the Artists' profiles----------------
@app.route("/profiledelete/<int:id>", methods=['GET','POST'])
def profiledelete(id):
      
   try:

      print ("making a connection")
      connection = sqlite3.connect('artistss.db')

      print ("Getting a Cursor")
      cursor = connection.cursor()
      
      print ("Executing the DML")
      cursor.execute("DELETE from artistss where id=(?)", (id,))
      
      print ("Commiting the changes")
      connection.commit()

      print ("Closing the datbase")
      connection.close()
      
      return redirect(url_for('profilelist'))
   
   
   except Exception as error:
      return_message = str(error)
      return(return_message)

#----------------Sending love to Artists'----------------
@app.route("/sendlove/<int:id>",methods=['GET','POST'])
def sendlove(id):
   print ("making a connection")
   connection = sqlite3.connect('artistss.db')

   print ("Getting a Cursor")
   cursor = connection.cursor()
      
   print ("Executing the DML")
   cursor.execute("UPDATE artistss SET appr=appr+1 WHERE id=(?)",(id,))

   print ("Commiting the changes")
   connection.commit()

   print ("Closing the datbase")
   connection.close()

   print ("making a connection")
   connection = sqlite3.connect('artistss.db')

   print ("Getting a Cursor")
   cursor = connection.cursor()

   print ("Executing the DML")
   cursor.execute("SELECT * from artistss where id=(?)",(id,))

   print ("Get the Rows from cursor")
   data = cursor.fetchall() 

   print ("Closing the datbase")
   connection.close()

   return render_template("sendlove.html", item = data)

if __name__ == '__main__':
   app.run()
   app.debug = True