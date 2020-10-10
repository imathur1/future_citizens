import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x1400")
chrome_driver = os.path.join(os.getcwd(), "chromedriver")

driver = webdriver.Chrome(
	chrome_options=chrome_options, executable_path=chrome_driver)
driver.get("https://egov.uscis.gov/processing-times/home")


def getFormsAndOffices():
	js = """
	function getOffices(myOffices, formsArray, index) {
		if (index === formsArray.length) {
			document.body.innerHTML += "<div id='myOffices'>" + myOffices + "</div>";
			return;
		} else {
			axios({
				method: "GET",
				url: "./api/formoffices/" + formsArray[index]
			}).then(function(response) {
				let offices = "";
				for (let i = 0; i < response.data.data.form_offices.offices.length; i++) {
					offices += response.data.data.form_offices.offices[i].office_code + "%22" + \
						response.data.data.form_offices.offices[i].office_description + "%21";
				}
				getOffices(myOffices + offices + "%20", formsArray, index + 1);
			});
		}
	}

	axios({
		method: "GET",
		url: "./api/forms"
	}).then(function(response) {
		let myForms = "";
		let formsArray = [];
		for (let i = 0; i < response.data.data.forms.forms.length; i++) {
			myForms += response.data.data.forms.forms[i].form_name + "%21" + \
				response.data.data.forms.forms[i].form_description_en + "%20";
			formsArray.push(response.data.data.forms.forms[i].form_name);
		}
		document.body.innerHTML += "<div id='myForms'>" + myForms + "</div>";
		getOffices("", formsArray, 0);
	});
	"""

	driver.execute_script(js)
	time.sleep(15)
	forms_data = driver.find_element_by_id("myForms").text.split("%20")
	offices_data = driver.find_element_by_id("myOffices").text.split("%20")
	forms = []
	offices = []
	for i in forms_data:
		forms.append(i.split("%21"))
	for i in offices_data:
		office = []
		for j in i.split("%21"):
			office.append(j.split("%22"))
		del office[-1]
		offices.append(office)
	del forms[-1]
	del offices[-1]

	with open('forms', 'wb') as f:
		pickle.dump(forms, f)
	with open("offices", "wb") as f:
		pickle.dump(offices, f)

def getEstimatedTimes(form, office):
	js = """
	axios({
		method: 'GET',
		url: './api/processingtime/""" + form + "/" + office + """'
	}).then(function (response) {
		let range = "";
		if (response.data.data.processing_time.range !== null) {
			range = response.data.data.processing_time.range[1].value + "%21" + response.data.data.processing_time.range[1].unit + "%21" + response.data.data.processing_time.range[0].value + "%21" + response.data.data.processing_time.range[0].unit;
		}
		let subtypes = "";
		if (response.data.data.processing_time.subtypes !== null) {
			for (let i = 0; i < response.data.data.processing_time.subtypes.length; i++) {
				subtypes += response.data.data.processing_time.subtypes[i].form_type + "%21" + response.data.data.processing_time.subtypes[i].publication_date + "%21" + response.data.data.processing_time.subtypes[i].service_request_date + \
					"%21" + response.data.data.processing_time.subtypes[i].subtype_info_en + "%21" + \
						response.data.data.processing_time.subtypes[i].range[1].value + "%21" + response.data.data.processing_time.subtypes[i].range[1].unit + "%21" + \
							response.data.data.processing_time.subtypes[i].range[0].value + "%21" + response.data.data.processing_time.subtypes[i].range[0].unit + "%20";
			}
		}
		if (document.getElementById('myRange') !== null){
			document.getElementById('myRange').remove();
		}
		if (document.getElementById('mySubtypes') !== null){
			document.getElementById('mySubtypes').remove();
		}		
		document.body.innerHTML += "<div id='myRange'>" + range + "</div>";
		document.body.innerHTML += "<div id='mySubtypes'>" + subtypes + "</div>";
	});
	"""

	driver.execute_script(js)
	time.sleep(2)
	ranges_data = driver.find_element_by_id("myRange").text
	subtypes_data = driver.find_element_by_id("mySubtypes").text.split("%20")
	ranges = ranges_data.split("%21")
	subtypes = []
	for i in subtypes_data:
		if i.split("%21") != [""]:
			subtypes.append(i.split("%21"))
	return [ranges, subtypes]

def getAllEstimations():
	forms = []
	with open('forms', 'rb') as f:
		forms = pickle.load(f)

	offices = []
	with open('offices', 'rb') as f:
		offices = pickle.load(f)

	estimations = dict()
	for i in range(len(forms)):
		try:
			for j in offices[i]:
				data = getEstimatedTimes(forms[i][0], j[0])
				estimations[forms[i][0] + "%21" + j[0]] = data
		except Exception as e:
			print(e)
			break

	with open("estimations", "wb") as f:
		pickle.dump(estimations, f)

if __name__ == '__main__':
	# getFormsAndOffices()
	# getAllEstimations()
	driver.close()
