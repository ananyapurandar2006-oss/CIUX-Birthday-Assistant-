
def enrich_with_context(parsed, state):
    e = parsed['entities']

    # Carry forward month and relationship when omitted.
    for key in ('month', 'relationship'):
        if key not in e and state.get(key) is not None:
            e[key] = state[key]

    # Use a previous person only if no new search has
    # replaced the earlier person-specific context.
    if e.get('person_reference'):
        previous_person = state.get('person_id')

        if previous_person is not None:
            e['person_id'] = previous_person
            e['person_name'] = state.get('person_name')
            e.pop('needs_clarification', None)
        else:
            e['needs_clarification'] = True

    return parsed


def update_state(parsed, state, last_result_ids=None):
    e = parsed['entities']

    # A new search by month or relationship replaces
    # the previous person-specific context.
    if any(key in e for key in (
        'month', 'relationship', 'relative_date', 'relative_month'
    )):
        state.pop('person_id', None)
        state.pop('person_name', None)

    # Remember a newly identified person.
    if 'person_id' in e:
        state['person_id'] = e['person_id']
        state['person_name'] = e.get('person_name')

    for key in ('month', 'relationship'):
        if key in e:
            state[key] = e[key]

    if last_result_ids is not None:
        state['last_result_ids'] = last_result_ids

    return state
