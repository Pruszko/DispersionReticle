## DispersionReticle
Updated and completely reworked mod that adds additional circle displaying fully focused dispersion of a gun.

Original idea by **StranikS_Scan**, completely reworked by me.

Also, over time, this mod now contains **following mutually compatible mods**:
- Dispersion reticle
- Server reticle
- Latency reticle (**NEW**)
- Fix Reticle Size (adjustment in config file)

## Config file
All features from config file **are reloadable on-the-fly** using **CTRL + P** hotkey in the game **anywhere**.

Check [Installation](#installation) section for more info about config file.

## Features
All of those features can be enabled/adjusted **independently**.

They are also compatible with "Use server aim" from in-game option.

**Dispersion reticle** (enabled by default):
- enabled by "dispersion-reticle-enabled" option
- adds green reticle displaying **fully focused dispersion** to **vanilla reticle**
- when both client-side and server-side reticle is on, it attaches to client-side reticle

**Latency reticle**:
- enabled by "latency-reticle-enabled" option
- adds green reticle displaying **current server-side dispersion** to **client-side reticle**
- by this, client-side and server-side dispersion desynchronization is clearly visible

**Server reticle**
- enabled by "server-reticle-enabled" option
- adds purple **server-side reticle** alongside with **client-side reticle**

**Fix reticle size**
- controlled by "reticle-size-multiplier" option
- WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion
- by this setting you can scale it to actual displayed dispersion
- good known values:
- 1.0 (default "wrong" WG dispersion)
- 0.6 (factor determined by me)
- 0.5848 (factor determined by **Jak_Attackk**a, **StranikS_Scan** and others)

## Resource
- [WGMods](https://wgmods.net/5251/)
- [CurseForge](https://www.curseforge.com/worldoftanks/wot-mods/dispersionreticle-reworked)
- [Github Releases Page](https://github.com/Pruszko/DispersionReticle/releases)

## Installation
1. Copy "DispersionReticle.wotmod" file into "[WoT game directory]/mods/[version]/" directory
2. Run a game with mod installed to generate default config file
3. Adjust config file to your liking
4. Reload it in-game whenever you want using **CTRL + P** hotkey

A default config file will be automatically created when you launch a game
with my mod installed or when it is not present on config reload.

Full config file location: **"[WoT game directory]/mods/config/DispersionReticle/config.json"**

To control which features are enabled, navigate to an above mentioned file
and open it using text editor (preferably **Notepad++**).

If config gets invalid format while editing, reload attempt will just be ignored.

All config options **are reloadable on-the-fly** using **CTRL + P** hotkey in the game **anywhere**.

## Compatibility
This mod **IS NOT** compatible with other mods with similar features as mine.

Current known incompatible mods:
- AwfulTanker's Server Marker (and other similar)
- Jak_Atackka's Fix Reticle Size (and other similar)

Use preferred options from above features for similar functionality instead.

However, it should be compatible with any crosshair mods that changes
how crosshair or reticle looks like.