/**
 * PriorityBadge Component
 *
 * Displays a colored badge for task priority levels with icon and label.
 * Features:
 * - Color-coded by priority (high=red, medium=yellow, low=green)
 * - Icon representation
 * - Dark mode support
 * - Accessible with title attribute
 */

import { PRIORITIES, PRIORITY_COLORS } from '@/lib/constants';

interface PriorityBadgeProps {
  priority: string | null;
  size?: 'sm' | 'md';
}

export default function PriorityBadge({ priority, size = 'sm' }: PriorityBadgeProps) {
  if (!priority) return null;

  const pri = PRIORITIES.find(p => p.value === priority);
  if (!pri) return null;

  const sizeClasses = size === 'sm' ? 'px-2.5 py-1 text-xs' : 'px-3 py-1.5 text-sm';

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-medium border ${PRIORITY_COLORS[pri.color]} ${sizeClasses}`}
      title={`Priority: ${pri.label}`}
    >
      <span>{pri.icon}</span>
      <span>{pri.label}</span>
    </span>
  );
}
