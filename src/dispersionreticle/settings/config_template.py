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

    // Focused reticle (enabled by default)
    //
    // Adds standard reticle displaying fully-focused dispersion to in-game reticle.
    // Other mods may influence the look of this reticle.
    //
    // When both client-side and server-side reticles are on, it attaches to client-side reticle.

    "focused-reticle": {

        // Valid values: true/false (default: true)
        //
        // If true, displays this reticle.
        "enabled": %(focused-reticle-enabled)s,

        // Valid values: ["default", "purple"]
        // Default value: "default"
        //
        // Type of this reticle:
        // - "default" - displays reticle the way game renders it by default,
        // - "purple"  - same as above, but additionally tries to color it to purple.
        //
        // If other mods changed colors of default reticle, then purple option may incorrectly color it.
        // This restriction is not present in extended reticles.
        "type": %(focused-reticle-type)s
    },

    // Focused reticle extended
    //
    // Adds configurable reticle displaying fully-focused dispersion to in-game reticle.
    // Other mods does not have influence on the look of this reticle.
    //
    // When both client-side and server-side reticles are on, it attaches to client-side reticle.
    // 
    // For SPG artillery view, a standard version of this reticle will be used.

    "focused-reticle-extended": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(focused-reticle-extended-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "circle"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(focused-reticle-extended-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [255, 255, 0] (this is yellow color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(focused-reticle-extended-color)s,

        // Valid values: any number >= 0.0 (for default behavior: 0.0)
        //
        // Size of dot displayed in reticle center.
        // 
        // Value 1.0 is default size.
        // Value 0.0 disables center dot.
        "center-dot-size": %(focused-reticle-extended-center-dot-size)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(focused-reticle-extended-draw-outline)s,

        // Valid values: ["top", "bottom"]
        // Default value: "bottom"
        //
        // Chooses layer on which reticle should be displayed:
        // - "top"    - display above standard reticles,
        // - "bottom" - display below standard reticles.
        "layer": %(focused-reticle-extended-layer)s,

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
        "blend": %(focused-reticle-extended-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(focused-reticle-extended-alpha)s,

        // Shape specific configuration
        "shapes": {

            // Pentagon figure specific configuration
            "pentagon": {

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Width of pentagon.
                "width": %(focused-reticle-extended-shapes-pentagon-width)s,

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Height of pentagon.
                "height": %(focused-reticle-extended-shapes-pentagon-height)s
            },

            // T-shape figure specific configuration
            "t-shape": {

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Thickness of lines.
                "thickness": %(focused-reticle-extended-shapes-t-shape-thickness)s,

                // Valid values: any number (for default behavior: 1.0)
                //
                // Length of lines coming from intersection.
                //
                // Negative values inverts direction of the line facing reticle center.
                "length": %(focused-reticle-extended-shapes-t-shape-length)s
            }
        }
    },

    // Hybrid reticle
    // 
    // Adds standard reticle displaying current server-side dispersion to client-side reticle.
    // Other mods may influence the look of this reticle.
    //
    // Basically, client-side position, but server-side dispersion.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    //
    // Useful if you want to know server-side dispersion, but still want client-side responsiveness.

    "hybrid-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(hybrid-reticle-enabled)s,

        // Valid values: ["default", "purple"]
        // Default value: "default"
        //
        // Type of this reticle:
        // - "default" - displays reticle the way game renders it by default,
        // - "purple"  - same as above, but additionally tries to color it to purple.
        //
        // If other mods changed colors of default reticle, then purple option may incorrectly color it.
        // This restriction is not present in extended reticles.
        "type": %(hybrid-reticle-type)s,

        // Valid values: true/false (default: false)
        //
        // If true, standard client reticle is hidden while hybrid reticle is enabled..
        // Useful if you want to only use hybrid reticle instead of standard reticle.
        "hide-standard-reticle": %(hybrid-reticle-hide-standard-reticle)s
    },

    // Hybrid reticle extended
    // 
    // Adds configurable reticle displaying current server-side dispersion to client-side reticle.
    // Other mods does not have influence on the look of this reticle.
    //
    // Basically, client-side position, but server-side dispersion.
    // By this, client-side and server-side dispersion desynchronization is clearly visible.
    //
    // Useful if you want to know server-side dispersion, but still want client-side responsiveness.
    //
    // For SPG artillery view, a standard version of this reticle will be used.

    "hybrid-reticle-extended": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(hybrid-reticle-extended-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "circle"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(hybrid-reticle-extended-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [0, 255, 255] (this is cyan color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(hybrid-reticle-extended-color)s,

        // Valid values: any number >= 0.0 (for default behavior: 0.0)
        //
        // Size of dot displayed in reticle center.
        // 
        // Value 1.0 is default size.
        // Value 0.0 disables center dot.
        "center-dot-size": %(hybrid-reticle-extended-center-dot-size)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(hybrid-reticle-extended-draw-outline)s,

        // Valid values: ["top", "bottom"]
        // Default value: "bottom"
        //
        // Chooses layer on which reticle should be displayed:
        // - "top"    - display above standard reticles,
        // - "bottom" - display below standard reticles.
        "layer": %(hybrid-reticle-extended-layer)s,

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
        "blend": %(hybrid-reticle-extended-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(hybrid-reticle-extended-alpha)s,

        // Shape specific configuration
        "shapes": {

            // Pentagon figure specific configuration
            "pentagon": {

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Width of pentagon.
                "width": %(hybrid-reticle-extended-shapes-pentagon-width)s,

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Height of pentagon.
                "height": %(hybrid-reticle-extended-shapes-pentagon-height)s
            },

            // T-shape figure specific configuration
            "t-shape": {

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Thickness of lines.
                "thickness": %(hybrid-reticle-extended-shapes-t-shape-thickness)s,

                // Valid values: any number (for default behavior: 1.0)
                //
                // Length of lines coming from intersection.
                //
                // Negative values inverts direction of the line facing reticle center.
                "length": %(hybrid-reticle-extended-shapes-t-shape-length)s
            }
        }
    },

    // Server reticle
    // 
    // Adds server-side standard reticle alongside with client-side reticle.
    // Other mods may influence the look of this reticle.

    "server-reticle": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(server-reticle-enabled)s,

        // Valid values: ["default", "purple"]
        // Default value: "purple"
        //
        // Type of this reticle:
        // - "default" - displays reticle the way game renders it by default,
        // - "purple"  - same as above, but additionally tries to color it to purple.
        //
        // If other mods changed colors of default reticle, then purple option may incorrectly color it.
        // This restriction is not present in extended reticles.
        "type": %(server-reticle-type)s
    },

    // Server reticle extended
    // 
    // Adds configurable server-side reticle alongside with client-side reticle.
    // Other mods does not have influence on the look of this reticle.
    //
    // For SPG artillery view, a standard version of this reticle will be used.

    "server-reticle-extended": {

        // Valid values: true/false (default: false)
        //
        // If true, displays this reticle.
        "enabled": %(server-reticle-extended-enabled)s,

        // Valid values: ["pentagon", "t-shape", "circle", "dashed"]
        // Default value: "pentagon"
        //
        // Shape which this reticle should have:
        // - "pentagon" - displays reticle made of pentagons,
        // - "t-shape"  - displays reticle made of T-shaped figures,
        // - "circle"   - displays reticle as a circle with 1 pixel thickness; similar to vanilla reticle,
        // - "dashed"   - displays reticle made of dash lines; similar to vanilla reticle.
        "shape": %(server-reticle-extended-shape)s,

        // Valid value: 3-element array of numbers between 0 and 255
        // Default value: [255, 0, 255] (this is purple color)
        //
        // Colors this reticle using red, green and blue components.
        // You can use color picker from internet to visually choose desired color.
        "color": %(server-reticle-extended-color)s,

        // Valid values: any number >= 0.0 (for default behavior: 0.0)
        //
        // Size of dot displayed in reticle center.
        // 
        // Value 1.0 is default size.
        // Value 0.0 disables center dot.
        "center-dot-size": %(server-reticle-extended-center-dot-size)s,

        // Valid values: true/false (default: false)
        //
        // If true, shape is additionally displayed with 1 pixel black outline.
        // Useful if shape color blends with the background.
        "draw-outline": %(server-reticle-extended-draw-outline)s,

        // Valid values: ["top", "bottom"]
        // Default value: "bottom"
        //
        // Chooses layer on which reticle should be displayed:
        // - "top"    - display above standard reticles,
        // - "bottom" - display below standard reticles.
        "layer": %(server-reticle-extended-layer)s,

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
        "blend": %(server-reticle-extended-blend)s,

        // Valid values: number between 0.0 and 1.0 (default 1.0)
        //
        // Controls transparency of displayed reticle:
        // - value 1.0 means full visibility
        // - value 0.0 means zero visibility
        "alpha": %(server-reticle-extended-alpha)s,

        // Shape specific configuration
        "shapes": {

            // Pentagon figure specific configuration
            "pentagon": {

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Width of pentagon.
                "width": %(server-reticle-extended-shapes-pentagon-width)s,

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Height of pentagon.
                "height": %(server-reticle-extended-shapes-pentagon-height)s
            },

            // T-shape figure specific configuration
            "t-shape": {

                // Valid values: any number > 0.0 (for default behavior: 1.0)
                //
                // Thickness of lines.
                "thickness": %(server-reticle-extended-shapes-t-shape-thickness)s,

                // Valid values: any number (for default behavior: 1.0)
                //
                // Length of lines coming from intersection.
                //
                // Negative values inverts direction of the line facing reticle center.
                "length": %(server-reticle-extended-shapes-t-shape-length)s
            }
        }
    },

    // DO NOT touch "__version__" field
    // It is used by me to seamlessly update config file :)
    "__version__": 6
}"""
