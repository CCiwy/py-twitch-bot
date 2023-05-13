{% extends 'base.tpl' %}

{% macro show_command(command, response) %}
        <div className="row">
            <div>{{ command }} </div>
            <input name={{command}} type="text" value="{{ response }}"/>
        </div>
{% endmacro %}

{% block content %}
<h2> Messages Overview </h2>

<div styles="width=80%; margin: auto;">
    <ul styles="list-style-type=none;display: flex; flex-direction=column;width=100%">
    <form action="/github/update" method="POST">
    {% for command, response in handlers.items() %}
    <li styles="width=100%">
        {{ show_command(command, response) }}
    </li>
    {% endfor %}
    <ul>
    <input type="submit" value="[U]"/>
    </form>
</div>
{% endblock %}
