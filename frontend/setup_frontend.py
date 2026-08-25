import os
import json

base_dir = r"c:\Users\PC-ACER\Documents\GEHealthCare\frontend"

directories = [
    "src/app",
    "src/app/policy",
    "src/app/hospitals",
    "src/app/hospitals/[id]",
    "src/app/coverage",
    "src/app/journey",
    "src/app/chat",
    "src/app/verification",
    "src/app/data-sources",
    "src/app/fhir",
    "src/components/ui",
    "src/lib",
    "src/types",
    "public"
]

files = {}

files["package.json"] = """{
  "name": "hospitality-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.4",
    "react": "^18",
    "react-dom": "^18",
    "lucide-react": "^0.395.0",
    "recharts": "^2.12.7",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.3.0",
    "class-variance-authority": "^0.7.0"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "eslint": "^8",
    "eslint-config-next": "14.2.4"
  }
}
"""

files["tsconfig.json"] = """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

files["tailwind.config.js"] = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        ge: {
          blue: "#005EB8",
          light: "#E1F1FD",
          dark: "#00478B"
        }
      },
    },
  },
  plugins: [],
};
"""

files["postcss.config.js"] = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

files["src/app/globals.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #f8fafc;
  --foreground: #0f172a;
}
"""

files["src/lib/utils.ts"] = """import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""

files["src/types/index.ts"] = """export type DataConfidence = "AUTHORITATIVE" | "PUBLIC_VERIFIED" | "SIMULATED" | "NEEDS_VERIFICATION";
export type DataStatus = "ACTIVE" | "ARCHIVED" | "PENDING";

export interface Provenance {
  source_id: string;
  retrieved_at: string;
  data_status: DataStatus;
  confidence: DataConfidence;
}

export interface Hospital {
  id: string;
  name: string;
  city: string;
  pincode: string;
  specialty: string[];
  provenance: Provenance;
}

export interface RoomType {
  id: string;
  hospital_id: string;
  name: string;
  is_ac: boolean;
  provenance: Provenance;
}

export interface BedInventory {
  hospital_id: string;
  room_type_id: string;
  total_beds: parseInt;
  available_beds: parseInt;
  last_updated: string;
  provenance: Provenance;
}

export interface Tariff {
  hospital_id: string;
  room_type_id: string;
  daily_rate: number;
  provenance: Provenance;
}

export interface Policy {
  id: string;
  user_id: string;
  policy_number: string;
  insurer: string;
  room_rent_limit: number | null;
  room_rent_type: string | null;
  provenance: Provenance;
}

export interface MatchResult {
  hospital_id: string;
  score: number;
  reasons: string[];
}

export interface ProportionateDeductionResult {
  allowed_room_rent: number;
  actual_tariff: number;
  proportionate_factor: number;
  surgeon_fee_deduction: number;
  net_patient_share: number;
}
"""

files["src/lib/api.ts"] = """import { Hospital, RoomType, BedInventory, Tariff, Policy, MatchResult, ProportionateDeductionResult } from '../types';

const API_BASE = "http://localhost:8000/api/v1";

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  if (!res.ok) throw new Error(`API Error: ${res.statusText}`);
  return res.json();
}

export const api = {
  getHospitals: () => fetchAPI('/hospitals'),
  getHospital: (id: string) => fetchAPI(`/hospitals/${id}`),
  searchHospitals: (query: string) => fetchAPI(`/hospitals/search?q=${query}`),
  getPolicy: (id: string) => fetchAPI(`/policies/${id}`),
  simulateDeductions: (data: any) => fetchAPI('/simulate', { method: 'POST', body: JSON.stringify(data) }),
};
"""

