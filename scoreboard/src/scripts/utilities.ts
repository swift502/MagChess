export function formatTimestamp(ts: string) {
    const date = new Date(ts);
    return date.toLocaleString('cs-CZ', { hour: '2-digit', minute: '2-digit', year: 'numeric', month: '2-digit', day: '2-digit' });
}