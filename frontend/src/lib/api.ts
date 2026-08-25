import { 
  Hospital, RoomType, BedInventory, Tariff, Policy, MatchResult, 
  ProportionateDeductionResult, PatientJourney, JourneyEvent, ChatResponse 
} from '../types';

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

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
  
  getPatientJourney: (id: string) => fetchAPI(`/journey/${id}`),
  addJourneyEvent: (id: string, event: any) => fetchAPI(`/journey/${id}/events`, { method: 'POST', body: JSON.stringify(event) }),
  
  queryChatbot: (query: string, context?: any) => fetchAPI('/chat', { method: 'POST', body: JSON.stringify({ query, context }) }),
  
  getDataSources: () => fetchAPI('/data-sources'),
  getDataQuality: () => fetchAPI('/data-sources/quality'),
  
  getFHIRCoverage: (id: string) => fetchAPI(`/fhir/Coverage/${id}`),
  getFHIRLocation: (id: string) => fetchAPI(`/fhir/Location/${id}`),
};
