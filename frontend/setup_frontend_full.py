import os

base_dir = r"c:\Users\PC-ACER\Documents\GEHealthCare\frontend"

directories = [
    "src/app", "src/app/policy", "src/app/hospitals", "src/app/hospitals/[id]", 
    "src/app/coverage", "src/app/journey", "src/app/chat", "src/app/verification", 
    "src/app/data-sources", "src/app/fhir", "src/components/ui", "src/lib", 
    "src/types", "public"
]

files = {}

files["src/types/index.ts"] = '''export type DataConfidence = "AUTHORITATIVE" | "PUBLIC_VERIFIED" | "SIMULATED" | "NEEDS_VERIFICATION";
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
  total_beds: number;
  available_beds: number;
  last_updated: string;
  provenance: Provenance;
}

export interface Tariff {
  hospital_id: string;
  room_type_id: string;
  daily_rate: number;
  provenance: Provenance;
}

export interface Scheme {
  id: string;
  name: string;
}

export interface InsuranceNetwork {
  id: string;
  insurer: string;
  hospital_ids: string[];
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

export interface PolicyClause {
  id: string;
  text: string;
}

export interface PolicyExclusion {
  id: string;
  description: string;
}

export interface PolicyExtracted extends Policy {
  clauses: PolicyClause[];
  exclusions: PolicyExclusion[];
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
  co_pay: number;
  net_patient_share: number;
}

export interface CostBreakdownEstimate {
  hospital_id: string;
  procedure_id: string;
  room_type_id: string;
  deduction_result: ProportionateDeductionResult;
}

export type JourneyStage = "PRE_ADMISSION" | "ADMISSION" | "INVESTIGATION" | "PROCEDURE" | "RECOVERY" | "DISCHARGE" | "CLAIM";

export interface JourneyEvent {
  id: string;
  stage: JourneyStage;
  timestamp: string;
  description: string;
}

export interface PatientJourney {
  id: string;
  patient_id: string;
  events: JourneyEvent[];
  current_stage: JourneyStage;
}

export interface Citation {
  text: string;
  source: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  reply: string;
  citations: Citation[];
}
'''

files["src/lib/api.ts"] = '''import { 
  Hospital, RoomType, BedInventory, Tariff, Policy, MatchResult, 
  ProportionateDeductionResult, PatientJourney, JourneyEvent, ChatResponse 
} from '../types';

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
  getHospitalRooms: (id: string) => fetchAPI(`/hospitals/${id}/rooms`),
  getHospitalBeds: (id: string) => fetchAPI(`/hospitals/${id}/beds`),
  getHospitalTariffs: (id: string) => fetchAPI(`/hospitals/${id}/tariffs`),
  
  uploadPolicy: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return fetch(`${API_BASE}/policies/upload`, { method: 'POST', body: formData }).then(r => r.json());
  },
  createPolicyManual: (data: any) => fetchAPI('/policies', { method: 'POST', body: JSON.stringify(data) }),
  getMockPolicy: () => fetchAPI('/policies/mock'),
  getPolicy: (id: string) => fetchAPI(`/policies/${id}`),
  
  matchHospitals: (data: any) => fetchAPI('/hospitals/match', { method: 'POST', body: JSON.stringify(data) }),
  simulateDeductions: (data: any) => fetchAPI('/simulate', { method: 'POST', body: JSON.stringify(data) }),
  checkRoomFit: (data: any) => fetchAPI('/simulate/room-fit', { method: 'POST', body: JSON.stringify(data) }),
  
  getPatientJourney: (id: string) => fetchAPI(`/journeys/${id}`),
  addJourneyEvent: (id: string, event: any) => fetchAPI(`/journeys/${id}/events`, { method: 'POST', body: JSON.stringify(event) }),
  
  queryChatbot: (query: string) => fetchAPI('/chat', { method: 'POST', body: JSON.stringify({ query }) }),
  
  getDataSources: () => fetchAPI('/data-sources'),
  getDataQuality: () => fetchAPI('/data-quality'),
  
  getFHIRCoverage: (id: string) => fetchAPI(`/fhir/coverage/${id}`),
  getFHIRLocation: (id: string) => fetchAPI(`/fhir/location/${id}`),
};
'''

