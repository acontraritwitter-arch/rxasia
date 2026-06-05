import "./globals.css";

import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import { SiteHeader } from "@/components/layout/site-header";
import { ThemeProvider } from "@/components/providers/theme-provider";

const montserrat = Montserrat({
  subsets: ["latin", "cyrillic"],
  weight: ["400", "500", "600"],
  display: "swap",
  variable: "--font-montserrat",
});

export const metadata: Metadata = {
  title: "RXAsia",
  description:
    "Empowering business with tech excellence. Your trusted partners in digital future.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={montserrat.variable} data-theme="dark" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <a
            href="#main"
            className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-overlay focus:rounded-lg focus:bg-brand focus:px-4 focus:py-2 focus:text-canvas"
          >
            Skip to main content
          </a>
          <SiteHeader />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
