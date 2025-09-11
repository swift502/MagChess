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