/*==================== SHOW MENU ====================*/
const showMenu = (toggleId, navId) => {
    const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId)

    // Validate that variables exist
    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            // We add the show-menu class to the div tag with the nav__menu class
            nav.classList.toggle('show-menu')
        })
    }
}
showMenu('nav-toggle', 'nav-menu')

const navItems = document.querySelectorAll('.nav__item');
navItems.forEach(item => {
    item.addEventListener('click', function () {
        const dropdownContent = this.querySelector('.dropdown-content');
        if (!dropdownContent.classList.contains('show')) {
            document.querySelectorAll('.dropdown-content').forEach(dropdown => {
                dropdown.classList.remove('show');
            });
            dropdownContent.classList.add('show');
        } else {
            dropdownContent.classList.remove('show');
        }
    });

    // เพิ่ม event listener เพื่อหยุดการกระจายเหตุการณ์เมื่อคลิกที่เมนูย่อย
    const dropdownItems = item.querySelectorAll('.dropdown-content .nav__link');
    dropdownItems.forEach(dropdownItem => {
        dropdownItem.addEventListener('click', function (event) {
            event.stopPropagation(); // หยุดการกระจายเหตุการณ์
        });
    });
});



/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
    const scrollY = window.pageYOffset

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight
        const sectionTop = current.offsetTop - 50;
        sectionId = current.getAttribute('id')

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.add('active-link')
        } else {
            document.querySelector('.nav__menu a[href*=' + sectionId + ']').classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)

/*==================== CHANGE BACKGROUND HEADER ====================*/
function scrollHeader() {
    const nav = document.getElementById('header')
    // When the scroll is greater than 200 viewport height, add the scroll-header class to the header tag
    if (this.scrollY >= 200) nav.classList.add('scroll-header'); else nav.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)

/*==================== SHOW SCROLL TOP ====================*/
function scrollTop() {
    const scrollTop = document.getElementById('scroll-top');
    // When the scroll is higher than 560 viewport height, add the show-scroll class to the a tag with the scroll-top class
    if (this.scrollY >= 560) scrollTop.classList.add('show-scroll'); else scrollTop.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollTop)

/*==================== DARK LIGHT THEME ====================*/
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'bx-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'bx-moon' : 'bx-sun'


/*==================== SCROLL REVEAL ANIMATION ====================*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '30px',
    duration: 2000,
    reset: true
});

sr.reveal(`.home__data, .home__img,
            .about__data, .about__img,
            .services__content, .menu__content,
            .app__data, .app__img,
            .contact__data, .contact__button,
            .footer__content`, {
    interval: 200
})



/*==================== Tasking ====================*/
document.addEventListener('DOMContentLoaded', function () {
    var menus = document.querySelectorAll('.menu-left a');

    menus.forEach(function (menu) {
        menu.addEventListener('click', function (event) {
            event.preventDefault();

            var circleId = this.hash.substring(1);
            var circle = document.getElementById(circleId);

            if (circle !== null) {
                document.querySelectorAll('.circle').forEach(function (el) {
                    el.classList.remove('clicked');
                    el.classList.remove('clicked-green');
                });

                if (this.textContent.trim() === 'ดำเนินการ') {
                    circle.classList.add('clicked');
                } else {
                    circle.classList.add('clicked-green');
                }
            }
        });
    });
});

