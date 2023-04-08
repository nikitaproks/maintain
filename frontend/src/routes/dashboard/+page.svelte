<script>
	import user from '../../user';
	$: isLoggedIn = $user === null ? false : true;
	$: username = isLoggedIn ? $user.email : '';
</script>

<h1>Welcome to the Dashboard, {username}! By now there is no info</h1>
