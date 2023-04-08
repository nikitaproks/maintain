const manifest = {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png","robots.txt"]),
	mimeTypes: {".png":"image/png",".txt":"text/plain"},
	_: {
		client: {"start":{"file":"_app/immutable/entry/start.53de2c0d.js","imports":["_app/immutable/entry/start.53de2c0d.js","_app/immutable/chunks/index.33f1777b.js","_app/immutable/chunks/singletons.26b0b33e.js","_app/immutable/chunks/index.cca47b0a.js","_app/immutable/chunks/parse.d12b0d5b.js"],"stylesheets":[],"fonts":[]},"app":{"file":"_app/immutable/entry/app.a648e05b.js","imports":["_app/immutable/entry/app.a648e05b.js","_app/immutable/chunks/index.33f1777b.js"],"stylesheets":[],"fonts":[]}},
		nodes: [
			() => import('./chunks/0-d0b986ee.js'),
			() => import('./chunks/1-b19ce905.js'),
			() => import('./chunks/2-d9d0218e.js'),
			() => import('./chunks/3-a3e807ba.js'),
			() => import('./chunks/4-a162b189.js'),
			() => import('./chunks/5-e13508b2.js')
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0], errors: [1], leaf: 2 },
				endpoint: null
			},
			{
				id: "/about",
				pattern: /^\/about\/?$/,
				params: [],
				page: { layouts: [0], errors: [1], leaf: 3 },
				endpoint: null
			},
			{
				id: "/sverdle",
				pattern: /^\/sverdle\/?$/,
				params: [],
				page: { layouts: [0], errors: [1], leaf: 4 },
				endpoint: null
			},
			{
				id: "/sverdle/how-to-play",
				pattern: /^\/sverdle\/how-to-play\/?$/,
				params: [],
				page: { layouts: [0], errors: [1], leaf: 5 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		}
	}
};

const prerendered = new Set(["/","/about","/sverdle/how-to-play"]);

export { manifest, prerendered };
//# sourceMappingURL=manifest.js.map
