{% extends 'base.tpl' %}
{% set get_url = template_context["get_url"] %}

{% set endpoint = template_context["endpoint"] %}


{% macro plugin_navigation(rules, get_url) %}

        {% for rule in rules %}
            <div class="row sidebar_link">
                <a class="nav_link" href="{{ get_url(endpoint, rule)}}"> {{ rule }} </a>
            </div>

        {% endfor %}
        
{% endmacro %}



{% block content %}
<div class="wrapper" styles="display:flex; flex-direction:column";>
        <div class="sidebar">
        {{ plugin_navigation(template_context["rules"], get_url) }}
        </div>
        <div class="content">
            {% block plugin %}

            {% endblock plugin %}
        </div>    
</div>
{% endblock %}

