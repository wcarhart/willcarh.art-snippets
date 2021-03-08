// init dark mode
(async () => {
	let update = false
	if (localStorage.getItem('darkMode') === 'true') {
		if (!$('html').hasClass('dark-mode')) {
			update = true
		}
	} else {
		if ($('html').hasClass('dark-mode')) {
			update = true
		}
		localStorage.setItem('darkMode', 'false')
	}

	if (update === true) {
		$('html').toggleClass('dark-mode')
	}
})();

// toggle dark mode
$(document).ready(async () => {
	$('#dark-mode-toggle').click(async () => {
		if (localStorage.getItem('darkMode') === 'true') {
			localStorage.setItem('darkMode', 'false')
		} else {
			localStorage.setItem('darkMode', 'true')
		}
		$('html').toggleClass('dark-mode')
	})
})
