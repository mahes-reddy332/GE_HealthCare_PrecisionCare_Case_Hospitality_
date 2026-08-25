import os

code = r'''"use client"

import React, { useState, useEffect } from "react"
import { 
  FileText, Activity, Users, ShieldCheck, Upload, CheckCircle2, AlertTriangle, 
  Building2, Bed, HeartPulse, Stethoscope, Sparkles, Send, 
  Layers, Database, FileCode, Check, RefreshCw, Info, MapPin, User, ArrowLeft, 
  ArrowRight, ArrowLeftRight, HelpCircle, CheckSquare, Square, ChevronDown, 
  ChevronUp, ShieldAlert, Clock, Zap, ChevronRight, X, ExternalLink, Navigation, Compass, LocateFixed
} from "lucide-react"

// Types
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

interface FacilityMatchStatus {
  name: string
  status: "AVAILABLE" | "VERIFY" | "UNAVAILABLE"
  note?: string
}

interface HospitalOption {
  id: number
  name: string
  city: string
  pincode: string
  address: string
  distance_km: number
  match_score: number
  care_fit_score: number
  match_status: "FULL MATCH" | "PARTIAL MATCH" | "NEEDS VERIFICATION" | "NOT SUITABLE"
  network_status: string
  available_beds: number
  total_beds: number
  occupied_beds: number
  available_icu_beds: number
  facilities: FacilityMatchStatus[]
  room_compatibility: string
  indicative_cost: number
  reasons: string[]
  score_breakdown: {
    facility_match: number
    network_compatibility: number
    room_fit: number
    bed_availability: number
    cost_compatibility: number
    data_confidence: number
  }
}

interface RoomOption {
  category: string
  label: string
  tariff: number
  status: "COMPATIBLE" | "EXCEEDS_CAP" | "VERIFY"
  status_text: string
  available_beds: number
  total_beds: number
  occupied_beds: number
  bed_status: "SIMULATED" | "REAL" | "STALE"
}

export default function PatientFirstHospitality() {
  // Navigation & Screen Flow State:
  // "UPLOAD" -> "FACILITY_SELECT" -> "HOSPITAL_OPTIONS" -> "DASHBOARD"
  const [activeStep, setActiveStep] = useState<"UPLOAD" | "FACILITY_SELECT" | "HOSPITAL_OPTIONS" | "DASHBOARD">("UPLOAD")
  const [activeNavSection, setActiveNavSection] = useState("overview")

  // Patient Profile
  const [patientName, setPatientName] = useState("Ananya")
  const [patientAge, setPatientAge] = useState("54")
  const [patientGender, setPatientGender] = useState("Female")
  const [patientAbha, setPatientAbha] = useState("91-8273-1928-1144")

  // Patient Location State (GPS / Manual PIN Code)
  const [patientCity, setPatientCity] = useState("Hyderabad")
  const [patientPincode, setPatientPincode] = useState("500001")
  const [locationSource, setLocationSource] = useState<"GPS_AUTO" | "MANUAL_PINCODE" | "POLICY_EXTRACTED">("MANUAL_PINCODE")
  const [detectingLocation, setDetectingLocation] = useState(false)
  const [fetchingHospitals, setFetchingHospitals] = useState(false)
  const [gpsCoords, setGpsCoords] = useState<{ lat: number; lng: number } | null>(null)

  const handleDetectLiveLocation = () => {
    setDetectingLocation(true)
    if (typeof window !== "undefined" && "geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setDetectingLocation(false)
          setGpsCoords({ lat: pos.coords.latitude, lng: pos.coords.longitude })
          setLocationSource("GPS_AUTO")
          setPatientCity("Auto-GPS")
          setPatientPincode("500001")
        },
        () => {
          setDetectingLocation(false)
          setLocationSource("MANUAL_PINCODE")
        },
        { timeout: 4000 }
      )
    } else {
      setDetectingLocation(false)
    }
  }

  // Multi-Facility Selection State
  const availableFacilityChoices = [
    { id: "cardiology", label: "Cardiology", desc: "Consultation, Echo & Diagnostics" },
    { id: "icu", label: "ICU (Intensive Care)", desc: "24/7 Cardiac & Critical Care Unit" },
    { id: "cath_lab", label: "Cath Lab", desc: "Coronary Angiography & Angioplasty" },
    { id: "emergency", label: "Emergency Care", desc: "Rapid Cardiac Resuscitation 24/7" },
    { id: "radiology", label: "Radiology & CT", desc: "64-Slice Cardiac CT & MRI" },
    { id: "dialysis", label: "Dialysis Unit", desc: "Hemodialysis with ICU backup" },
    { id: "oncology", label: "Oncology", desc: "Medical & Surgical Oncology" },
    { id: "maternity", label: "Maternity & NICU", desc: "Labour suites & Neonatal care" },
    { id: "orthopedics", label: "Orthopedics", desc: "Joint replacement & Trauma" },
    { id: "diagnostics", label: "Advanced Lab", desc: "Automated pathology & Troponin tests" }
  ]

  // Default pre-selected: ICU + Cath Lab + Emergency
  const [selectedFacilities, setSelectedFacilities] = useState<string[]>(["icu", "cath_lab", "emergency"])

  // Policy State
  const [uploadedFile, setUploadedFile] = useState<{ name: string; size: string } | null>(null)
  const [analyzingPolicy, setAnalyzingPolicy] = useState(false)
  const [analysisStep, setAnalysisStep] = useState(0)
  const [showPolicyEvidenceModal, setShowPolicyEvidenceModal] = useState(false)
  const [selectedEvidenceItem, setSelectedEvidenceItem] = useState<string | null>(null)

  const [policy, setPolicy] = useState<PolicyData>({
    id: 1,
    policy_number: "STAR-FHO-2026-9812",
    insurer: "Star Health and Allied Insurance",
    sum_insured: 500000,
    room_rent_cap_type: "1% of Sum Insured",
    room_rent_limit: 5000,
    icu_limit: 10000,
    copay_percentage: 10,
    deductible: 5000,
    extraction_confidence: 0.96,
    clauses: [
      { type: "Room Rent", page: 7, text: "Section 3.1: Room Rent, Boarding and Nursing Expenses shall be limited to 1% of Sum Insured per day.", confidence: "96% High" },
      { type: "ICU Rent", page: 7, text: "Section 3.2: Intensive Care Unit (ICU) expenses shall be limited to 2% of Sum Insured per day.", confidence: "94% High" },
      { type: "Co-payment", page: 12, text: "Section 5.4: A mandatory 10% co-payment applies to all eligible claims for policyholders above 50 years.", confidence: "98% High" },
      { type: "Pre-Auth", page: 18, text: "Section 7.1: Cashless pre-authorisation request must be submitted at least 48 hours prior to planned admission.", confidence: "95% High" }
    ],
    exclusions: ["Cosmetic and aesthetic treatments", "Non-prescribed dietary supplements", "External durable medical equipment unless critical"]
  })

  // Dynamic Hospitals List from Backend API
  const [hospitalList, setHospitalList] = useState<HospitalOption[]>([])
  const [selectedHospital, setSelectedHospital] = useState<HospitalOption | null>(null)
  const [showMatchScoreModal, setShowMatchScoreModal] = useState(false)
  const [showHospitalSwitcherModal, setShowHospitalSwitcherModal] = useState(false)

  // Fetch Hospitals from Backend API
  const fetchMatchingHospitals = async () => {
    setFetchingHospitals(true)
    try {
      const res = await fetch("http://localhost:8000/api/v1/matching/hospitals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          city: patientCity,
          pincode: patientPincode,
          facilities: selectedFacilities,
          policy_id: policy.id,
          lat: gpsCoords?.lat,
          lng: gpsCoords?.lng,
          radius_km: 40.0
        })
      })
      const data: HospitalOption[] = await res.json()
      if (data && data.length > 0) {
        setHospitalList(data)
        if (!selectedHospital || !data.find(h => h.id === selectedHospital.id)) {
          setSelectedHospital(data[0])
        }
      }
    } catch (err) {
      console.error("Failed to query hospital matching backend:", err)
    } finally {
      setFetchingHospitals(false)
    }
  }

  // Interactive Room Selection State
  const roomTiers: Record<string, RoomOption> = {
    GENERAL: {
      category: "GENERAL",
      label: "General Ward",
      tariff: 1900,
      status: "COMPATIBLE",
      status_text: "✓ Policy compatible (Zero Penalty)",
      available_beds: 16,
      total_beds: 80,
      occupied_beds: 64,
      bed_status: "SIMULATED"
    },
    SEMI_PRIVATE: {
      category: "SEMI_PRIVATE",
      label: "Semi-Private Room",
      tariff: 4200,
      status: "COMPATIBLE",
      status_text: "✓ Policy compatible (Within ₹5,000 cap)",
      available_beds: 6,
      total_beds: 30,
      occupied_beds: 24,
      bed_status: "SIMULATED"
    },
    PRIVATE: {
      category: "PRIVATE",
      label: "Single Private Room",
      tariff: 7800,
      status: "EXCEEDS_CAP",
      status_text: "⚠ Exceeds policy room limit of ₹5,000/day",
      available_beds: 4,
      total_beds: 25,
      occupied_beds: 21,
      bed_status: "SIMULATED"
    },
    ICU: {
      category: "ICU",
      label: "ICU (Critical Care)",
      tariff: 11500,
      status: "VERIFY",
      status_text: "⚠ Critical care authorization required",
      available_beds: 4,
      total_beds: 18,
      occupied_beds: 14,
      bed_status: "SIMULATED"
    }
  }

  const [selectedRoomKey, setSelectedRoomKey] = useState<string>("SEMI_PRIVATE")
  const currentRoom = roomTiers[selectedRoomKey]

  // Dynamic Financial & Deduction Calculation
  const calculateFinancials = (room: RoomOption) => {
    const days = 4
    const actualDailyTariff = room.tariff
    const allowedDailyTariff = policy.room_rent_limit // ₹5,000

    const billedRoomTotal = actualDailyTariff * days
    const payableRoomTotal = Math.min(actualDailyTariff, allowedDailyTariff) * days
    const roomExcessPaidByPatient = billedRoomTotal - payableRoomTotal

    const isRoomCapped = actualDailyTariff > allowedDailyTariff
    const proportionateRatio = isRoomCapped ? allowedDailyTariff / actualDailyTariff : 1.0

    const billedAssociatedCharges = 45000 // Surgeon + OT + Anesthesia
    const payableAssociatedCharges = billedAssociatedCharges * proportionateRatio
    const proportionatePenalty = billedAssociatedCharges - payableAssociatedCharges

    const fixedStentsAndDiagnostics = 25000 // Stents (non-proportionate)
    const nonPayableConsumables = 6000

    const totalHospitalBill = billedRoomTotal + billedAssociatedCharges + fixedStentsAndDiagnostics + nonPayableConsumables
    const totalAdmissibleClaim = payableRoomTotal + payableAssociatedCharges + fixedStentsAndDiagnostics
    const copayAmount = totalAdmissibleClaim * (policy.copay_percentage / 100)
    const insurerSettlement = totalAdmissibleClaim - copayAmount
    const patientOutofPocket = totalHospitalBill - insurerSettlement

    return {
      totalHospitalBill,
      totalAdmissibleClaim,
      insurerSettlement,
      patientOutofPocket,
      proportionatePenalty,
      isRoomCapped,
      proportionateRatio,
      copayAmount,
      billedRoomTotal,
      roomExcessPaidByPatient
    }
  }

  const financials = calculateFinancials(currentRoom)

  // Capability Node detail
  const [selectedCapabilityNode, setSelectedCapabilityNode] = useState<{
    name: string
    status: string
    source: string
    freshness: string
    details: string
  } | null>(null)

  // Chatbot State ("ASK HOSPITALITY")
  const [chatMessages, setChatMessages] = useState<Array<{ role: string; content: string; citations?: any[] }>>([
    {
      role: "assistant",
      content: `Hello Ananya! I am ASK HOSPITALITY. I am actively tracking your Star Health policy (₹5,00,000 SI), your current location in ${patientCity} (PIN ${patientPincode}), your requested care (${selectedFacilities.map(f => f.toUpperCase()).join(" + ")}), and ${selectedHospital?.name || "your matched facility"}. How can I assist your admission decision today?`
    }
  ])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)

  // Handle Facility Toggle
  const toggleFacility = (facilityId: string) => {
    setSelectedFacilities(prev => 
      prev.includes(facilityId) ? prev.filter(f => f !== facilityId) : [...prev, facilityId]
    )
  }

  // Handle Policy Upload & Analysis Trigger
  const handleUploadAndAnalyze = async () => {
    if (!uploadedFile) return
    setAnalyzingPolicy(true)
    setAnalysisStep(1)
    await new Promise(r => setTimeout(r, 400))
    setAnalysisStep(2)
    await new Promise(r => setTimeout(r, 400))
    setAnalysisStep(3)
    await new Promise(r => setTimeout(r, 400))
    setAnalysisStep(4)
    setAnalyzingPolicy(false)
    setActiveStep("FACILITY_SELECT")
  }

  // Handle Proceed to Hospital Matches
  const handleProceedToMatches = async () => {
    await fetchMatchingHospitals()
    setActiveStep("HOSPITAL_OPTIONS")
  }

  // Handle Chat Query
  const handleSendChatMessage = (textToSend?: string) => {
    const query = textToSend || chatInput
    if (!query.trim()) return

    const hospName = selectedHospital?.name || "Apollo Hospitals, Jubilee Hills"
    const hospDist = selectedHospital?.distance_km ?? 3.2

    setChatInput("")
    setChatMessages(prev => [...prev, { role: "user", content: query }])
    setChatLoading(true)

    setTimeout(() => {
      let reply = ""
      let citations: any[] = []

      const q = query.toLowerCase()
      if (q.includes("private room") || q.includes("why is private room not recommended") || q.includes("not recommended")) {
        reply = `**Why Single Private Room is not recommended for Ananya:**\n\n` +
          `1. **Room Rent Limit Breach**: Your Star Health policy limits room rent to **1% of Sum Insured = ₹5,000/day** (Section 3.1, Page 7).\n` +
          `2. **Actual Tariff**: A Single Private Room at ${hospName} costs **₹${currentRoom.tariff.toLocaleString("en-IN")}/day**.\n` +
          `3. **IRDAI Proportionate Deduction Penalty**: Choosing this room triggers a proportionate factor of $\\gamma = 5,000 / ${currentRoom.tariff.toLocaleString("en-IN")}$. The insurer will deduct **penalty (₹${financials.proportionatePenalty.toLocaleString("en-IN")})** from doctor, surgeon, and OT charges!\n` +
          `4. **Financial Impact**: Your out-of-pocket responsibility jumps from **₹21,800** in Semi-Private to **₹${financials.patientOutofPocket.toLocaleString("en-IN")}** in Private Room.\n\n` +
          `**Recommendation**: Stay in the **Semi-Private Room** to enjoy 100% admissible coverage with zero proportionate penalty.`
        citations = [
          { source: "Uploaded Policy Document", clause: "Section 3.1: Room Rent Cap (1% of SI)", page: 7 },
          { source: `${hospName} Tariff Card`, clause: "Single Private Room vs Semi-Private Schedule", page: 1 }
        ]
      } else if (q.includes("recommend") || q.includes("why was this hospital recommended") || q.includes("apollo") || q.includes("yashoda") || q.includes("care")) {
        reply = `**Why ${hospName} was recommended for Ananya:**\n\n` +
          `• **100% Need Coverage**: Provides all your selected facilities: **${selectedFacilities.map(f => f.toUpperCase()).join(", ")}**.\n` +
          `• **Network Empanelment**: Empanelled on Star Health's **Cashless Preferred Network** for instant electronic pre-authorisation.\n` +
          `• **Room Compatibility**: Semi-Private rooms fall safely below your ₹5,000 daily cap.\n` +
          `• **Proximity**: Located **${hospDist} km** from your location in **${patientCity} (PIN ${patientPincode})**.\n` +
          `• **Bed Availability**: General and ICU beds currently unoccupied (Simulated Telemetry).`
        citations = [
          { source: "data.gov.in / ABDM HFR", clause: "Facility Location Registry", page: 1 },
          { source: "Star Health Network Master", clause: "Hospital Empanelment Agreement", page: 3 }
        ]
      } else if (q.includes("verify") || q.includes("what do i need to verify")) {
        reply = `**Actionable Pre-Admission Checklist for Ananya at ${hospName}:**\n\n` +
          `1. **TPA Cashless Pre-Authorisation**: Submit Star Health E-Card & ABHA ID (${patientAbha}) at the hospital insurance desk at least 48h prior.\n` +
          `2. **Admission Slip Confirmation**: Ensure doctor's note specifies **Semi-Private Room** to prevent unexpected overage.\n` +
          `3. **Consumables List**: Review hospital non-payable list (gloves, sanitizers, admin fees) estimated at ₹6,000.`
        citations = [
          { source: "IRDAI Cashless Standard Guidelines", clause: "SLA for Cashless Authorisation", page: 2 }
        ]
      } else {
        reply = `Based on Ananya's Star Health policy (₹5,00,000 SI) at ${hospName} (${hospDist} km from PIN ${patientPincode}), you are currently configured for **${currentRoom.label}** with an indicative out-of-pocket responsibility of **₹${financials.patientOutofPocket.toLocaleString("en-IN")}**. Is there a specific procedure, room overage rule, or pre-auth step you would like to explore?`
      }

      setChatMessages(prev => [...prev, { role: "assistant", content: reply, citations }])
      setChatLoading(false)
    }, 400)
  }

  const scrollToSection = (id: string) => {
    setActiveNavSection(id)
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  return (
    <div className="min-h-screen bg-[#070D1E] text-slate-100 font-sans antialiased selection:bg-teal-500 selection:text-white">
      
      {/* ========================================================================= */}
      {/* SCREEN 1: PATIENT POLICY INGESTION */}
      {/* ========================================================================= */}
      {activeStep === "UPLOAD" && (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-b from-[#070D1E] via-[#0B1530] to-[#070D1E]">
          <div className="w-full max-w-4xl space-y-8 animate-fadeIn">
            
            {/* Brand Header */}
            <div className="text-center space-y-3">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-teal-950/80 border border-teal-500/30 text-teal-400 text-xs font-bold tracking-wide shadow-lg shadow-teal-950/50">
                <Sparkles className="w-3.5 h-3.5 text-teal-400 animate-pulse" />
                GE Healthcare Precision Care Challenge 2026
              </div>
              <h1 className="text-4xl sm:text-5xl font-black tracking-tight text-white">
                HOSPITALITY
              </h1>
              <p className="text-slate-400 text-sm sm:text-base max-w-xl mx-auto leading-relaxed">
                Policy-Aware Healthcare Navigation & Coverage Intelligence. Upload your policy to unlock tailored care options.
              </p>
            </div>

            {/* Ingestion Surface */}
            <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-8 shadow-2xl backdrop-blur-xl space-y-6">
              
              {/* Patient Profile Details */}
              <div className="border-b border-slate-700/60 pb-5">
                <span className="text-[11px] font-bold uppercase tracking-widest text-teal-400 flex items-center gap-1.5 mb-3">
                  <User className="w-3.5 h-3.5" /> Patient Identity & Current Location
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
                  <div>
                    <label className="text-slate-400 font-medium block mb-1">Patient Name</label>
                    <input 
                      type="text" 
                      value={patientName} 
                      onChange={e => setPatientName(e.target.value)} 
                      className="w-full bg-[#16254A] border border-slate-600 rounded-xl px-3 py-2 text-white font-bold focus:outline-none focus:border-teal-400"
                    />
                  </div>
                  <div>
                    <label className="text-slate-400 font-medium block mb-1">Age</label>
                    <input 
                      type="text" 
                      value={patientAge} 
                      onChange={e => setPatientAge(e.target.value)} 
                      className="w-full bg-[#16254A] border border-slate-600 rounded-xl px-3 py-2 text-white font-bold focus:outline-none focus:border-teal-400"
                    />
                  </div>
                  <div>
                    <label className="text-slate-400 font-medium block mb-1">Gender</label>
                    <select 
                      value={patientGender} 
                      onChange={e => setPatientGender(e.target.value)} 
                      className="w-full bg-[#16254A] border border-slate-600 rounded-xl px-3 py-2 text-white font-bold focus:outline-none focus:border-teal-400"
                    >
                      <option value="Female">Female</option>
                      <option value="Male">Male</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-slate-400 font-medium block mb-1">ABHA Health ID</label>
                    <input 
                      type="text" 
                      value={patientAbha} 
                      onChange={e => setPatientAbha(e.target.value)} 
                      className="w-full bg-[#16254A] border border-slate-600 rounded-xl px-3 py-2 text-white font-bold focus:outline-none focus:border-teal-400"
                    />
                  </div>
                </div>

                {/* Patient Current Location & PIN Code Capture */}
                <div className="mt-4 pt-4 border-t border-slate-700/40 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs items-end">
                  <div>
                    <label className="text-slate-400 font-medium block mb-1">Current City / District</label>
                    <input 
                      type="text" 
                      value={patientCity} 
                      onChange={e => {
                        setPatientCity(e.target.value)
                        setLocationSource("MANUAL_PINCODE")
                      }} 
                      placeholder="e.g. Hyderabad, Bengaluru, Mumbai"
                      className="w-full bg-[#16254A] border border-slate-600 rounded-xl px-3 py-2 text-white font-bold focus:outline-none focus:border-teal-400"
                    />
                  </div>
                  <div>
                    <label className="text-slate-400 font-medium block mb-1">6-Digit PIN Code</label>
                    <input 
                      type="text" 
                      value={patientPincode} 
                      onChange={e => {
                        setPatientPincode(e.target.value)
                        setLocationSource("MANUAL_PINCODE")
                      }} 
                      placeholder="e.g. 500001, 560076"
                      className="w-full bg-[#16254A] border border-slate-600 rounded-xl px-3 py-2 text-white font-bold focus:outline-none focus:border-teal-400"
                    />
                  </div>
                  <div>
                    <button
                      type="button"
                      onClick={handleDetectLiveLocation}
                      disabled={detectingLocation}
                      className="w-full bg-[#1A2C56] hover:bg-[#22396E] text-teal-300 border border-teal-500/40 px-3 py-2 rounded-xl font-bold flex items-center justify-center gap-2 transition-all"
                    >
                      {detectingLocation ? (
                        <>
                          <RefreshCw className="w-3.5 h-3.5 animate-spin text-teal-400" />
                          <span>Detecting GPS...</span>
                        </>
                      ) : (
                        <>
                          <LocateFixed className="w-3.5 h-3.5 text-teal-400" />
                          <span>Auto-Detect Live GPS</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

              </div>

              {/* Upload Dropzone */}
              <div className="border-2 border-dashed border-slate-600/80 hover:border-teal-400/80 rounded-2xl p-8 text-center bg-[#132042]/50 transition-all flex flex-col items-center justify-center space-y-4">
                <div className="w-14 h-14 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center shadow-inner">
                  <Upload className="w-7 h-7" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-base">Upload Health Insurance Policy Certificate</h3>
                  <p className="text-xs text-slate-400 mt-1">Supports PDF or Mock JSON policy schedule</p>
                </div>

                {uploadedFile ? (
                  <div className="bg-teal-950/80 border border-teal-500/40 rounded-xl px-4 py-3 flex items-center justify-between gap-3 text-sm text-teal-200 w-full max-w-md">
                    <div className="flex items-center gap-2.5 truncate">
                      <FileText className="w-4 h-4 text-teal-400 shrink-0" />
                      <span className="font-semibold truncate">{uploadedFile.name}</span>
                      <span className="text-xs text-teal-400/80">({uploadedFile.size})</span>
                    </div>
                    <span className="text-[10px] bg-teal-400 text-slate-950 font-black px-2 py-0.5 rounded">READY</span>
                  </div>
                ) : (
                  <div className="flex flex-wrap gap-3 justify-center">
                    <label className="cursor-pointer bg-teal-500 hover:bg-teal-400 text-slate-950 text-xs font-bold px-5 py-2.5 rounded-xl shadow-lg shadow-teal-500/20 transition-all">
                      Choose PDF File
                      <input 
                        type="file" 
                        accept=".pdf,.json,.txt" 
                        className="hidden" 
                        onChange={e => {
                          if (e.target.files?.[0]) {
                            const f = e.target.files[0]
                            setUploadedFile({ name: f.name, size: `${(f.size / 1024).toFixed(0)} KB` })
                          }
                        }}
                      />
                    </label>
                    <button 
                      onClick={() => setUploadedFile({ name: "Star_Health_Family_Optima_Schedule_2026.pdf", size: "248 KB" })}
                      className="bg-[#1A2C56] hover:bg-[#203668] text-teal-300 border border-teal-500/30 text-xs font-semibold px-4 py-2.5 rounded-xl transition-all"
                    >
                      Load Sample Star Health Policy
                    </button>
                  </div>
                )}

                {uploadedFile && (
                  <button
                    onClick={handleUploadAndAnalyze}
                    disabled={analyzingPolicy}
                    className="w-full max-w-md bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-400 hover:to-blue-500 text-slate-950 font-black text-sm py-3.5 rounded-xl shadow-xl shadow-teal-500/25 transition-all flex items-center justify-center gap-2 mt-2"
                  >
                    {analyzingPolicy ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                        Extracting Policy Constraints & Room Limits...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        ANALYSE POLICY & PROCEED TO FACILITY SELECTION →
                      </>
                    )}
                  </button>
                )}
              </div>

              {/* Live Extraction Stepper if active */}
              {analyzingPolicy && (
                <div className="bg-[#0A1226] rounded-2xl p-4 border border-slate-700/60 space-y-2 text-xs">
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 1 ? "text-teal-400 font-semibold" : "text-slate-500"}`}>
                    {analysisStep >= 1 ? <CheckCircle2 className="w-4 h-4 text-teal-400" /> : <Clock className="w-4 h-4" />}
                    <span>1. Reading policy schedule text via OCR</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 2 ? "text-teal-400 font-semibold" : "text-slate-500"}`}>
                    {analysisStep >= 2 ? <CheckCircle2 className="w-4 h-4 text-teal-400" /> : <Clock className="w-4 h-4" />}
                    <span>2. Extracting Sum Insured (₹5,00,000) & Room Rent Limit (₹5,000/day)</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 3 ? "text-teal-400 font-semibold" : "text-slate-500"}`}>
                    {analysisStep >= 3 ? <CheckCircle2 className="w-4 h-4 text-teal-400" /> : <Clock className="w-4 h-4" />}
                    <span>3. Identifying Co-payment (10%) & Deductible (₹5,00,000)</span>
                  </div>
                  <div className={`flex items-center gap-2.5 ${analysisStep >= 4 ? "text-teal-400 font-semibold" : "text-slate-500"}`}>
                    {analysisStep >= 4 ? <CheckCircle2 className="w-4 h-4 text-teal-400" /> : <Clock className="w-4 h-4" />}
                    <span>4. Policy constraints normalized and verified with page citations</span>
                  </div>
                </div>
              )}

            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCREEN 2: "WHAT DO YOU NEED?" (MULTI-FACILITY SELECTION) */}
      {/* ========================================================================= */}
      {activeStep === "FACILITY_SELECT" && (
        <div className="min-h-screen p-6 sm:p-10 max-w-5xl mx-auto space-y-8 animate-fadeIn">
          
          {/* Top Compact Policy & Location Pill */}
          <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-2xl p-4 shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-teal-500 text-slate-950 font-black flex items-center justify-center text-base">
                {patientName.charAt(0)}
              </div>
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-bold text-white text-sm">{patientName}</span>
                  <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded">{patientAge} Yrs, {patientGender}</span>
                  <span className="text-xs bg-teal-950 text-teal-400 font-semibold border border-teal-500/30 px-2 py-0.5 rounded">
                    {policy.insurer}
                  </span>
                  <span className="text-xs bg-blue-950 text-blue-300 font-semibold border border-blue-500/30 px-2 py-0.5 rounded flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-blue-400" />
                    <span>{patientCity} ({patientPincode})</span>
                  </span>
                </div>
                <div className="text-xs text-slate-400 mt-0.5">
                  Sum Insured: <strong className="text-slate-200">₹{policy.sum_insured.toLocaleString("en-IN")}</strong> • Daily Room Cap: <strong className="text-teal-300">₹{policy.room_rent_limit.toLocaleString("en-IN")}/day</strong>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2 self-end sm:self-center flex-wrap">
              <button 
                onClick={() => setShowPolicyEvidenceModal(true)}
                className="text-xs text-teal-400 hover:text-teal-300 bg-teal-950/60 border border-teal-500/30 px-3 py-1.5 rounded-lg font-semibold transition-all flex items-center gap-1.5"
              >
                <FileText className="w-3.5 h-3.5" /> View Policy Evidence
              </button>
              <button 
                onClick={() => setActiveStep("UPLOAD")}
                className="text-xs text-slate-400 hover:text-slate-200 bg-slate-800 px-3 py-1.5 rounded-lg transition-all"
              >
                Change Policy / Location
              </button>
            </div>
          </div>

          {/* Heading */}
          <div className="space-y-2">
            <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
              Step 2 — Healthcare Need Specification
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
              WHAT DO YOU NEED?
            </h2>
            <p className="text-slate-400 text-sm sm:text-base max-w-2xl">
              Select the facilities or services you need. We'll find hospitals near <strong>{patientCity} ({patientPincode})</strong> from official registries that can provide them while considering your policy constraints.
            </p>
          </div>

          {/* Multi-Facility Checkbox Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {availableFacilityChoices.map(item => {
              const isSelected = selectedFacilities.includes(item.id)
              return (
                <div
                  key={item.id}
                  onClick={() => toggleFacility(item.id)}
                  className={`p-5 rounded-2xl border transition-all cursor-pointer flex items-start gap-4 select-none ${
                    isSelected 
                      ? "bg-[#14234B] border-teal-400/80 shadow-lg shadow-teal-950/50 ring-1 ring-teal-400/40" 
                      : "bg-[#0D1730]/80 border-slate-700/60 hover:border-slate-500/80 hover:bg-[#111E3D]"
                  }`}
                >
                  <div className="mt-0.5">
                    {isSelected ? (
                      <CheckSquare className="w-5 h-5 text-teal-400" />
                    ) : (
                      <Square className="w-5 h-5 text-slate-500" />
                    )}
                  </div>
                  <div className="space-y-1 flex-1">
                    <div className="font-bold text-white text-sm flex items-center justify-between">
                      <span>{item.label}</span>
                      {isSelected && (
                        <span className="text-[10px] bg-teal-400 text-slate-950 font-extrabold px-1.5 py-0.2 rounded">
                          SELECTED
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-400">{item.desc}</p>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Action Bar */}
          <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
            <div className="text-xs text-slate-300">
              <span className="font-bold text-white">{selectedFacilities.length} facilities selected:</span>{" "}
              <span className="text-teal-300 font-semibold">{selectedFacilities.map(f => availableFacilityChoices.find(c => c.id === f)?.label).join(", ")}</span>
            </div>
            <button
              onClick={handleProceedToMatches}
              disabled={selectedFacilities.length === 0 || fetchingHospitals}
              className="w-full sm:w-auto bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-400 hover:to-blue-500 disabled:opacity-50 text-slate-950 font-black text-sm px-8 py-3 rounded-xl shadow-lg shadow-teal-500/25 transition-all flex items-center justify-center gap-2"
            >
              {fetchingHospitals ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                  <span>Matching Hospitals from Database...</span>
                </>
              ) : (
                <>
                  <span>FIND MATCHED HOSPITALS</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>

        </div>
      )}

      {/* ========================================================================= */}
      {/* SCREEN 3: "YOUR HOSPITAL OPTIONS" (MATCHED RESULTS CARDS) */}
      {/* ========================================================================= */}
      {activeStep === "HOSPITAL_OPTIONS" && (
        <div className="min-h-screen p-6 sm:p-10 max-w-5xl mx-auto space-y-8 animate-fadeIn">
          
          {/* Header Context */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full mb-2">
                Step 3 — Matched Facilities Found from Backend
              </div>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white">YOUR HOSPITAL OPTIONS</h2>
              <p className="text-slate-400 text-sm mt-1">
                Based on {patientName}'s policy, location (<strong>{patientCity} - {patientPincode}</strong>) and selected needs (<strong className="text-teal-300">{selectedFacilities.map(f => f.toUpperCase()).join(" + ")}</strong>).
              </p>
            </div>

            <button
              onClick={() => setActiveStep("FACILITY_SELECT")}
              className="text-xs bg-[#16254A] hover:bg-[#1E3364] text-slate-200 font-semibold px-4 py-2 rounded-xl border border-slate-600 transition-all flex items-center gap-1.5 shrink-0"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Adjust Needed Facilities
            </button>
          </div>

          {/* Matched Hospital Cards List */}
          <div className="space-y-6">
            {hospitalList.map((hosp, idx) => (
              <div
                key={hosp.id}
                className="bg-[#0F1B38]/90 border border-slate-700/80 hover:border-teal-500/80 rounded-3xl p-6 sm:p-8 shadow-2xl transition-all space-y-6"
              >
                {/* Hospital Header Row */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-700/60 pb-5">
                  <div className="space-y-1">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className="w-7 h-7 rounded-full bg-teal-500 text-slate-950 font-black flex items-center justify-center text-xs">
                        #{idx + 1}
                      </span>
                      <h3 className="text-2xl font-black text-white">{hosp.name}</h3>
                      <span className={`text-xs font-extrabold px-3 py-1 rounded-full ${
                        hosp.match_status === "FULL MATCH" 
                          ? "bg-emerald-950 border border-emerald-500/50 text-emerald-300"
                          : (hosp.match_status === "NEEDS VERIFICATION" ? "bg-amber-950 border border-amber-500/50 text-amber-300" : "bg-slate-800 text-slate-300")
                      }`}>
                        {hosp.match_status}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-400 flex-wrap">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-500" />
                        {hosp.address}
                      </span>
                      <span className="bg-blue-950/80 text-blue-300 border border-blue-500/30 px-2.5 py-0.5 rounded-full font-bold">
                        📍 {hosp.distance_km} km away from PIN {patientPincode}
                      </span>
                    </div>
                  </div>

                  {/* Care Fit Score Box */}
                  <div className="flex items-center gap-3 bg-[#0A1226] border border-slate-700/80 rounded-2xl px-4 py-3 shrink-0">
                    <div className="text-right">
                      <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">CARE FIT</div>
                      <div className="text-2xl font-black text-teal-400">{hosp.care_fit_score}%</div>
                    </div>
                    <button
                      onClick={() => {
                        setSelectedHospital(hosp)
                        setShowMatchScoreModal(true)
                      }}
                      className="text-[11px] text-teal-300 hover:text-teal-200 underline font-semibold ml-2"
                    >
                      Why this match?
                    </button>
                  </div>
                </div>

                {/* 4-Column Feature Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                  {/* Facilities */}
                  <div className="bg-[#14234B]/60 border border-slate-700/60 rounded-xl p-3.5 space-y-1.5">
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Requested Facilities</span>
                    <div className="space-y-1">
                      {hosp.facilities.map((fac, fi) => (
                        <div key={fi} className="flex items-center justify-between text-slate-200">
                          <span className="font-semibold">{fac.name}</span>
                          <span className={`text-[10px] font-bold ${fac.status === "AVAILABLE" ? "text-emerald-400" : (fac.status === "VERIFY" ? "text-amber-400" : "text-rose-400")}`}>
                            {fac.status === "AVAILABLE" ? "✓ Available" : (fac.status === "VERIFY" ? "⚠ Verify" : "✕ Unavailable")}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Insurance */}
                  <div className="bg-[#14234B]/60 border border-slate-700/60 rounded-xl p-3.5 space-y-1.5">
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Insurance Network</span>
                    <div className="text-emerald-300 font-bold flex items-center gap-1.5">
                      <Check className="w-4 h-4 text-emerald-400" />
                      <span>{hosp.network_status === "CASHLESS_NETWORK" ? "Cashless Preferred" : "Reimbursement Only"}</span>
                    </div>
                    <p className="text-[11px] text-slate-400">Cashless pre-auth accepted for {policy.insurer}</p>
                  </div>

                  {/* Room */}
                  <div className="bg-[#14234B]/60 border border-slate-700/60 rounded-xl p-3.5 space-y-1.5">
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Room Compatibility</span>
                    <div className="text-teal-300 font-bold flex items-center gap-1.5">
                      <Check className="w-4 h-4 text-teal-400" />
                      <span>{hosp.room_compatibility}</span>
                    </div>
                    <p className="text-[11px] text-slate-400">Semi-Private rate fits under ₹5,000 cap</p>
                  </div>

                  {/* Beds & Indicative Cost */}
                  <div className="bg-[#14234B]/60 border border-slate-700/60 rounded-xl p-3.5 space-y-1.5">
                    <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Bed Telemetry</span>
                    <div className="text-purple-300 font-bold flex items-center gap-1.5">
                      <Bed className="w-4 h-4 text-purple-400" />
                      <span>{hosp.available_beds} Available ({hosp.available_icu_beds} ICU)</span>
                    </div>
                    <span className="inline-block text-[10px] bg-purple-950 text-purple-300 border border-purple-500/30 px-1.5 py-0.2 rounded font-bold">
                      SIMULATED
                    </span>
                  </div>
                </div>

                {/* Card Action Footer */}
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
                  <div className="text-xs text-slate-400">
                    Indicative Treatment Cost: <strong className="text-white text-sm">₹{hosp.indicative_cost.toLocaleString("en-IN")}</strong>
                  </div>
                  <button
                    onClick={() => {
                      setSelectedHospital(hosp)
                      setActiveStep("DASHBOARD")
                      window.scrollTo({ top: 0, behavior: "smooth" })
                    }}
                    className="w-full sm:w-auto bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-400 hover:to-blue-500 text-slate-950 font-black text-xs px-6 py-3 rounded-xl shadow-lg shadow-teal-500/20 transition-all flex items-center justify-center gap-2"
                  >
                    <span>VIEW PERSONALIZED HOSPITAL DASHBOARD</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>

              </div>
            ))}
          </div>

        </div>
      )}

      {/* ========================================================================= */}
      {/* SCREEN 4: PERSONALIZED SELECTED HOSPITAL DASHBOARD & FULL SUITE */}
      {/* ========================================================================= */}
      {activeStep === "DASHBOARD" && selectedHospital && (
        <div className="min-h-screen flex">
          
          {/* STICKY REDESIGNED SIDEBAR */}
          <aside className="w-72 bg-[#0A1226] border-r border-slate-800 text-slate-300 flex flex-col fixed inset-y-0 left-0 z-40 shadow-2xl">
            {/* Header Brand */}
            <div className="p-5 border-b border-slate-800 flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-teal-500 flex items-center justify-center font-black text-slate-950 text-lg shadow-md shadow-teal-500/30">
                H
              </div>
              <div>
                <div className="font-black text-white text-base tracking-tight">HOSPITALITY</div>
                <div className="text-[10px] text-teal-400 font-bold uppercase tracking-wider">GE Precision Care</div>
              </div>
            </div>

            {/* Patient & Hospital Anchor Pill */}
            <div className="p-4 bg-[#0F1B38]/80 border-b border-slate-800 space-y-1">
              <div className="text-[10px] font-extrabold uppercase tracking-wider text-teal-400">PATIENT CONTEXT</div>
              <div className="font-bold text-sm text-white truncate">Hi, {patientName}</div>
              <div className="text-xs text-slate-300 truncate font-semibold">🏥 {selectedHospital.name.split(",")[0]}</div>
              <div className="text-[11px] text-blue-300 font-medium truncate flex items-center gap-1">
                <MapPin className="w-3 h-3 text-blue-400" />
                <span>{selectedHospital.distance_km} km from PIN {patientPincode}</span>
              </div>
              <div className="text-[11px] text-teal-300 font-medium truncate pt-0.5">
                {selectedFacilities.map(f => f.toUpperCase()).join(" + ")}
              </div>
            </div>

            {/* Navigation Section */}
            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-3 mb-2">Patient Suite</div>
              {[
                { id: "overview", label: "Overview & Decision Fit", icon: Activity },
                { id: "capabilities", label: "Facility Capability Map", icon: Layers },
                { id: "room-cost", label: "Room, Beds & Cost", icon: HeartPulse },
                { id: "policy-fit", label: "Policy Fit & Evidence", icon: FileText },
                { id: "verification", label: "Verification Center", icon: ShieldCheck },
                { id: "journey", label: "Care Roadmap", icon: Stethoscope },
                { id: "ai-assistant", label: "Ask HOSPITALITY AI", icon: Sparkles }
              ].map(nav => {
                const Icon = nav.icon
                const active = activeNavSection === nav.id
                return (
                  <button
                    key={nav.id}
                    onClick={() => scrollToSection(nav.id)}
                    className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all text-left ${
                      active 
                        ? "bg-gradient-to-r from-teal-500 to-blue-600 text-slate-950 font-black shadow-lg shadow-teal-500/20" 
                        : "text-slate-400 hover:bg-[#14234B] hover:text-white"
                    }`}
                  >
                    <Icon className={`w-4 h-4 ${active ? "text-slate-950" : "text-slate-400"}`} />
                    <span>{nav.label}</span>
                  </button>
                )
              })}

              <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-3 mt-6 mb-2">Standards & Audit</div>
              {[
                { id: "data-audit", label: "Data Audit & Integrity", icon: ShieldAlert },
                { id: "sources", label: "Data Source Registry", icon: Database },
                { id: "fhir", label: "FHIR / NHCX Payload", icon: FileCode }
              ].map(nav => {
                const Icon = nav.icon
                const active = activeNavSection === nav.id
                return (
                  <button
                    key={nav.id}
                    onClick={() => scrollToSection(nav.id)}
                    className={`w-full flex items-center gap-3 px-3.5 py-2 rounded-xl text-xs font-medium transition-all text-left ${
                      active 
                        ? "bg-slate-800 text-white font-bold" 
                        : "text-slate-500 hover:bg-slate-800/60 hover:text-slate-300"
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{nav.label}</span>
                  </button>
                )
              })}
            </nav>

            {/* Sidebar Footer */}
            <div className="p-4 border-t border-slate-800 bg-[#070D1E] text-xs space-y-1.5">
              <div className="flex items-center justify-between text-slate-400">
                <span>System Status</span>
                <span className="text-emerald-400 font-bold flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" /> Live :8000
                </span>
              </div>
              <p className="text-[10px] text-slate-500 leading-tight">
                Decision support system. Non-binding indicative estimate.
              </p>
            </div>
          </aside>

          {/* MAIN PERSONALIZED CONTENT AREA */}
          <main className="flex-1 ml-72 p-8 max-w-6xl mx-auto space-y-16">
            
            {/* TOP PERSONALIZED HERO BANNER */}
            <section id="overview" className="scroll-mt-8 space-y-6">
              <div className="bg-gradient-to-r from-[#0F1B38] via-[#14234B] to-[#0F1B38] border border-teal-500/30 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
                
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
                  <div className="space-y-2">
                    <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                      HI {patientName.toUpperCase()} • YOUR CARE OPTION
                    </div>
                    <h1 className="text-3xl sm:text-4xl font-black text-white">
                      {selectedHospital.name}
                    </h1>
                    <div className="flex items-center gap-3 text-xs text-slate-300 flex-wrap">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-400" />
                        {selectedHospital.address}
                      </span>
                      <span className="bg-blue-950/80 text-blue-300 border border-blue-500/30 px-2.5 py-0.5 rounded-full font-bold">
                        📍 {selectedHospital.distance_km} km from your registered location ({patientPincode})
                      </span>
                    </div>
                    <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
                      <span className="text-slate-400">Your selected needs:</span>
                      <strong className="text-teal-300 font-bold uppercase">
                        {selectedFacilities.map(f => f.toUpperCase()).join(" + ")}
                      </strong>
                      <span className="text-emerald-400 font-bold bg-emerald-950/80 border border-emerald-500/40 px-2 py-0.5 rounded ml-2">
                        ● Network Compatible
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-col gap-2 shrink-0 self-stretch sm:self-auto">
                    <button
                      onClick={() => setShowHospitalSwitcherModal(true)}
                      className="bg-teal-500 hover:bg-teal-400 text-slate-950 text-xs font-extrabold px-5 py-3 rounded-xl shadow-lg shadow-teal-500/20 transition-all flex items-center justify-center gap-2"
                    >
                      <ArrowLeftRight className="w-4 h-4" />
                      <span>Change Hospital</span>
                    </button>
                    <button
                      onClick={() => setActiveStep("FACILITY_SELECT")}
                      className="text-xs text-slate-400 hover:text-slate-200 bg-slate-900 border border-slate-700 px-4 py-2 rounded-xl transition-all"
                    >
                      Change Healthcare Needs
                    </button>
                  </div>
                </div>

                {/* DECISION CARD: "CAN THIS HOSPITAL SUPPORT YOUR NEED?" */}
                <div className="bg-[#0A1226]/90 border border-teal-500/40 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-inner">
                  <div className="space-y-2 flex-1">
                    <span className="text-[11px] font-extrabold uppercase tracking-widest text-teal-400">DECISION VERDICT</span>
                    <h3 className="text-lg font-black text-white">Can this hospital support your need?</h3>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs text-slate-200 pt-1">
                      <div className="flex items-center gap-1.5 text-emerald-300 font-semibold">
                        <Check className="w-4 h-4 text-emerald-400" /> Facilities Supported
                      </div>
                      <div className="flex items-center gap-1.5 text-emerald-300 font-semibold">
                        <Check className="w-4 h-4 text-emerald-400" /> Cashless Empanelled
                      </div>
                      <div className="flex items-center gap-1.5 text-emerald-300 font-semibold">
                        <Check className="w-4 h-4 text-emerald-400" /> Compatible Room Limit
                      </div>
                      <div className="flex items-center gap-1.5 text-purple-300 font-semibold">
                        <AlertTriangle className="w-4 h-4 text-purple-400" /> Bed Telemetry (Simulated)
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-col items-center md:items-end justify-center shrink-0 border-t md:border-t-0 pt-4 md:pt-0 border-slate-800 w-full md:w-auto">
                    <div className="text-3xl font-black text-teal-400">{selectedHospital.care_fit_score}%</div>
                    <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">OVERALL CARE FIT</div>
                    <button
                      onClick={() => setShowMatchScoreModal(true)}
                      className="mt-2 text-xs text-teal-300 hover:text-teal-200 font-bold underline"
                    >
                      [ WHY THIS MATCH? ]
                    </button>
                  </div>
                </div>

              </div>
            </section>

            {/* ========================================================================= */}
            {/* SECTION 2: FACILITY CAPABILITY VISUALIZATION MAP */}
            {/* ========================================================================= */}
            <section id="capabilities" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                  Capability Architecture
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">Facility Capability Map</h2>
                <p className="text-slate-400 text-sm mt-1">
                  Visual relationship of care departments at {selectedHospital.name}. Click any node for audit telemetry.
                </p>
              </div>

              <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-8 shadow-xl space-y-8">
                
                {/* Visual Tree / Graph */}
                <div className="flex flex-col items-center space-y-6 max-w-2xl mx-auto">
                  
                  {/* Root Node: Primary Specialty */}
                  <button
                    onClick={() => setSelectedCapabilityNode({
                      name: "Cardiology Department",
                      status: "AVAILABLE",
                      source: "ABDM Health Facility Registry (HFR)",
                      freshness: "Synchronized 2026",
                      details: `Comprehensive adult & pediatric cardiology OPD, Echo & diagnostics at ${selectedHospital.name}.`
                    })}
                    className="bg-emerald-950/80 hover:bg-emerald-900 border-2 border-emerald-400 text-emerald-200 font-black text-sm px-8 py-4 rounded-2xl shadow-xl shadow-emerald-950/50 transition-all flex items-center gap-2"
                  >
                    <span className="w-3 h-3 rounded-full bg-emerald-400 animate-pulse" />
                    <span>CARDIOLOGY (PRIMARY SPECIALTY)</span>
                  </button>

                  <div className="w-0.5 h-6 bg-slate-600" />

                  {/* Level 2 Nodes */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full">
                    <button
                      onClick={() => setSelectedCapabilityNode({
                        name: "Intensive Care Unit (ICU)",
                        status: "AVAILABLE",
                        source: "State Health Bed Telemetry",
                        freshness: "Simulated Telemetry",
                        details: `${selectedHospital.available_icu_beds} ICU beds currently unoccupied.`
                      })}
                      className="p-4 bg-emerald-950/70 hover:bg-emerald-900/80 border border-emerald-500/50 rounded-2xl text-center space-y-1 transition-all"
                    >
                      <div className="text-xs font-extrabold text-emerald-300 flex items-center justify-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-emerald-400" />
                        <span>ICU / CCU</span>
                      </div>
                      <div className="text-[11px] text-slate-400">{selectedHospital.available_icu_beds} Beds Unoccupied</div>
                    </button>

                    <button
                      onClick={() => setSelectedCapabilityNode({
                        name: "Cath Lab Suite",
                        status: "AVAILABLE",
                        source: "Hospital Infrastructure Master",
                        freshness: "Verified 2026",
                        details: "Digital angiography suite for Angioplasty (PTCA) & Stenting."
                      })}
                      className="p-4 bg-emerald-950/70 hover:bg-emerald-900/80 border border-emerald-500/50 rounded-2xl text-center space-y-1 transition-all"
                    >
                      <div className="text-xs font-extrabold text-emerald-300 flex items-center justify-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-emerald-400" />
                        <span>CATH LAB</span>
                      </div>
                      <div className="text-[11px] text-slate-400">24/7 Operational</div>
                    </button>

                    <button
                      onClick={() => setSelectedCapabilityNode({
                        name: "Emergency & Trauma",
                        status: "AVAILABLE",
                        source: "ABDM Emergency Directory",
                        freshness: "Verified 2026",
                        details: "Cardiac emergency resuscitation unit with rapid triage."
                      })}
                      className="p-4 bg-emerald-950/70 hover:bg-emerald-900/80 border border-emerald-500/50 rounded-2xl text-center space-y-1 transition-all"
                    >
                      <div className="text-xs font-extrabold text-emerald-300 flex items-center justify-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-emerald-400" />
                        <span>EMERGENCY</span>
                      </div>
                      <div className="text-[11px] text-slate-400">Active 24/7</div>
                    </button>
                  </div>

                  <div className="w-0.5 h-6 bg-slate-600" />

                  {/* Level 3 Node: OT & Diagnostics */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-lg">
                    <button
                      onClick={() => setSelectedCapabilityNode({
                        name: "Cardiac OT (Operation Theatre)",
                        status: "AVAILABLE",
                        source: "NABH Hospital Accreditation Register",
                        freshness: "Verified 2026",
                        details: "Modular surgical suites for open and minimally invasive cardiac procedures."
                      })}
                      className="p-3.5 bg-emerald-950/70 hover:bg-emerald-900/80 border border-emerald-500/50 rounded-xl text-center text-xs font-bold text-emerald-300"
                    >
                      ✓ CARDIAC OT (SURGICAL SUITE)
                    </button>

                    <button
                      onClick={() => setSelectedCapabilityNode({
                        name: "Advanced Diagnostics",
                        status: "AVAILABLE",
                        source: "Diagnostic Network Master",
                        freshness: "Verified 2026",
                        details: "Cardiac Troponin I, NT-proBNP, CT Angiography."
                      })}
                      className="p-3.5 bg-emerald-950/70 hover:bg-emerald-900/80 border border-emerald-500/50 rounded-xl text-center text-xs font-bold text-emerald-300"
                    >
                      ✓ 64-SLICE CT & ADVANCED LAB
                    </button>
                  </div>

                </div>

                {/* Node Detail Drawer if clicked */}
                {selectedCapabilityNode && (
                  <div className="bg-[#0A1226] border border-teal-500/40 rounded-2xl p-5 space-y-2 text-xs animate-fadeIn">
                    <div className="flex items-center justify-between">
                      <span className="font-extrabold text-white text-sm">{selectedCapabilityNode.name}</span>
                      <span className="bg-emerald-400 text-slate-950 font-black px-2 py-0.5 rounded text-[10px]">
                        {selectedCapabilityNode.status}
                      </span>
                    </div>
                    <p className="text-slate-300">{selectedCapabilityNode.details}</p>
                    <div className="text-[11px] text-slate-500 pt-1 border-t border-slate-800 flex gap-4">
                      <span>Source: <strong className="text-slate-400">{selectedCapabilityNode.source}</strong></span>
                      <span>Freshness: <strong className="text-slate-400">{selectedCapabilityNode.freshness}</strong></span>
                    </div>
                  </div>
                )}

              </div>
            </section>

            {/* ========================================================================= */}
            {/* SECTION 3: INTERACTIVE ROOM SELECTION, BEDS & COST SIMULATOR */}
            {/* ========================================================================= */}
            <section id="room-cost" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                  Financial Transparency
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">Room Selection, Beds & Indicative Cost</h2>
                <p className="text-slate-400 text-sm mt-1">
                  Selecting a room category updates bed telemetry, policy room fit, and proportionate deduction penalties in real time.
                </p>
              </div>

              {/* Room Category Buttons */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {Object.values(roomTiers).map(room => {
                  const isSelected = selectedRoomKey === room.category
                  return (
                    <button
                      key={room.category}
                      onClick={() => setSelectedRoomKey(room.category)}
                      className={`p-5 rounded-2xl border text-left transition-all space-y-3 ${
                        isSelected 
                          ? "bg-[#14234B] border-teal-400 shadow-xl shadow-teal-950/60 ring-2 ring-teal-400/40" 
                          : "bg-[#0F1B38]/80 border-slate-700/60 hover:border-slate-500"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase tracking-wider text-slate-400">{room.label}</span>
                        {isSelected && (
                          <span className="text-[10px] bg-teal-400 text-slate-950 font-black px-2 py-0.5 rounded">
                            ACTIVE
                          </span>
                        )}
                      </div>
                      <div className="text-2xl font-black text-white">
                        ₹{room.tariff.toLocaleString("en-IN")}<span className="text-xs text-slate-400 font-normal">/day</span>
                      </div>
                      <div className={`text-xs font-bold ${
                        room.status === "COMPATIBLE" ? "text-emerald-400" : "text-amber-400"
                      }`}>
                        {room.status_text}
                      </div>
                    </button>
                  )
                })}
              </div>

              {/* WARNING BANNER IF ROOM CAPPED */}
              {financials.isRoomCapped && (
                <div className="bg-amber-950/80 border border-amber-500/50 rounded-2xl p-5 flex items-start gap-3.5 text-amber-200 text-xs shadow-lg animate-fadeIn">
                  <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                  <div className="space-y-1">
                    <strong className="font-bold text-amber-300 text-sm">Proportionate Deduction Penalty Triggered!</strong>
                    <p className="leading-relaxed">
                      {currentRoom.label} tariff (₹{currentRoom.tariff.toLocaleString("en-IN")}/day) exceeds {patientName}'s policy limit of ₹{policy.room_rent_limit.toLocaleString("en-IN")}/day.
                      The insurer will only pay <strong>{(financials.proportionateRatio * 100).toFixed(1)}%</strong> of associated surgeon, OT, and medical charges, adding a <strong>₹{financials.proportionatePenalty.toLocaleString("en-IN")} penalty</strong> to your out-of-pocket share.
                    </p>
                  </div>
                </div>
              )}

              {/* Live Bed & Cost Split Card */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* Bed Availability for Selected Room */}
                <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-6 shadow-xl flex flex-col justify-between space-y-4">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-widest text-purple-400 flex items-center gap-1.5">
                      <Bed className="w-3.5 h-3.5" /> Room Bed Telemetry
                    </span>
                    <h3 className="text-lg font-black text-white mt-1">{currentRoom.label}</h3>
                    
                    <div className="mt-4 p-4 bg-[#0A1226] border border-purple-500/30 rounded-2xl text-center space-y-1">
                      <div className="text-3xl font-black text-purple-300">{currentRoom.available_beds} AVAILABLE</div>
                      <div className="text-xs text-slate-400">
                        {currentRoom.occupied_beds} occupied of {currentRoom.total_beds} total beds
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-700/60 flex items-center justify-between text-xs">
                    <span className="text-slate-400">Status Tag:</span>
                    <span className="text-purple-300 font-bold bg-purple-950 px-2 py-0.5 rounded border border-purple-500/40 text-[10px]">
                      {currentRoom.bed_status}
                    </span>
                  </div>
                </div>

                {/* Financial Care Cost Summary */}
                <div className="lg:col-span-2 bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-6 sm:p-8 shadow-xl space-y-5">
                  <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-widest text-teal-400">FINANCIAL BREAKDOWN</span>
                      <h3 className="text-lg font-black text-white">Indicative Care Cost & Patient Share</h3>
                    </div>
                    <span className="text-[10px] bg-slate-800 text-slate-300 font-bold px-2 py-1 rounded">
                      Procedure: Angioplasty (4 Days)
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                    <div className="p-4 bg-[#0A1226] rounded-xl border border-slate-700/60">
                      <span className="text-slate-400 font-semibold">Total Hospital Bill</span>
                      <div className="text-xl font-black text-white mt-1">₹{financials.totalHospitalBill.toLocaleString("en-IN")}</div>
                      <span className="text-[10px] text-slate-500 font-medium">Billed by Hospital</span>
                    </div>

                    <div className="p-4 bg-emerald-950/60 rounded-xl border border-emerald-500/30">
                      <span className="text-emerald-400 font-semibold">Insurer Settlement</span>
                      <div className="text-xl font-black text-emerald-300 mt-1">₹{financials.insurerSettlement.toLocaleString("en-IN")}</div>
                      <span className="text-[10px] text-emerald-400/80 font-medium">After 10% Co-pay</span>
                    </div>

                    <div className="p-4 bg-amber-950/60 rounded-xl border border-amber-500/30">
                      <span className="text-amber-400 font-semibold">Indicative Patient Share</span>
                      <div className="text-xl font-black text-amber-300 mt-1">₹{financials.patientOutofPocket.toLocaleString("en-IN")}</div>
                      <span className="text-[10px] text-amber-400/80 font-medium">
                        {financials.isRoomCapped ? "Includes Room Penalty" : "Co-pay + Consumables"}
                      </span>
                    </div>
                  </div>

                  {/* Progress Bar of Coverage */}
                  <div className="space-y-1.5 pt-2">
                    <div className="flex justify-between text-xs text-slate-300">
                      <span>Insurer Coverage: {((financials.insurerSettlement / financials.totalHospitalBill) * 100).toFixed(0)}%</span>
                      <span>Patient Out-of-Pocket: {((financials.patientOutofPocket / financials.totalHospitalBill) * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden flex">
                      <div 
                        style={{ width: `${(financials.insurerSettlement / financials.totalHospitalBill) * 100}%` }} 
                        className="bg-emerald-500 h-full"
                      />
                      <div 
                        style={{ width: `${(financials.patientOutofPocket / financials.totalHospitalBill) * 100}%` }} 
                        className="bg-amber-500 h-full"
                      />
                    </div>
                  </div>

                  <p className="text-[11px] text-slate-400 italic">
                    *INDICATIVE ESTIMATE ONLY. Final claim settlement requires formal insurer TPA adjudication.
                  </p>
                </div>

              </div>
            </section>

            {/* ========================================================================= */}
            {/* SECTION 4: POLICY FIT METER & EVIDENCE PROOF */}
            {/* ========================================================================= */}
            <section id="policy-fit" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                  Policy Audit & Proof
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">Policy Fit & Clause Evidence</h2>
                <p className="text-slate-400 text-sm mt-1">
                  Click any policy dimension below to inspect the extracted clause and document page citation.
                </p>
              </div>

              <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-6 sm:p-8 shadow-xl space-y-6">
                
                {/* Meter Header */}
                <div className="flex items-center justify-between border-b border-slate-700/60 pb-4">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">OVERALL POLICY FIT</span>
                    <div className="text-2xl font-black text-emerald-400">GOOD FIT (92%)</div>
                  </div>
                  <button
                    onClick={() => setShowPolicyEvidenceModal(true)}
                    className="text-xs bg-teal-950/80 border border-teal-500/40 text-teal-300 font-bold px-4 py-2 rounded-xl hover:bg-teal-900 transition-all flex items-center gap-1.5"
                  >
                    <FileText className="w-3.5 h-3.5" /> Full Policy Schedule
                  </button>
                </div>

                {/* 5 Interactive Policy Dimensions */}
                <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 text-xs">
                  {[
                    { key: "room_limit", label: "ROOM LIMIT", val: "₹5,000/day", status: currentRoom.status === "COMPATIBLE" ? "✓ Fit" : "⚠ Breached", ok: currentRoom.status === "COMPATIBLE" },
                    { key: "network", label: "NETWORK", val: "Cashless Network", status: "✓ Verified", ok: true },
                    { key: "copay", label: "CO-PAY", val: "10% Co-pay", status: "✓ Standard", ok: true },
                    { key: "deductible", label: "DEDUCTIBLE", val: "₹5,000 Nil Excess", status: "✓ Admissible", ok: true },
                    { key: "pre_auth", label: "PRE-AUTH", val: "48h Prior Notice", status: "⚠ Required", ok: false }
                  ].map((dim, i) => (
                    <button
                      key={i}
                      onClick={() => {
                        setSelectedEvidenceItem(dim.key)
                        setShowPolicyEvidenceModal(true)
                      }}
                      className="p-3.5 bg-[#0A1226] hover:bg-[#14234B] border border-slate-700/60 hover:border-teal-400 rounded-xl text-left transition-all space-y-1"
                    >
                      <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{dim.label}</div>
                      <div className="font-bold text-white text-xs truncate">{dim.val}</div>
                      <div className={`text-[11px] font-extrabold ${dim.ok ? "text-emerald-400" : "text-amber-400"}`}>
                        {dim.status}
                      </div>
                    </button>
                  ))}
                </div>

              </div>
            </section>

            {/* ========================================================================= */}
            {/* SECTION 5: VERIFICATION CENTER ("BEFORE YOU PROCEED") */}
            {/* ========================================================================= */}
            <section id="verification" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                  Actionable Checklist
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">Before You Proceed (Verification Center)</h2>
                <p className="text-slate-400 text-sm mt-1">
                  Transparent breakdown of confirmed parameters versus items requiring hospital/TPA verification.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
                
                {/* Confirmed */}
                <div className="bg-[#0F1B38]/90 border border-emerald-500/30 rounded-3xl p-6 shadow-xl space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>CONFIRMED FACTS</span>
                  </div>
                  <div className="space-y-2 text-slate-200">
                    <div className="p-2.5 bg-emerald-950/40 rounded-xl border border-emerald-500/20">
                      ✓ <strong>Required Facilities:</strong> Selected facilities operational
                    </div>
                    <div className="p-2.5 bg-emerald-950/40 rounded-xl border border-emerald-500/20">
                      ✓ <strong>Policy Limits:</strong> ₹5,00,000 Sum Insured, ₹5,000 room cap
                    </div>
                    <div className="p-2.5 bg-emerald-950/40 rounded-xl border border-emerald-500/20">
                      ✓ <strong>Hospital Proximity:</strong> Verified geocodes ({selectedHospital.distance_km} km away)
                    </div>
                  </div>
                </div>

                {/* Needs Verification */}
                <div className="bg-[#0F1B38]/90 border border-amber-500/30 rounded-3xl p-6 shadow-xl space-y-3">
                  <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
                    <AlertTriangle className="w-4 h-4" />
                    <span>NEEDS VERIFICATION</span>
                  </div>
                  <div className="space-y-2 text-slate-200">
                    <div className="p-2.5 bg-amber-950/40 rounded-xl border border-amber-500/20">
                      ⚠ <strong>Cashless Initial Approval:</strong> Submit pre-auth 48h prior
                    </div>
                    <div className="p-2.5 bg-amber-950/40 rounded-xl border border-amber-500/20">
                      ⚠ <strong>Live Bed Occupancy:</strong> Confirm at hospital desk on admission day
                    </div>
                    <div className="p-2.5 bg-amber-950/40 rounded-xl border border-amber-500/20">
                      ⚠ <strong>Room Rent Match:</strong> Verify doctor orders Semi-Private room
                    </div>
                  </div>
                </div>

                {/* Next Best Action Primary CTA */}
                <div className="bg-gradient-to-br from-teal-950 via-[#0F1B38] to-blue-950 border border-teal-500/50 rounded-3xl p-6 shadow-xl flex flex-col justify-between space-y-4">
                  <div>
                    <span className="text-[10px] font-black uppercase tracking-widest text-teal-400">RECOMMENDED ACTION</span>
                    <h4 className="text-base font-black text-white mt-1">Next Best Action for Ananya</h4>
                    <p className="text-slate-300 mt-2 leading-relaxed">
                      {financials.isRoomCapped
                        ? `Switch back to Semi-Private Room to avoid ₹${financials.proportionatePenalty.toLocaleString("en-IN")} in proportionate deductions, then initiate cashless pre-authorization.`
                        : `Your room, distance (${selectedHospital.distance_km} km), and policy are optimal! Proceed to verify cashless pre-authorization at ${selectedHospital.name.split(",")[0]}.`}
                    </p>
                  </div>

                  <button
                    onClick={() => handleSendChatMessage("What do I need to verify before admission?")}
                    className="w-full bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-400 hover:to-blue-500 text-slate-950 font-black py-3.5 rounded-xl shadow-lg shadow-teal-500/20 transition-all text-xs"
                  >
                    VERIFY PRE-AUTHORIZATION →
                  </button>
                </div>

              </div>
            </section>

            {/* ========================================================================= */}
            {/* SECTION 6: CARE ROADMAP JOURNEY */}
            {/* ========================================================================= */}
            <section id="journey" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                  Flowing Roadmap
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">Care Journey State Machine</h2>
                <p className="text-slate-400 text-sm mt-1">
                  Active lifecycle milestones tailored for {patientName} at {selectedHospital.name}.
                </p>
              </div>

              <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-8 shadow-xl space-y-6">
                
                {/* Vertical Step Timeline */}
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs">
                  {[
                    { num: "01", title: "NEED IDENTIFIED", desc: selectedFacilities.map(f => f.toUpperCase()).join(" + "), done: true },
                    { num: "02", title: "HOSPITAL SELECTED", desc: selectedHospital.name, done: true },
                    { num: "03", title: "ROOM SELECTED", desc: `${currentRoom.label} (₹${currentRoom.tariff.toLocaleString("en-IN")})`, done: true },
                    { num: "04", title: "PRE-AUTHORIZATION", desc: "⚠ Action Required (48h)", active: true }
                  ].map((st, idx) => (
                    <div
                      key={idx}
                      className={`p-4 rounded-2xl border ${
                        st.active 
                          ? "bg-teal-950/70 border-teal-400 text-teal-200 ring-1 ring-teal-400/50"
                          : (st.done ? "bg-[#0A1226] border-slate-700/60 text-slate-300" : "bg-[#070D1E] border-slate-800 text-slate-500")
                      }`}
                    >
                      <div className="text-[10px] font-black text-teal-400">{st.num}</div>
                      <div className="font-black text-white text-xs mt-0.5">{st.title}</div>
                      <div className="text-[11px] text-slate-400 mt-1">{st.desc}</div>
                    </div>
                  ))}
                </div>

                <div className="p-4 bg-[#0A1226] border border-teal-500/30 rounded-2xl text-xs space-y-2">
                  <div className="font-bold text-white flex items-center justify-between">
                    <span>Active Milestone: Pre-Authorization at {selectedHospital.name}</span>
                    <span className="text-teal-400 font-bold bg-teal-950 px-2 py-0.5 rounded text-[10px]">IN PROGRESS</span>
                  </div>
                  <p className="text-slate-300 leading-relaxed">
                    Submit Star Health Policy E-Card & Aadhaar (ABHA: {patientAbha}) to the insurance coordinator at {selectedHospital.name}. Ensure admission slip explicitly indicates <strong>{currentRoom.label}</strong>.
                  </p>
                </div>

              </div>
            </section>

            {/* ========================================================================= */}
            {/* SECTION 7: CONTEXTUAL PATIENT AI ("ASK HOSPITALITY") */}
            {/* ========================================================================= */}
            <section id="ai-assistant" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-teal-400 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
                  Conversational AI
                </span>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">ASK HOSPITALITY</h2>
                <p className="text-slate-400 text-sm mt-1">
                  Context-aware assistant pre-grounded in {patientName}'s policy, location ({patientCity} - PIN {patientPincode}), {selectedHospital.name}, and selected {currentRoom.label}.
                </p>
              </div>

              <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl shadow-2xl flex flex-col h-[480px]">
                
                {/* Messages Box */}
                <div className="flex-1 p-6 overflow-y-auto space-y-4 text-xs">
                  {chatMessages.map((m, i) => (
                    <div key={i} className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}>
                      <div className={`p-4 rounded-2xl max-w-xl leading-relaxed whitespace-pre-wrap ${
                        m.role === "user"
                          ? "bg-teal-500 text-slate-950 font-bold"
                          : "bg-[#0A1226] text-slate-200 border border-slate-700/60"
                      }`}>
                        {m.content}
                      </div>
                      {m.citations && m.citations.length > 0 && (
                        <div className="mt-1.5 flex flex-wrap gap-2">
                          {m.citations.map((c: any, ci: number) => (
                            <span key={ci} className="text-[10px] bg-slate-800 text-teal-300 border border-slate-700 px-2 py-0.5 rounded font-semibold">
                              📖 {c.source} ({c.clause})
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}

                  {chatLoading && (
                    <div className="flex items-center gap-2 text-teal-400 text-xs italic">
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      Consulting policy clauses & hospital tariff simulator...
                    </div>
                  )}
                </div>

                {/* Prompt Buttons */}
                <div className="px-6 py-2.5 bg-[#0A1226]/80 border-t border-slate-800 flex gap-2 overflow-x-auto text-[11px]">
                  <button 
                    onClick={() => handleSendChatMessage("Why is private room not recommended?")}
                    className="bg-[#14234B] hover:bg-[#1A2E62] border border-slate-700 px-3 py-1.5 rounded-full text-teal-300 whitespace-nowrap"
                  >
                    "Why is private room not recommended?"
                  </button>
                  <button 
                    onClick={() => handleSendChatMessage("Why was this hospital recommended?")}
                    className="bg-[#14234B] hover:bg-[#1A2E62] border border-slate-700 px-3 py-1.5 rounded-full text-teal-300 whitespace-nowrap"
                  >
                    "Why was this hospital recommended?"
                  </button>
                  <button 
                    onClick={() => handleSendChatMessage("What do I need to verify?")}
                    className="bg-[#14234B] hover:bg-[#1A2E62] border border-slate-700 px-3 py-1.5 rounded-full text-teal-300 whitespace-nowrap"
                  >
                    "What do I need to verify?"
                  </button>
                </div>

                {/* Input Form */}
                <form onSubmit={e => { e.preventDefault(); handleSendChatMessage() }} className="p-4 border-t border-slate-800 flex gap-3">
                  <input 
                    type="text"
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    placeholder="Ask about room rent overages, co-pays, or pre-auth rules..."
                    className="flex-1 bg-[#0A1226] border border-slate-700 text-white rounded-xl px-4 py-2.5 text-xs focus:outline-none focus:border-teal-400"
                  />
                  <button 
                    type="submit"
                    disabled={chatLoading}
                    className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-black px-5 py-2.5 rounded-xl text-xs shadow-lg shadow-teal-500/20 flex items-center gap-1.5"
                  >
                    <Send className="w-3.5 h-3.5" /> Send
                  </button>
                </form>

              </div>
            </section>

            {/* ========================================================================= */}
            {/* TECHNICAL AUDIT & STANDARDS SECTIONS */}
            {/* ========================================================================= */}
            <section id="data-audit" className="scroll-mt-8 space-y-6">
              <div className="border-b border-slate-800 pb-4">
                <span className="text-xs font-bold uppercase tracking-widest text-slate-400 bg-slate-800 px-3 py-1 rounded-full">
                  Provenance & Verification
                </span>
                <h2 className="text-xl font-bold text-white mt-2">Data Audit & Provenance Transparency</h2>
              </div>
              <div className="bg-[#0F1B38]/90 border border-slate-700/60 rounded-3xl p-6 overflow-x-auto text-xs">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-slate-700 text-slate-400 uppercase text-[10px]">
                      <th className="pb-3">Dimension</th>
                      <th className="pb-3">Source Provider</th>
                      <th className="pb-3">Status Badge</th>
                      <th className="pb-3">Audit Details</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 text-slate-300">
                    <tr>
                      <td className="py-3 font-bold text-white">Hospital Identity & Geo-Codes</td>
                      <td>data.gov.in (MoHFW)</td>
                      <td><span className="bg-emerald-950 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-bold">AUTHORITATIVE</span></td>
                      <td>Verified official hospital geocodes and 6-digit PIN.</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-bold text-white">Procedure Package Rates</td>
                      <td>PM-JAY HBP 2022 Master</td>
                      <td><span className="bg-emerald-950 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-bold">AUTHORITATIVE</span></td>
                      <td>1,949 standard procedure packages with NABH rates.</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-bold text-white">Room Rent Benchmarks</td>
                      <td>CGHS Rate Cards (MoHFW)</td>
                      <td><span className="bg-emerald-950 text-emerald-300 border border-emerald-500/40 px-2 py-0.5 rounded font-bold">AUTHORITATIVE</span></td>
                      <td>General, Semi-Private, Private, ICU standard baseline.</td>
                    </tr>
                    <tr>
                      <td className="py-3 font-bold text-white">Live Bed Telemetry</td>
                      <td>HOSPITALITY Synthetic Feed</td>
                      <td><span className="bg-purple-950 text-purple-300 border border-purple-500/40 px-2 py-0.5 rounded font-bold">SIMULATED</span></td>
                      <td>Simulated real-time feed; no public live bed API exists post-COVID.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>

            <section id="sources" className="scroll-mt-8 space-y-4">
              <h3 className="text-base font-bold text-white">Data Source Registry</h3>
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
                {[
                  { name: "data.gov.in", org: "MoHFW", status: "Active (9 Metros)" },
                  { name: "PM-JAY HBP 2022", org: "NHA", status: "Active (1,949 Packages)" },
                  { name: "CGHS Rate Cards", org: "MoHFW", status: "Active (5 Categories)" },
                  { name: "ABDM HFR Sandbox", org: "NHA", status: "Connected" }
                ].map((s, i) => (
                  <div key={i} className="p-3.5 bg-[#0F1B38] border border-slate-700/60 rounded-xl space-y-1">
                    <div className="font-bold text-white">{s.name}</div>
                    <div className="text-slate-400">{s.org}</div>
                    <div className="text-emerald-400 font-semibold text-[11px]">{s.status}</div>
                  </div>
                ))}
              </div>
            </section>

            <section id="fhir" className="scroll-mt-8 space-y-4 pb-16">
              <h3 className="text-base font-bold text-white">HL7 FHIR R4 CoverageEligibilityResponse</h3>
              <div className="bg-[#0A1226] border border-slate-800 p-5 rounded-2xl font-mono text-xs text-emerald-400 overflow-x-auto">
                <pre>{JSON.stringify({
                  resourceType: "CoverageEligibilityResponse",
                  id: "nhcx-ananya-2026",
                  status: "active",
                  patient: { reference: `Patient/ABHA-${patientAbha}` },
                  insurer: { display: policy.insurer },
                  insurance: [{
                    coverage: { reference: `Coverage/${policy.policy_number}` },
                    inforce: true,
                    item: [
                      { category: { text: "Room Rent Cap" }, benefit: [{ allowedMoney: { value: policy.room_rent_limit, currency: "INR" } }] },
                      { category: { text: "Co-payment" }, benefit: [{ allowedUnsignedInt: policy.copay_percentage }] }
                    ]
                  }]
                }, null, 2)}</pre>
              </div>
            </section>

          </main>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODAL 1: "WHY THIS MATCH?" SCORE BREAKDOWN */}
      {/* ========================================================================= */}
      {showMatchScoreModal && selectedHospital && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-[#0F1B38] border border-teal-500/40 rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-6">
            <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
              <div>
                <span className="text-[10px] font-black uppercase text-teal-400 tracking-wider">EXPLAINABLE MATCH SCORE</span>
                <h3 className="text-lg font-black text-white">{selectedHospital.name} Match Proof</h3>
              </div>
              <button 
                onClick={() => setShowMatchScoreModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between items-center p-2.5 bg-[#0A1226] rounded-xl">
                <span className="text-slate-300">Facility Match ({selectedFacilities.map(f => f.toUpperCase()).join(", ")})</span>
                <span className="font-black text-teal-400">{selectedHospital.score_breakdown.facility_match} / 100</span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-[#0A1226] rounded-xl">
                <span className="text-slate-300">Insurance Network Compatibility</span>
                <span className="font-black text-teal-400">{selectedHospital.score_breakdown.network_compatibility} / 100</span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-[#0A1226] rounded-xl">
                <span className="text-slate-300">Room Rent Limit Fit</span>
                <span className="font-black text-teal-400">{selectedHospital.score_breakdown.room_fit} / 100</span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-[#0A1226] rounded-xl">
                <span className="text-slate-300">Bed Availability Telemetry</span>
                <span className="font-black text-purple-400">{selectedHospital.score_breakdown.bed_availability} / 100</span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-[#0A1226] rounded-xl">
                <span className="text-slate-300">Indicative Cost Fit</span>
                <span className="font-black text-teal-400">{selectedHospital.score_breakdown.cost_compatibility} / 100</span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-[#0A1226] rounded-xl">
                <span className="text-slate-300">Data Confidence & Integrity</span>
                <span className="font-black text-emerald-400">{selectedHospital.score_breakdown.data_confidence} / 100</span>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-700/60 flex items-center justify-between text-xs font-bold">
              <span className="text-white">Weighted Care Fit Score</span>
              <span className="text-2xl font-black text-teal-400">{selectedHospital.care_fit_score}%</span>
            </div>

            <button
              onClick={() => setShowMatchScoreModal(false)}
              className="w-full bg-teal-500 hover:bg-teal-400 text-slate-950 font-black py-3 rounded-xl text-xs"
            >
              CLOSE BREAKDOWN
            </button>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODAL 2: POLICY EVIDENCE AUDITOR */}
      {/* ========================================================================= */}
      {showPolicyEvidenceModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-[#0F1B38] border border-teal-500/40 rounded-3xl max-w-2xl w-full p-6 shadow-2xl space-y-6">
            <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
              <div>
                <span className="text-[10px] font-black uppercase text-teal-400 tracking-wider">AUDIT TRAIL</span>
                <h3 className="text-lg font-black text-white">{policy.insurer} Evidence</h3>
              </div>
              <button 
                onClick={() => setShowPolicyEvidenceModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs max-h-[350px] overflow-y-auto pr-1">
              {policy.clauses.map((c, idx) => (
                <div key={idx} className="p-4 bg-[#0A1226] border border-slate-700 rounded-2xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-teal-300 text-xs">{c.type} Clause</span>
                    <span className="text-[10px] bg-teal-950 text-teal-400 border border-teal-500/30 px-2 py-0.5 rounded font-bold">
                      PAGE {c.page} • {c.confidence}
                    </span>
                  </div>
                  <p className="text-slate-200 leading-relaxed italic">"{c.text}"</p>
                  <div className="text-[10px] text-slate-500">Source: Uploaded Star Health Policy Schedule</div>
                </div>
              ))}
            </div>

            <button
              onClick={() => setShowPolicyEvidenceModal(false)}
              className="w-full bg-teal-500 hover:bg-teal-400 text-slate-950 font-black py-3 rounded-xl text-xs"
            >
              DONE
            </button>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODAL 3: HOSPITAL SWITCHER QUICK DRAWER */}
      {/* ========================================================================= */}
      {showHospitalSwitcherModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 animate-fadeIn">
          <div className="bg-[#0F1B38] border border-teal-500/40 rounded-3xl max-w-xl w-full p-6 shadow-2xl space-y-6">
            <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
              <div>
                <span className="text-[10px] font-black uppercase text-teal-400 tracking-wider">CHANGE FACILITY</span>
                <h3 className="text-lg font-black text-white">Switch to Alternative Hospital</h3>
              </div>
              <button 
                onClick={() => setShowHospitalSwitcherModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs max-h-[380px] overflow-y-auto pr-1">
              {hospitalList.map(h => (
                <div
                  key={h.id}
                  onClick={() => {
                    setSelectedHospital(h)
                    setShowHospitalSwitcherModal(false)
                  }}
                  className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-center justify-between ${
                    selectedHospital?.id === h.id 
                      ? "bg-[#14234B] border-teal-400 ring-1 ring-teal-400/40" 
                      : "bg-[#0A1226] border-slate-700 hover:border-slate-500"
                  }`}
                >
                  <div>
                    <div className="font-extrabold text-white text-sm">{h.name}</div>
                    <div className="text-slate-400 text-xs">{h.address}</div>
                    <div className="flex items-center gap-2 text-xs mt-1">
                      <span className="text-emerald-400 font-semibold">✓ {h.match_status}</span>
                      <span className="text-blue-300 font-bold">• 📍 {h.distance_km} km</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-black text-teal-400">{h.care_fit_score}%</div>
                    <div className="text-[10px] text-slate-400 uppercase font-bold">Care Fit</div>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={() => setShowHospitalSwitcherModal(false)}
              className="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold py-3 rounded-xl text-xs"
            >
              CANCEL
            </button>
          </div>
        </div>
      )}

    </div>
  )
}
'''

target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "components", "single-page-app.tsx"))
with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)
print(f"Successfully generated Full Dynamic Integration SPA to {target_path}")
