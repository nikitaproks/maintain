<script context="module">
	export async function load({ params }) {
		const response = await fetch(`/api/v1/tickets/${params.id}`);
		const ticket = await response.json();

		return {
			props: {
				ticket
			}
		};
	}
</script>

<script>
	import { goto } from '$app/navigation';

	export let ticket;

	function goBack() {
		goto('/dashboard/tickets');
	}
</script>

<div>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		class="w-6 h-6 back-arrow"
		fill="none"
		viewBox="0 0 24 24"
		stroke="currentColor"
		on:click={goBack}
	>
		<path
			strokeLinecap="round"
			strokeLinejoin="round"
			strokeWidth={2}
			d="M10 19l-7-7m0 0l7-7m-7 7h18"
		/>
	</svg>

	<div class="ticket-box">
		<h2 class="ticket-title">{ticket.name}</h2>
		<p class="ticket-description">{ticket.description}</p>
		<p class="ticket-status">Status: {ticket.status}</p>
	</div>
</div>

<style>
	.back-arrow {
		@apply cursor-pointer text-primary mb-4;
	}

	.ticket-box {
		@apply p-6 rounded-lg shadow-md bg-white;
	}

	.ticket-title {
		@apply text-2xl font-semibold mb-4;
	}

	.ticket-description {
		@apply text-base text-gray-600 mb-4;
	}

	.ticket-status {
		@apply text-base font-medium;
	}
</style>
