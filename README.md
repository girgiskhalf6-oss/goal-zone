# GOAL ZONE
Bilingual (English/Arabic, RTL) football fan site. Plain HTML/CSS/JS, no build step, no API keys.

## What changed in v3
New generated player portraits and unique team, story and hero artwork (all original SVG, no third-party photos). Larger mobile text, always-visible mobile search, corrected RTL for matches and hero.

## Run
`index.html` is a self-contained build (CSS, JS and favicon are inlined), so it works even if opened on its own, e.g. from a phone file manager. Always extract the ZIP first; do not open files from inside the ZIP preview.
To edit, change files in `css/` and `js/` (or `index.template.html`) and run `python3 build.py` to regenerate `index.html`.

Open `index.html` in a browser, or serve the folder: `python3 -m http.server 8000` then visit http://localhost:8000

## Publish
Upload the whole folder to any static host (Netlify, Vercel, GitHub Pages, Cloudflare Pages). Then replace `YOUR-DOMAIN` in `index.html`, `sitemap.xml`, `robots.txt`.
For social previews, convert `assets/og.svg` to a 1200x630 PNG and point `og:image` to it (most networks ignore SVG).

## Content
All clubs, players, news and matches in `js/data.js` are **fictional demonstration data** with original generated SVG art (no real logos or photos). Edit that file, or replace it with your own data.

## Connecting a real data API
Never put secret keys in front-end code. Create a small server or serverless function (Netlify/Cloudflare/Vercel) that holds the key in an environment variable, calls the provider, and returns JSON. Then in `js/app.js` replace the static `D` arrays with `fetch('/api/matches')`. Pages already show loading and error states.

## Notes
Routing uses `#/` hashes so it works on any static host. Favorites, votes, quiz language and posts are stored in the visitor's browser (localStorage) only. Fan Zone posts are local and not shared between visitors; a real community needs a moderated backend.

## User accounts (Supabase): step-by-step setup
Accounts use **Supabase** (real authentication + Postgres database). Until you complete these steps the site runs normally, but Sign up / Log in show a clear "not set up" notice and are disabled. Nothing is faked.

1. Create a free project at https://supabase.com (Dashboard > New project). Save the database password somewhere safe; this site never needs it.
2. Open **SQL Editor > New query**, paste the whole of `supabase/schema.sql`, click **Run**. This creates the `profiles` table, turns on Row Level Security (each user can read/write only their own row) and adds a trigger that creates a profile at sign-up.
3. Open **Authentication > Sign In / Providers > Email**: keep Email enabled. Set minimum password length to 8. Choose whether to keep **Confirm email** on (recommended for production; the site handles both).
4. Open **Authentication > URL Configuration**: set **Site URL** to your published address (for local testing use `http://localhost:8000`) and add the same address under **Redirect URLs**. Email confirmation and password-reset links return there.
5. Open **Project Settings > API**. Copy the **Project URL** and the **anon public** key into `js/config.js`:
   `SUPABASE_URL:"https://xxxx.supabase.co", SUPABASE_ANON_KEY:"eyJ..."`
   Never paste the `service_role` key anywhere in this project. The anon key is meant to be public; the Row Level Security rules from step 2 are what protect user data.
6. Test locally: run `python3 -m http.server 8000` in the project folder, open http://localhost:8000, create an account, refresh (you stay signed in), edit your profile, log out and log in again. Check **Authentication > Users** and **Table Editor > profiles** in Supabase to see the data.
7. Publish: upload the folder (including your edited `js/config.js`) to your static host. `index.html` inlines the app code but deliberately **not** `js/config.js`, so keep that file next to it. Add your live address to Supabase Redirect URLs (step 4).
8. Production email: Supabase's built-in email sender is rate-limited. Under **Authentication > SMTP Settings** connect your own provider (Resend, SendGrid, etc.) before launch.

### What is stored and how it is protected
- Collected: username, email, avatar choice, favorite team (plus the favorites/saved-article lists you create). Nothing else.
- Passwords are sent over HTTPS to Supabase Auth and stored only as a salted hash there. This site never stores or logs them.
- The browser keeps a session token (localStorage if "Remember me" is ticked, otherwise sessionStorage). Logging out removes it and clears cached favorites.
- All user text is escaped before display. Profiles are private: other users cannot read them.
- Not included (needs a server): account deletion by the user, and abuse moderation for a shared community.
Using Firebase instead? Replace `js/auth.js` (the only file that talks to the backend) with Firebase Auth + Firestore calls exposing the same `GZAuth` methods.
