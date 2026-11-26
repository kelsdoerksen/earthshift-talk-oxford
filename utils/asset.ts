// Prefix a public/ path with the site's base URL, so images load both in `npm run dev` (base "/")
// and when the deck is hosted under a sub-path (e.g. https://<user>.github.io/earthshift-talk/).
// Use for every file in public/: asset('/tiles/x.png'). External and data: URLs pass through.
export function asset(path: string): string {
  if (/^(https?:|data:|blob:)/.test(path)) return path
  return import.meta.env.BASE_URL.replace(/\/$/, '') + '/' + path.replace(/^\//, '')
}
