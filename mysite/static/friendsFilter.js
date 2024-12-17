
document.addEventListener("DOMContentLoaded", () => {
	document.getElementById('searchBar').addEventListener('input', function() {
		let searchTerm = this.value.toLowerCase();
		let friends = document.querySelectorAll('.friend-item');

		friends.forEach(function(friend) {
			let spanText = friend.querySelector('span').textContent.toLowerCase();
			if (spanText.includes(searchTerm)) {
				friend.style.display = 'block';
			} else {
				friend.style.display = 'none';
			}
		});
	});
});
