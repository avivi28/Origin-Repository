const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries()); //get query string

const orderNumber = params['number'];

const orderPlaceholder = document.getElementById('order_number');
orderPlaceholder.textContent = '訂單編號： ' + orderNumber;

function backHome() {
	location.href = '/';
}
