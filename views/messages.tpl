    {% from 'macros/plugins.macro' import render_command_list %}
    {% extends 'base.tpl' %}


{% block content %}
<h3> Messages Overview </h3>
    {% set endpoint = template_context["endpoint"] %}
    {{ render_command_list(endpoint, handlers) }}
</div>
{% endblock %}
