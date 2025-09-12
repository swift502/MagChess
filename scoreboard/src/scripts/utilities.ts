export function formatTimestamp(ts: string)
{
    const date = new Date(ts);
    const dateFormat = new Intl.DateTimeFormat('cs-CZ', {
        day: 'numeric',
        month: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hourCycle: 'h23', // ensure 00–23
    });

    const parts = Object.fromEntries(dateFormat.formatToParts(date).map(p => [p.type, p.value]));
    return `${parts.day}.${parts.month}. ${parts.hour}:${parts.minute}`;
}

export function formatTimestampTooltip(ts: string)
{
    const date = new Date(ts);
    const dateFormat = new Intl.DateTimeFormat('cs-CZ', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hourCycle: 'h23', // ensure 00–23
    });

    const parts = Object.fromEntries(dateFormat.formatToParts(date).map(p => [p.type, p.value]));
    return `${parts.day}.${parts.month}.${parts.year}. ${parts.hour}:${parts.minute}:${parts.second}`;
}