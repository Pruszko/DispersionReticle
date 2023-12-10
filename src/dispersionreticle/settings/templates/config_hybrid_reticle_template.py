CONFIG_HYBRID_RETICLE_TEMPLATE = """{
    // Configs can be reloaded in game using hotkeys: CTRL + P
    // To generate default config, delete config files and:
    // - either reload them with above hotkey
    // - or launch a game again

    // Standard hybrid reticle
    // 
    // Adds standard reticle displaying current server-side dispersion to client-side reticle.
    // Basically, client-side position, but server-side dispersion.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    //
    // Useful if you want to know server-side dispersion, but still want client-side responsiveness.

    "standard-hybrid-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(standard-hybrid-reticle-enabled)s,

        // Valid values: true/false (default: false)
        //
        // If true, standard client reticle is hidden.
        // Useful if you want to only use hybrid reticle instead of standard reticle.
        "hide-standard-reticle": %(standard-hybrid-reticle-hide-standard-reticle)s
    }
}"""
