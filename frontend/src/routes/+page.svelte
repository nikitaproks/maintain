<script>
	import Loading from '../components/Loading.svelte';
	import user from '../user';
	import { onMount } from 'svelte';
	export let data;

	$: isLoggedIn = $user === null ? false : true;
	$: username = isLoggedIn ? $user.email : '';

	onMount(() => {
		user.update((val) => (val = data.authData));
	});
</script>

<div class="min-h-screen flex items-center justify-center">
	<div class="w-full sm:w-3/4 lg:w-1/2 xl:w-1/3 p-4">
		{#if isLoggedIn}
			<div class="card shadow-xl bg-secondary">
				<div class="card-body">
					<h2 class="text-2xl font-semibold mb-6 text-center text-primary">Welcome, {username}!</h2>
					<p class="text-white">
						This is a simple and clean welcome page after the user logs in. You can add personalized
						content and features for the user here.
					</p>
				</div>
			</div>
		{:else}
			<Loading />
		{/if}
	</div>
</div>
