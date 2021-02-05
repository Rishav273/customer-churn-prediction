from flask import Flask, render_template, jsonify, request

from keras.models import load_model

model = load_model('ANN.h5')

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		CreditScore = int(request.form['credit_score'])
		Age = int(request.form['age'])
		Tenure = int(request.form['tenure'])
		Balance = float(request.form['balance'])
		has_credit_card = request.form['has_credit_card']
		is_active_member = request.form['is_active_member']
		EstimatedSalary = float(request.form['estimated_salary'])
		customer_location = request.form['customer_location']
		gender = request.form['gender']

		if CreditScore not in range(300,851):
			return render_template('results.html',prediction_text='Error: Credit Score should be between 300 and 850.')

		if Tenure >= 90:
			return render_template('results.html',prediction_text='Error: Invalid tenure value.')


		if has_credit_card in ['yes','Yes','YES']:
			HasCrCard = 1
		elif has_credit_card in ['no','No','NO']:
			HasCrCard = 0
		else:
			return render_template('results.html',prediction_text='Error: Credit card value should be either Yes/No.')

		if is_active_member in ['yes','Yes','YES']:
			IsActiveMember = 1
		elif is_active_member in ['no','No','NO']:
			IsActiveMember = 0
		else:
			return render_template('results.html',prediction_text='Error: Active member value should be either Yes/No.')
		if(customer_location == 'Germany'):
			Germany = 1
			Spain= 0
			France = 0

		elif(customer_location == 'Spain'):
			Germany = 0
			Spain= 1
			France = 0

		elif(customer_location == 'France'):
			Germany = 0
			Spain= 0
			France = 1
		

		if(gender == 'Male'):
			Male = 1
			Female = 0
		elif(gender == 'Female'):
			Male = 0
			Female = 1

		prediction = model.predict([[CreditScore,
			Age,Tenure,Balance,HasCrCard,IsActiveMember,
		EstimatedSalary,Germany,Spain,Male]])
		if prediction==1:
			return render_template('results.html',prediction_text="Unfortunately, the customer will be leaving the bank.")
		else:
			return render_template('results.html',prediction_text="The customer won't be leaving the bank!")


if __name__ == '__main__':
	app.run(debug=True)