<h1> BASE TPL HEADER </h1>
<hr>
<div>
{% for plugin_name, endpoint in navigation.items() %}
    <div><a href="localhost:8888{{endpoint}}/health"> {{ plugin_name }} </a></div>
{% endfor %}
</div>

{% block content %}

{% endblock %}
<br>
<hr>
BASE TPL FOOTER
