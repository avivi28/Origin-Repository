let pageData = 0;
let nextPage = 0;
let keyword;
let data = document.getElementById('image-data');
function connectAPI(url) {
	url = '/api/attractions?page=' + pageData.toString();
	fetch(url, {
		method: 'GET',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			nextPage = Res.nextPage;
			if (nextPage != null) {
				getImage(Res);
			}
		})
		.catch((error) => (data.innerHTML = '抱歉,沒有相關景點QQ'));
}

function getImage(Res) {
	let image = document.querySelector('.image-data');

	for (let i = 0; i < Res.data.length; i++) {
		let result = Res.data[i];
		let imageLink = result['images'][0];
		let stitle = result['name'];
		let addressData = result['address'].slice(3, 6);
		let catergoryData = result['category'];
		let id = result['id'];
		id.toString();

		let imageData = document.createElement('a');
		imageData.className = 'imageData';
		let container = document.createElement('div');
		container.className = 'image-container';
		let name = document.createElement('p');
		name.className = 'name';
		name.textContent = stitle;
		let address = document.createElement('p');
		address.className = 'address';
		address.textContent = addressData;
		let img = document.createElement('img');
		img.src = imageLink;
		let catergory = document.createElement('div');
		catergory.className = 'catergory';
		catergory.textContent = catergoryData;
		let introContainer = document.createElement('div');
		introContainer.className = 'intro-container';
		let gridContainer = document.createElement('div');
		gridContainer.className = 'grid-container';

		container.appendChild(img);
		gridContainer.appendChild(container);
		gridContainer.appendChild(name);
		introContainer.appendChild(address);
		introContainer.appendChild(catergory);
		gridContainer.appendChild(introContainer);
		image.appendChild(imageData);
		imageData.appendChild(gridContainer);

		imageData.setAttribute('href', '/attraction/' + id);
	}
}

//------keyword searching--------
let pageNumber = 0;
const myForm = document.getElementById('search-form');
myForm.addEventListener('submit', function searchKeyword(ev) {
	ev.preventDefault();
	let nextPage = 1;
	const formData = new FormData(myForm);
	const queryKeyword = new URLSearchParams(formData);
	const params = Object.fromEntries(queryKeyword.entries());
	let queryUrl =
		'/api/attractions?page=' +
		pageNumber.toString() +
		'&keyword=' +
		params.keyword.toString();
	data.textContent = '';
	observer.disconnect();
	fetch(queryUrl, {
		method: 'GET',
	})
		.then((Res) => Res.json())
		.then((Res) => {
			nextPage = Res.nextPage;
			if (nextPage != null) {
				observer.connect();
				getImage(Res);
			} else if (Res.data.length != 0) {
				getImage(Res);
			} else {
				data.innerHTML = '抱歉,沒有相關景點';
			}
		})
		.catch((error) => (data.innerHTML = '抱歉,系統出現錯誤'));
});

//-------scroll event------------
let option = {
	rootMargin: '100px',
	threshold: 0.5,
};
// 製作鈴鐺：建立一個 intersection observer，帶入相關設定資訊
let observer = new IntersectionObserver(onEnterView, option);
observer.observe(document.querySelector('footer')); // 設定觀察對象：告訴 observer 要觀察哪個目標元素
function onEnterView(entries, observer) {
	entries.forEach((entry) => {
		// entries 能拿到所有目標元素進出(intersect)變化的資訊
		if (entry.isIntersecting) {
			// 條件達成做什麼：符合設定條件下，目標進入或離開 viewport 時觸發此 callback 函式
			if (nextPage == null) {
				return;
			}
			if (!keyword) {
				connectAPI();
				pageData++;
			} else {
				searchKeyword();
				pageData++;
			}
		}
	});
}
