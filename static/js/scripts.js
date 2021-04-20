/*!
    * Start Bootstrap - Agency v6.0.3 (https://startbootstrap.com/theme/agency)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
    */
(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 72,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 74,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);


    let data = [
        {time: '09:00', a: true, b: false, c: false},
        {time: '10:00', a: true, b: true, c: true}
    ]

    setTable(data);


})(jQuery); // End of use strict



function setTable(data) {
    let table = $('#table').DataTable({
        width: 100,
        data: data,
        searching: false,
        lengthChange: false,
        ordering: false,
        paging: false,
        info: false,
        columns: [
            {title: "Time", data: "time"},
            {title: "1446", data: "a"},
            {title: "B", data: "b"},
            {title: "C", data: "c"},
        ],
        columnDefs: [
            {
                targets: [1, 2, 3],
                render: function (data, type, row) {
                    let css = data ? 'tb-btn-blue' : 'tb-btn-red'
                    return '<span class="tb-btn ' + css + '"></span>'
                }
            }
        ]
    })

    $('.tb-btn-blue').click(function () {
        let data = table.row($(this).parents('tr')).data()
        console.log(data.time)
    })
}
