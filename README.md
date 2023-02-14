## DispersionReticle
Updated and completely reworked mod that adds additional circle displaying fully focused dispersion of a gun.

Original idea by **StranikS_Scan**, completely reworked by me.

## Features
**NEW**
- variants with "fixed reticle size" of all below versions with x0.6 multiplier

**DispersionReticle**:
- closest to vanilla behavior
- shows additional reticle displaying fully focused dispersion of a gun
- works well with "Use server reticle" option from game settings
- works well in replays

**ClientServerReticle**:
- always shows client reticle only (without dispersion reticle)
- **"Use server reticle"** option additionally shows server reticle

**DispersionReticle_all**:
- combines features of **DispersionReticle** and **DispersionReticle_server**

## Resource
- [WGMods](https://wgmods.net/5251/)
- [CurseForge](https://www.curseforge.com/worldoftanks/wot-mods/dispersionreticle-reworked)
- [Github Releases Page](https://github.com/Pruszko/DispersionReticle/releases)

## Installation
For vanilla behavior with gun dispersion (adds dispersion reticle to client/server reticle):
- Copy "DispersionReticle.wotmod" file into "[WoT game directory]/mods/[version]/" directory
For the same behavior but with fixed reticle size (by x0.6 multiplication):
- Copy "DispersionReticle_x0_6.wotmod" file into "[WoT game directory]/mods/[version]/" directory

For both client and server crosshair only:
- Copy "ClientServerReticle.wotmod" file into "[WoT game directory]/mods/[version]/" directory
For the same behavior but with fixed reticle size (by x0.6 multiplication):
- Copy "ClientServerReticle_x0_6.wotmod" file into "[WoT game directory]/mods/[version]/" directory

For both client and server crosshair with gun dispersion:
- Copy "DispersionReticle_all.wotmod" file into "[WoT game directory]/mods/[version]/" directory
For the same behavior but with fixed reticle size (by x0.6 multiplication):
- Copy "DispersionReticle_all_x0_6.wotmod" file into "[WoT game directory]/mods/[version]/" directory

Note: Choose **ONLY ONE** of them

## Compatibility
This mod **IS NOT** compatible with mods adding **client+server marker** at once.
Also, this mod **IS NOT** compatible with mods changing reticle size.

Use "ClientServerReticle.wotmod" or "DispersionReticle_all.wotmod"
with also their x0.6 fixed reticle size variants for similar functionality instead.

However, it should be compatible with any crosshair mods that changes
how crosshair or reticle looks like.