{% extends 'base.tpl' %}

{% macro show_command(command, response) %}
    <div>{{ command }} </div>  <input type="text" value="{{ response }}"></input>
{% endmacro %}

{% block content %}
<h2> Messages Overview </h2>

<div styles="width=80%; margin: auto;">
    <ul styles="list-style-type=none;display: flex; flex-direction=column;width=100%">
    {% for command, response in handlers.items() %}
    <li styles="width=100%">
        {{ show_command(command, response) }}
    </li>
    {% endfor %}
    <ul>
</div>
{% endblock %}
