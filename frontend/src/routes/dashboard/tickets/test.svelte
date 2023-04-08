<script>
	import { goto } from '$app/navigation';

	function goBack() {
		goto('/dashboard/tickets');
	}
</script>

<h1>Test Route</h1>
<button on:click={goBack}>Go back to tickets list</button>
