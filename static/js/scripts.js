(function() {
    'use strict';

    var content_dir = 'contents/';
    var config_file = 'config.yml';

    var homeContent = { en: '', zh: '' };

    function safeTypeset() {
        if (window.MathJax && window.MathJax.typesetPromise) {
            MathJax.typesetPromise().catch(function(e) {
                console.warn('MathJax typeset failed:', e);
            });
        } else if (window.MathJax && window.MathJax.typeset) {
            try { MathJax.typeset(); } catch (e) { /* ignore */ }
        }
    }

    function applyLang(lang) {
        var el = document.getElementById('home-md');
        if (el && homeContent[lang]) {
            el.innerHTML = homeContent[lang];
            safeTypeset();
        }
        var btn = document.getElementById('lang-toggle');
        if (btn) {
            btn.textContent = lang === 'en' ? '\u4E2D\u6587' : 'Eng';
        }
        localStorage.setItem('lang', lang);
    }

    window.addEventListener('DOMContentLoaded', function() {

        // Activate Bootstrap scrollspy on the main nav element
        var mainNav = document.body.querySelector('#mainNav');
        if (mainNav) {
            new bootstrap.ScrollSpy(document.body, {
                target: '#mainNav',
                offset: mainNav.offsetHeight + 2,
            });
        }

        // Collapse responsive navbar when toggler is visible
        var navbarToggler = document.body.querySelector('.navbar-toggler');
        if (navbarToggler) {
            var responsiveNavItems = [].slice.call(
                document.querySelectorAll('#navbarResponsive .nav-link')
            );
            responsiveNavItems.forEach(function(navItem) {
                navItem.addEventListener('click', function() {
                    if (window.getComputedStyle(navbarToggler).display !== 'none') {
                        navbarToggler.click();
                    }
                });
            });
        }

        // Load config YAML
        fetch(content_dir + config_file)
            .then(function(response) { return response.text(); })
            .then(function(text) {
                var yml = jsyaml.load(text);
                Object.keys(yml).forEach(function(key) {
                    try {
                        var el = document.getElementById(key);
                        if (el && typeof yml[key] === 'string') {
                            el.innerHTML = yml[key];
                        }
                    } catch (error) {
                        console.warn('Unknown id and value: ' + key, error);
                    }
                });
            })
            .catch(function(error) { console.warn('Config load error:', error); });

        // Marked
        marked.use({ mangle: false, headerIds: false });

        // Load both English and Chinese home content, then apply saved language
        var savedLang = localStorage.getItem('lang') || 'en';

        Promise.allSettled([
            fetch(content_dir + 'home.md').then(function(r) { return r.text(); }).then(function(md) { homeContent.en = marked.parse(md); }),
            fetch(content_dir + 'home-zh.md').then(function(r) { return r.text(); }).then(function(md) { homeContent.zh = marked.parse(md); })
        ]).then(function() {
            applyLang(savedLang);
        }).catch(function(error) { console.warn('Content load error:', error); });

        // Language toggle
        var langBtn = document.getElementById('lang-toggle');
        if (langBtn) {
            langBtn.addEventListener('click', function() {
                var current = localStorage.getItem('lang') || 'en';
                var next = current === 'en' ? 'zh' : 'en';
                applyLang(next);
            });
        }

    });
})();
