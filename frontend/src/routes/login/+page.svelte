<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import user from '../../user';

	$: isLoggedIn = $user === null ? false : true;
	onMount(() => {
		if (isLoggedIn) goto('/');
	});

	let username = '';
	let password = '';
	let errorMessage = '';

	async function handleSubmit(event) {
		event.preventDefault();

		const formData = new URLSearchParams({
			username: username,
			password: password
		});

		const response = await fetch('/api/v1/auth/access-token', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: formData
		});

		if (response.ok) {
			const token = await response.json();
			// document.cookie = `access_token=${token.access_token}; expires=${new Date(token.exp * 1000)}; path=/; Secure; HttpOnly`;
			// document.cookie = `Authorization=Bearer ${token.access_token}; path=/; Secure; HttpOnly`;
			document.cookie = `Authorization=Bearer ${token.access_token}; expires=${new Date(
				token.exp * 1000
			)}; path=/;`;
			window.location.href = '/dashboard/';
			user.update((val) => (val = { ...token }));
		} else {
			errorMessage = await response.text();
			console.log(errorMessage);
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8 p-8 bg-secondary text-primary shadow-md rounded-lg">
		<div class="text-center text-3xl font-bold py-4">Login</div>
		<form class="mt-8 space-y-6" on:submit={handleSubmit}>
			<input type="hidden" name="remember" value="true" />
			<div class="rounded-md shadow-sm -space-y-px">
				<div class="form-control">
					<label for="email" class="block font-bold mb-2">Email address</label>
					<input
						type="email"
						id="email"
						name="email"
						bind:value={username}
						class="w-full px-3 py-2 leading-tight border rounded appearance-none focus:outline-none focus:shadow-outline "
						required
					/>
				</div>

				<div class="form-control">
					<label for="password" class="block font-bold mb-2">Password</label>
					<input
						type="password"
						id="password"
						name="password"
						bind:value={password}
						class="w-full px-3 py-2 leading-tight border rounded appearance-none focus:outline-none focus:shadow-outline"
						required
					/>
				</div>
			</div>

			<div class="flex items-center justify-between">
				<div class="form-checkbox form-switch">
					<input type="checkbox" id="remember_me" name="remember_me" class="form-input" />
					<label for="remember_me" class="form-label">Remember me</label>
				</div>

				<div class="text-sm">
					<a href="/" class="font-medium text-primary hover:text-white"> Forgot your password? </a>
				</div>
			</div>

			<div>
				<button type="submit" class="btn btn-primary btn-block">
					<span class="mx-auto"> Sign in </span>
				</button>
			</div>
			{errorMessage}
		</form>
	</div>
</div>
