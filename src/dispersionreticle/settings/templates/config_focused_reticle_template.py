CONFIG_FOCUSED_RETICLE_TEMPLATE = """{
    // Configs can be reloaded in game using hotkeys: CTRL + P
    // To generate default config, delete config files and:
    // - either reload them with above hotkey
    // - or launch a game again

    // Standard focused reticle (enabled by default)
    //
    // Adds standard reticle displaying fully-focused dispersion to standard reticle.
    // When both client-side and server-side reticle are on, it attaches to client-side reticle.

    "standard-focused-reticle": {

        // Valid values: true/false (default: true)
        //
        // If true, displays this reticle.
        "enabled": %(standard-focused-reticle-enabled)s
    }
}"""
