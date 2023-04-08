<script>
	export let ticket;

	function getStatusClass(status) {
		if (status === 'open') {
			return 'text-green-600';
		} else if (status === 'in progress') {
			return 'text-yellow-600';
		} else if (status === 'closed') {
			return 'text-red-600';
		} else {
			return 'text-gray-600';
		}
	}
</script>

<div class="ticket-box">
	<div>
		<h2 class="ticket-title">{ticket.name}</h2>
		<!-- <p class="ticket-description">{ticket.description}</p> -->
	</div>
	<p class="ticket-status {getStatusClass(ticket.status)}">Status: {ticket.status}</p>
</div>

<style>
	.ticket-box {
		@apply p-6 rounded-lg shadow-md bg-white mb-6 flex flex-col md:flex-row md:items-start md:justify-between;
	}

	.ticket-title {
		@apply text-xl font-semibold mb-2 md:mb-0;
	}

	.ticket-description {
		@apply text-base text-gray-600 mb-4;
	}

	.ticket-status {
		@apply text-base font-medium;
	}
</style>
