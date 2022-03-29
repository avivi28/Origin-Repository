let pathName = window.location.pathname;
let attractionId = pathName.split('/')[2];
let data = document.getElementById('image-data');

function connectAttractionAPI(url) {
	url = '/api/attraction/' + attractionId;
	fetch(url, {
		method: 'GET',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			getDataFromID(Res);
			showImg(indexValue);
		})
		.catch((error) => (data.innerHTML = '抱歉,出現錯誤QQ'));
}

connectAttractionAPI();

function getDataFromID(Res) {
	let result = Res.data;
	let imageData = result['images'];
	let stitle = result['name'];
	let addressData = result['address'];
	let catergoryData = result['category'];
	let descriptionData = result['description'];
	let transportData = result['transport'];
	let districtData = result['address'].slice(3, 6);

	let name = document.getElementById('attractionName');
	name.textContent = stitle;
	let planningDescription = document.getElementById('catergory');
	planningDescription.textContent = catergoryData + ' at ' + districtData;
	let description = document.getElementById('description');
	description.textContent = descriptionData;
	let address = document.getElementById('address');
	address.textContent = addressData;
	let transport = document.getElementById('transport');
	transport.textContent = transportData;

	for (let i = 0; i < imageData.length; i++) {
		let imageLink = imageData[i];
		let listContainer = document.getElementById('ul');
		let imageContainer = document.createElement('li');
		let img = document.createElement('img');
		img.src = imageLink;
		let dots = document.createElement('p');
		let dotsList = document.getElementById('dots-list');
		dots.className = 'dots';
		let j = i + 1;
		let triggerTarget = 'btm_slide(' + j + ')';
		dots.setAttribute('onclick', triggerTarget);

		imageContainer.appendChild(img);
		listContainer.appendChild(imageContainer);
		data.appendChild(listContainer);
		dotsList.appendChild(dots);
	}
}

//----------------Images-Slider-----------------
let indexValue = 1;
function btm_slide(e) {
	showImg((indexValue = e));
}
function image_slide(e) {
	showImg((indexValue += e));
}
function showImg(e) {
	let i;
	let img = document.querySelectorAll('img');
	let dots = document.querySelectorAll('.dots');
	if (e > img.length) {
		indexValue = 1;
	}
	if (e < 1) {
		indexValue = img.length;
	}
	for (i = 0; i < img.length; i++) {
		img[i].style.display = 'none';
	}
	img[indexValue - 1].style.display = 'block';

	for (i = 0; i < dots.length; i++) {
		dots[i].style = 'background:white;width: 12px;height: 12px;';
	}
	dots[indexValue - 1].style =
		'background:black; border: 1px solid #FFFFFF;width: 12px;height: 12px;';
}

///----------disable dates before tomorrow------------
let today = new Date().toISOString().split('T')[0]; // convert into ISO format-like date
document.getElementsByName('date')[0].setAttribute('min', today);

//-----------Change-Price-Function--------------
function priceChange() {
	let evening = document.getElementById('evening');
	let targetContext = document.getElementById('price-change');

	if (evening.checked == true) {
		targetContext.innerHTML = '新台幣 2500 元';
	} else {
		targetContext.innerHTML = '新台幣 2000 元';
	}
}

//-----Submit the schedule info to Booking page-----
let bookingForm = document.getElementById('bookingForm');

bookingForm.addEventListener('submit', function bookingSubmit(ev) {
	ev.preventDefault();

	let formData = new FormData(bookingForm);
	const bookingInput = new URLSearchParams(formData);
	const jsonData = Object.fromEntries(bookingInput.entries());
	let selectedTime;
	if (jsonData['button'] == 2000) {
		selectedTime = 'morning';
	} else {
		selectedTime = 'evening';
	}
	let bodyData = {
		attractionId: attractionId,
		date: jsonData['date'],
		time: selectedTime,
		price: jsonData['button'],
	};

	fetch('/api/booking', {
		method: 'POST',
		headers: new Headers({
			'Content-Type': 'application/json;charset=utf-8',
		}),
		body: JSON.stringify(bodyData),
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			console.log(Res);
		})
		.catch((error) => console.log(error));
});
