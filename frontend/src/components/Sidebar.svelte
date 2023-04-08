<script>
	import { page } from '$app/stores';
	export let menuItems;

	$: activeItem = $page.url.pathname;
</script>

<div class="bg-neutral md:w-64 px-6 py-8 md:py-12 flex flex-col">
	<div class="mt-8 md:mt-0">
		<ul class="space-y-2">
			{#each menuItems as item}
				<li>
					<a
						href={item.href}
						class="btn btn-default w-full flex items-center py-2 px-4 rounded-lg transition-colors duration-200 hover:bg-primary hover:text-white {item.href ===
						activeItem
							? 'bg-primary text-white'
							: 'bg-white text-neutral'}"
					>
						<span>{item.name}</span>
					</a>
				</li>
			{/each}
		</ul>
	</div>
</div>
