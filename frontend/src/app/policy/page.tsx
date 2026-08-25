import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
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
}