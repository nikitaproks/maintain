<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import TicketInList from './TicketInList.svelte';

	let tickets = [];
	let searchTerm = '';
	let filteredTickets = [];

	onMount(async () => {
		const response = await fetch('/api/v1/tickets');
		tickets = await response.json();
		console.log(tickets);
	});

	$: filteredTickets = tickets.filter((ticket) => {
		if (!searchTerm) return true;

		const searchRegex = new RegExp(searchTerm, 'i');
		return (
			searchRegex.test(ticket.name) ||
			searchRegex.test(ticket.status) ||
			searchRegex.test(ticket.description)
		);
	});

	function navigateToTicket(ticketId) {
		goto(`/dashboard/tickets/${ticketId}`);
	}
</script>

<div>
	<input
		type="text"
		bind:value={searchTerm}
		placeholder="Search for tickets..."
		class="search-input"
	/>
	{#each filteredTickets as ticket}
		<div class="ticket-box cursor-pointer" on:click={() => navigateToTicket(ticket.id)}>
			<TicketInList {ticket} />
		</div>
	{/each}
</div>

<style>
	.search-input {
		@apply bg-white w-full mb-6 px-4 py-2 border border-gray-300 rounded-lg focus:border-primary focus:outline-none;
	}
</style>
