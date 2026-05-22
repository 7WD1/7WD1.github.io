const content_dir = 'contents/'
const config_file = 'config.yml'
const section_names = ['home', 'awards'];

const homeContent = { en: '', zh: '' };

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });


    // Yaml
    fetch(content_dir + config_file)
        .then(response => response.text())
        .then(text => {
            const yml = jsyaml.load(text);
            Object.keys(yml).forEach(key => {
                try {
                    document.getElementById(key).innerHTML = yml[key];
                } catch {
                    console.log("Unknown id and value: " + key + "," + yml[key].toString())
                }

            })
        })
        .catch(error => console.log(error));


    // Marked
    marked.use({ mangle: false, headerIds: false })

    // Load both English and Chinese home content, then apply saved language
    const savedLang = localStorage.getItem('lang') || 'en';

    Promise.all([
        fetch(content_dir + 'home.md').then(r => r.text()).then(md => { homeContent.en = marked.parse(md); }),
        fetch(content_dir + 'home-zh.md').then(r => r.text()).then(md => { homeContent.zh = marked.parse(md); })
    ]).then(() => {
        applyLang(savedLang);
    }).catch(error => console.log(error));

    // Language toggle
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
        langBtn.addEventListener('click', function () {
            const current = localStorage.getItem('lang') || 'en';
            const next = current === 'en' ? 'zh' : 'en';
            applyLang(next);
            localStorage.setItem('lang', next);
        });
    }

    function applyLang(lang) {
        const el = document.getElementById('home-md');
        if (el && homeContent[lang]) {
            el.innerHTML = homeContent[lang];
            MathJax.typeset();
        }
        const btn = document.getElementById('lang-toggle');
        if (btn) {
            btn.textContent = lang === 'en' ? '中文' : 'Eng';
        }
        localStorage.setItem('lang', lang);
    }

    // Load non-home sections
    section_names.filter(n => n !== 'home').forEach((name, idx) => {
        fetch(content_dir + name + '.md')
            .then(response => response.text())
            .then(markdown => {
                const html = marked.parse(markdown);
                document.getElementById(name + '-md').innerHTML = html;
            }).then(() => {
                // MathJax
                MathJax.typeset();
            })
            .catch(error => console.log(error));
    })

}); 
