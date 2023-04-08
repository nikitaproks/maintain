<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import user from '../../user';

	$: isLoggedIn = $user === null ? false : true;
	onMount(() => {
		//if (isLoggedIn) goto('/');
	});

	let name = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let errorMessage = '';

	async function handleSubmit(event) {
		event.preventDefault();

		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match';
			return;
		}

		const formData = new URLSearchParams({
			name: name,
			email: email,
			password: password
		});

		const response = await fetch('/api/v1/auth/register', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: formData
		});

		if (response.ok) {
			goto('/login');
		} else {
			errorMessage = await response.text();
			console.log(errorMessage);
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8 p-8 bg-secondary text-primary shadow-md rounded-lg">
		<div class="text-center text-3xl font-bold py-4">Register</div>
		<form class="mt-8 space-y-6" on:submit={handleSubmit}>
			<input type="hidden" name="remember" value="true" />
			<div class="rounded-md shadow-sm -space-y-px">
				<div class="form-control">
					<label for="name" class="block font-bold mb-2">Name*</label>
					<input
						type="text"
						id="name"
						name="name"
						bind:value={name}
						class="w-full px-3 py-2 leading-tight border rounded appearance-none focus:outline-none focus:shadow-outline "
						required
					/>
				</div>

				<div class="form-control">
					<label for="email" class="block font-bold mb-2">Email address*</label>
					<input
						type="email"
						id="email"
						name="email"
						bind:value={email}
						class="w-full px-3 py-2 leading-tight border rounded appearance-none focus:outline-none focus:shadow-outline "
						required
					/>
				</div>

				<div class="form-control">
					<label for="password" class="block font-bold mb-2">Password*</label>
					<input
						type="password"
						id="password"
						name="password"
						bind:value={password}
						class="w-full px-3 py-2 leading-tight border rounded appearance-none focus:outline-none focus:shadow-outline"
						required
					/>
				</div>

				<div class="form-control">
					<label for="confirm-password" class="block font-bold mb-2">Confirm Password*</label>
					<input
						type="password"
						id="confirm-password"
						name="confirm-password"
						bind:value={confirmPassword}
						class="w-full px-3 py-2 leading-tight border rounded appearance-none focus:outline-none focus:shadow-outline"
						required
					/>
				</div>
			</div>
			<p class="text-sm mt-2">
				Fields marked with <span class="required">*</span> are required.
			</p>

			<div>
				<button type="submit" class="btn btn-primary btn-block">
					<span class="mx-auto"> Register </span>
				</button>
			</div>
			{errorMessage}
		</form>
	</div>
</div>
