(function($) {

    function readCMSCookie() {
        var cookieJsonMode = $.cookie.json,
            cookieValue;
        $.cookie.json = true;
        cookieValue = $.cookie(window.__cms_cookie_name);
        $.cookie.json = cookieJsonMode;
        if (cookieValue) {
            return cookieValue;
        }
        return {};
    }

    function writeCMSCookie(cookieValue) {
        var cookieJsonMode = $.cookie.json;
        $.cookie.json = true;
        $.cookie(window.__cms_cookie_name,
            cookieValue, {
                'path': window.__admin_url,
                'expires': 10
            });
        $.cookie.json = cookieJsonMode;
    }

    function updateMenuToolTexts($menuTool, newText) {
        $('a', $menuTool).text(newText);
    }

    function collapsibleLeftMenu() {
        var settings = readCMSCookie();
        if (!$('body').hasClass('cms-folded')) {
            $('body').addClass('cms-folded');
            updateMenuToolTexts($('#collapse-menu'), $('#collapse-menu').data('text-collapsed'));
            settings['folded'] = true;
        } else {
            $('body').removeClass('cms-folded');
            updateMenuToolTexts($('#collapse-menu'), $('#collapse-menu').data('text-expanded'));
            settings['folded'] = false;
        }
        writeCMSCookie(settings);
    }

    function pinnableLeftMenu() {
        var settings = readCMSCookie();
        if (!$('body').hasClass('cms-pinned')) {
            $('body').addClass('cms-pinned');
            updateMenuToolTexts($('#pin-menu'), $('#pin-menu').data('text-pinned'));
            settings['pinned'] = true;
        } else {
            $('body').removeClass('cms-pinned');
            updateMenuToolTexts($('#pin-menu'), $('#pin-menu').data('text-unpinned'));
            settings['pinned'] = false;
        }
        writeCMSCookie(settings);
    }

    function fitTopMenu() {
        var $topMenu = $('#adminbar').removeClass('cms-narrow'),
            maxWidth = $topMenu.outerWidth(true),
            width = 0;

        $topMenu.children('li').each(
            function() {
                width += $(this).outerWidth(true);
            }
        );

        if (width > maxWidth) {
            $topMenu.addClass('cms-narrow');
        }
    }

    function fitLeftMenu() {
        if ($(window).width() < 780) {
            $('body').addClass('cms-folded cms-force-folded');
            $('#collapse-menu').hide();
        } else {
            if ($('body').hasClass('cms-force-folded')) {
                var settings = readCMSCookie();
                $('#collapse-menu').show();
                $('body').removeClass('cms-force-folded');
                if (!settings['folded']) {
                    $('body').removeClass('cms-folded');
                }
            }
        }
    }

    $(document).ready(function() {

        var settings = readCMSCookie();
        if (settings['folded'] && !$('body').hasClass('cms-folded')) {
            collapsibleLeftMenu();
        }
        if (settings['pinned'] && !$('body').hasClass('cms-pinned')) {
            pinnableLeftMenu();
        }

        $(window).resize(
            function() {
                fitTopMenu();
                fitLeftMenu();
            }
        ).resize();

        $('#collapse-menu').click(function() {
            collapsibleLeftMenu();
        });

        $('#pin-menu').click(function() {
            pinnableLeftMenu();
        });

        // left submenus should stay on page
        $('#adminmenu .cms-has-submenu').hover(
            function() {
                if (!$(this).hasClass('cms-menu-top') || ($('body').hasClass('cms-folded') || $(this).hasClass('cms-menu-not-open'))) {
                    var $submenu = $(this).children('.cms-submenu').css({ 'visibility': 'hidden', 'display': 'block' }),
                        extra_margin = 0,
                        window_bottom_edge = $(window).scrollTop() + $(window).height(),
                        submenu_bottom_edge = $submenu.offset().top + $submenu.outerHeight() + extra_margin;

                    if (window_bottom_edge < submenu_bottom_edge) {
                        $submenu.css({ 'margin-top': '-' + (submenu_bottom_edge - window_bottom_edge) + 'px' });
                    }
                    $submenu.css({ 'visibility': 'visible' });
                }
            },
            function() {
                $(this).children('.cms-submenu').removeAttr('style');
            }
        );

        // top submenus should stay on page
        $('#adminbar .cms-has-submenu').hover(
            function() {
                var $submenu = $(this).children('.cms-submenu').css({ 'visibility': 'hidden', 'display': 'block' }),
                    extra_margin = 0,
                    window_right_edge = $(window).width(),
                    submenu_right_edge = $submenu.offset().left + $submenu.width() + extra_margin;

                if (window_right_edge < submenu_right_edge) {
                    $submenu.css({ 'margin-left': '-' + (submenu_right_edge - window_right_edge) + 'px' });
                }
                $submenu.css({ 'visibility': 'visible' });
            },
            function() {
                $(this).children('.cms-submenu').removeAttr('style');
            }
        );

    });

})(jQuery);