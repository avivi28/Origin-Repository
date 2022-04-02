function checkDigit(event) {
	let code = event.which ? event.which : event.keyCode;
	if ((code < 48 || code > 57) && code > 31) {
		return false; //cannot enter a-z
	}
	return true;
}

let creditCardNumber = document.getElementById('creditCard_number');
creditCardNumber.addEventListener('keydown', function (e) {
	// console.log(e.keyCode);
	if (e.keyCode !== 8) {
		//8: backspace
		console.log(this.value.length);
		if (
			this.value.length === 4 ||
			this.value.length === 9 ||
			this.value.length === 14
		) {
			this.value = this.value += ' ';
		}
	}
});

//---------Verify the user status------
let bookingCookie = document.cookie;

function verifyUser() {
	if (bookingCookie == '') {
		location.href = '/';
	}
}

verifyUser();

//---------Get Planned Info from API-------
const bookingAPIUrl = '/api/booking';
let bookingBody = document.getElementById('entire_information');
let footer = document.querySelector('footer');

function getBookingAPI() {
	fetch(bookingAPIUrl, {
		method: 'GET',
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			const getData = Res['data'];
			if (getData == null) {
				bookingBody.textContent = '目前沒有任何待預訂的行程';
				bookingBody.style = 'margin: 35px 0px 40px';
				footer.style = 'padding-bottom: 806px';
			} else {
				function Timer() {
					setTimeout(showLoading, 1000);
				}
				Timer();
				showData(Res);
				showUserDate();
			}
		})
		.catch((error) => console.log(error));
}

getBookingAPI();

//------------show the data after connected get API------------
function showData(Res) {
	const returnData = Res['data'];
	let attractionData = returnData['attraction'];

	let attractionImage = document.getElementById('attraction_image');
	attractionImage.src = attractionData['image'];
	attractionImage.className = 'informationContainer_selectedAttractionImg';

	let attractionName = document.getElementById('attraction_name');
	attractionName.textContent = '台北一日遊：' + attractionData['name'];

	let selectedDate = document.getElementById('selected_date');
	inputDate = returnData['date'];
	let newDate = new Date(inputDate);
	convertedDate = newDate.toISOString().split('T')[0];
	selectedDate.textContent = convertedDate;

	let selectedTime = document.getElementById('selected_time');
	selectedTime.textContent = returnData['time'];

	let selectedFee = document.getElementById('selected_fee');
	priceData = returnData['price'];
	selectedFee.textContent = priceData;

	let selectedPlace = document.getElementById('selected_place');
	selectedPlace.textContent = attractionData['address'];

	let totalPrice = document.getElementById('total_price');
	totalPrice.textContent = '總價：新台幣 ' + priceData + ' 元';
}

//----------get User info from JWT------------
let base64Url = bookingCookie.split('.')[1];
let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
let jsonPayload = decodeURIComponent(
	atob(base64)
		.split('')
		.map(function (c) {
			return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
		})
		.join('')
);
let userData = JSON.parse(jsonPayload);

let titleName = document.getElementById('title_username');
userName = userData['name'];
userEmail = userData['email'];
titleName.textContent = '您好，' + userName + '，待預訂的行程如下：';

//----------show User info by using data in JWT-------
function showUserDate() {
	let contactName = document.getElementById('contact_name');
	contactName.setAttribute('value', userName);
	let contactEmail = document.getElementById('contact_email');
	contactEmail.setAttribute('value', userEmail);
}

//-----------delete the selected booking--------------
function deleteBooking() {
	fetch(bookingAPIUrl, {
		method: 'DELETE',
		credentials: 'same-origin',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			deleteData = Res['ok'];
			if (deleteData == true) {
				location.reload();
			}
		})
		.catch((error) => console.log(error));
}

//--------loading effect-----------
let loadingImage = document.getElementById('loader');

function showLoading() {
	document.getElementById('loader').style.display = 'none';
	document.getElementById('attraction_image').style.display = 'block';
}
