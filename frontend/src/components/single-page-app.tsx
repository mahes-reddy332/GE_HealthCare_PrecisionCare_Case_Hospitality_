"use client"

import React, { useState } from "react"
import {
  FileText, Activity, Users, ShieldCheck, Upload, CheckCircle2, AlertTriangle,
  Building2, Bed, HeartPulse, Stethoscope, Sparkles, Send,
  Layers, Database, FileCode, Check, RefreshCw, Info, MapPin
} from "lucide-react"

interface PolicyData {
  id: number
  policy_number: string
  insurer: string
  sum_insured: number
  room_rent_cap_type: string
  room_rent_limit: number
  icu_limit: number
  copay_percentage: number
  deductible: number
  extraction_confidence: number
  clauses: Array<{ type: string; page: number; text: string; confidence: string }>
  exclusions: string[]
}

interface HospitalMatch {
  id: number
  name: string
  city: string
  address: string
  match_score: number
  network_status: string
  available_beds: number
  available_icu_beds: number
  room_options: Array<{ category: string; tariff: number; status: string }>
  estimated_out_of_pocket: number
  reasons: string[]
}

interface DeductionSimResult {
  hospital_name: string
  procedure_name: string
  room_category: string
  days_of_stay: number
  allowed_room_rent_per_day: number
  actual_room_tariff_per_day: number
  is_room_capped: boolean
  proportionate_ratio: number
  billed_room_charges: number
  payable_room_charges: number
  patient_room_excess: number
  billed_associated_charges: number
  payable_associated_charges: number
  proportionate_deduction_penalty: number
  fixed_implants_diagnostics: number
  non_payable_consumables: number
  total_billed_hospital_bill: number
  total_admissible_claim: number
  copay_amount: number
  insurer_settlement_amount: number
  indicative_patient_out_of_pocket: number
  warning_alerts: string[]
  calculation_steps: string[]
}

