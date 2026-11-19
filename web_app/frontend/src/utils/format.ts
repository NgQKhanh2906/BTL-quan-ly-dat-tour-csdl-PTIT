export function formatVnd(amount: number | null | undefined): string {
  if (amount === null || amount === undefined || Number.isNaN(Number(amount))) {
    return '0 đ';
  }
  const rounded = Math.round(Number(amount));
  const formatted = new Intl.NumberFormat('vi-VN').format(rounded);
  return `${formatted} đ`;
}

function pad2(n: number): string {
  return String(n).padStart(2, '0');
}

function parseIsoParts(iso: string | null | undefined): {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  second: number;
} | null {
  if (!iso) return null;
  const cleaned = iso.trim().replace(' ', 'T');
  const match = cleaned.match(
    /^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2})(?::(\d{2}))?)?/
  );
  if (!match) {
    const parsed = new Date(iso);
    if (Number.isNaN(parsed.getTime())) return null;
    return {
      year: parsed.getFullYear(),
      month: parsed.getMonth() + 1,
      day: parsed.getDate(),
      hour: parsed.getHours(),
      minute: parsed.getMinutes(),
      second: parsed.getSeconds(),
    };
  }
  return {
    year: Number(match[1]),
    month: Number(match[2]),
    day: Number(match[3]),
    hour: Number(match[4] ?? 0),
    minute: Number(match[5] ?? 0),
    second: Number(match[6] ?? 0),
  };
}

export function formatDateTime(iso: string | null | undefined): string {
  const p = parseIsoParts(iso);
  if (!p) return '—';
  return `${pad2(p.day)}/${pad2(p.month)}/${p.year} ${pad2(p.hour)}:${pad2(p.minute)}`;
}

export function formatDate(iso: string | null | undefined): string {
  const p = parseIsoParts(iso);
  if (!p) return '—';
  return `${pad2(p.day)}/${pad2(p.month)}/${p.year}`;
}

export function toSqlDateTimeInput(date: string, time: string): string {
  const cleanDate = (date || '').trim();
  const cleanTime = (time || '00:00').trim();
  if (!cleanDate) return '';
  const timeWithSeconds = cleanTime.length === 5 ? `${cleanTime}:00` : cleanTime;
  return `${cleanDate}T${timeWithSeconds}`;
}

export function extractDatePart(iso: string | null | undefined): string {
  const p = parseIsoParts(iso);
  if (!p) return '';
  return `${p.year}-${pad2(p.month)}-${pad2(p.day)}`;
}

export function extractTimePart(iso: string | null | undefined): string {
  const p = parseIsoParts(iso);
  if (!p) return '08:00';
  return `${pad2(p.hour)}:${pad2(p.minute)}`;
}

export function shiftHoursToDateAndTime(
  iso: string | null | undefined,
  deltaHours: number
): { date: string; time: string } {
  const p = parseIsoParts(iso);
  if (!p) return { date: '', time: '06:00' };
  const dt = new Date(p.year, p.month - 1, p.day, p.hour, p.minute, p.second);
  dt.setHours(dt.getHours() + deltaHours);
  return {
    date: `${dt.getFullYear()}-${pad2(dt.getMonth() + 1)}-${pad2(dt.getDate())}`,
    time: `${pad2(dt.getHours())}:${pad2(dt.getMinutes())}`,
  };
}

export function formatDuration(soDem: number): string {
  if (soDem <= 0) return '1 ngày (trong ngày)';
  return `${soDem + 1} ngày ${soDem} đêm`;
}

export function getInitials(fullName: string | null | undefined): string {
  if (!fullName) return 'BV';
  const parts = fullName.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return 'BV';
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
}
