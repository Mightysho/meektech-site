from django import template
from django.conf import settings
from django.contrib.admin.models import LogEntry

register = template.Library()


def _action_label(flag):
    return {1: 'Added', 2: 'Changed', 3: 'Deleted'}.get(flag, 'Action')


@register.inclusion_tag('spectra/widgets/_recent_actions_list.html', takes_context=True)
def get_recent_admin_actions(context, limit=None):
    request = context.get('request')
    if limit is None:
        try:
            limit = settings.SPECTRA_CONFIG.get('recent_actions_limit', 10)
        except Exception:
            limit = 10

    entries = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:limit]
    actions = []
    for e in entries:
        obj_url = None
        try:
            if e.content_type and e.object_id:
                app_label = e.content_type.app_label
                model = e.content_type.model
                # admin change URL pattern: admin:app_model_change
                url_name = f"admin:{app_label}_{model}_change"
                from django.urls import reverse
                obj_url = reverse(url_name, args=[e.object_id])
        except Exception:
            obj_url = None

        actions.append({
            'user': e.user,
            'action_time': e.action_time,
            'action_flag': _action_label(e.action_flag),
            'object_repr': e.object_repr,
            'content_type': e.content_type,
            'object_url': obj_url,
        })

    return {'recent_actions': actions, 'request': request}


@register.inclusion_tag('spectra/partials/_recent_actions_sidebar.html', takes_context=True)
def get_recent_admin_actions_sidebar(context, limit=6):
    """Return a compact list of recent actions for sidebar dropdown."""
    request = context.get('request')
    try:
        limit = int(limit)
    except Exception:
        try:
            limit = settings.SPECTRA_CONFIG.get('recent_actions_limit', 6)
        except Exception:
            limit = 6

    entries = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:limit]
    actions = []
    for e in entries:
        obj_url = None
        try:
            if e.content_type and e.object_id:
                app_label = e.content_type.app_label
                model = e.content_type.model
                url_name = f"admin:{app_label}_{model}_change"
                from django.urls import reverse
                obj_url = reverse(url_name, args=[e.object_id])
        except Exception:
            obj_url = None

        actions.append({
            'user': e.user,
            'action_time': e.action_time,
            'action_flag': _action_label(e.action_flag),
            'object_repr': e.object_repr,
            'object_url': obj_url,
        })

    return {'recent_actions': actions, 'request': request}
