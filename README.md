# The Aaron Munro Diary of Sheep Counting

A practical and structured Progressive Web App (PWA) designed for tracking sleep patterns, medications, and daily habits. Built for the modern user, it provides a clean interface for nightly logging and practitioner review.

## Features

- **Quick Entry:** One-tap logging for common events (Coffee, Meds, Alcohol, Exercise, Bed, Asleep).
- **Daily Summary:** Visual nightly log summaries to track trends at a glance.
- **Table & Export:** Comprehensive table view with CSV, JSON, and PDF export capabilities.
- **Practitioner Mode:** Secure invite-based system to allow healthcare practitioners to view your sleep data without edit permissions.
- **PWA Ready:** Installable on iOS and Android with offline support via Service Workers.
- **Themed UI:** Custom "Sheep Counting" aesthetic with a dark-mode first design.

## Tech Stack

- **Frontend:** HTML5, CSS3 (Custom Variables), Vanilla JavaScript.
- **Backend/Auth:** Supabase (PostgreSQL + GoTrue).
- **Service Worker:** Custom implementation for offline caching and PWA functionality.

---

## Changelog

### v1.1.0 - 2026-05-11
- **Feature:** Implemented new custom app icon with "The Aaron Munro Diary of Sheep Counting" branding.
- **Bugfix:** Resolved intermittent mobile login failures by implementing a Network-First navigation strategy in the Service Worker.
- **Improvement:** Unified Auth UI synchronization logic to prevent the login screen from persisting after successful authentication.
- **PWA:** Added `apple-touch-icon` support for improved iOS home screen integration.

### v1.0.1 - 2026-05-10
- **Feature:** Finalized Practitioner Mode with secure read-only access.
- **Improvement:** Added "Scale-to-fit" logic for large data tables on mobile devices.
- **Bugfix:** Fixed PDF export visibility issues for diary notes.
- **Bugfix:** Resolved template literal parsing errors in table rendering.
- **UI:** Added collapsible sections (Quick Entry, Nightly Log) to reduce cognitive load.

### v1.0.0 - 2026-05-09
- **Launch:** Redesigned UI to "The Aaron Munro Diary of Sheep Counting" theme.
- **Feature:** Added Daily Summary view.
- **Feature:** Implemented Practitioner invite system.
- **Feature:** Added CSV and JSON export options.
- **Bugfix:** Fixed Temporal Dead Zone (TDZ) initialization errors.
- **Performance:** Optimized Service Worker caching (v3).

### v0.9.0 - 2026-05-08
- **Feature:** Initial Supabase integration (Auth & Database).
- **Feature:** Basic PDF export functionality.
- **Feature:** PWA manifest and initial Service Worker (v1/v2).
- **Initial Release:** Core tracking functionality established.
