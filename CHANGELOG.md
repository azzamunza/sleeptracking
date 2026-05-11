# Detailed Changelog - The Aaron Munro Diary of Sheep Counting

All notable changes to this project are documented in this file, organized by version and individual commit.

## [v1.1.0] - 2026-05-11
### Summary
Major stability update focused on mobile authentication and visual identity.

- **Commits:**
    - `646f2d9` - Update README with changelog, add new app icon, and fix mobile login bugs
- **Bug Fixes:**
    - **Reported Issue:** Login screen persists on mobile after successful sign-in.
    - **Fix:** Implemented `syncAuthUI` and immediate URL parameter detection.
    - **Fix:** Switched Service Worker to Network-First navigation to bypass stale cache.
- **Features:**
    - **App Icon:** Replaced default SVG with custom "Sheep Counting" PNG.
    - **iOS Support:** Added `apple-touch-icon` for home screen installs.

---

## [v1.0.1] - 2026-05-10
### Summary
Refining Practitioner Mode and PDF exports.

- **Commits:**
    - `06f7a6a` - Cleanup workspace
    - `27d7e44` - Update Diary title to include Aaron Munro
    - `87969e7` - Cleanup workspace
    - `06e0fe4` - Fix PDF export for Diary Notes to ensure visibility regardless of notes position
    - `c73d1e9` - Cleanup workspace
    - `bea1de3` - Move practitioner init block to ensure variables are defined and fix state order
    - `b43dd85` - Finalize practitioner mode, relocate fullscreen button, and fix PDF print scaling
    - `0939aa9` - Fix script parsing bug, restore grid columns, fix template literals
    - `5b59ef6` - Fix HTML escaping inside script tag
    - `e9fa430` - Fix JS marks template literal, implement scale-to-fit, update export layout
    - `85fa886` - Cleanup workspace scripts
    - `3f20c0b` - Ignore node_modules and cleanup scripts
    - `2a832a2` - Fix JS crash, relocate notes, and finalize collapsible sections
    - `b93deb7` - Fix duplicate export section and table rendering issues
    - `947a37c` - Update UI, collapsibles, export dialog, PDF formatting
- **Bug Fixes:**
    - Fixed JS crash caused by improper script tag nesting.
    - Resolved Template Literal syntax errors in table generation.
    - Fixed scaling issues where tables were cut off on small PDF prints.

---

## [v1.0.0] - 2026-05-09
### Summary
Thematic overhaul and Practitioner Invite system launch.

- **Commits:**
    - `e269a80` - Add Toggle Notes button and fix PDF print width formatting
    - `8c36afe` - Redesign UI to The Aaron Munro Diary of Sheep Counting theme
    - `8e33713` - Display practitioner name in header when in practitioner mode
    - `2172f0e` - Practitioner mode styling and hour log disabled states
    - `3c95507` - Enable date navigation buttons in Practitioner mode and fix Day View loading
    - `e628ab0` - Fix stray legend HTML and improve modal mobile CSS
    - `627c408` - Mass UI update: Clear Cache, Invite Modal, Reordering, Daily Summary, Practitioner Mode Styling
    - `cc76ef1` - Fix syntax error with escaped quotes in table rendering
    - `22133b4` - Fix date column width and wrapping
    - `7089883` - Format notes with carriage returns for readability in table and CSV
    - `0893eda` - Increase vertical line spacing for notes in table view
    - `c2548ae` - Update index.html
    - `2164951` - Force Service Worker to skipWaiting and claim clients to fix caching
    - `ce393e6` - Update index.html
    - `38f796b` - Fix TDZ initialization error and tighten URL cleanup for auth/invite links
    - `0b83639` - Improve table view styling for notes, date, and type columns
    - `a72ef23` - Fix ReferenceError for showingTable in practitioner mode
    - `b9dda30` - Update service worker cache to v3 for practitioner fix
    - `494193d` - Fix practitioner view layout and data sorting
    - `4bec5fc` - Add practitioner invite mode and UI
- **Features:**
    - **Practitioner Mode:** Added invite link generation and read-only view state.
    - **UI Redesign:** Implemented "Sheep Counting" color palette and typography.
    - **Daily Summary:** Added the Nightly Log summary section.

---

## [v0.9.0] - 2026-05-08
### Summary
Initial development phase and Supabase integration.

- **Commits:**
    - `7ad784e` - Add PDF export functionality and update table view title/key
    - `b7ae261` - Fix auth init race condition and URL cleanup scope
    - `8f2e487` - Update service worker cache to v2
    - `79a98d6` - Fix OAuth redirect and remove manual code exchange
    - `851ef8f` - Initial commit
- **Features:**
    - Supabase Auth (Google) and Database schema integration.
    - Basic Table View and local storage caching.
    - Initial PWA Manifest and Service Worker implementation.
