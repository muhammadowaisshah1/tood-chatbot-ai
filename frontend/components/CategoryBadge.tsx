/**
 * CategoryBadge Component
 *
 * Displays a colored badge for task categories with icon and label.
 * Features:
 * - Color-coded by category type
 * - Icon representation
 * - Dark mode support
 * - Accessible with title attribute
 */

import { CATEGORIES, CATEGORY_COLORS } from '@/lib/constants';

interface CategoryBadgeProps {
  category: string | null;
  size?: 'sm' | 'md';
}

export default function CategoryBadge({ category, size = 'sm' }: CategoryBadgeProps) {
  if (!category) return null;

  const cat = CATEGORIES.find(c => c.value === category);
  if (!cat) return null;

  const sizeClasses = size === 'sm' ? 'px-2.5 py-1 text-xs' : 'px-3 py-1.5 text-sm';

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-medium border ${CATEGORY_COLORS[cat.color]} ${sizeClasses}`}
      title={`Category: ${cat.label}`}
    >
      <span>{cat.icon}</span>
      <span>{cat.label}</span>
    </span>
  );
}
