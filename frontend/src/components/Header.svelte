<!-- src/components/Header.svelte -->
<script>
	import { goto } from '$app/navigation';
	import user from '../user';

	$: isLoggedIn = $user === null ? false : true;

	function handleLogout() {
		document.cookie = 'Authorization=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
		user.update((val) => (val = null));
		goto('/login');
	}
</script>

<header class="bg-secondary text-primary py-4">
	<div class="container mx-auto flex justify-between items-center px-4">
		<div class="font-bold text-xl"><a href="/">Qwello Maintainance</a></div>
		{#if isLoggedIn}
			<nav class="space-x-6">
				<a href="/dashboard" class="hover:text-white">Dashboard</a>
				<button on:click={handleLogout} class="hover:text-white"> Logout </button>
			</nav>
		{:else if !isLoggedIn}
			<nav class="space-x-6">
				<a href="/register" class="hover:text-white">Register</a>
				<a href="/login" class="hover:text-white">Login</a>
			</nav>
		{:else}
			Loading...
		{/if}
	</div>
</header>
