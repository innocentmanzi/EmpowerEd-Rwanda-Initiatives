(function () {
    window.onload = function () {
        // INITIALIZATION OF NAVBAR VERTICAL ASIDE
        new HSSideNav('.js-navbar-vertical-aside').init()

        // INITIALIZATION OF FORM SEARCH
        new HSFormSearch('.js-form-search')

        // INITIALIZATION OF BOOTSTRAP DROPDOWN
        HSBsDropdown.init()

        // INITIALIZATION OF SELECT
        HSCore.components.HSTomSelect.init('.js-select')

        // INITIALIZATION OF INPUT MASK
        HSCore.components.HSMask.init('.js-input-mask')

        // INITIALIZATION OF FILE ATTACHMENT
        new HSFileAttach('.js-file-attach')

        // INITIALIZATION OF STICKY BLOCKS
        new HSStickyBlock('.js-sticky-block', {
            targetSelector: document.getElementById('header').classList.contains('navbar-fixed') ? '#header' : null
        })

        // SCROLLSPY
        new bootstrap.ScrollSpy(document.body, {
            target: '#navbarSettings',
            offset: 100
        })

        new HSScrollspy('#navbarVerticalNavMenu', {
            breakpoint: 'lg',
            scrollOffset: -20
        })
    }
})()