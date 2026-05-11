# Complete Repository History - The Aaron Munro Diary of Sheep Counting

This file documents every push and commit made to the repository, including internal maintenance, bug reports, and features.

---

## [May 11, 2026]
- **[89b8147]** - Align table cell content to the top
    - *Improvement:* Updated CSS to use `vertical-align: top` for all table cells in both the main app and full-screen view.
- **[9b431bc]** - Update CHANGELOG for mobile layout fix
- **[1f6ba0e]** - Fix initial full-screen width bug on mobile and force layout reflow
    - *Bug Report:* Full screen table doesn't fill width correctly on initial load in portrait mode.
    - *Fix:* Added a `fixLayout` script to the full-screen window that forces a document reflow on load.
    - *Fix:* Ensured `table-notes-bottom` is explicitly set to `display: block` in the full-screen view.
    - *Improvement:* Increased font size for notes in full-screen mode for better readability.
- **[0fa5feb]** - Update CHANGELOG for mobile viewport fix
- **[812801b]** - Switch full-screen view to scrollable layout with proper mobile viewport
    - *Bug Report:* Full screen table is tiny/unreadable and only shows when notes are present.
    - *Fix:* Replaced failing scaling logic with standard mobile-friendly scrollable container.
    - *Fix:* Added missing `viewport` meta tag to the new window.
    - *Fix:* Stripped card UI elements (buttons/headers) from the full-screen view for a cleaner data-only display.
- **[7d3e698]** - Update CHANGELOG for mobile scaling fix
- **[3110b47]** - Fix save functionality by restoring missing variable declarations and improving auth fallback
    - *Bug Report:* Adding data does not save entries.
    - *Fix:* Restored `saveTimeout` and `allData` variables which were accidentally removed in a previous cleanup.
    - *Fix:* Enhanced `saveData` with error alerts and console logging.
    - *Fix:* Improved initial session handling to ensure data loads on first visit if already authenticated.
- **[6b9211c]** - Comprehensive changelog update: synced every recorded commit from reflog
- **[7cc7755]** - Add detailed CHANGELOG with commit history and versioning
- **[646f2d9]** - Update README with changelog, add new app icon, and fix mobile login bugs
    - *Bug Report:* Mobile login screen persists after sign-in.
    - *Fix:* Unified auth UI state and updated Service Worker navigation strategy.

## [May 10, 2026]
- **[06f7a6a]** - Cleanup workspace
- **[27d7e44]** - Update Diary title to include Aaron Munro
- **[87969e7]** - Cleanup workspace
- **[06e0fe4]** - Fix PDF export for Diary Notes visibility
- **[c73d1e9]** - Cleanup workspace
- **[bea1de3]** - Move practitioner init block (state order fix)
- **[b43dd85]** - Finalize practitioner mode, relocate fullscreen button, fix PDF print scaling
- **[0939aa9]** - Fix script parsing bug, restore grid columns, fix template literals
- **[5b59ef6]** - Fix HTML escaping inside script tag
- **[e9fa430]** - Fix JS marks template literal, implement scale-to-fit, update export layout
- **[85fa886]** - Cleanup workspace scripts
- **[3f20c0b]** - Ignore node_modules and cleanup scripts
- **[2a832a2]** - Fix JS crash, relocate notes, and finalize collapsible sections
- **[b93deb7]** - Fix duplicate export section and table rendering issues
- **[947a37c]** - Update UI, collapsibles, export dialog, PDF formatting

## [May 9, 2026]
- **[e269a80]** - Add Toggle Notes button and fix PDF print width formatting
- **[8c36afe]** - Redesign UI to "The Aaron Munro Diary of Sheep Counting" theme
- **[8e33713]** - Display practitioner name in header (Practitioner Mode)
- **[2172f0e]** - Practitioner mode styling and hour log disabled states
- **[3c95507]** - Enable date navigation in Practitioner mode and fix Day View loading
- **[e628ab0]** - Fix stray legend HTML and improve modal mobile CSS
- **[627c408]** - Mass UI update: Clear Cache, Invite Modal, Reordering, Daily Summary, Practitioner Mode Styling
- **[cc76ef1]** - Fix syntax error with escaped quotes in table rendering
- **[22133b4]** - Fix date column width and wrapping
- **[7089883]** - Format notes with carriage returns for readability
- **[0893eda]** - Increase vertical line spacing for notes in table view
- **[2164951]** - Force Service Worker to skipWaiting and claim clients to fix caching
- **[38f796b]** - Fix TDZ initialization error and tighten URL cleanup
- **[0b83639]** - Improve table view styling for notes, date, and type columns
- **[a72ef23]** - Fix ReferenceError for `showingTable` in practitioner mode
- **[b9dda30]** - Update service worker cache to v3 for practitioner fix
- **[494193d]** - Fix practitioner view layout and data sorting
- **[4bec5fc]** - Add practitioner invite mode and UI

## [May 8, 2026]
- **[7ad784e]** - Add PDF export functionality and update table view title/key
- **[b7ae261]** - Fix auth init race condition and URL cleanup scope
- **[8f2e487]** - Update service worker cache to v2
- **[79a98d6]** - Fix OAuth redirect and remove manual code exchange
- **[851ef8f]** - Initial commit
