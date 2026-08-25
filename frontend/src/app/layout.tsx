import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import { ShieldAlert } from 'lucide-react';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'HOSPITALITY - GE Healthcare',
  description: 'Precision Care Challenge 2026',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="bg-amber-100 flex items-center justify-center p-2 text-sm font-semibold text-amber-900 border-b border-amber-200">
          <ShieldAlert className="w-4 h-4 mr-2" />
          DISCLAIMER: This system provides non-binding decision support and estimates. Not medical or financial advice.
        </div>
        <div className="flex h-[calc(100vh-40px)] overflow-hidden">
          <aside className="w-64 bg-ge-dark text-white p-6 shadow-xl flex flex-col">
            <div className="mb-8 flex items-center gap-2">
              <span className="text-2xl font-bold tracking-tight">HOSPITALITY</span>
            </div>
            <nav className="space-y-1 flex-1">
              {[
                { href: '/', label: 'Dashboard' },
                { href: '/policy', label: 'Policy Analysis' },
                { href: '/hospitals', label: 'Hospitals' },
                { href: '/coverage', label: 'Coverage Simulator' },
                { href: '/journey', label: 'Care Journey' },
                { href: '/chat', label: 'Patient AI' },
                { href: '/verification', label: 'Data Audit' },
                { href: '/data-sources', label: 'Data Sources' },
                { href: '/fhir', label: 'FHIR Viewer' },
              ].map(link => (
                <Link key={link.href} href={link.href} className="block px-3 py-2 rounded-md hover:bg-ge-blue transition-colors text-sm font-medium text-slate-200 hover:text-white">
                  {link.label}
                </Link>
              ))}
            </nav>
            <div className="mt-auto text-xs text-ge-light opacity-60">
              GE Healthcare Precision Care Challenge 2026
            </div>
          </aside>
          <main className="flex-1 overflow-y-auto bg-slate-50">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
