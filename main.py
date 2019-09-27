import sqlite3 as sql
from flask import Flask,request, render_template

#create the connection of the database
try:
	conn=sql.connect('farm.db')
except:
	print("Error while creating connection")


#create table farm1 to store data from farm 1 if not exist
conn.execute('''
	CREATE TABLE IF NOT EXISTS farm1(
		name varchar(25),
		number int
	);
	''')

#create table for farm 2 if not exist
conn.execute('''
	CREATE TABLE  IF NOT EXISTS farm2(
		name varchar(25),
		number int
	);
	''')

#create table for fram 3 if not exist
conn.execute('''
	CREATE TABLE IF NOT EXISTS farm3(
		name varchar(25),
		number int
	);

''')
#curso=conn.execute('SELECT * from farm1')
#print(curso.fetchall())

conn.close()

def flask():
	#create flask app
	app= Flask(__name__)

	#route for index page
	@app.route('/')
	def index():
		return render_template('index.html')


	# route for farm 1
	@app.route('/farm1')
	def farm1():
		conn=sql.connect('farm.db')
		f1cursor=conn.execute('SELECT * from farm1')
		return render_template('farm1.html',items=f1cursor.fetchall())
		conn.close()
	
	#route for farm 3
	@app.route('/farm2')
	def farm2():
		conn=sql.connect('farm.db')
		f1cursor=conn.execute('SELECT * from farm2')
		return render_template('farm2.html',items=f1cursor.fetchall())
		conn.close()
		


	#route for farm 4
	@app.route('/farm3')
	def farm3():
		return render_template('farm3.html')

	#data update route for farm1 table
	@app.route('/update1',methods=['GET','POST'])
	def update1():
		if request.method=='POST':
			name=request.form['name']
			num=request.form['num']
			conn=sql.connect('farm.db')
			s="SELECT * from farm1 where name='"+str(name)+"'"
			data=conn.execute(s).fetchall()
			if(len(data)==0):
				conn.execute('INSERT INTO farm1 VALUES(?, ?)',(name,num))
			else:
				s="UPDATE farm1 SET number="+str(int(data[0][1])+int(num))+" where name='"+str(name)+"'"
				conn.execute(s)
				conn.commit()
			conn.commit()
			conn.close()
		return render_template('update.html',name="Updated Farm One")
	
	#data update route for farm2 table
	@app.route('/update2',methods=['GET','POST'])
	def update2():
		if request.method=='POST':
			name=request.form['name']
			num=request.form['num']
			conn=sql.connect('farm.db')
			s="SELECT * from farm2 where name='"+str(name)+"'"
			data=conn.execute(s).fetchall()
			if(len(data)==0):
				conn.execute('INSERT INTO farm2 VALUES(?, ?)',(name,num))
			else:
				s="UPDATE farm2 SET number="+str(int(data[0][1])+int(num))+" where name='"+str(name)+"'"
				conn.execute(s)
				conn.commit()
			conn.close()
		return render_template('update.html',name="Updated Farm Two")

	@app.route('/delete1',methods=['GET','POST'])
	def delete1():
		if request.method=='POST':
			name=request.form['delName']
			conn=sql.connect('farm.db')
			s="DELETE from farm1 where name='"+str(name)+"'"
			conn.execute(s)
			conn.commit()
			conn.close()
		else:
			return "Not passed in a condition"
		return render_template('update.html',name="Deleted In Farm One")
	@app.route('/transfer',methods=['GET','POST'])
	def transfer():
		if (request.method)=='POST':
			fromTable=request.form['fromTable']
			toTable=request.form['toTable']
			name=request.form['name']
			number=request.form['number']
			conn=sql.connect('farm.db')
			#getting data from from table
			s="SELECT * from "+str(fromTable)+" where name='"+str(name)+"'"
			cursor=conn.execute(s)
			data=cursor.fetchall()
			noInDatabase=int(data[0][1])
			
			#getting data from to table
			
			s_two="SELECT * from "+str(toTable)+" where name='"+str(name)+"'"
			cursor_two=conn.execute(s_two)
			data_two=cursor_two.fetchall()
			if(len(data_two)==0):
				noInDatabase_two=0
			else:
				noInDatabase_two=int(data_two[0][1])
				
			
			#if from table doesn't have that value
			if(len(data)==0):
				msg=str(name)+" not found in the database"
			
			
			
			#if from table doesn't have enough no
			if(noInDatabase<int(number)):
				msg="Not sufficient no of "+str(name)+" to transfer"
				
			
			#if all data are to be transfered from table 1
			if(noInDatabase==int(number)):
				s3="DELETE FROM "+str(fromTable)+" where name='"+str(name)+"'"
				conn.execute(s3)
				conn.commit()
				if(len(data_two)==0):
					s3="INSERT INTO "+str(toTable)+" values('"+str(name)+"',"+str(int(number))+")"
					conn.execute(s3)
					conn.commit()
				else:
					s3="UPDATE "+str(toTable)+" SET number="+str(noInDatabase_two+int(number))+" where name='"+str(name)+"'"
					conn.execute(s3)
					conn.commit()
				msg="Data Transfered Succesfully"

			#if some data are to be transferred from "from table"
			if(noInDatabase>int(number)):
				s="UPDATE "+str(fromTable)+" SET number="+str(noInDatabase-int(number))+" where name='"+str(name)+"'"
				conn.execute(s)
				conn.commit()
				if(len(data_two)==0):
					s="INSERT INTO "+str(toTable)+" values('"+str(name)+"',"+str(int(number))+")"
					conn.execute(s)
					conn.commit()
				else:
					s="UPDATE "+str(toTable)+" SET number="+str(noInDatabase_two+int(number))+" where name='"+str(name)+"'"
					conn.execute(s)
					conn.commit()
				msg="Data Transfered Succesfully"
			conn.close()
			
		else:
			return "Post condition not passed"
		return render_template("update.html",name=msg)
		#main function decleration
	if __name__=="__main__":
		app.run(debug=True)
flask()