files["src/components/ui/data-confidence-badge.tsx"] = """import React from 'react';
import { DataConfidence } from '@/types';
import { ShieldCheck, ShieldAlert, ShieldQuestion, BrainCircuit } from 'lucide-react';
import { cn } from '@/lib/utils';

export function DataConfidenceBadge({ confidence }: { confidence: DataConfidence }) {
  const config = {
    AUTHORITATIVE: { color: 'bg-green-100 text-green-800', icon: ShieldCheck, label: 'Authoritative' },
    PUBLIC_VERIFIED: { color: 'bg-blue-100 text-blue-800', icon: ShieldCheck, label: 'Verified' },
    SIMULATED: { color: 'bg-purple-100 text-purple-800', icon: BrainCircuit, label: 'Simulated' },
    NEEDS_VERIFICATION: { color: 'bg-orange-100 text-orange-800', icon: ShieldQuestion, label: 'Needs Verification' },
  };
  
  const { color, icon: Icon, label } = config[confidence] || config.NEEDS_VERIFICATION;
  
  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded text-xs font-medium", color)}>
      <Icon className="w-3 h-3 mr-1" />
      {label}
    </span>
  );
}
"""

files["src/app/layout.tsx"] = """import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'HOSPITALITY - GE Healthcare',
  description: 'Precision Care Challenge 2026',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="bg-yellow-100 p-2 text-center text-sm font-semibold text-yellow-900 border-b border-yellow-200">
          DISCLAIMER: This system provides non-binding decision support and estimates. Not medical or financial advice.
        </div>
        <div className="flex h-screen overflow-hidden">
          <aside className="w-64 bg-ge-dark text-white p-4">
            <h1 className="text-xl font-bold mb-8">GE HealthCare</h1>
            <nav className="space-y-2">
              <a href="/" className="block p-2 hover:bg-ge-blue rounded">Dashboard</a>
              <a href="/policy" className="block p-2 hover:bg-ge-blue rounded">Policy</a>
              <a href="/hospitals" className="block p-2 hover:bg-ge-blue rounded">Hospitals</a>
              <a href="/coverage" className="block p-2 hover:bg-ge-blue rounded">Coverage Simulator</a>
              <a href="/journey" className="block p-2 hover:bg-ge-blue rounded">Care Journey</a>
              <a href="/chat" className="block p-2 hover:bg-ge-blue rounded">Patient AI</a>
              <a href="/verification" className="block p-2 hover:bg-ge-blue rounded">Data Audit</a>
            </nav>
          </aside>
          <main className="flex-1 overflow-y-auto p-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
"""

files["src/app/page.tsx"] = """export default function Home() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold text-lg mb-2">Active Policy</h2>
          <p className="text-gray-600">Policy #123456 - Star Health</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold text-lg mb-2">Recommended Hospitals</h2>
          <p className="text-gray-600">3 Hospitals near you</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="font-semibold text-lg mb-2">Live Bed Status</h2>
          <p className="text-gray-600">45 Beds Available Globally</p>
        </div>
      </div>
    </div>
  );
}
"""

files["src/app/policy/page.tsx"] = """export default function PolicyPage() { return <div>Policy Management (PDF OCR)</div>; }"""
files["src/app/hospitals/page.tsx"] = """export default function HospitalsPage() { return <div>Hospital Search & Map</div>; }"""
files["src/app/hospitals/[id]/page.tsx"] = """export default function HospitalDetail() { return <div>Hospital Deep Dive</div>; }"""
files["src/app/coverage/page.tsx"] = """export default function CoveragePage() { return <div>Cost Simulator</div>; }"""
files["src/app/journey/page.tsx"] = """export default function JourneyPage() { return <div>Care Journey Tracker</div>; }"""
files["src/app/chat/page.tsx"] = """export default function ChatPage() { return <div>AI Patient Assistant</div>; }"""
files["src/app/verification/page.tsx"] = """export default function VerificationPage() { return <div>Verification Center</div>; }"""
files["src/app/data-sources/page.tsx"] = """export default function DataSourcesPage() { return <div>Data Ops & Provenance</div>; }"""
files["src/app/fhir/page.tsx"] = """export default function FHIRPage() { return <div>FHIR Interoperability</div>; }"""

import os
for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

for path, content in files.items():
    with open(os.path.join(base_dir, path), 'w', encoding='utf-8') as f:
        f.write(content)

print("Setup Complete")
