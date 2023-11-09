## DispersionReticle
Updated and completely reworked mod that adds additional circle displaying fully focused dispersion of a gun.

Original idea by **StranikS_Scan**, completely reworked by me.

Also, over time, this mod now contains **following mutually compatible mods**:
- Dispersion reticle
- Server reticle
- Simple server reticle with customizable shape, color, blending, outline presence and transparency
- Latency reticle
- Reticle Size (adjustment in config file)

![All presented reticles](images/all.png)
![Simple server reticle features](images/simple_server.png)

## Config file
All features from config file **are reloadable on-the-fly** using **CTRL + P** hotkey in the game **anywhere**.

This mod also supports **Mod Configurator by IzeBerg** allowing for configuring
this mod using its GUI.
It's also implicitly present in some modpacks. 

Check [Installation](#installation) section for more info
about config file and **Mod Configurator**.

## Features
All of those features can be enabled/adjusted **independently**.

They are also compatible with "Use server aim" from in-game option.

**Dispersion reticle** (enabled by default):
- adds green reticle displaying **fully focused dispersion** to **vanilla reticle**
- when both client-side and server-side reticle is on, it attaches to client-side reticle

**Latency reticle**:
- adds green reticle displaying **current server-side dispersion** to **client-side reticle**
- basically, client-side position, but server-side dispersion
- by this, client-side and server-side dispersion desynchronization is clearly visible
- useful if you want to know server-side dispersion, but still want client-side responsiveness

**Server reticle**
- adds purple **server-side reticle** alongside with **client-side reticle**

**Simple server reticle**
- adds **server-side reticle with customizable shape** alongside with **client-side reticle**
- has configurable shape, coloring, blending, outline presence and transparency
- original idea by **AwfulTanker's Server Marker**, but **implemented from scratch** by me

**Reticle size**
- controlled by "reticle-size-multiplier" option
- WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion
- it was discovered by **Jak_Attackka**, **StranikS_Scan** and others
- by this setting you can scale it to actual displayed dispersion
- good known values:
    - 1.0 (default "wrong" WG dispersion)
    - 0.6 (factor determined by me)
    - 0.5848 (factor determined by **Jak_Attackk**a, **StranikS_Scan** and others)

## Resource
- [WGMods](https://wgmods.net/5251/)
- [CurseForge](https://www.curseforge.com/worldoftanks/wot-mods/dispersionreticle-reworked)
- [GitHub Releases Page](https://github.com/Pruszko/DispersionReticle/releases)

## Installation
With Mod Configurator:
1. Copy "DispersionReticle.wotmod" file and all other *.wotmod files extracted from zip into "[WoT game directory]/mods/[version]/" directory
2. Open button with "<>" icon in garage and find **DispersionReticle section**.
3. Adjust mod to your liking

Without Mod Configurator:
1. Copy "DispersionReticle.wotmod" file extracted from zip into "[WoT game directory]/mods/[version]/" directory
2. Run a game with mod installed to generate default config file
3. Adjust config file to your liking
4. Reload it in-game whenever you want using **CTRL + P** hotkey

A default config file will be automatically created when you launch a game
with my mod installed or when it is not present on config reload.

Full config file location: **"[WoT game directory]/mods/configs/DispersionReticle/config.json"**

To control which features are enabled, either change it in Mod Configurator 
or navigate to an above mentioned file
and open it using text editor (preferably **Notepad++**).

If config gets invalid format while editing, reload attempt will just be ignored.

All config options **are reloadable on-the-fly** using **CTRL + P** hotkey in the game **anywhere**.


## Optional dependencies
* **Mod Configurator by IzeBerg** - allows configuring my mod using its in-game interface;
  thanks to **IzeBerg** for cool GUI configuration API
* **ModsList by POLIROID** - allows for displaying button for Mod Configurator; thanks to **POLIROID**

## Contributions
Thanks to:
* **shuxue** - for Russian translations
* **yinx2002** - for Chinese translations

## Compatibility
This mod **IS NOT** compatible with other mods with similar features as mine.

Current known incompatible mods:
- AwfulTanker's Server Marker (and other similar)
- Jak_Atackka's Better Reticle Size (and other similar)

Use preferred options from above features for similar functionality instead.

However, it should be compatible with any crosshair mods that changes
how crosshair or reticle looks like.