export type DataConfidence = "AUTHORITATIVE" | "PUBLIC_VERIFIED" | "SIMULATED" | "NEEDS_VERIFICATION";
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
