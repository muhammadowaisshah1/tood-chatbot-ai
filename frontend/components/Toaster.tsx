'use client';

import { Toaster as HotToaster } from 'react-hot-toast';

/**
 * Toaster component for displaying toast notifications.
 *
 * Features:
 * - Positioned at top-right of screen
 * - Auto-dismisses after 4 seconds
 * - Styled to match app design system
 * - Accessible with ARIA labels
 * - Supports success and error states
 */
export default function Toaster() {
  return (
    <HotToaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: '#fff',
          color: '#1f2937',
          borderRadius: '0.75rem',
          padding: '1rem',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        },
        success: {
          iconTheme: {
            primary: '#10b981',
            secondary: '#fff',
          },
        },
        error: {
          iconTheme: {
            primary: '#ef4444',
            secondary: '#fff',
          },
        },
      }}
    />
  );
}
