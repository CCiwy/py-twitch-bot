{% extends 'index.tpl' %}



{% macro show_command(command, response) %}
        <div className="row">
            <div>{{ command }} </div>
            <input name={{command}} type="text" value="{{ response }}"/>
        </div>
{% endmacro %}

{% block plugin %}
<h2> Users Overview </h2>
 {% if lurkers %}
     {% for name in lurkers %}
        {{ name }}
     {% endfor %}
 
 {% elif first %}

    First Chatter: {{ first }}
 {% else %}
 
    NO DATA
 
 {% endif %}


{% endblock %}