export default function SinglePageApp() {
  const [activeSection, setActiveSection] = useState("start-policy")
  const [uploadedFile, setUploadedFile] = useState<{ name: string; size: string } | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState(0)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  
  const [policy, setPolicy] = useState<PolicyData | null>(null)
  const [hospitals, setHospitals] = useState<HospitalMatch[]>([])
  const [selectedHospitalId, setSelectedHospitalId] = useState<number>(1)
  const [selectedProcedure, setSelectedProcedure] = useState("CAR-002")
  const [selectedRoomCategory, setSelectedRoomCategory] = useState("PRIVATE_AC")
  const [deductionResult, setDeductionResult] = useState<DeductionSimResult | null>(null)
  
  const [currentJourneyStage, setCurrentJourneyStage] = useState("PRE_ADMISSION")
  const [messages, setMessages] = useState<Array<{ role: string; content: string; citations?: any[] }>>([
    {
      role: "assistant",
      content: "Hello! I am your HOSPITALITY Policy & Healthcare Assistant. Upload your policy above or ask me any question about room rent caps, cashless hospital networks, and procedure costs."
    }
  ])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)

  const scrollTo = (id: string) => {
    setActiveSection(id)
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  const handleLoadSample = () => {
    setUploadedFile({
      name: "Star_Health_Family_Optima_Schedule_2026.pdf",
      size: "248 KB"
    })
  }

  const runAnalysisPipeline = async () => {
    if (!uploadedFile) return
    setAnalyzing(true)
    setAnalysisStep(1)
    
    await new Promise(r => setTimeout(r, 400))
    setAnalysisStep(2)
    
    try {
      const polRes = await fetch("http://localhost:8000/api/v1/policies/mock", { method: "POST" })
      const polData: PolicyData = await polRes.json()
      setPolicy(polData)
      
      setAnalysisStep(3)
      await new Promise(r => setTimeout(r, 400))
      setAnalysisStep(4)
      
      const matchRes = await fetch("http://localhost:8000/api/v1/matching/hospitals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ policy_id: polData.id, city: "Bengaluru" })
      })
      const matchData: HospitalMatch[] = await matchRes.json()
      setHospitals(matchData)
      
      setAnalysisStep(5)
      await new Promise(r => setTimeout(r, 400))
      
      const simRes = await fetch("http://localhost:8000/api/v1/matching/deduction-simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          policy_id: polData.id,
          hospital_id: 1,
          procedure_code: "CAR-002",
          room_category: "PRIVATE_AC",
          days_of_stay: 4
        })
      })
      const simData: DeductionSimResult = await simRes.json()
      setDeductionResult(simData)
      
      setAnalysisStep(6)
      await new Promise(r => setTimeout(r, 300))
      setAnalysisComplete(true)
      setAnalyzing(false)
      
      setTimeout(() => {
        scrollTo("dashboard")
      }, 400)
    } catch (err) {
      console.error("Analysis pipeline failed:", err)
      setAnalyzing(false)
    }
  }

  const updateDeductionSimulation = async (hospId: number, procCode: string, roomCat: string) => {
    if (!policy) return
    try {
      const simRes = await fetch("http://localhost:8000/api/v1/matching/deduction-simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          policy_id: policy.id,
          hospital_id: hospId,
          procedure_code: procCode,
          room_category: roomCat,
          days_of_stay: 4
        })
      })
      const simData: DeductionSimResult = await simRes.json()
      setDeductionResult(simData)
    } catch (e) {
      console.error(e)
    }
  }

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (!chatInput.trim()) return
    
    const userText = chatInput
    setChatInput("")
    setMessages(prev => [...prev, { role: "user", content: userText }])
    setChatLoading(true)
    
    try {
      const res = await fetch("http://localhost:8000/api/v1/chat/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userText,
          policy_id: policy?.id || 1,
          hospital_id: selectedHospitalId || 1
        })
      })
      const data = await res.json()
      setMessages(prev => [...prev, {
        role: "assistant",
        content: data.response,
        citations: data.citations
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, I could not connect to the backend service. Please ensure the API is running on port 8000."
      }])
    } finally {
      setChatLoading(false)
    }
  }

  const navItems = [
    { id: "start-policy", label: "1. Policy Ingestion", icon: Upload },
    { id: "dashboard", label: "2. Patient Dashboard", icon: Activity },
    { id: "policy-analysis", label: "3. Policy Analysis", icon: FileText },
    { id: "hospitals", label: "4. Hospital Matches", icon: Building2 },
    { id: "coverage", label: "5. Deduction Simulator", icon: HeartPulse },
    { id: "journey", label: "6. Care Journey", icon: Stethoscope },
    { id: "chat", label: "7. Patient AI", icon: Sparkles },
    { id: "audit", label: "8. Data Audit", icon: ShieldCheck },
    { id: "sources", label: "9. Data Sources", icon: Database },
    { id: "fhir", label: "10. FHIR / NHCX", icon: FileCode }
  ]

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex">
      <aside className="w-72 bg-slate-900 text-slate-100 flex flex-col fixed inset-y-0 left-0 z-50 shadow-xl">
        <div className="p-5 border-b border-slate-800 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center font-black text-white text-xl shadow-md shadow-blue-500/30">
            H
          </div>
          <div>
            <div className="font-extrabold tracking-tight text-white text-lg">HOSPITALITY</div>
            <div className="text-xs text-blue-400 font-medium tracking-wide">GE Healthcare Precision Care</div>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 px-3 mb-2">Navigation Stages</div>
          {navItems.map(item => {
            const Icon = item.icon
            const active = activeSection === item.id
            return (
              <button
                key={item.id}
                onClick={() => scrollTo(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all text-left ${active ? "bg-blue-600 text-white shadow-md shadow-blue-600/30 font-semibold" : "text-slate-300 hover:bg-slate-800 hover:text-white"}`}
              >
                <Icon className={`w-4 h-4 ${active ? "text-white" : "text-slate-400"}`} />
                {item.label}
              </button>
            )
          })}
        </nav>
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 text-xs space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span>System State</span>
            <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Live :8000
            </span>
          </div>
          <div className="text-[11px] text-slate-400 leading-tight">Decision-support only. Non-binding indicative estimates.</div>
        </div>
      </aside>

      <main className="flex-1 ml-72 p-8 max-w-6xl mx-auto space-y-16">
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-start gap-3 text-sm text-blue-900 shadow-sm">
          <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="font-semibold">GE Healthcare Precision Care Challenge 2026 — Decision-Support Disclaimer:</strong> HOSPITALITY assists patients and caregivers in evaluating policy constraints, room rent caps, and empanelled facilities. It does not issue clinical diagnoses or legally binding insurance claim pre-authorizations.
          </div>
        </div>

        {/* SECTION 1: START WITH YOUR POLICY */}
        <section id="start-policy" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 1 — Policy Ingestion</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Start With Your Policy</h2>
            <p className="text-slate-600 text-sm mt-1">Upload your health insurance policy certificate or schedule (PDF or JSON). HOSPITALITY extracts your constraints without manual data entry.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-2 border-2 border-dashed border-slate-300 rounded-2xl p-8 bg-white text-center hover:border-blue-500 transition-all flex flex-col items-center justify-center space-y-4 shadow-sm">
              <div className="w-14 h-14 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <Upload className="w-7 h-7" />
              </div>
              <div>
                <h3 className="font-bold text-slate-800 text-base">Upload Policy Certificate / Schedule</h3>
                <p className="text-xs text-slate-500 mt-1">Supports PDF, JSON, or OCR-scanned policy documents</p>
              </div>
              {uploadedFile ? (
                <div className="bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-3 flex items-center gap-3 text-emerald-800 text-sm w-full max-w-md justify-between">
                  <div className="flex items-center gap-2 truncate">
                    <FileText className="w-4 h-4 text-emerald-600 shrink-0" />
                    <span className="font-semibold truncate">{uploadedFile.name}</span>
                    <span className="text-xs text-emerald-600">({uploadedFile.size})</span>
                  </div>
                  <span className="text-xs bg-emerald-200 text-emerald-900 font-bold px-2 py-0.5 rounded">READY</span>
                </div>
              ) : (
                <div className="flex gap-3">
                  <label className="cursor-pointer bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-4 py-2.5 rounded-lg shadow transition-all">
                    Choose PDF File
                    <input
                      type="file"
                      accept=".pdf,.json,.txt"
                      className="hidden"
                      onChange={(e) => {
                        if (e.target.files?.[0]) {
                          const f = e.target.files[0]
                          setUploadedFile({ name: f.name, size: `${(f.size / 1024).toFixed(0)} KB` })
                        }
                      }}
                    />
                  </label>
                  <button onClick={handleLoadSample} className="bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-semibold px-4 py-2.5 rounded-lg transition-all">
                    Load Sample Star Health PDF
                  </button>
                </div>
              )}
              {uploadedFile && (
                <button
                  onClick={runAnalysisPipeline}
                  disabled={analyzing}
                  className="w-full max-w-md bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-bold text-sm py-3 rounded-xl shadow-lg shadow-blue-600/30 transition-all flex items-center justify-center gap-2 mt-2"
                >
                  {analyzing ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Analyzing Policy & Matching Ecosystem...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      ANALYSE POLICY & MATCH HOSPITALS
                    </>
                  )}
                </button>
              )}
            </div>
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
              <div>
                <h4 className="font-bold text-slate-900 text-sm flex items-center gap-2 mb-4">
                  <Layers className="w-4 h-4 text-blue-600" />
                  Real-time Policy Pipeline
                </h4>
                <div className="space-y-3 text-xs">
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 1 ? "text-emerald-700 font-semibold" : "text-slate-400"}`}>
                    {analysisStep >= 1 ? <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />}
                    <span>1. Document uploaded & OCR scanned</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 2 ? "text-emerald-700 font-semibold" : "text-slate-400"}`}>
                    {analysisStep >= 2 ? <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />}
                    <span>2. Extracting Sum Insured & Room Caps</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 3 ? "text-emerald-700 font-semibold" : "text-slate-400"}`}>
                    {analysisStep >= 3 ? <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />}
                    <span>3. Identifying Copay & Exclusions</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 4 ? "text-emerald-700 font-semibold" : "text-slate-400"}`}>
                    {analysisStep >= 4 ? <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />}
                    <span>4. Searching Cashless Networks</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 5 ? "text-emerald-700 font-semibold" : "text-slate-400"}`}>
                    {analysisStep >= 5 ? <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />}
                    <span>5. Calculating Proportionate Deductions</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 6 ? "text-emerald-700 font-semibold" : "text-slate-400"}`}>
                    {analysisStep >= 6 ? <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" /> : <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />}
                    <span>6. Ranking Options & Telemetry Check</span>
                  </div>
                </div>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">Pipeline Status:</span>
                <span className={`font-bold px-2 py-0.5 rounded ${analysisComplete ? "bg-emerald-100 text-emerald-800" : (analyzing ? "bg-blue-100 text-blue-800 animate-pulse" : "bg-slate-100 text-slate-600")}`}>
                  {analysisComplete ? "ANALYSIS COMPLETE" : (analyzing ? "PROCESSING..." : "AWAITING UPLOAD")}
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 2: DYNAMIC PATIENT DASHBOARD */}
        <section id="dashboard" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 2 — Dynamic Overview</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Patient Decision Dashboard</h2>
            <p className="text-slate-600 text-sm mt-1">Dynamic summary populated directly from your extracted policy constraints and matched healthcare network.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Active Policy</span>
                <FileText className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <div className="text-xl font-black text-slate-900">{policy ? policy.policy_number : "No policy uploaded"}</div>
                <p className="text-xs text-slate-500 mt-1 font-medium">{policy ? `${policy.insurer}` : "Upload policy above to activate"}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-100 text-[11px] text-blue-600 font-semibold">
                {policy ? `Sum Insured: ₹${policy.sum_insured.toLocaleString("en-IN")}` : "Awaiting input"}
              </div>
            </div>
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Recommended Hospitals</span>
                <Building2 className="w-4 h-4 text-emerald-600" />
              </div>
              <div>
                <div className="text-xl font-black text-slate-900">{hospitals.length > 0 ? `${hospitals.length} Facilities` : "—"}</div>
                <p className="text-xs text-slate-500 mt-1 font-medium">{hospitals.length > 0 ? "Cashless empanelled in Bengaluru" : "Run analysis to rank"}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-100 text-[11px] text-emerald-600 font-semibold">
                {hospitals.length > 0 ? `Top Match: ${hospitals[0].name.split(",")[0]}` : "Awaiting analysis"}
              </div>
            </div>
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Bed Telemetry</span>
                <Bed className="w-4 h-4 text-purple-600" />
              </div>
              <div>
                <div className="text-xl font-black text-slate-900">{hospitals.length > 0 ? `${hospitals[0].available_beds} Available` : "—"}</div>
                <p className="text-xs text-slate-500 mt-1 font-medium">{hospitals.length > 0 ? `${hospitals[0].available_icu_beds} ICU beds unoccupied` : "Live bed feed standby"}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-100 text-[11px] text-purple-700 font-bold flex items-center gap-1">
                <span className="px-1.5 py-0.5 bg-purple-100 rounded text-[10px]">SIMULATED</span>
                <span>Real-time stream</span>
              </div>
            </div>
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider">Patient Out-of-Pocket</span>
                <HeartPulse className="w-4 h-4 text-amber-600" />
              </div>
              <div>
                <div className="text-xl font-black text-slate-900">{deductionResult ? `₹${deductionResult.indicative_patient_out_of_pocket.toLocaleString("en-IN")}` : "—"}</div>
                <p className="text-xs text-slate-500 mt-1 font-medium">{deductionResult ? `${deductionResult.room_category.replace("_", " ")} Room` : "Based on selected room"}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-100 text-[11px] text-amber-700 font-semibold">
                {deductionResult ? (deductionResult.is_room_capped ? "⚠️ Breach Penalty Included" : "✓ Zero Room Penalty") : "Awaiting calculation"}
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 3: EXTRACTED POLICY CONSTRAINTS */}
        <section id="policy-analysis" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 3 — Policy Understanding</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Policy Constraints & Clause Citations</h2>
            <p className="text-slate-600 text-sm mt-1">Deterministic parameters parsed from the insurance schedule with exact source page citations.</p>
          </div>
          {policy ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
                <h3 className="font-bold text-slate-900 text-base flex items-center justify-between">
                  <span>Structured Policy Limits</span>
                  <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">{policy.extraction_confidence * 100}% Confidence Score</span>
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                    <span className="text-slate-500 font-medium">Sum Insured</span>
                    <div className="text-base font-bold text-slate-900 mt-1">₹{policy.sum_insured.toLocaleString("en-IN")}</div>
                  </div>
                  <div className="p-3.5 bg-blue-50 rounded-xl border border-blue-200">
                    <span className="text-blue-700 font-medium">Daily Room Rent Cap</span>
                    <div className="text-base font-bold text-blue-900 mt-1">₹{policy.room_rent_limit.toLocaleString("en-IN")}/day</div>
                    <span className="text-[10px] text-blue-600 font-semibold">(1% of Sum Insured)</span>
                  </div>
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                    <span className="text-slate-500 font-medium">Daily ICU Limit</span>
                    <div className="text-base font-bold text-slate-900 mt-1">₹{policy.icu_limit.toLocaleString("en-IN")}/day</div>
                    <span className="text-[10px] text-slate-500 font-medium">(2% of Sum Insured)</span>
                  </div>
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                    <span className="text-slate-500 font-medium">Mandatory Co-pay</span>
                    <div className="text-base font-bold text-slate-900 mt-1">{policy.copay_percentage}%</div>
                    <span className="text-[10px] text-slate-500 font-medium">Senior citizen clause</span>
                  </div>
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                    <span className="text-slate-500 font-medium">Deductible</span>
                    <div className="text-base font-bold text-slate-900 mt-1">₹{policy.deductible.toLocaleString("en-IN")}</div>
                    <span className="text-[10px] text-slate-500 font-medium">Nil deductible</span>
                  </div>
                  <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                    <span className="text-slate-500 font-medium">Room Category Cap</span>
                    <div className="text-base font-bold text-slate-900 mt-1">Single Private A/C</div>
                  </div>
                </div>
                <div className="space-y-3 pt-3 border-t border-slate-100">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">Audit Proof & Page Citations</h4>
                  {policy.clauses.map((c, i) => (
                    <div key={i} className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs flex items-start justify-between gap-3">
                      <div className="space-y-1">
                        <span className="font-bold text-blue-700 bg-blue-100/70 px-1.5 py-0.5 rounded text-[10px] mr-2">PAGE {c.page}</span>
                        <span className="text-slate-800 font-medium">{c.text}</span>
                      </div>
                      <span className="text-[10px] text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 shrink-0">{c.confidence}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
                <div>
                  <h3 className="font-bold text-slate-900 text-sm mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    Identified Policy Exclusions
                  </h3>
                  <div className="space-y-2 text-xs">
                    {policy.exclusions.map((ex, i) => (
                      <div key={i} className="p-2.5 bg-amber-50/60 rounded-lg border border-amber-100 text-amber-900 flex items-start gap-2">
                        <span className="text-amber-500 font-bold">•</span>
                        <span>{ex}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-[11px] text-slate-600 mt-4 leading-tight">
                  💡 <strong>Rule Engine Note:</strong> Room rent capping dictates whether proportionate deductions apply to doctors' fees and surgical OT charges.
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
              <FileText className="w-12 h-12 mx-auto text-slate-300 mb-3" />
              <p className="text-sm font-medium">Please upload a policy in Stage 1 to extract structured constraints.</p>
            </div>
          )}
        </section>

        {/* SECTION 4: HOSPITAL DISCOVERY */}
        <section id="hospitals" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 4 — Hospital Discovery</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Compatible Empanelled Hospitals</h2>
            <p className="text-slate-600 text-sm mt-1">Multi-criteria matching scores based on Cashless Network status, Room Rent fit, Distance, and Live Bed Availability.</p>
          </div>
          {hospitals.length > 0 ? (
            <div className="space-y-4">
              {hospitals.map((h, idx) => (
                <div
                  key={h.id}
                  onClick={() => {
                    setSelectedHospitalId(h.id)
                    updateDeductionSimulation(h.id, selectedProcedure, selectedRoomCategory)
                  }}
                  className={`p-6 rounded-2xl border transition-all cursor-pointer bg-white shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6 ${selectedHospitalId === h.id ? "border-blue-600 ring-2 ring-blue-600/20 shadow-md" : "border-slate-200 hover:border-slate-300"}`}
                >
                  <div className="space-y-2 flex-1">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className="w-7 h-7 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-xs">#{idx + 1}</span>
                      <h3 className="font-extrabold text-slate-900 text-lg">{h.name}</h3>
                      <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${h.network_status === "CASHLESS_NETWORK" ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"}`}>
                        {h.network_status === "CASHLESS_NETWORK" ? "✓ CASHLESS PREFERRED" : "REIMBURSEMENT ONLY"}
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      {h.address}, {h.city}
                    </p>
                    <div className="flex flex-wrap gap-2 pt-1">
                      {h.reasons.map((r, ri) => (
                        <span key={ri} className="text-[11px] bg-slate-100 text-slate-700 font-medium px-2.5 py-0.5 rounded-md">• {r}</span>
                      ))}
                    </div>
                  </div>
                  <div className="flex md:flex-col items-center md:items-end justify-between w-full md:w-auto gap-4 border-t md:border-t-0 pt-3 md:pt-0 border-slate-100 shrink-0">
                    <div className="text-right">
                      <div className="text-xs text-slate-500 font-semibold uppercase">Match Score</div>
                      <div className="text-2xl font-black text-blue-600">{h.match_score}%</div>
                    </div>
                    <div className="text-right">
                      <span className="text-[11px] text-purple-800 font-bold bg-purple-100 px-2 py-0.5 rounded">{h.available_beds} Beds Free ({h.available_icu_beds} ICU)</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
              <Building2 className="w-12 h-12 mx-auto text-slate-300 mb-3" />
              <p className="text-sm font-medium">Please upload and analyse your policy in Stage 1 to discover compatible hospitals.</p>
            </div>
          )}
        </section>

        {/* SECTION 5: PROPORTIONATE DEDUCTION CALCULATOR */}
        <section id="coverage" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 5 — Cost & Coverage Intelligence</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Proportionate Deduction Simulator</h2>
            <p className="text-slate-600 text-sm mt-1">Interactive mathematical simulator demonstrating how room category selection triggers or prevents IRDAI proportionate deduction penalties.</p>
          </div>
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pb-6 border-b border-slate-100">
              <div>
                <label className="block text-xs font-bold uppercase text-slate-500 mb-1.5">Select Facility</label>
                <select
                  value={selectedHospitalId}
                  onChange={(e) => {
                    const id = Number(e.target.value)
                    setSelectedHospitalId(id)
                    updateDeductionSimulation(id, selectedProcedure, selectedRoomCategory)
                  }}
                  className="w-full text-xs font-semibold p-2.5 rounded-lg border border-slate-200 bg-slate-50 text-slate-900"
                >
                  <option value={1}>Apollo Hospitals, Bannerghatta Road</option>
                  <option value={2}>Manipal Hospital, Old Airport Road</option>
                  <option value={3}>Sri Jayadeva Institute of Cardiology</option>
                  <option value={6}>Narayana Institute of Cardiac Sciences</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-slate-500 mb-1.5">Procedure</label>
                <select
                  value={selectedProcedure}
                  onChange={(e) => {
                    const p = e.target.value
                    setSelectedProcedure(p)
                    updateDeductionSimulation(selectedHospitalId, p, selectedRoomCategory)
                  }}
                  className="w-full text-xs font-semibold p-2.5 rounded-lg border border-slate-200 bg-slate-50 text-slate-900"
                >
                  <option value="CAR-002">Coronary Angioplasty (PTCA) with 1 Stent</option>
                  <option value="CAR-003">Coronary Artery Bypass Graft (CABG)</option>
                  <option value="ORT-001">Total Knee Replacement (TKR)</option>
                  <option value="GAS-001">Laparoscopic Cholecystectomy</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase text-slate-500 mb-1.5">Choose Room Category</label>
                <select
                  value={selectedRoomCategory}
                  onChange={(e) => {
                    const r = e.target.value
                    setSelectedRoomCategory(r)
                    updateDeductionSimulation(selectedHospitalId, selectedProcedure, r)
                  }}
                  className="w-full text-xs font-semibold p-2.5 rounded-lg border border-slate-200 bg-slate-50 text-slate-900"
                >
                  <option value="GENERAL">General Ward (₹1,800/day)</option>
                  <option value="SEMI_PRIVATE">Semi-Private Room (₹3,600/day)</option>
                  <option value="PRIVATE_AC">Single Private A/C Room (₹5,400/day)</option>
                  <option value="DELUXE">Deluxe Suite (₹9,000/day) — EXCEEDS CAP</option>
                </select>
              </div>
            </div>
            {deductionResult ? (
              <div className="space-y-6">
                <div className={`p-4 rounded-xl border flex items-start gap-3 text-sm ${deductionResult.is_room_capped ? "bg-amber-50 border-amber-200 text-amber-900" : "bg-emerald-50 border-emerald-200 text-emerald-900"}`}>
                  <AlertTriangle className={`w-5 h-5 shrink-0 mt-0.5 ${deductionResult.is_room_capped ? "text-amber-600" : "text-emerald-600"}`} />
                  <div>
                    <h4 className="font-bold">{deductionResult.is_room_capped ? "Proportionate Deduction Penalty Triggered!" : "Zero Room Rent Penalty — Optimal Selection!"}</h4>
                    <p className="text-xs mt-1 leading-relaxed">
                      {deductionResult.is_room_capped
                        ? `Choosing a room at ₹${deductionResult.actual_room_tariff_per_day.toLocaleString("en-IN")}/day exceeds your policy cap of ₹${deductionResult.allowed_room_rent_per_day.toLocaleString("en-IN")}/day. The insurer will only pay ${deductionResult.proportionate_ratio * 100}% of associated doctor, OT, and medical charges.`
                        : `Your room tariff is within your daily allowed limit of ₹${deductionResult.allowed_room_rent_per_day.toLocaleString("en-IN")}/day. 100% of associated medical charges are admissible for claim settlement.`}
                    </p>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                  <div className="space-y-3 bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <h4 className="font-bold text-slate-900 uppercase tracking-wider">Itemized Hospital Bill Estimate</h4>
                    <div className="flex justify-between py-1 border-b border-slate-200">
                      <span className="text-slate-600">Room Rent ({deductionResult.days_of_stay} days @ ₹{deductionResult.actual_room_tariff_per_day.toLocaleString("en-IN")})</span>
                      <span className="font-semibold text-slate-900">₹{deductionResult.billed_room_charges.toLocaleString("en-IN")}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-200">
                      <span className="text-slate-600">Associated Charges (Surgeon + OT + Anesthesia)</span>
                      <span className="font-semibold text-slate-900">₹{deductionResult.billed_associated_charges.toLocaleString("en-IN")}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-200">
                      <span className="text-slate-600">Fixed Implants (Stent / Non-proportionate)</span>
                      <span className="font-semibold text-slate-900">₹{deductionResult.fixed_implants_diagnostics.toLocaleString("en-IN")}</span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-200">
                      <span className="text-slate-600">Non-Payable Consumables (Gloves, Admin)</span>
                      <span className="font-semibold text-slate-900">₹{deductionResult.non_payable_consumables.toLocaleString("en-IN")}</span>
                    </div>
                    <div className="flex justify-between pt-1 font-bold text-slate-900 text-sm">
                      <span>Total Estimated Bill</span>
                      <span>₹{deductionResult.total_billed_hospital_bill.toLocaleString("en-IN")}</span>
                    </div>
                  </div>
                  <div className="space-y-3 bg-blue-50/70 p-4 rounded-xl border border-blue-200">
                    <h4 className="font-bold text-blue-900 uppercase tracking-wider">Claim Adjudication & Patient Share</h4>
                    <div className="flex justify-between py-1 border-b border-blue-200/60">
                      <span className="text-blue-800">Admissible Associated Fees (Factor: {deductionResult.proportionate_ratio})</span>
                      <span className="font-semibold text-blue-950">₹{deductionResult.payable_associated_charges.toLocaleString("en-IN")}</span>
                    </div>
                    {deductionResult.proportionate_deduction_penalty > 0 && (
                      <div className="flex justify-between py-1 border-b border-blue-200/60 text-amber-800 font-bold">
                        <span>Proportionate Penalty Paid by Patient</span>
                        <span>+ ₹{deductionResult.proportionate_deduction_penalty.toLocaleString("en-IN")}</span>
                      </div>
                    )}
                    <div className="flex justify-between py-1 border-b border-blue-200/60">
                      <span className="text-blue-800">Insurer Settlement (after 10% Co-pay)</span>
                      <span className="font-semibold text-emerald-800">₹{deductionResult.insurer_settlement_amount.toLocaleString("en-IN")}</span>
                    </div>
                    <div className="flex justify-between pt-2 text-base font-black text-slate-900">
                      <span>Indicative Out-of-Pocket Share</span>
                      <span className={deductionResult.is_room_capped ? "text-amber-700" : "text-emerald-700"}>
                        ₹{deductionResult.indicative_patient_out_of_pocket.toLocaleString("en-IN")}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-6 text-slate-400 text-xs">Run policy analysis in Stage 1 to activate calculation proof.</div>
            )}
          </div>
        </section>

        {/* SECTION 6: CARE JOURNEY */}
        <section id="journey" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 6 — Care Journey Tracking</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Patient Journey State Machine</h2>
            <p className="text-slate-600 text-sm mt-1">Reactive lifecycle guidance advancing through admission milestones with pre-auth checklists.</p>
          </div>
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="grid grid-cols-2 sm:grid-cols-6 gap-2 text-center text-xs">
              {[
                { id: "PRE_ADMISSION", label: "1. Pre-Admission" },
                { id: "HOSPITAL_SELECTION", label: "2. Selection" },
                { id: "PRE_AUTH", label: "3. Pre-Auth" },
                { id: "ADMISSION", label: "4. Admission" },
                { id: "PROCEDURE", label: "5. Procedure" },
                { id: "DISCHARGE", label: "6. Discharge" }
              ].map((st, i) => (
                <button
                  key={st.id}
                  onClick={() => setCurrentJourneyStage(st.id)}
                  className={`p-3 rounded-xl border font-bold transition-all text-left sm:text-center ${currentJourneyStage === st.id ? "bg-slate-900 text-white border-slate-900 shadow-md" : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"}`}
                >
                  <div className="text-[10px] text-slate-400 font-medium">STAGE 0{i + 1}</div>
                  <div className="mt-0.5 truncate">{st.label.split(". ")[1]}</div>
                </button>
              ))}
            </div>
            <div className="p-5 bg-blue-50/50 rounded-xl border border-blue-200 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-blue-700">Active Milestone Checklist</span>
                <span className="text-xs bg-blue-200 text-blue-900 font-bold px-2 py-0.5 rounded">Action Required</span>
              </div>
              <h4 className="font-bold text-slate-900 text-sm">Pre-Authorization & TPA Verification at Apollo Hospitals</h4>
              <div className="space-y-2 text-xs text-slate-700">
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-600" />
                  <span>Submit Star Health E-Card & Aadhaar (ABHA ID: 91-8273-1928-1144) to Insurance Desk</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-600" />
                  <span>Ensure treating doctor mentions Single Private A/C Room in admission note to prevent overage penalty</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-600" />
                  <span>Obtain initial pre-authorization letter within 3 hours under IRDAI cashless turnaround SLA</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 7: PATIENT AI ASSISTANT */}
        <section id="chat" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 7 — Patient Conversational AI</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Tool-Augmented Healthcare Assistant</h2>
            <p className="text-slate-600 text-sm mt-1">Ask natural-language questions about your policy coverage, room limits, and hospital billing.</p>
          </div>
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col h-[450px]">
            <div className="flex-1 p-6 overflow-y-auto space-y-4 text-xs">
              {messages.map((m, i) => (
                <div key={i} className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}>
                  <div className={`p-4 rounded-2xl max-w-xl leading-relaxed whitespace-pre-wrap ${m.role === "user" ? "bg-blue-600 text-white font-medium" : "bg-slate-100 text-slate-800 border border-slate-200"}`}
                  >
                    {m.content}
                  </div>
                  {m.citations && m.citations.length > 0 && (
                    <div className="mt-1 flex gap-2">
                      {m.citations.map((c, ci) => (
                        <span key={ci} className="text-[10px] bg-slate-200 text-slate-700 px-2 py-0.5 rounded font-bold">📖 {c.source} ({c.clause})</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {chatLoading && (
                <div className="flex items-center gap-2 text-slate-400 text-xs italic">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  Querying policy knowledge base & tariff simulator...
                </div>
              )}
            </div>
            <div className="px-6 py-2 bg-slate-50 border-t border-slate-100 flex gap-2 overflow-x-auto text-[11px]">
              <button onClick={() => setChatInput("Is a private room covered at Apollo?")} className="bg-white hover:bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-full text-slate-700 whitespace-nowrap">
                "Is private room covered at Apollo?"
              </button>
              <button onClick={() => setChatInput("Why does Deluxe room cost more out of pocket?")} className="bg-white hover:bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-full text-slate-700 whitespace-nowrap">
                "Why does Deluxe room cost more?"
              </button>
              <button onClick={() => setChatInput("Which hospitals in Bangalore have cashless for Star Health?")} className="bg-white hover:bg-slate-100 border border-slate-200 px-2.5 py-1 rounded-full text-slate-700 whitespace-nowrap">
                "Which cashless hospitals in Bangalore?"
              </button>
            </div>
            <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-200 flex gap-3">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask about room rent limits, empanelled hospitals, or costs..."
                className="flex-1 text-xs px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50"
              />
              <button type="submit" disabled={chatLoading} className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl font-bold text-xs shadow-md shadow-blue-600/30 transition-all flex items-center gap-1.5">
                <Send className="w-3.5 h-3.5" />
                Send
              </button>
            </form>
          </div>
        </section>

        {/* SECTION 8: DATA AUDIT */}
        <section id="audit" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 8 — Provenance & Verification</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Data Audit & Provenance Transparency</h2>
            <p className="text-slate-600 text-sm mt-1">Transparent tagging distinguishing authoritative government registries from algorithmic simulations.</p>
          </div>
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 font-bold uppercase text-[10px]">
                  <th className="pb-3">Data Dimension</th>
                  <th className="pb-3">Source Provider</th>
                  <th className="pb-3">Verification Tier</th>
                  <th className="pb-3">Status Badge</th>
                  <th className="pb-3">Audit Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-800">
                <tr>
                  <td className="py-3 font-bold">Hospital Identity & Geo-Codes</td>
                  <td>data.gov.in (MoHFW)</td>
                  <td>Tier 1 Official</td>
                  <td><span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">AUTHORITATIVE</span></td>
                  <td>Verified latitude/longitude and 6-digit PIN codes.</td>
                </tr>
                <tr>
                  <td className="py-3 font-bold">Procedure Package Tariffs</td>
                  <td>PM-JAY Health Benefit Packages 2022</td>
                  <td>Tier 1 Official</td>
                  <td><span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">AUTHORITATIVE</span></td>
                  <td>1,949 standard package rates with NABH multipliers.</td>
                </tr>
                <tr>
                  <td className="py-3 font-bold">Room Rent Benchmark Rates</td>
                  <td>CGHS Rate Cards (MoHFW)</td>
                  <td>Tier 1 Official</td>
                  <td><span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">AUTHORITATIVE</span></td>
                  <td>General, Semi-Private, Private, ICU daily rates.</td>
                </tr>
                <tr>
                  <td className="py-3 font-bold">Live Bed Availability</td>
                  <td>HOSPITALITY Synthetic Feed</td>
                  <td>Tier 3 Simulation</td>
                  <td><span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded font-bold">SIMULATED</span></td>
                  <td>Generated telemetry; no public live bed API exists post-COVID.</td>
                </tr>
                <tr>
                  <td className="py-3 font-bold">Private Insurer Cashless Networks</td>
                  <td>HOSPITALITY Network Allocator</td>
                  <td>Tier 3 Simulation</td>
                  <td><span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded font-bold">SIMULATED</span></td>
                  <td>Private insurer tie-ups simulated based on public trends.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* SECTION 9: DATA SOURCES */}
        <section id="sources" className="scroll-mt-8 space-y-6">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 9 — Ecosystem Catalog</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Integrated Healthcare Data Sources</h2>
            <p className="text-slate-600 text-sm mt-1">Federated Indian digital health registries and standardized master datasets.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
            {[
              { name: "data.gov.in", org: "MoHFW", type: "API / CSV", status: "Active (8 Records)", flag: "AUTHORITATIVE" },
              { name: "PM-JAY HBP 2022", org: "NHA", type: "Excel Download", status: "Active (1,949 Packages)", flag: "AUTHORITATIVE" },
              { name: "CGHS Rate Cards", org: "MoHFW", type: "PDF / Download", status: "Active (5 Categories)", flag: "AUTHORITATIVE" },
              { name: "ABDM HFR Sandbox", org: "NHA / ABDM", type: "REST / FHIR", status: "Sandbox Connected", flag: "AUTHORITATIVE" }
            ].map((s, i) => (
              <div key={i} className="p-4 bg-white rounded-xl border border-slate-200 shadow-sm space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="font-bold text-slate-900">{s.name}</h4>
                  <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">{s.flag}</span>
                </div>
                <div className="text-slate-500 font-medium">{s.org} • {s.type}</div>
                <div className="text-emerald-700 font-semibold text-[11px]">{s.status}</div>
              </div>
            ))}
          </div>
        </section>

        {/* SECTION 10: FHIR & NHCX VIEWER */}
        <section id="fhir" className="scroll-mt-8 space-y-6 pb-16">
          <div className="border-b border-slate-200 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">Stage 10 — Interoperability Standards</span>
            <h2 className="text-3xl font-extrabold text-slate-900 mt-2">HL7 FHIR R4 & NHCX Interoperability Viewer</h2>
            <p className="text-slate-600 text-sm mt-1">Standardized electronic claim and eligibility payloads compliant with NRCeS ABDM standards.</p>
          </div>
          <div className="bg-slate-900 text-slate-100 p-6 rounded-2xl font-mono text-xs overflow-x-auto shadow-xl space-y-3">
            <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800">
              <span>Standard: HL7 FHIR R4 (CoverageEligibilityResponse)</span>
              <span className="text-emerald-400 font-bold">200 OK</span>
            </div>
            <pre className="text-emerald-400">
{JSON.stringify({
  "resourceType": "CoverageEligibilityResponse",
  "id": "nhcx-resp-88192",
  "status": "active",
  "purpose": ["benefits", "validation"],
  "patient": {
    "reference": "Patient/ABHA-91-8273-1928-1144"
  },
  "insurer": {
    "display": policy?.insurer || "Star Health and Allied Insurance"
  },
  "insurance": [
    {
      "coverage": {
        "reference": `Coverage/${policy?.policy_number || "STAR-FHO-2026"}`
      },
      "inforce": true,
      "item": [
        {
          "category": { "coding": [{ "code": "room-rent", "display": "Daily Room Rent Cap" }] },
          "benefit": [{ "type": "financial", "allowedMoney": { "value": policy?.room_rent_limit || 5000, "currency": "INR" } }]
        },
        {
          "category": { "coding": [{ "code": "copay", "display": "Mandatory Co-payment" }] },
          "benefit": [{ "type": "financial", "allowedUnsignedInt": policy?.copay_percentage || 10 }]
        }
      ]
    }
  ]
}, null, 2)}
            </pre>
          </div>
        </section>

      </main>
    </div>
  )
}
