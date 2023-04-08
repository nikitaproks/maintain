<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
</script>

{#if $page.status === 404}
	<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
		<div class="max-w-md w-full space-y-8">
			<div class="text-center text-3xl font-bold py-4">Page Not Found</div>
			<div class="text-center text-lg font-medium py-4">
				The requested URL {$page.error.message} was not found on this server.
			</div>
			<div class="text-center text-lg font-medium py-4">
				<button
					type="button"
					class="bg-secondary text-primary font-medium py-2 px-4 rounded hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
					on:click={() => goto('/')}
				>
					Return to Home Page
				</button>
			</div>
		</div>
	</div>
{:else}
	<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
		<div class="max-w-md w-full space-y-8">
			<div class="text-center text-3xl font-bold py-4">Error {$page.status}</div>
			<div class="text-center text-lg font-medium py-4">{$page.error.message}</div>
			<div class="text-center text-lg font-medium py-4">
				<button
					type="button"
					class="bg-primary text-white font-medium py-2 px-4 rounded hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
					on:click={() => goto('/')}
				>
					Return to Home Page
				</button>
			</div>
		</div>
	</div>
{/if}
