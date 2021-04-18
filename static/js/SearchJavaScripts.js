$(function () {
    let data = [
        {time: '09:00', a: true, b: false, c: false},
        {time: '10:00', a: true, b: true, c: true}
    ]

    setTable(data);
})

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
            {title: "1235446", data: "a"},
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