function prettierCreditCardInput() {
	// this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');
	// return this.value.replace(
	// 	value.replace(/\W/gi, '').replace(/(.{4})/g, '$1 ')
	// );
}

const bookingAPIUrl = '/api/booking';
let bookingBody = document.getElementById('entire_information');
let footer = document.querySelector('footer');

function getBookingAPI() {
	fetch(bookingAPIUrl, {
		method: 'GET',
		credentials: 'same-origin', //for bring cookies
	})
		.then((Res) => Res.json())
		.then((Res) => {
			const getData = Res['data'];
			const errorData = Res['error'];
			if (getData == null) {
				bookingBody.textContent = '目前沒有任何待預訂的行程';
				bookingBody.style = 'margin: 35px 0px 40px';
				footer.style = 'padding-bottom: 806px';
			} else {
				console.log(Res);
			}
		})
		.catch((error) => console.log(error));
}
