<script>
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';
</script>

<div class="app">
	<Header />
	<slot />
	<Footer />
</div>

<style>
	@import '../main.css';
</style>
