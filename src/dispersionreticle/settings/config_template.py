CONFIG_TEMPLATE = """{
    // Configs can be reloaded in game using hotkeys: CTRL + P
    // To generate default configs, delete config files and:
    // - either reload them with above hotkey
    // - or launch a game again

    // Global features toggle
    // Valid values: true/false (default: true)
    //
    // When set to false, it globally disables all features of this mod
    // however it does not remove mod presence itself. 
    "enabled": %(enabled)s,

    // Reticle size
    // Valid values: any number > 0.0 (for default behavior: 1.0)
    //
    // Scales all reticles size by factor, except SPG top-view reticle.
    //
    // WG's displayed reticle dispersion is noticeably bigger than actual gun dispersion.
    // It was discovered by Jak_Attackka, StranikS_Scan and others.
    // By this setting you can scale it to actual displayed dispersion.
    //
    // Good known values:
    // - 1.0    (default "wrong" WG dispersion)
    // - 0.6    (factor determined by me)
    // - 0.5848 (factor determined by Jak_Attackka, StranikS_Scan and others)

    "reticle-size-multiplier": %(reticle-size-multiplier)s,

    // Standard focused reticle (enabled by default)
    //
    // Adds standard reticle displaying fully-focused dispersion to in-game reticle.
    // When both client-side and server-side reticles are on, it attaches to client-side reticle.

    "standard-focused-reticle": {

        // Valid values: true/false (default: true)
        //
        // If true, displays this reticle.
        "enabled": %(standard-focused-reticle-enabled)s
    },

    // Customizable focused reticle
    //
    // Adds configurable reticle displaying fully-focused dispersion to in-game reticle.
    // When both client-side and server-side reticles are on, it attaches to client-side reticle.
    // 
    // For SPG artillery view, a standard version of this reticle will be used.

    "custom-focused-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(custom-focused-reticle-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "circle"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(custom-focused-reticle-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [255, 255, 0] (this is yellow color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(custom-focused-reticle-color)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with center dot.
        "draw-center-dot": %(custom-focused-reticle-draw-center-dot)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(custom-focused-reticle-draw-outline)s,

        // Valid values: number between 0.0 and 1.0 (default 0.5)
        //
        // Controls, how much reticle color will blend with the background color instead of replacing it.
        // Vanilla "dashed" reticle uses this with value 1.0 without outline to make reticle look more natural.
        //
        // Set it to 1.0 if you want color to fully act as an addition to background color.
        // Set it to 0.0 if you want color to fully replace background color.
        // Values between them controls strength of those effects the closer it gets to them.
        //
        // Value 1.0 effectively prevents you from getting dark colors
        // because ... black color + background color = background color.
        "blend": %(custom-focused-reticle-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(custom-focused-reticle-alpha)s
    },

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
        // If true, standard client reticle is hidden while hybrid reticle is enabled..
        // Useful if you want to only use hybrid reticle instead of standard reticle.
        "hide-standard-reticle": %(standard-hybrid-reticle-hide-standard-reticle)s
    },

    // Customizable hybrid reticle
    // 
    // Adds configurable reticle displaying current server-side dispersion to client-side reticle.
    // Basically, client-side position, but server-side dispersion.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    //
    // Useful if you want to know server-side dispersion, but still want client-side responsiveness.
    //
    // For SPG artillery view, a standard version of this reticle will be used.

    "custom-hybrid-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(custom-hybrid-reticle-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "circle"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(custom-hybrid-reticle-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [0, 255, 255] (this is cyan color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(custom-hybrid-reticle-color)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with center dot.
        "draw-center-dot": %(custom-hybrid-reticle-draw-center-dot)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(custom-hybrid-reticle-draw-outline)s,

        // Valid values: number between 0.0 and 1.0 (default 0.5)
        //
        // Controls, how much reticle color will blend with the background color instead of replacing it.
        // Vanilla "dashed" reticle uses this with value 1.0 without outline to make reticle look more natural.
        //
        // Set it to 1.0 if you want color to fully act as an addition to background color.
        // Set it to 0.0 if you want color to fully replace background color.
        // Values between them controls strength of those effects the closer it gets to them.
        //
        // Value 1.0 effectively prevents you from getting dark colors
        // because ... black color + background color = background color.
        "blend": %(custom-hybrid-reticle-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(custom-hybrid-reticle-alpha)s
    },

    // Standard server reticle
    // 
    // Adds server-side standard reticle alongside with client-side reticle.

    "standard-server-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(standard-server-reticle-enabled)s
    },

    // Custom server reticle
    // 
    // Adds configurable server-side reticle alongside with client-side reticle.
    // For SPG artillery view, a standard version of this reticle will be used.

    "custom-server-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(custom-server-reticle-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "pentagon"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(custom-server-reticle-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [255, 0, 255] (this is purple color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(custom-server-reticle-color)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with center dot.
        "draw-center-dot": %(custom-server-reticle-draw-center-dot)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(custom-server-reticle-draw-outline)s,

        // Valid values: number between 0.0 and 1.0 (default 0.5)
        //
        // Controls, how much reticle color will blend with the background color instead of replacing it.
        // Vanilla "dashed" reticle uses this with value 1.0 without outline to make reticle look more natural.
        //
        // Set it to 1.0 if you want color to fully act as an addition to background color.
        // Set it to 0.0 if you want color to fully replace background color.
        // Values between them controls strength of those effects the closer it gets to them.
        //
        // Value 1.0 effectively prevents you from getting dark colors
        // because ... black color + background color = background color.
        "blend": %(custom-server-reticle-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(custom-server-reticle-alpha)s
    },

    // DO NOT touch "__version__" field
    // It is used by me to seamlessly update config file :)
    "__version__": 6
}"""
