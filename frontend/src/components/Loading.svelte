<script>
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let isLoading = true;

	onMount(() => {
		setTimeout(() => {
			isLoading = false;
			dispatch('loaded');
		}, 3000);
	});
</script>

{#if isLoading}
	<div class="fixed inset-0 z-50 flex items-center justify-center">
		<div class="relative">
			<div class="inline-flex rounded-full">
				<div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-gray-900" />
			</div>
		</div>
	</div>
{/if}

<style>
	.animate-spin {
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}

		100% {
			transform: rotate(360deg);
		}
	}
</style>
