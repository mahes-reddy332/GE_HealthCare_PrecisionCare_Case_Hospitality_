import React from 'react';
import { DataConfidence } from '../../types';
import { ShieldCheck, ShieldAlert, ShieldQuestion, BrainCircuit } from 'lucide-react';
import { cn } from '../../lib/utils';

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
