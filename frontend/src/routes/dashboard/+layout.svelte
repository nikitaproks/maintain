<script>
	import user from '../../user';
	import { onMount } from 'svelte';
	import Sidebar from '../../components/Sidebar.svelte';
	export let data;

	const menuItems = [
		{ name: 'Tickets', icon: 'TicketIcon', href: '/dashboard/tickets' },
		{ name: 'Tasks', icon: 'TaskIcon', href: '/dashboard/tasks' }
	];

	onMount(() => {
		user.update((val) => (val = data.authData));
	});
</script>

<div class="min-h-screen flex flex-col md:flex-row">
	<Sidebar {menuItems} />
	<div class="flex-1 px-4 py-8">
		<slot />
	</div>
</div>