files["src/components/ui/card.tsx"] = '''import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("rounded-xl border bg-card text-card-foreground shadow", className)} {...props} />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(({ className, ...props }, ref) => (
  <h3 ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
))
CardTitle.displayName = "CardTitle"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardContent }
'''

files["src/components/ui/badge.tsx"] = '''import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div className={cn("inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2", className)} {...props} />
  )
}
export { Badge }
'''

files["src/components/ui/button.tsx"] = '''import * as React from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, ...props }, ref) => {
  return (
    <button ref={ref} className={cn("inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-ge-blue text-white shadow hover:bg-ge-dark h-9 px-4 py-2", className)} {...props} />
  )
})
Button.displayName = "Button"
export { Button }
'''

files["src/app/globals.css"] = '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: #f8fafc;
  --foreground: #0f172a;
  --card: #ffffff;
  --card-foreground: #0f172a;
  --border: #e2e8f0;
}
body {
  background-color: var(--background);
  color: var(--foreground);
}
'''

files["src/app/layout.tsx"] = '''import './globals.css';
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
'''

files["src/app/page.tsx"] = '''import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ShieldCheck, Activity, Users, FileText } from "lucide-react"

export default function Home() {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Active Policy</CardTitle>
            <FileText className="w-4 h-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Policy #8942-A</div>
            <p className="text-xs text-slate-500 mt-1">Star Health Comprehensive</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Recommended Hospitals</CardTitle>
            <Activity className="w-4 h-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-slate-500 mt-1">Cashless network matches</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Live Bed Availability</CardTitle>
            <Users className="w-4 h-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">148</div>
            <p className="text-xs text-slate-500 mt-1">Available across top 5 hospitals</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Data Source Health</CardTitle>
            <ShieldCheck className="w-4 h-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-700">Healthy</div>
            <p className="text-xs text-slate-500 mt-1">All 8 integrations active</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
'''

files["src/app/policy/page.tsx"] = '''import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
export default function PolicyPage() { 
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Policy Upload & Analysis</h1>
      <Card className="max-w-2xl">
        <CardHeader><CardTitle>Upload Policy PDF</CardTitle></CardHeader>
        <CardContent>
          <div className="border-2 border-dashed border-slate-300 rounded-lg p-12 text-center">
            <p className="text-slate-500 mb-4">Drag and drop your policy document here</p>
            <button className="bg-ge-blue text-white px-4 py-2 rounded">Select File</button>
          </div>
        </CardContent>
      </Card>
    </div>
  ); 
}'''

files["src/app/hospitals/page.tsx"] = '''export default function HospitalsPage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Hospital Search & Map</h1></div>; 
}'''

files["src/app/hospitals/[id]/page.tsx"] = '''export default function HospitalDetail() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Hospital Deep Dive</h1></div>; 
}'''

files["src/app/coverage/page.tsx"] = '''export default function CoveragePage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Cost & Proportionate Deduction Simulator</h1></div>; 
}'''

files["src/app/journey/page.tsx"] = '''export default function JourneyPage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Care Journey State Machine</h1></div>; 
}'''

files["src/app/chat/page.tsx"] = '''export default function ChatPage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Patient AI Assistant</h1></div>; 
}'''

files["src/app/verification/page.tsx"] = '''export default function VerificationPage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Verification Center</h1></div>; 
}'''

files["src/app/data-sources/page.tsx"] = '''export default function DataSourcesPage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">Data Ops & Provenance</h1></div>; 
}'''

files["src/app/fhir/page.tsx"] = '''export default function FHIRPage() { 
  return <div className="p-8"><h1 className="text-2xl font-bold">FHIR Viewer</h1></div>; 
}'''

import os
for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

for path, content in files.items():
    with open(os.path.join(base_dir, path), 'w', encoding='utf-8') as f:
        f.write(content)

print("Setup Complete")
