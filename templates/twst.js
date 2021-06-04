
var ctx = document.getElementById("bar_chart").getContext("2d");
var myChart = new Chart(ctx, {
    type: 'bar'
    data: {
        labels: [
        {% for item in labels %}
        "{{ item }}",
        {% endfor %}
        ],
        datasets: [{
            data: [
            {% for item in values %}
            "{{ item }}",
            {% endfor %}
            ],
            backgroundColor: "rgba(153,255,51,1)"
        }]
    }
});