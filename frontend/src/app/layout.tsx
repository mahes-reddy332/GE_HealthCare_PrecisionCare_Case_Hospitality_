import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'HOSPITALITY — Policy-Aware Healthcare Navigation',
  description: 'GE Healthcare Precision Care Challenge 2026',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} bg-[#070D1E] text-slate-100 antialiased`}>
        {children}
      </body>
    </html>
  );
}
