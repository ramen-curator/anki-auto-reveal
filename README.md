# Auto Reveal (Customizable Answer Timer)

An Anki addon that automatically flips the card and shows the answer after a delay.

## Why?

When reviewing flashcards, it's easy to overthink — spending 30+ seconds struggling to remember a word or concept, often ending in frustration.

This addon helps break that cycle by automatically showing the answer after a set time.  
Just enough to test recall, but not long enough to get stuck.

It’s not about being lazy.  
It’s about being kind to your brain.

## Features

- Automatically shows the answer side after a user-defined delay
- Supports custom note types and deck name filters
- Optional longer delay for cards tagged as `longform`
- Lightweight, non-intrusive, self-contained
- Works with most Anki versions (tested on 25.02+)
- GUI-based configuration (no code editing required)

## Install

You can install the addon from AnkiWeb:  
[Auto Reveal on AnkiWeb](https://ankiweb.net/shared/info/1616044684?cb=1744024933530)

## Settings

Find the settings in the Anki top menu:  
**Tools → Auto Reveal Settings**

## Packaging for AnkiWeb

To generate a release zip for AnkiWeb upload, use the provided PowerShell script:

```powershell
powershell.exe -File build.ps1
```

This creates a auto-reveal.zip file to the project directory, containing only the necessary files:

- \_\_init\_\_.py
- manifest.json
- README.md

You can upload this zip directly to AnkiWeb for release.

Note: Make sure PowerShell script execution is allowed on your system. If you see a permissions error, run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## License

MIT. You can use it, modify it, or ignore it. Just don't set it to 0 seconds — that’s cheating.
