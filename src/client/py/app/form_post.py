from flask import Flask, render_template, session, url_for, escape, request, redirect
from app import app
import json, random
from os import listdir, system, chdir
from os.path import isfile, join, abspath, dirname

jspath = abspath(join(dirname( __file__ ), '..', '..','javascript'))

@app.route('/group1', methods=['POST'])
def group1():
        user_data=request.form
        chdir(jspath)
        user_data = str(json.dumps(user_data))
        print(user_data)
        print(session['wallet'])
        system("node setRequest.js " + session['wallet'].strip() + " " + user_data.replace(" ",""))
        return json.dumps({'status':'OK'})

@app.route('/group2', methods=['POST'])
def group2():
	user_data=request.form
	chdir(jspath)
	user_data = str( json.dumps(user_data))
	system("node setWork.js " + session['wallet'].strip() + " " + user_data.replace(" ",""))
	return json.dumps({'status':'OK'})

@app.route('/fbsignup', methods=['POST'])
def fbsignup():
	email=request.form['email_id']
	passwd=request.form['passwd']
	user_name=request.form['user-name']
	user_group=request.form['user-group']
	s=SignUp()
	s.signup_user(email,passwd,user_name,user_group)
	return redirect(url_for('signin'))

@app.route('/login', methods=['POST'])
def login():
	error_msg='Wrong Email/Password'
	user_login=request.form
	wallet=user_login['wallet']

	try:
		session['wallet'] = wallet
		print(session['wallet'])
	except:
		return render_template('login.html',error_msg=error_msg)
	if session['wallet'] == 'admin':
		return redirect(url_for('admin'))
	return redirect(url_for('forms'))

@app.route('/vote', methods=['POST'])
def vote():
	poll_data=request.form
	g1=Poll_Vote()
	result=g1.submit_vote(poll_data['choice-radio'], poll_data['poll-id'],session['group'],session['username'])
	return json.dumps({'status':result,'poll-data':poll_data})

@app.route('/logout')
def logout():
	session.pop('wallet', None)
	return redirect(url_for('index'))
