def form_errors_message(form):
    """Ошибки формы одной строкой для показа пользователю."""
    lines = []
    for name, errors in form.errors.items():
        label = form.fields[name].label if name in form.fields else ''
        lines.append(f'{label}: {errors[0]}' if label else errors[0])
    return '\n'.join(lines)
