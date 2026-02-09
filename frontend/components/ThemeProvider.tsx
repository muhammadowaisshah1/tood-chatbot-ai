'use client';

import { ThemeProvider as NextThemesProvider } from 'next-themes';
import { ReactNode } from 'react';

/**
 * Theme Provider Component
 *
 * Wraps the application with next-themes provider for dark mode support.
 *
 * Features:
 * - System preference detection
 * - Persistent theme selection
 * - No flash of unstyled content (FOUC)
 * - Smooth transitions between themes
 */
export default function ThemeProvider({ children }: { children: ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange={false}
    >
      {children}
    </NextThemesProvider>
  );
}
