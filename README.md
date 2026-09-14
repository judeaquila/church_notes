# Notes Hub 📝

Notes Hub is a full-featured web application built with **Django**, **Tailwind CSS**, and **Alpine.js**. I built it to enable me to create, categorize, and manage personal Church notes and service records alongside media attachments, featuring fast interactive in-note text searching and an integrated in-page lightbox gallery.

---

## Key Features

- **Categorized Note Management:** Organize notes by customizable categories with custom color badges and service dates.
- **In-Note Live Search:** Highlighting search query matches in real-time with next/previous stepping controls and automatic view scrolling.
- **Attachment Gallery & Lightbox:** Upload images and document attachments. Click any image attachment to launch an interactive, in-page full-screen image slider with keyboard navigation (`Left`, `Right`, `Escape`).
- **Captions & Metadata:** Display custom attachment captions, timestamps, and file details seamlessly.
- **Responsive & Modern UI:** Designed with mobile-first Tailwind CSS components and lightweight Alpine.js interactivity.

---

## Tech Stack

- **Backend:** Python 3.13.5, Django 6.1.1
- **Frontend:** HTML5, Tailwind CSS v4, Alpine.js
- **Database:** SQLite (default / development)
- **Icons & Visuals:** Heroicons (SVG)

---

## Prerequisites

Ensure you have the following installed locally:

- Python 3.10+
- `pip` (Python package installer)
- `node` & `npm` (if compiling Tailwind CSS assets)

---

## Quick Start & Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/judeaquila/church_notes](https://github.com/judeaquila/church_notes)
   cd notes-hub