 // Adiciona um evento de clique a todos os elementos <li> com a classe 'config-item'
document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll('.clickable-item').forEach(item => {
		item.addEventListener('click', event => {
			// Verifica se o <li> contém um link
			const link = item.querySelector('a');
			if (link) {
				// Simula o clique no link
				link.click();
			}
		});
	});
});
