# Adding Naoberry's photos

Drop her photos into this folder with these exact filenames and they will
appear on the site automatically — no code changes needed:

| Filename       | Where it shows            | What to pick                              |
| -------------- | ------------------------- | ----------------------------------------- |
| `hero.jpg`     | Big hero image (top)      | Her strongest bridal shot (portrait)      |
| `naomi.jpg`    | "The Artist" section      | A photo of Naomi herself                  |
| `class.jpg`    | Makeup classes section    | A training/class photo                    |
| `logo.jpg`     | Phone home-screen icon    | Her logo / profile picture (square)       |
| `student-01.jpg` → `student-04.jpg` | Certified Students section | Graduates holding their certificates |
| `collection-01.jpg`, `collection-02.jpg` | Gallery ("Studio" filter) | Makeup shelf + full collection |
| `work-13.jpg` | Gallery (Bridal) | The new wedding photo |
| `work-15.jpg` → `work-19.jpg` | Gallery (Glam) | The 5 new beauty makeup photos |
| `work-01.jpg` → `work-12.jpg` … | Portfolio gallery | Her best looks, best first (add as many as you want — see below) |
| `product-01.jpg` → `product-10.jpg` | The Beauty Bar (shop) | Square shots of her 10 products |

Gallery categories (set in `js/main.js`, edit freely):

- `work-01`, `work-02`, `work-09`, `work-12` → **Bridal**
- `work-03`, `work-07`, `work-11` → **Owanbe / gele**
- `work-04`, `work-08`, `work-10` → **Glam / birthday**
- `work-05`, `work-06` → **Before / After** pair

To add MORE than 12: copy any line in the `WORKS` list in `js/main.js`,
change the filename (e.g. `work-13.jpg`), set its category (`bridal`,
`owanbe`, `glam`, `transform`), caption and shape (`ar`: `4/5`, `3/4` or
`1/1`), and drop the matching photo here. The gallery shows the first 12
and puts the rest behind a "Show more looks" button, so the page stays
fast no matter how many you add. Order the list best-first — the first
12 are the storefront.

Products: no names or prices needed — just drop the 10 photos in as
`product-01.jpg` … `product-10.jpg`. Each card shows the photo with a
number (№ 01 …) and a "DM for price" button that opens WhatsApp quoting
that number, so Naomi knows which product the customer means. If the
product count changes, edit `PRODUCT_COUNT` at the top of `js/main.js`.

After the site goes live, set `SITE_URL` at the top of `js/main.js` to the
live address — enquiry messages will then include a direct link to the
product photo instead of the number (WhatsApp shows a preview of it).

## How to get the photos off Instagram

Best quality options, in order:

1. **Original files** — Naomi sends the original photos from her phone/camera
   roll (best quality, no compression).
2. **Instagram export** — on her account: *Settings → Accounts Centre → Your
   information and permissions → Download your information*. Instagram emails
   a zip of every photo she has posted.
3. For each gallery photo, paste the real Instagram post URL into the `link`
   field in `js/main.js` so "View on Instagram" opens the exact post.

Tips:
- Portrait orientation works best (the grid handles any shape).
- Keep files under ~500 KB each for fast loading — https://squoosh.app
  is a free compressor.
- JPG format, or rename the entries in `js/main.js` if using .png/.webp.
